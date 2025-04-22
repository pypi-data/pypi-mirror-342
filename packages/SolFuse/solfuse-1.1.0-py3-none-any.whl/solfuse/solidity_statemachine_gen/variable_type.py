import slither.core.solidity_types.elementary_type as elementary_type
from slither.core.solidity_types.array_type import ArrayType
from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.solidity_types.mapping_type import MappingType
from slither.core.solidity_types.type import Type
from slither.core.solidity_types.user_defined_type import UserDefinedType
from z3 import *


def from_variable_to_soildity(): ...


def select_z3sort(_type: Type) -> SortRef:
  if isinstance(_type, ElementaryType):
    if _type.name == "bool":
      return BoolSort()
    elif _type.name == "string":
      return StringSort()
    elif _type.name == "address":
      return IntSort()
    elif (
      _type.name in elementary_type.Int + elementary_type.Uint + elementary_type.Byte
    ):
      return IntSort()
    elif _type.name in elementary_type.Fixed + elementary_type.Ufixed:
      return RealSort()
    else:
      return RealSort()
  elif isinstance(_type, ArrayType):
    return select_z3sort(_type.type)
  elif isinstance(_type, MappingType):
    return select_z3sort(_type.type_to)
  elif isinstance(_type, UserDefinedType):
    return RealSort()


def get_variable_default_value(_type: Type):
  assert isinstance(_type, ElementaryType)
  if _type.name == "bool":
    return BoolVal(False)
  if _type.name == "string":
    return String("")
  if _type.name in elementary_type.Int + elementary_type.Uint + elementary_type.Byte + [
    "address"
  ]:
    return IntVal(0)
  if _type.name in elementary_type.Fixed + elementary_type.Ufixed:
    return Real(0)


def get_variable_range(_type: Type):
  if _type is None or not isinstance(_type, ElementaryType):
    return None
  if _type.name == "bool":
    return None

  if _type.name == "string":
    return ()  # why in the hell i need this?

  if _type.name == "address":
    return (0, 1 << (8 * 20) - 1)

  if _type.name in elementary_type.Int:
    return (-(1 << (int(_type.name[3:]) - 1)), (1 << (int(_type.name[3:]) - 1)) - 1)

  if _type.name in elementary_type.Uint:
    return (0, (1 << (int(_type.name[4:]))) - 1)
  return None


def make_z3variable(_type: Type, name: str):
  # * elementary type
  if _type is None:
    return Real(name)
  if isinstance(_type, ElementaryType):
    if _type.name == "bool":
      return Bool(name)
    elif _type.name == "string":
      return String(name)
    elif _type.name == "address":
      return Int(name)
    elif (
      _type.name in elementary_type.Int + elementary_type.Uint + elementary_type.Byte
    ):
      return Int(name)
    elif _type.name in elementary_type.Fixed + elementary_type.Ufixed:
      return Real(name)
    else:
      # TODO i dont know what _type == 'var' means so just put a Real here. may change later.
      return Real(name)
  elif isinstance(_type, ArrayType):
    return Const(name, select_z3sort(_type.type))
  elif isinstance(_type, MappingType):
    return Const(name, select_z3sort(_type.type_to))
  return Real(name)
