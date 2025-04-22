from typing import Tuple, List
from slither.core.cfg.node import Node, NodeType
from copy import deepcopy

from solfuse.solfuse_ir.config import ConfigProvider
from solfuse.solfuse_ir.utils import compute_merged_env
from .handler import ForkSelector
from . import env as environment
from .logger import log
from z3 import BoolVal, And, Not, simplify, Solver, sat
from .context import Context, ForkStatus


class NoPathError(Exception):
  pass


class Scheduler:
  def __init__(
    self, entry_point: Node, config: ConfigProvider, pending_calls, pending_arguments
  ) -> None:
    self.queue: List[Context] = []
    self.done_list: List[Context] = []
    self._next_node = entry_point
    self._next_env = environment.Env()
    self._curr_fork_status: List[ForkStatus] = []
    self._curr_pending_call = pending_calls
    self._curr_pending_arguments = pending_arguments
    self.last_context: Context = Context(
      self._next_node,
      deepcopy(self._next_env),
      self._curr_fork_status,
      pending_calls=pending_calls,
      pending_arguments=pending_arguments,
    )
    self.config = config

  def update_last_context(self):
    self.last_context: Context = Context(
      self._next_node,
      self._next_env,
      self._curr_fork_status[:],
      self._curr_pending_call[:],
      self._curr_pending_arguments[:],
    )

  def update_next(
    self, handler_result: Tuple[List[Node], ForkSelector, environment.Env]
  ) -> None:
    curr_node: Node | None = self._next_node
    self.update_last_context()

    if (cond := getattr(handler_result[1], "payload", None)) is None:
      cond = BoolVal(True)
    if handler_result[1] == ForkSelector.Yes:
      assert len(handler_result[0]) == 2, "should be two paths"
      # exec son_true first
      self._next_node = handler_result[0][0]
      if self._next_node.type is NodeType.THROW:
        # if next node is throw, there is no need to fork or execute that branch, just execute the false branch with modified pc is ok
        self._next_node = handler_result[0][1]
        log(f"Next node type: {self._next_node.type}")
        self._next_env = handler_result[2]
        self._curr_fork_status.append(ForkStatus.No)
        self._curr_pending_call = handler_result[3][:]
        self._curr_pending_arguments = handler_result[4][:]
        self._next_env.add(
          name="@pc",
          soltype=self._next_env.pc,
          value=self._next_env.pc._value,
          symbolic_value=simplify(And(self._next_env.pc._symbolic_value, Not(cond))),
        )
        return
      self._next_env: environment.Env = handler_result[2]
      self._curr_pending_call = handler_result[3][:]
      self._curr_pending_arguments = handler_result[4][:]

      # * maintain fork status
      false_fork_status = self._curr_fork_status[:]
      self._curr_fork_status.append(ForkStatus.YesTrue)
      false_fork_status.append(ForkStatus.YesFalse)

      false_env = deepcopy(self._next_env)
      pc = self._next_env.get(name="@pc")
      self._next_env.add(
        name="@pc",
        soltype=pc._type,
        value=pc._value,
        symbolic_value=simplify(And(pc._symbolic_value, cond)),
      )
      false_env.add(
        name="@pc",
        soltype=pc._type,
        value=pc._value,
        symbolic_value=simplify(And(pc._symbolic_value, simplify(Not(cond)))),
      )
      self.push_new_context(
        Context(
          handler_result[0][1],
          false_env,
          false_fork_status,
          handler_result[3][:],
          handler_result[4][:],
        )
      )
    else:
      # * if node is from IF Node, push a ForkStatus.No to pass the nearest ENDIF Node
      self._next_node: Node | None = (
        handler_result[0][0] if len(handler_result[0]) > 0 else None
      )
      if curr_node.contains_if(include_loop=False) or curr_node.type in (
        NodeType.ENTRYPOINT,
        NodeType.OTHER_ENTRYPOINT,
      ):
        if curr_node.type not in (NodeType.ENTRYPOINT, NodeType.OTHER_ENTRYPOINT):
          self._curr_fork_status.append(ForkStatus.No)
        # * prepare for throw, reverting cond, automatically treating as require
        log("cond: ", cond)
        if self._next_node is not None:
          self._next_node.to_throw_cond = cond
      self._next_env = handler_result[2]
      self._curr_pending_call = handler_result[3][:]
      self._curr_pending_arguments = handler_result[4][:]

  def __iter__(self):
    return self

  def __next__(self):
    return self.next

  def extract_new_context(self):
    try:
      ctx: Context = self.queue.pop(0)
      (
        self._next_node,
        self._next_env,
        self._curr_fork_status,
        self._curr_pending_call,
        self._curr_pending_arguments,
      ) = (
        ctx.node,
        deepcopy(ctx.env),
        ctx.fork_stack[:],
        ctx.pending_calls[:],
        ctx.pending_arguments[:],
      )
      log(f"Extracted new context {ctx}")
      return ctx
    except IndexError:
      raise StopIteration

  def push_new_context(self, ctx: Context):
    self.queue.append(ctx)

  @property
  def next(self) -> Context:
    if self._next_node is None:
      # add one path result
      if self.last_context.node is None:
        return self.extract_new_context()
      if self.last_context.node.type is not NodeType.THROW:
        self.done_list.append(self.last_context)
      return self.extract_new_context()
    elif self.config.use_state_merging and self._next_node.type is NodeType.ENDIF:
      fork_status = self._curr_fork_status.pop()
      match fork_status:
        case ForkStatus.No:
          pass
        case ForkStatus.YesTrue | ForkStatus.YesFalse:
          ctx = Context(
            self._next_node,
            self._next_env,
            self._curr_fork_status[:],
            self._curr_pending_call[:],
            self._curr_pending_arguments[:],
          )
          true_item, false_item = (
            (ctx, getattr(self._next_node, "true_ctx", None)),
            (getattr(self._next_node, "false_ctx", None), ctx),
          )[fork_status == ForkStatus.YesFalse]
          setattr(
            self._next_node, "true_ctx", getattr(self._next_node, "true_ctx", true_item)
          )
          setattr(
            self._next_node,
            "false_ctx",
            getattr(self._next_env, "false_ctx", false_item),
          )
          if all(
            map(
              lambda x: x is not None,
              (self._next_node.true_ctx, self._next_node.false_ctx),
            )
          ):
            merged_env = compute_merged_env(
              [self._next_node.true_ctx, self._next_node.false_ctx]
            )
            self.push_new_context(
              Context(
                self._next_node,
                merged_env,
                self._curr_fork_status[:],
                self._curr_pending_call[:],
                self._curr_pending_arguments[:],
              )
            )
          return self.extract_new_context()
    return Context(
      self._next_node,
      self._next_env,
      self._curr_fork_status,
      self._curr_pending_call[:],
      self._curr_pending_arguments[:],
    )
