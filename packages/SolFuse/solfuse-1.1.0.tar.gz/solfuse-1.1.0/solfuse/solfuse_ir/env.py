from functools import reduce
from .utils import (
  make_z3variable,
  get_variable_default_value,
  select_z3sort,
  get_variable_default_range,
)
from .symbol import Symbol
from slither.core.variables.variable import Variable
from slither.slithir.variables import ReferenceVariable
from slither.core.solidity_types.type import Type
from slither.core.solidity_types import UserDefinedType
from slither.core.declarations import Enum, FunctionContract
from slither.core.solidity_types.elementary_type import ElementaryType, Byte
from z3 import BoolVal, simplify, is_string, IntVal, And, BoolRef
from typing import Any, Dict, List, Self, Tuple
from enum import Enum
from disjoint_set import DisjointSet
from .logger import log


class SymbolNotFoundError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class TypeNotFoundError(Exception):
  pass


class AddressNullError(Exception):
  pass


class Env:
  class UserDefinedType(Enum):
    Contract = 0
    Enum_ = 1
    Structure = 2

  def __init__(self, copied=False) -> None:
    self.state_binding: Dict[str, Symbol] = {}  # state variable binding
    self.param_binding: Dict[str, Symbol] = {}  # function parameter binding
    self.global_binding: Dict[str, Symbol] = {}  # global variable binding
    self.local_binding: Dict[str, Symbol] = {}  # local variable binding
    self._pc: List = []
    self.param_binding["@pc"] = Symbol(
      name="@pc", soltype=ElementaryType(t="bool"), symbolic_value=BoolVal(val=True)
    )
    self.global_binding["@pc"] = Symbol(
      name="@pc", soltype=ElementaryType(t="bool"), symbolic_value=BoolVal(val=True)
    )
    self.state_binding["@pc"] = Symbol(
      name="@pc", soltype=ElementaryType(t="bool"), symbolic_value=BoolVal(val=True)
    )
    self.functable = {}
    self.ref_disjoint_set = DisjointSet()
    self.ref_to_symbolic_value = {}
    self.ref_to_name = {}
    self.symbolic_value_to_ref = {}
    self.memory: Dict[int, str] = {}
    self.copied = copied

  @property
  def binding(self):
    return self.state_binding

  @binding.setter
  def binding(self, value):
    self.state_binding = value

  def get_by_address(self, address: int):
    if (symbol := self.memory.get(address, None)) is not None:
      return self.get(name=symbol)
    raise AddressNullError

  def ref_to_actual_target(self, name: str):
    symbol = self.get(name=name)
    if isinstance(symbol._value, ReferenceVariable):
      return self.ref_to_symbolic_value.get(
        self.ref_disjoint_set.find(symbol._value.index), None
      )
    return symbol._symbolic_value

  def get(self, name: str) -> Symbol:
    if (symbol := self.state_binding.get(name, None)) is not None:
      return symbol
    raise SymbolNotFoundError(name)

  def add_pc(self, symbolic_value: Any) -> None:
    self._pc.append(simplify(symbolic_value))
    self.binding["@pc"]._symbolic_value = simplify(reduce(And, self._pc))

  def add(
    self,
    name: str,
    soltype: Type,
    value: Variable | None = None,
    symbolic_value: BoolRef = None,
    address=None,
    need_default=False,
    sym_ref=None,
  ) -> None:
    if name == "@pc":
      self._pc = [symbolic_value]
    if (
      isinstance(soltype, ElementaryType)
      and soltype.name in Byte
      and (symbolic_value is not None and is_string(symbolic_value))
    ):
      symbolic_value = IntVal(0)  # ! Temporary patch

    if isinstance(soltype, List):
      if not isinstance(soltype[0], str):
        soltype = tuple([name] + soltype)

    self.state_binding[name] = Symbol(
      name=name,
      soltype=soltype,
      value=value,
      symbolic_value=(
        make_z3variable(
          _type=soltype, name=f"@{name}" if not name.startswith("@") else name
        )
        if (not need_default or not isinstance(soltype, ElementaryType))
        else get_variable_default_value(_type=soltype)
      )
      if symbolic_value is None
      else symbolic_value,
      sym_right=sym_ref,
    )
    self.state_binding[name]._address = address

    symbolic_value = self.state_binding[name]._symbolic_value

    if isinstance(value, ReferenceVariable):
      if sym_ref is None:
        sym_ref = self.ref_to_actual_target(name=name)
        if sym_ref is None:
          sym_ref = symbolic_value
      root_ref = self.symbolic_value_to_ref.get(sym_ref, None)
      if root_ref is None:
        self.ref_to_symbolic_value[value.index] = sym_ref
        self.symbolic_value_to_ref[sym_ref] = value.index
        # not use union because union will make variable attached to it fall apart
        self.ref_disjoint_set.union(value.index, value.index)
      elif root_ref != value.index:
        self.ref_disjoint_set.union(value.index, root_ref)

    if (
      soltype is not None
      and isinstance(soltype, UserDefinedType)
      and isinstance(soltype.type, Enum)
    ):
      thing = select_z3sort(soltype)
      if isinstance(thing, tuple):
        rng = get_variable_default_range(soltype)
        variable = self.state_binding[name]._symbolic_value
        self.add(
          name="@pc",
          soltype=self.pc._type,
          value=self.pc._value,
          symbolic_value=simplify(
            And(self.pc._symbolic_value, variable <= rng[1], variable >= rng[0])
          ),
        )
    if address is not None:
      self.memory[address] = name

  @property
  def pc(self):
    return self.get("@pc")

  def simplify(self):
    for _, v in self.state_binding.items():
      if not isinstance(v._symbolic_value, FunctionContract):
        v._symbolic_value = simplify(v._symbolic_value)

  def __str__(self):
    return repr(self.state_binding)
