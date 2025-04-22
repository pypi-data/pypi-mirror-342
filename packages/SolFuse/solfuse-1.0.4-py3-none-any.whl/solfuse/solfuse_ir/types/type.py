from z3 import SortRef
from slither.core.solidity_types.type import Type
from typing import Any, Dict, List, Tuple


class MType:
  def __init__(self, sort: SortRef, solidity_type: Type):
    self._sort: SortRef = sort
    self._solidity_type: Type = solidity_type

  def __str__(self):
    return f"MType(sort: {self._sort}, solidity_type: {self._solidity_type})"

  __repr__ = __str__
