from z3.z3 import BoolRef, IntNumRef, SeqRef, IntVal
from .handler import Handler
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import FunctionContract
from slither.core.expressions import AssignmentOperation
from slither.core.expressions import AssignmentOperationType
from slither.core.expressions import BinaryOperation
from slither.core.expressions import BinaryOperationType
from slither.core.expressions import CallExpression
from slither.core.expressions import ConditionalExpression
from slither.core.expressions import ElementaryTypeNameExpression
from slither.core.expressions import Identifier, Literal
from slither.core.expressions import IndexAccess
from slither.core.expressions import MemberAccess
from slither.core.expressions import NewArray
from slither.core.expressions import NewElementaryType
from slither.core.expressions import TupleExpression
from slither.core.expressions import TypeConversion
from slither.core.expressions import UnaryOperation
from slither.core.expressions import UnaryOperationType
from slither.core.expressions.expression import Expression

from slither.core.variables import (
  StateVariable,
  LocalVariable,
  LocalVariableInitFromTuple,
)

from slither.slithir.operations import (
  Operation,
  Assignment,
  Binary,
  BinaryType,
)
from slither.slithir.variables import (
  Constant,
  ReferenceVariable,
  StateIRVariable,
  TemporaryVariable,
  TupleVariable,
)
from slither.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue, LVALUE, RVALUE
from slither.core.declarations import SolidityVariable, SolidityVariableComposed
from typing import Callable, Tuple, List

from z3 import (
  IntVal,
  BoolVal,
  StringVal,
  is_array,
  is_int,
  Int2BV,
  BV2Int,
  simplify,
  is_string,
)
from .handler import Handler, ForkSelector
from .env import Env, SymbolNotFoundError
from .logger import log
from .utils import (
  get_variable_default_value,
  get_variable_name,
  make_z3variable,
  ref_to_actual_target,
)


class VariableHandler(Handler):
  def __init__(self) -> None:
    super().__init__(name_dispatch_keyword="variable")

  def handle_Constant(
    self, variable: Constant, env: Env, *args, **kwargs
  ) -> BoolRef | IntNumRef | SeqRef:
    match value := variable.value:
      case bool():
        return BoolVal(val=value)
      case int():
        return IntVal(val=value)
      case str():
        return StringVal(s=value)
      case _:
        assert False, "value should only be bool, int or str"

  def handle_StateVariable(self, variable: StateVariable, env: Env, *args, **kwargs):
    assert isinstance(variable, StateVariable)
    # ? this should be fine, because state variables are always predefined at entry point by node handler
    return env.get(name=get_variable_name(variable=variable))._symbolic_value

  def handle_SolidityVariable(
    self, variable: SolidityVariable, env: Env, *args, **kwargs
  ):
    # ? It seems i cannot decide any value of a solidity variable, probably just return some random
    value = None
    try:
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    except SymbolNotFoundError:
      env.add(
        name=get_variable_name(variable=variable), soltype=variable.type, value=variable
      )
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    if variable.name == "msg.sender":
      env.binding[get_variable_name(variable=variable)]._is_on_chain = True
      env.binding[get_variable_name(variable=variable)]._symbolic_value = IntVal(
        0x00A329C0648769A73AFAC7F9381E08FB43DBEA72
      )
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    return value
    self.handle_default(variable=variable, env=env)

  def handle_TemporaryVariable(
    self, variable: TemporaryVariable, env: Env, *args, **kwargs
  ):
    assert isinstance(variable, TemporaryVariable)
    return env.get(name=get_variable_name(variable=variable))._symbolic_value

  def handle_LocalVariable(self, variable: LocalVariable, env: Env, *args, **kwargs):
    assert isinstance(variable, LocalVariable)
    return env.get(name=get_variable_name(variable=variable))._symbolic_value

  def handle_SolidityVariableComposed(
    self, variable: SolidityVariableComposed, env: Env, *args, **kwargs
  ):
    value = None
    try:
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    except SymbolNotFoundError:
      env.add(
        name=get_variable_name(variable=variable), soltype=variable.type, value=variable
      )
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    if variable.name == "msg.sender":
      env.binding[get_variable_name(variable=variable)]._is_on_chain = True
      env.binding[get_variable_name(variable=variable)]._symbolic_value = IntVal(
        0x00A329C0648769A73AFAC7F9381E08FB43DBEA72
      )
      value = env.get(name=get_variable_name(variable=variable))._symbolic_value
    return value
    self.handle_default(variable=variable, env=env)

  def handle_ReferenceVariable(
    self, variable: ReferenceVariable, env: Env, *args, **kwargs
  ):
    if getattr(variable, "sym_right", None) is None:
      return env.get(name=get_variable_name(variable=variable))._symbolic_value
      # return ref_to_actual_target(env.get(get_variable_name(variable=variable)), env)
    value_left = self.handle_(variable=variable.points_to, env=env)
    if not is_array(value_left):
      if is_int(value_left):
        return simplify(
          BV2Int(
            (Int2BV(value_left, 256) >> Int2BV(variable.sym_right, 256) << 3) & 0xFF,
            256,
          )
        )
      assert is_string(value_left), "Handle other cases"
      return (self.handle_(variable=variable.points_to, env=env))[variable.sym_right]
    return (self.handle_(variable=variable.points_to, env=env))[variable.sym_right]
    self.handle_default(variable=variable, env=env)

  def handle_LocalVariableInitFromTuple(
    self, variable: LocalVariableInitFromTuple, env: Env, *args, **kwargs
  ):
    return env.get(name=get_variable_name(variable))._symbolic_value
    self.handle_default(variable=variable, env=env)

  def handle_FunctionContract(
    self, variable: FunctionContract, env: Env, *args, **kwargs
  ):
    return variable
    self.handle_default(variable=variable, env=env)

  def handle_TupleVariable(self, variable: TupleVariable, env: Env, *args, **kwargs):
    return make_z3variable(_type=variable.type, name=get_variable_name(variable))
