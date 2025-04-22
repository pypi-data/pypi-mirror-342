from typing import Tuple
from dataclasses import dataclass


@dataclass
class ConfigProfile:
  debug: bool = True
  print_stmt: bool = False
  print_on_constraints_found: bool = False
  print_executor_process: bool = False
  print_summary_process: bool = False
  print_executor_summary: bool = False
  print_state_machine: bool = True
  use_pre2: bool = True
  global_tab: int = 0
  constraints_func_names: Tuple[str, str] = (
    "Verification.Assume_Complex",
    "Verification.Assume",
  )
  constraints_func_name_simple: str = constraints_func_names[0]
  constraints_func_name_complex: str = constraints_func_names[1]


class ConfigProvider:
  def __init__(self, profile: ConfigProfile) -> None:
    self._profile = profile

  @property
  def profile(self) -> ConfigProfile:
    return self._profile

  @profile.setter
  def profile(self, profile: ConfigProfile):
    self.profile = profile

  @property
  def debug(self) -> bool:
    return self.profile.debug

  @property
  def print_stmt(self) -> bool:
    return self.profile.print_stmt

  @property
  def print_on_constraints_found(self) -> bool:
    return self.profile.print_on_constraints_found

  @property
  def print_executor_process(self) -> bool:
    return self.profile.print_executor_process

  @property
  def print_summary_process(self) -> bool:
    return self.profile.print_summary_process

  @property
  def print_executor_summary(self) -> bool:
    return self.profile.print_executor_summary

  @property
  def print_state_machine(self) -> bool:
    return self.profile.print_state_machine

  @property
  def use_pre2(self) -> bool:
    return self.profile.use_pre2

  @property
  def global_tab(self) -> int:
    return self.profile.global_tab

  @property
  def constraints_func_names(self) -> Tuple[str, str]:
    return self.profile.constraints_func_names

  @property
  def constraints_func_name_simple(self) -> str:
    return self.profile.constraints_func_name_simple

  @property
  def constraints_func_name_complex(self) -> str:
    return self.profile.constraints_func_name_complex

  @debug.setter
  def debug(self, debug: bool):
    self.profile.debug = debug

  @print_stmt.setter
  def print_stmt(self, print_stmt: bool):
    self.profile.print_stmt = print_stmt

  @print_on_constraints_found.setter
  def print_on_constraints_found(self, print_on_constraints_found: bool):
    self.profile.print_on_constraints_found = print_on_constraints_found

  @print_executor_process.setter
  def print_executor_process(self, print_executor_process: bool):
    self.profile.print_executor_process = print_executor_process

  @print_summary_process.setter
  def print_summary_process(self, print_summary_process: bool):
    self.profile.print_summary_process = print_summary_process

  @print_executor_summary.setter
  def print_executor_summary(self, print_executor_summary: bool):
    self.profile.print_executor_summary = print_executor_summary

  @print_state_machine.setter
  def print_state_machine(self, print_state_machine: bool):
    self.profile.print_state_machine = print_state_machine

  @global_tab.setter
  def global_tab(self, value: int):
    self.profile.global_tab = value


default_config = ConfigProvider(profile=ConfigProfile())

debug_config = ConfigProvider(
  profile=ConfigProfile(
    debug=True,
    print_stmt=True,
    print_on_constraints_found=False,
    print_executor_process=True,
    print_summary_process=True,
    print_executor_summary=True,
    print_state_machine=True,
    constraints_func_names=("Verification.Assume_Complex", "Verification.Assume"),
    use_pre2=True,
    global_tab=0,
  )
)
