from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
  from solfuse.solfuse_ir.env import Env
from io import StringIO
from symtable import Function

from slither.core.declarations import Contract, FunctionContract
from slither.core.solidity_types.elementary_type import ElementaryType, Uint, Int
from z3 import Optimize, sat, simplify, Solver, Const

from .config import ConfigProvider
from . import context
from .indent_print import indent_print
from .logger import log
from .utils import (
  compute_merged_env,
  get_variable_name,
  make_z3variable,
  get_variable_default_range,
  compute_on_chain_info,
)


class Summary:
  def __init__(self, contract: Contract, config: ConfigProvider) -> None:
    self.contract = contract
    self.functions = contract.functions_declared
    self.constants = {}
    self._pre = {}
    self._post = {}
    self._post_og = {}
    self._post_range = {}
    self._chain_info: Dict[str, Dict[str, Dict[str, Any]]] = {}
    self._construct_params = {}
    self._construct_fail_reason = ""
    self.config = config

  def print_to_file(self, s):
    indent_print(f"\033[32mSummary of {self.contract.name}:\033[0m", indent=0, file=s)
    for func in self.functions:
      if func not in self._pre.keys():
        continue
      indent_print(f"\033[33m{func.name}:\033[0m", indent=1, file=s)
      indent_print("\033[34mpre:\033[0m", indent=2, file=s)
      indent_print(f"{self.get_func_pre(func)}", indent=3, file=s)
      indent_print("\033[34mpost:\033[0m", indent=2, file=s)
      indent_print(f"{self.get_func_post(func)}", indent=3, file=s)

  def __str__(self):
    s = StringIO()
    self.print_to_file(s)
    return s.getvalue()

  @property
  def all_pre(self):
    return self._pre

  @property
  def all_post(self):
    return self._post

  @property
  def construct_params(self):
    return self._construct_params

  @property
  def chain_info(self):
    return self._chain_info

  @chain_info.setter
  def chain_info(self, value: dict):
    self._chain_info = value

  @property
  def construct_fail_reason(self):
    return self._construct_fail_reason

  def set_func_pre(self, func: FunctionContract, pre):
    self._pre[func] = simplify(pre)

    def make_construct_params():
      parameters = func.parameters
      if not all(
        map(lambda x: x.type and isinstance(x.type, ElementaryType), parameters)
      ):
        self._construct_fail_reason = "param not elementary type"
        return
      pre_condition = self._pre[func]
      parameters_name = list(map(lambda x: get_variable_name(x), parameters))
      parameters_type = list(map(lambda x: x.type, parameters))

      parameters_sym = list(
        map(
          lambda x: make_z3variable(x[0], f"@{x[1]}"),
          zip(parameters_type, parameters_name),
        )
      )

      parameters_range = list(
        map(lambda x: get_variable_default_range(x.type), parameters)
      )

      s = Solver()
      s.add(pre_condition)
      for p, r in zip(parameters_sym, parameters_range):
        if r:
          s.add(p > r[0], p < r[1])

      chkres = s.check()
      if chkres == sat:
        m = s.model()
        for n, s in zip(map(lambda x: x.name, parameters), parameters_sym):
          # assert False
          self._construct_params[n] = eval(str(m.eval(s, model_completion=True)))

    if func.is_constructor:
      make_construct_params()

  def compute_expr_range(self, func: FunctionContract):
    from .env import Env

    log("Computing range for function ", func.name)

    post: Env = self.get_func_post(func)
    pre = self.get_func_pre(func)
    if post is None:
      return
    """
    Care about function's parameters only, for now
    """
    parameters = func.parameters
    parameters_name = list(map(lambda x: get_variable_name(x), parameters))
    parameters_type = list(map(lambda x: x.type, parameters))
    ranges = {}
    for p, _type in zip(parameters, parameters_type):
      name = p.name
      variable_name = get_variable_name(p)
      pcopy = Const(
        name=f"@{p.__str__()}", sort=post.get(variable_name)._symbolic_value.sort()
      )
      if not isinstance(_type, ElementaryType):
        ranges[name] = ()
        continue
      if _type.type not in Uint + Int:
        ranges[name] = ()
        continue
      import multiprocessing

      def optimize_with_timeout(optimizer, timeout):
        q = multiprocessing.Queue()

        def _do_optimize():
          q.put((optimizer.check(), optimizer.model()))

        p = multiprocessing.Process(target=_do_optimize)
        p.start()
        p.join(timeout=timeout)
        p.terminate()
        try:
          r = q.get_nowait()
        except Exception as e:
          return (None, None)
        return r

      max_optimizer = Optimize()
      min_optimizer = Optimize()
      max_optimizer.add(pcopy == post.get(variable_name)._symbolic_value)
      min_optimizer.add(pcopy == post.get(variable_name)._symbolic_value)
      max_optimizer.add(pre)
      min_optimizer.add(pre)
      # log("Optimizing pre :", pre)
      max_obj = max_optimizer.maximize(pcopy)
      min_obj = min_optimizer.minimize(pcopy)
      # log("Optimizing post :", post.get(variable_name)._symbolic_value)

      max_result = optimize_with_timeout(max_optimizer, 0.5)
      min_result = optimize_with_timeout(min_optimizer, 0.5)
      max_chk, max_model = max_result
      min_chk, min_model = min_result

      if max_chk != sat or min_chk != sat:
        ranges[name] = ()
        continue

      ranges[name] = (
        str(max_obj.upper()),
        str(min_obj.lower()),
      )
    return ranges

  def set_func_post(self, func: FunctionContract, post: list[context.Context]):
    self._post_og[func] = post
    self._post[func] = compute_merged_env(post)
    # self._chain_info[func] = compute_on_chain_info(post)
    # self._post_range[func] = self.compute_expr_range(func)

  def get_func_pre(self, func: FunctionContract):
    return self._pre[func]

  def get_func_post(self, func: FunctionContract) -> Env:
    return self._post[func]

  def get_func_post_og(self, func: FunctionContract):
    return self._post_og[func]

  def get_func_post_range(self, func: FunctionContract):
    return self._post_range[func]
