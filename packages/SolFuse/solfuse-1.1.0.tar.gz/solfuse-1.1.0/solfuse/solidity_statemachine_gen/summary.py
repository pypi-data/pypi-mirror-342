from io import StringIO
from typing import List

from slither.core.declarations import Contract, FunctionContract
from z3 import *

from .config import ConfigProvider
from .frame import Frame
from .indent_print import indent_print
from .logger import log


class Summary:
  def __init__(self, contract: Contract, config: ConfigProvider) -> None:
    self.contract = contract
    self.functions = contract.functions_declared
    self.constants = {}
    self._pre = {}
    self._post = {}
    self._post_og = {}
    self._post_range = {}
    self.config = config

  def print_to_file(self, s):
    indent_print(f"\033[32mSummary of {self.contract.name}:\033[0m", indent=0, file=s)
    for func in self.functions:
      if func not in self._pre.keys():
        continue
      indent_print(f"\033[33m{func.name}:\033[0m", indent=1, file=s)
      indent_print(f"\033[34mpre:\033[0m", indent=2, file=s)
      indent_print(f"{self.get_func_pre(func)}", indent=3, file=s)
      indent_print(f"\033[34mpost:\033[0m", indent=2, file=s)
      indent_print(f"{self.get_func_post_range(func)}", indent=3, file=s)

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

  def set_func_pre(self, func: FunctionContract, pre):
    self._pre[func] = simplify(pre)

  def set_func_post(self, func: FunctionContract, post: list[Frame]):
    self._post_og[func] = post
    self._post[func] = self.merge_frame(post, func)
    self._post_range[func] = {}
    self.compute_range(func, post)

  def compute_original_expr(self, done_frame: List[Frame], variable):
    if len(done_frame) == 1:
      return done_frame[0].binding.get(variable)
    if done_frame[0].binding.get(variable, None) is not None:
      return If(
        done_frame[0].get("@pc"),
        done_frame[0].binding.get(variable),
        self.compute_original_expr(done_frame[1:], variable),
      )
    return self.compute_original_expr(done_frame[1:], variable)

  def compute_range(self, func: FunctionContract, post: List[Frame]):
    log(
      f"{func.name}: ",
      indent=self.config.global_tab,
      will_do=self.config.print_summary_process,
    )
    # 5 minutes after writing this code, i forgot what this line did
    variables = dict(
      set(
        sum(
          map(lambda a: list(map(lambda b: (b[0], b[1]), a.variables.items())), post),
          [],
        )
      )
    )
    func_range = self._post_range[func]
    self.config.global_tab += 1
    for k, v in variables.items():
      if k != "@pc" and k in list(
        map(
          lambda x: x.name,
          func.all_state_variables_read() + func.all_state_variables_written(),
        )
      ):
        log(
          f"doing {k}",
          indent=self.config.global_tab,
          will_do=self.config.print_summary_process,
        )
        func_range[v] = self.check_and_solve(v, func)
    self.config.global_tab -= 1
    log("", will_do=self.config.print_summary_process, indent=self.config.global_tab)
    self._post_range[func] = func_range

  def check_and_solve(self, n, func: FunctionContract):
    expr = self._post[func]
    og = self.get_func_post_og(func)
    og_n = self.compute_original_expr(og, n)
    # this is just hilarious🤣
    return simplify(og_n)

  def flatten_frame(self, frame: Frame, func: FunctionContract):
    expr = frame.get("@pc")
    for k in frame.variables.keys():
      if k in list(
        map(lambda x: x.name, func.state_variables_read + func.state_variables_written)
      ) + list(map(lambda x: f"{func.name}.{x.name}", func.parameters)) + list(
        filter(lambda x: (x[0]).isdigit(), frame.variables.keys())
      ):
        expr = And(expr, frame.ensure_variable(k) == frame.get(k))
    return simplify(expr)

  def merge_frame(self, post: list[Frame], func: FunctionContract):
    expr = BoolVal(False)
    for f in post:
      expr = Or(expr, self.flatten_frame(f, func))
    return simplify(expr)

  def get_func_pre(self, func: FunctionContract):
    return self._pre.get(func, None)

  def get_func_post(self, func: FunctionContract):
    return self._post.get(func, None)

  def get_func_post_range(self, func: FunctionContract):
    return self._post_range.get(func, None)

  def get_func_post_og(self, func: FunctionContract):
    return self._post_og.get(func, None)
