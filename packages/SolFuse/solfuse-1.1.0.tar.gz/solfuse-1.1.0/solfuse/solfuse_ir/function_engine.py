from __future__ import annotations

from slither.core.declarations.function_contract import FunctionContract

from solfuse.solfuse_ir.pure_descriptor import PureDescriptor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from solfuse.solfuse_ir.pure_descriptor import PureDescriptor
  from slither.core.declarations import FunctionContract
from ast import arguments
from slither.core.declarations import Function
from slither.core.cfg.node import Node, NodeType
from slither.slithir.operations import InternalCall
from typing import Any, Optional, Tuple, List, TYPE_CHECKING
from slither.slithir.variables import (
  Constant,
  ReferenceVariable,
  StateIRVariable,
  TemporaryVariable,
)

from solfuse.solfuse_ir.config import ConfigProvider


from .utils import get_variable_name, ref_to_actual_target
from .handler import Handler, ForkSelector
from .scheduler import Scheduler, NoPathError, Context
from .env import Env
from .logger import log
from .symbol import Symbol


class FunctionEngine:
  """
  `FunctionEngine` delegates `Scheduler` to decide which node to execute next, and employs `node_handler` to process nodes
  """

  def __init__(
    self,
    function: Function,
    node_handler: Handler,
    config: ConfigProvider,
    call_from: Optional[Function] = None,
    call_origin: Optional[Function] = None,
    from_modifier: bool = False,
    done_pure: dict[FunctionContract, PureDescriptor] = {},
  ) -> None:
    self.node_handler = node_handler
    self.node_handler.from_engine = self
    self.config = config
    self.call_from = call_from
    self.call_origin = call_origin
    self.call_cnt = {}
    self.pending_arguments = [None]
    self.pending_functions = [function]
    if config.use_proper_modifier and not from_modifier:
      self.pending_functions = function.modifiers + [function]
      self.pending_arguments = [[] for _ in range(len(self.pending_functions))]
    self.function = self.pending_functions[0]
    if config.use_proper_modifier and not from_modifier:
      self.set_modifier_arguments()
    self.scheduler = Scheduler(
      self.function.entry_point,
      config=self.config,
      pending_calls=self.pending_functions,
      pending_arguments=self.pending_arguments,
    )
    self._env = Env()
    self.done_pure: dict[FunctionContract, PureDescriptor] = done_pure
    self.arguments: List | None = None
    self.done_list: List[Context] = []
    self.call_cnt[function.canonical_name] = 0
    if self.call_from:
      self.call_cnt[call_from.canonical_name] = 0
    if self.call_origin:
      self.call_cnt[call_origin.canonical_name] = 0

  def set_modifier_arguments(self):
    for n in self.function.nodes:
      for ir in n.irs:
        if isinstance(ir, InternalCall):
          assert isinstance(ir, InternalCall)
          if ir.function in self.function.modifiers:
            arguments = ir.arguments
            index = self.pending_functions.index(ir.function)
            self.pending_arguments[index] = (
              arguments  # ! This argument is not symbolic expressions, unlike what `set_argument` does
            )

  def set_arguments(self, arguments: List):
    self.arguments = arguments  # ! This argument is symbolic expressions
    self.pending_arguments[-1] = arguments

  @property
  def env(self, env: Env):
    return self._env

  @env.setter
  def env(self, env: Env):
    """
    Needs to write a setter to update scheduler.
    """
    self._env = env
    self.scheduler._next_env = env

  @env.getter
  def env(self):
    return self._env

  def exec(self) -> List[Context]:
    log(f"Function: {self.function.name}")
    log.config.global_tab += 1
    for next_node, next_env, _, pending_calls, pending_arguments in self.scheduler:
      # next_node, next_env = self.scheduler.next
      self._env: Env = next_env
      self.node_handler.pending_calls = pending_calls
      self.node_handler.pending_arguments = pending_arguments
      if next_node.type in (NodeType.ENTRYPOINT, NodeType.OTHER_ENTRYPOINT):
        handler_result: Tuple[
          List[Node], ForkSelector, Env, List[Function], List[Any]
        ] = self.node_handler.handle_(
          node=next_node,
          env=next_env,
          arguments=self.arguments,
          origin_call=self.call_origin is None and self.call_from is None,
          pending_calls=self.pending_functions,
          pending_arguments=self.pending_arguments,
        )
      else:
        handler_result: Tuple[
          List[Node], ForkSelector, Env, List[Function], List[Any]
        ] = self.node_handler.handle_(node=next_node, env=next_env)
      self.scheduler.update_next(handler_result=handler_result)
    self.done_list = self.scheduler.done_list
    log.config.global_tab -= 1
    if len(self.done_list) <= 0:
      self.done_list = [self.scheduler.last_context]
    return self.done_list
