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

from slither.core.variables.state_variable import StateVariable

from slither.slithir.operations import Operation, Assignment, Binary, BinaryType
from slither.slithir.variables import Constant, ReferenceVariable, StateIRVariable
from slither.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue, LVALUE, RVALUE
from typing import Callable, Tuple, List

from z3 import IntVal, BoolVal, StringVal
from .handler import Handler, ForkSelector
from .env import Env
from .logger import log
from .utils import get_variable_default_value


class ExprHandler(Handler):
  def __init__(self) -> None:
    super().__init__(name_dispatch_keyword="expr")
