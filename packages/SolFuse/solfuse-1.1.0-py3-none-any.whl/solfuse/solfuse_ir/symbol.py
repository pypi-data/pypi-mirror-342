from copy import deepcopy
from slither.core.variables.variable import Variable
from slither.core.declarations import FunctionContract
from slither.core.solidity_types.type import Type
from dataclasses import dataclass
from z3 import BoolVal, BoolRef
from typing import List, Self


@dataclass
class Symbol:
  def __init__(
    self,
    name: str,
    soltype: Type,
    value: Variable | None = None,
    symbolic_value=None,
    sym_right=None,
    addr=None,
    on_chain: bool = False,
  ) -> None:
    self._name: str = name
    self._type: Type = soltype
    self._value: Variable = value
    self._symbolic_value = symbolic_value
    self._sym_right = sym_right
    self._address = addr
    self._is_on_chain: bool = False

  def __deepcopy__(self, memo) -> Self:
    """
    Custom implementation of deepcopy. Only copy _symbolic_value for

    1. other attributes should never be changed.
    2. copying _type will exceed recursion limits for whatever reason.
    """
    newobj = type(self).__new__(self.__class__)
    if isinstance(self._symbolic_value, FunctionContract):
      newobj.__dict__.update({"_symbolic_value": self._symbolic_value, **self.__dict__})
    else:
      newobj.__dict__.update(
        {
          "_symbolic_value": deepcopy(self._symbolic_value, memo),
          **self.__dict__,
        }
      )
    return newobj

  def __str__(self) -> str:
    return f"Symbol(name: {self._name}, soltype: {self._type}, value: {self._value}, symbolic_value: {self._symbolic_value})"

  __repr__ = __str__
