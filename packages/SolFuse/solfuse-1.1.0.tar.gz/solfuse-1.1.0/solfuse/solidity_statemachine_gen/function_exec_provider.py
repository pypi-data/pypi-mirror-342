from slither.core.declarations import Contract
from slither.core.declarations.solidity_variables import SOLIDITY_FUNCTIONS


class FunctionProvider:
  def __init__(self, contract: Contract) -> None:
    self.contract = contract
    self.function_table = {}

  def is_solidity_function(self, signature: str):
    return signature in SOLIDITY_FUNCTIONS.keys()

  def is_internal(self, signature: str):
    return (
      self.contract.get_function_from_signature(signature) is not None
      or self.contract.get_modifier_from_signature(signature) is not None
    )

  def get_func_status(self, signature: str):
    if self.is_internal(signature=signature):
      if signature not in self.function_table.keys():
        self.function_table[signature] = self.contract.get_function_from_signature(
          signature
        )
        if not self.function_table[signature]:
          self.function_table[signature] = self.contract.get_modifier_from_signature(
            signature
          )
    # returning None means this function is a SolidityFunction or an external function and thus cannot be executed and need naive handling
    return self.function_table.get(signature, None)
