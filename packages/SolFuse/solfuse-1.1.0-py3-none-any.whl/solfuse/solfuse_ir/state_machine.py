from __future__ import annotations
import datetime
import queue
from typing import TYPE_CHECKING, List, Tuple, Any

if TYPE_CHECKING:
  from solfuse.solfuse_ir.env import Env
import pygraphviz as pgv
from slither.core.declarations import Contract
from slither.core.declarations import FunctionContract
from slither.slithir.variables import ReferenceVariable
from z3 import (
  Solver,
  BoolRef,
  IntNumRef,
  Bool,
  And,
  sat,
  Const,
  substitute,
  eq,
  is_int_value,
)
import multiprocessing as mp
from solfuse.solfuse_ir.symbol import Symbol
from solfuse.solfuse_ir.utils import ref_to_actual_target, select_z3sort

from .config import ConfigProvider
from .logger import log
from .summary import Summary


def make_constraints(name, thing: None | BoolRef | Tuple[IntNumRef, IntNumRef, list]):
  namecopy = Const(f"@{name.__str__()}", name.sort())
  if thing is None:
    return Bool(True)
  if isinstance(thing, BoolRef):
    return And(name == thing, namecopy == name)
  elif isinstance(thing, Tuple):
    _range = And(thing[0] <= name, name <= thing[1], namecopy == name)
    for i in thing[2]:
      _range = And(_range, name != i)
    return _range
  else:
    return namecopy == thing


