from .type import MType, SortRef, Type


class SymbolicElementaryType(MType):
  def __init__(self, sort: SortRef, solidity_type: Type) -> None:
    super().__init__(sort, solidity_type)

  def __str__(self) -> str:
    return f"SymbolicElementaryType(sort: {self._sort}, solidity_type: {self._solidity_type})"

  __repr__ = __str__
