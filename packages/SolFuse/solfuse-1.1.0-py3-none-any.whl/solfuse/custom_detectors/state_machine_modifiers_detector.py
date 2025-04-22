from slither.core.declarations import Enum, Contract, Modifier
from slither.core.variables.state_variable import StateVariable
from slither import Slither


class GeneralizedStateMachineWithModifiersDetector:
  def __init__(self, slither_: Slither):
    self.slither = slither_

  def _detect(self):
    detected = False
    for contract in self.slither.contracts:
      state_enums = [
        enum for enum in contract.enums if self._is_potential_state_enum(enum)
      ]
      for enum in state_enums:
        state_var = self._find_state_variable(contract, enum)
        if not state_var:
          continue
        has_transitions = False
        has_guards = False

        # Check functions for transitions and guards
        for func in contract.functions:
          # Detect state transitions
          if any(
            node for node in func.nodes if state_var in node.state_variables_written
          ):
            has_transitions = True

          # Detect guards in function and its modifiers
          if self._has_state_guards(func, state_var):
            has_guards = True

        # Check all modifiers in the contract for guards
        for modifier in contract.modifiers:
          if self._node_container_has_state_guards(modifier, state_var):
            has_guards = True

        detected = has_transitions and has_guards

    return detected

  def _is_potential_state_enum(self, enum: Enum) -> bool:
    return len(enum.values) >= 2

  def _find_state_variable(self, contract: Contract, enum: Enum) -> StateVariable:
    for var in contract.state_variables:
      if str(var.type) == enum.canonical_name and not var.is_constant:
        return var
    return None

  def _node_container_has_state_guards(
    self, node_container, state_var: StateVariable
  ) -> bool:
    """Check if a function/modifier has state guards."""
    if not node_container.nodes:
      return False
    for node in node_container.nodes:
      for ir in node.irs:
        if "require" in str(ir) or "assert" in str(ir):
          if state_var.name in str(ir.expression):
            return True
    return False

  def _has_state_guards(self, func, state_var: StateVariable) -> bool:
    """Check function and its modifiers for state guards."""
    # Check the function itself
    if self._node_container_has_state_guards(func, state_var):
      return True

    # Check modifiers applied to the function
    for modifier in func.modifiers:
      if isinstance(modifier, Modifier) and self._node_container_has_state_guards(
        modifier, state_var
      ):
        return True

    return False

  def _generate_result(self, contract, enum, state_var):
    info = f"State Machine (with modifiers) detected in {contract.name}:\n"
    info += f"- Enum: {enum.name}\n"
    info += f"- State Variable: {state_var.name}\n"
    return {"check": self.ARGUMENT, "result": info}
