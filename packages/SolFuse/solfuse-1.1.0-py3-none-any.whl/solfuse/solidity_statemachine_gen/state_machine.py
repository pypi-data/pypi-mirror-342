import datetime
from typing import List, Tuple

import pygraphviz as pgv
from slither.core.declarations import Contract
from slither.core.declarations import FunctionContract
from z3 import Solver, BoolRef, IntNumRef, Bool, And, sat, Const, substitute, eq

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

  def __init__(self, summary: Summary, config: ConfigProvider) -> None:
    self.summary = summary
    self.contract: Contract = summary.contract
    self.states = {}
    self.config = config
    self.use_pre2 = self.config.use_pre2
    self._functions: List[FunctionContract] = list(
      filter(
        lambda x: x.visibility in ("public", "external")
        and x.name not in self.config.constraints_func_names,
        self.contract.functions_declared,
      )
    )
    for func in self.functions:
      if func.visibility in ("public", "external"):
        self.states[func] = self.State(func.name, summary.get_func_pre(func))
    self.transitions_reject = {}
    self.transitions_accept = {}

  @property
  def functions(self):
    return self._functions

  def check_post_range_and_pre_match(self, post_range, pre, pre2=None) -> bool:
    if post_range is None or pre is None:
      return False
    solver = Solver()
    # ! TODO: this needs to be fixed!!!
    for k, v in post_range.items():
      kcopy = Const(name=f"@{k.__str__()}", sort=v.sort())
      pre_sub = substitute(pre, (kcopy, v))
      if not eq(pre_sub, pre):
        pre = pre_sub
    solver.add(pre)
    if self.use_pre2 and pre2 is not None:
      solver.add(pre2)
    return solver.check() == sat

  def compatible(self, func1: FunctionContract, func2: FunctionContract) -> bool:
    return self.check_post_range_and_pre_match(
      self.summary.get_func_post_range(func1),
      self.summary.get_func_pre(func2),
      self.summary.get_func_pre(func1),
    )

  def build(self):
    for i in self.functions:
      for j in self.functions:
        if not self.compatible(i, j):
          self.transitions_reject[i] = self.transitions_reject.get(i, []) + [
            (j, self.states[j])
          ]
        else:
          self.transitions_accept[i] = self.transitions_accept.get(i, []) + [
            (j, self.states[j])
          ]

  def export_to_dot_accept(self, folder="../../images", use_svg=False) -> None:
    G = pgv.AGraph(directed=True)
    G.edge_attr["style"] = "solid"
    G.edge_attr["arrowsize"] = 0.5
    # G.edge_attr['color'] = 'red'
    # G.edge_attr['label'] = '×'
    # G.edge_attr['labelfontcolor'] = 'red'
    G.add_nodes_from(map(lambda x: x.name, self.states.values()))
    for i in self.functions:
      for x in self.transitions_accept.get(i, []):
        G.add_edge(self.states[i].name, self.states[x[0]].name)
    layout = "circo"
    G.layout(prog=layout)
    if not use_svg:
      G.draw(
        f'{folder}/{self.contract.name}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{layout}.png'
      )
    else:
      G.draw(
        f'{folder}/{self.contract.name}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{layout}.svg'
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
        f'{folder}/{self.contract.name}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{layout}.png'
      )
    else:
      G.draw(
        f'{folder}/{self.contract.name}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{layout}.svg'
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