class StateMachine:
  class State:
    def __init__(self, name: str, space) -> None:
      self.name = name
      self.space = space

  def __init__(
    self, summary: Summary, config: ConfigProvider, timeout: float = 0.15
  ) -> None:
    self.timeout = timeout  # secs
    self.summary = summary
    self.contract: Contract = summary.contract
    self.states = {}
    self.config = config
    self.use_pre2 = self.config.use_pre2
    self._functions: List[FunctionContract] = list(
      filter(
        lambda x: x.visibility in ("public", "external")
        and x.name not in self.config.constraints_func_names
        and x not in self.contract.modifiers
        and x.contract_declarer == self.contract,
        # and not x.is_constructor,
        self.contract.functions,
      )
    )
    for func1 in self._functions:
      self.summary._chain_info[func1.name] = {}
      for func2 in self._functions:
        self.summary._chain_info[func1.name][func2.name] = {}

    for func in self.functions:
      self.states[func] = self.State(func.name, summary.get_func_pre(func))
    self.transitions_reject = {}
    self.transitions_accept = {}

  @property
  def functions(self):
    return self._functions

  @staticmethod
  def _solve(
    post: Env,
    pre,
    pre2=None,
    use_pre2=False,
    func1: FunctionContract = None,
    func2: FunctionContract = None,
    summary: Summary = None,
  ) -> (bool, list[tuple[str, Any]]):
    if post is None or pre is None:
      return False
    solver = Solver()
    for k, v1 in post.binding.items():
      assert isinstance(v1, Symbol)
      if isinstance(v1._symbolic_value, FunctionContract):
        continue
      if k == "@pc":
        continue
      v = v1._symbolic_value
      kcopy = Const(name=f"@{k.__str__()}", sort=v.sort())
      if isinstance(v1._value, ReferenceVariable):
        try:
          some = ref_to_actual_target(v1, post)
          if some is not None:
            kcopy = some
        except Exception:
          pass
      if not eq(kcopy.sort(), v.sort()):
        vsort = select_z3sort(v1._type)
        if is_int_value(kcopy) and isinstance(vsort, Tuple):
          _, item_list = vsort
          kcopy = item_list[kcopy.as_long()]
        else:
          kcopy = Const(name=f"@{k.__str__()}", sort=v.sort())
        assert eq(kcopy.sort(), v.sort()), (
          f"sort not equal: {kcopy.sort()} != {v.sort()}"
        )
      pre_sub = substitute(pre, (kcopy, v))
      if not eq(pre_sub, pre):
        pre = pre_sub
    solver.add(pre)
    if use_pre2 and pre2 is not None:
      for k, v1 in post.binding.items():
        assert isinstance(v1, Symbol)
        if isinstance(v1._symbolic_value, FunctionContract):
          continue
        if k == "@pc":
          continue
        v = v1._symbolic_value
        kcopy = Const(name=f"@{k.__str__()}", sort=v.sort())
        if isinstance(v1._value, ReferenceVariable):
          try:
            some = ref_to_actual_target(v1, post)
            if some is not None:
              kcopy = some
          except Exception:
            pass
        if not eq(kcopy.sort(), v.sort()):
          vsort = select_z3sort(v1._type)
          if is_int_value(kcopy) and isinstance(vsort, Tuple):
            _, item_list = vsort
            kcopy = item_list[kcopy.as_long()]
          else:
            kcopy = Const(name=f"@{k.__str__()}", sort=v.sort())
          assert eq(kcopy.sort(), v.sort()), (
            f"sort not equal: {kcopy.sort()} != {v.sort()}"
          )
          pre2_sub = substitute(pre2, (kcopy, v))
          if not eq(pre2_sub, pre2):
            pre2 = pre2_sub
      solver1 = Solver()
      solver1.add(pre2)
      if solver1.check() == sat:
        solver.add(pre2)
    # log(f"pre2: {pre2}")
    res = solver.check()
    to_push = []
    if res == sat:
      model = solver.model()
      for k, v in summary.get_func_post(func2).binding.items():
        if v._is_on_chain:
          to_push.append((k, str(model.eval(v._symbolic_value, model_completion=True))))
    return (res == sat), to_push[:]

  @staticmethod
  def check_post_and_pre_match(
    post,
    pre,
    pre2=None,
    use_pre2=False,
    func1: FunctionContract = None,
    func2: FunctionContract = None,
    summary: Summary = None,
  ) -> (bool, list[tuple[str, Any]]):
    log.config.global_tab += 1
    result = StateMachine._solve(post, pre, pre2, use_pre2, func1, func2, summary)
    log.config.global_tab -= 1
    return result

  def compatible(
    self, func1: FunctionContract, func2: FunctionContract, queue: mp.Queue, cnt1, cnt2
  ):
    check, to_push = self.check_post_and_pre_match(
      self.summary.get_func_post(func1),
      self.summary.get_func_pre(func2),
      self.summary.get_func_pre(func1),
      self.use_pre2,
      func1=func1,
      func2=func2,
      summary=self.summary,
    )
    queue.put((cnt1, cnt2, check, to_push[:]))

  def build(self):
    process_list: List[mp.Process] = []
    result_queue = mp.Queue()
    from rich.progress import track

    for cnt1, i in enumerate(self.functions):
      for cnt2, j in enumerate(self.functions):
        p = mp.Process(target=self.compatible, args=(i, j, result_queue, cnt1, cnt2))
        process_list.append(p)

    all_process_cnt = len(process_list)
    process_limit = 10
    current_process_cnt = 0
    current_process_list: List[mp.Process] = []

    for _ in track(
      range(all_process_cnt // process_limit + 1), description="Solving Functions..."
    ):
      while process_list and current_process_cnt < process_limit:
        p = process_list.pop()
        current_process_list.append(p)
        current_process_cnt += 1
        p.start()
      while current_process_list:
        p = current_process_list.pop()
        p.join(timeout=self.timeout)
        p.terminate()
        current_process_cnt -= 1
    itering = track(
      range(len(self.functions) ** 2), description="Collecting Results..."
    )
    if self.config.debug:
      itering = range((len(self.functions) ** 2))
    for _ in itering:
      try:
        i, j, check, to_push = result_queue.get_nowait()
      except queue.Empty:
        break
      i, j = self.functions[i], self.functions[j]
      if not check:
        self.transitions_reject[i] = self.transitions_reject.get(i, []) + [
          (j, self.states[j])
        ]
      else:
        self.transitions_accept[i] = self.transitions_accept.get(i, []) + [
          (j, self.states[j])
        ]
        for k, v in to_push:
          self.summary._chain_info[i.name][j.name][k] = v
    for i in self.functions:
      if i not in self.transitions_accept.keys():
        self.transitions_accept[i] = filter(
          lambda x: x not in self.transitions_reject.get(i, []),
          list(map(lambda x: (x, self.states[x]), self.functions)),
        )
      if i not in self.transitions_reject.keys():
        self.transitions_reject[i] = filter(
          lambda x: x not in self.transitions_accept.get(i, []),
          list(map(lambda x: (x, self.states[x]), self.functions)),
        )
    # for cnt1, i in enumerate(self.functions):
    #   for cnt2, j in enumerate(self.functions):
    #     if (j, self.states[j]) not in self.transitions_accept.get(i, []):
    #       self.transitions_accept[i] = self.transitions_accept.get(
    #           i, []) + [(j, self.states[j])]
    for p in process_list:
      # p.join(timeout=self.timeout)
      if p.is_alive():
        p.terminate()

  def export_to_dot_accept(self, folder="../../images", use_svg=False) -> None:
    G = pgv.AGraph(directed=True)
    G.edge_attr["style"] = "solid"
    G.edge_attr["arrowsize"] = 0.5
    G.add_nodes_from(map(lambda x: x.name, self.states.values()))
    for i in self.functions:
      for x in self.transitions_accept.get(i, []):
        G.add_edge(self.states[i].name, self.states[x[0]].name)
    layout = "circo"
    G.layout(prog=layout)
    if not use_svg:
      G.draw(
        f"{folder}/{self.contract.name}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{layout}-ir.png"
      )
    else:
      G.draw(
        f"{folder}/{self.contract.name}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{layout}-ir.svg"
      )

  def export_to_dot_reject(self, folder="../../images", use_svg=False) -> None:
    G = pgv.AGraph(directed=True)
    G.edge_attr["style"] = "solid"
    G.edge_attr["arrowsize"] = 0.5
    G.edge_attr["color"] = "red"
    G.edge_attr["label"] = "×"
    G.edge_attr["labelfontcolor"] = "red"
    G.add_nodes_from(map(lambda x: x.name, self.states.values()))
    for i in self.functions:
      for x in self.transitions_reject.get(i, []):
        G.add_edge(self.states[i].name, self.states[x[0]].name)
    layout = "circo"
    G.layout(prog=layout)
    if not use_svg:
      G.draw(
        f"{folder}/{self.contract.name}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{layout}-ir.png"
      )
    else:
      G.draw(
        f"{folder}/{self.contract.name}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-{layout}-ir.svg"
      )

  def statistic_deleted_edge(self, length=1):
    cnt = 0
    for i in self.states.keys():
      cnt += self.statistic_deleted_edge_dot(i, length, False)
    return cnt

  def statistic_deleted_edge_dot(self, begin, length=1, deleted=False):
    if length < 0:
      return 0
    if length == 0:
      if deleted:
        return 1
      return 0
    cnt = 0
    for j in self.states.keys():
      rejects = self.transitions_reject.get(begin, None)
      if rejects and (j in list(map(lambda x: x[0], rejects))):
        cnt += self.statistic_deleted_edge_dot(j, length - 1, True)
      else:
        cnt += self.statistic_deleted_edge_dot(j, length - 1, deleted)
    return cnt

  def to_dict(self):
    # 获取所有状态的名称
    states = [state.name for state in self.states.values()]

    # 获取接受转换的字典表示
    transitions_accept = {
      self.states[key].name: [self.states[target[0]].name for target in value]
      for key, value in self.transitions_accept.items()
    }

    # 获取拒绝转换的字典表示
    transitions_reject = {
      self.states[key].name: [self.states[target[0]].name for target in value]
      for key, value in self.transitions_reject.items()
    }

    return {
      "states": states,
      "transitions_accept": transitions_accept,
      "transitions_reject": transitions_reject,
      "black_holes": self.find_black_holes(),
    }

  def print_simple_reject(self):
    for k, v in self.transitions_reject.items():
      log(k, will_do=self.config.print_state_machine)
      self.config.global_tab += 1
      for v1 in v:
        log(
          f"-x-> ({v1[0].name})",
          indent=self.config.global_tab,
          will_do=self.config.print_state_machine,
        )
      self.config.global_tab -= 1

  def print_simple(self):
    for k, v in self.transitions_reject.items():
      log(k, will_do=self.config.print_state_machine)
      self.config.global_tab += 1
      for v1 in v:
        log(
          f"-x-> ({v1[0].name})",
          indent=self.config.global_tab,
          will_do=self.config.print_state_machine,
        )
      self.config.global_tab -= 1

  def find_black_holes(self) -> list[str]:
    black_holes = []
    for key, lst in self.transitions_accept.items():
      if not lst:
        black_holes.append(key.name)
    return black_holes
