from slither.core.declarations import Contract
from slither.core.variables.state_variable import StateVariable


class LooseStateMachineDetector:
  def __init__(self, slither):
    self.slither = slither

  def _detect(self):
    for contract in self.slither.contracts:
      # 1. Find boolean state variables (potential state flags)
      state_flags = [
        var
        for var in contract.state_variables
        if self._is_potential_state_variable(var)
      ]

      # 2. Check if these flags are used as state controls
      for flag in state_flags:
        if self._is_used_as_state_machine(contract, flag):
          return True

    return False

  def _is_potential_state_variable(self, var: StateVariable) -> bool:
    """Identify boolean state variables"""
    return str(var.type) == "bool" and not var.is_constant

  def _is_used_as_state_machine(self, contract: Contract, flag: StateVariable) -> bool:
    """Check if a boolean flag is used in state machine-like patterns"""
    has_transitions = False
    has_guards = False

    # Check all functions in contract
    for func in contract.functions:
      # Detect writes to the flag (state transitions)
      if any(node for node in func.nodes if flag in node.state_variables_written):
        has_transitions = True

      # Detect require statements using the flag (state guards)
      if self._has_state_guards(func, flag):
        has_guards = True

    return has_transitions and has_guards

  def _has_state_guards(self, func, flag: StateVariable) -> bool:
    """Check if function uses the flag in require statements"""
    for node in func.nodes:
      for ir in node.irs:
        if "require" in str(ir):
          if flag.name in str(ir.expression):
            return True
    return False
