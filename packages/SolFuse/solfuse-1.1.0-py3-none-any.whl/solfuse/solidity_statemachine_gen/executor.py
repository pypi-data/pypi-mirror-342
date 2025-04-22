import operator
from copy import deepcopy
from functools import reduce
from typing import List, Tuple

from slither.core.declarations.function import Function
import slither.core.solidity_types.elementary_type as elementary_type
from slither import Slither
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import (
  FunctionContract,
  Contract,
  SolidityFunction,
  SolidityVariable,
  SolidityVariableComposed,
)
from slither.core.declarations.event import Event
from slither.core.declarations.modifier import Modifier
from slither.core.declarations.solidity_variables import (
  SOLIDITY_VARIABLES,
  SOLIDITY_VARIABLES_COMPOSED,
)
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
from slither.core.solidity_types.elementary_type import (
  ElementaryType,
  ElementaryTypeName,
)
from slither.core.variables import *
from z3 import *

from .config import ConfigProvider
from .frame import Frame
from .function_exec_provider import FunctionProvider
from .logger import log
from .summary import Summary
from .utils import Counter
from .variable_type import make_z3variable


class Executor:
  def get_name(self, func: FunctionContract, variable: Variable):
    return (
      variable.name
      if not isinstance(variable, LocalVariable)
      else self.local_variable_name(func, variable)
    )

  class Context:
    def __init__(self, node: Node, frame: Frame) -> None:
      self.node = node
      self.frame = frame

  class NodeVisitor:
    def __init__(self, 主人我是你的狗: "FunctionExecutor") -> None:
      self.owner = 主人我是你的狗
      self.currFrame = self.owner.curr_frame

    def convert_to_full_name(self, member_name, member_type: str):
      member_type = (
        member_type.replace(" external", "").replace(" pure", "").replace(" view", "")
      )
      name = (
        member_name
        + member_type[
          member_type.find("function ") + len("function ") : member_type.find(
            " returns"
          )
        ]
      ).strip()
      return name

    @property
    def func_provider(self) -> FunctionProvider:
      return self.owner.owner.func_provider

    @property
    def contract(self) -> Contract:
      return self.owner.owner.contract

    def get_function_from(self, name: str, method: str) -> List[FunctionContract]:
      return self.owner.owner.get_function_from(name, method)

    def get_function_from_signature(self, sig: str) -> List[FunctionContract]:
      return self.get_function_from(sig, "get_function_from_signature")

    def get_function_from_canonical_name(
      self, canonical_name: str
    ) -> List[FunctionContract]:
      return self.get_function_from(canonical_name, "get_function_from_canonical_name")

    def get_function_from_full_name(self, full_name: str) -> List[FunctionContract]:
      return self.get_function_from(full_name, "get_function_from_full_name")

    @property
    def get_name(self):
      return self.owner.owner.get_name

    @property
    def local_variable_name(self):
      return self.owner.owner.local_variable_name

    @property
    def default_next(self):
      return self.owner.owner.default_counter.next()

    @property
    def config(self) -> ConfigProvider:
      return self.owner.owner.config

    _bin_ops = {
      BinaryOperationType.POWER: operator.pow,
      BinaryOperationType.MULTIPLICATION: operator.mul,
      BinaryOperationType.DIVISION: operator.truediv,
      BinaryOperationType.MODULO: lambda a, b: operator.mod((a), (b)),
      BinaryOperationType.ADDITION: operator.add,
      BinaryOperationType.SUBTRACTION: operator.sub,
      BinaryOperationType.LEFT_SHIFT: operator.lshift,
      BinaryOperationType.RIGHT_SHIFT: operator.rshift,
      BinaryOperationType.AND: operator.and_,
      BinaryOperationType.CARET: operator.xor,
      BinaryOperationType.OR: operator.or_,
      BinaryOperationType.LESS: operator.lt,
      BinaryOperationType.GREATER: operator.gt,
      BinaryOperationType.LESS_EQUAL: operator.le,
      BinaryOperationType.GREATER_EQUAL: operator.ge,
      BinaryOperationType.EQUAL: operator.eq,
      BinaryOperationType.NOT_EQUAL: operator.ne,
      BinaryOperationType.ANDAND: And,
      BinaryOperationType.OROR: Or,
    }

    _assign_ops = {
      AssignmentOperationType.ASSIGN: lambda a, b: b,
      AssignmentOperationType.ASSIGN_OR: operator.or_,
      AssignmentOperationType.ASSIGN_CARET: operator.xor,
      AssignmentOperationType.ASSIGN_AND: operator.and_,
      AssignmentOperationType.ASSIGN_LEFT_SHIFT: operator.lshift,
      AssignmentOperationType.ASSIGN_RIGHT_SHIFT: operator.rshift,
      AssignmentOperationType.ASSIGN_ADDITION: operator.add,
      AssignmentOperationType.ASSIGN_SUBTRACTION: operator.sub,
      AssignmentOperationType.ASSIGN_MULTIPLICATION: operator.mul,
      AssignmentOperationType.ASSIGN_DIVISION: operator.truediv,
      AssignmentOperationType.ASSIGN_MODULO: lambda a, b: operator.mod((a), (b)),
    }

    def handle_default(self, expr: Expression, frame: Frame, *args):
      raise NotImplementedError(type(expr).__name__.split(".")[-1])

    def handle_expression(self, expr: Expression, frame: Frame, *args):
      return getattr(
        self, f'handle_{type(expr).__name__.split(".")[-1]}', self.handle_default
      )(expr, frame, *args)

    def handle_ElementaryTypeNameExpression(
      self, expr: ElementaryTypeNameExpression, frame: Frame, *args
    ):
      return String(expr.type.name)

    def handle_NewElementaryType(self, expr: NewElementaryType, frame: Frame, *args):
      return make_z3variable(expr.type, f"@{self.default_next}d")

    def handle_NewArray(self, expr: NewArray, frame: Frame, *args):
      return make_z3variable(
        expr.array_type, f"@{self.owner.owner.array_counter.next()}arr"
      )

    def handle_MemberAccess(self, expr: MemberAccess, frame: Frame, *args):
      member_expr = expr.expression
      member_type = expr.type
      member_name = expr.member_name
      obj = self.handle_expression(expr.expression, frame=frame)
      if isinstance(member_type, str):
        if member_type in ElementaryTypeName:
          try:
            return frame.get(expr.__str__())
          except Frame.VariableNotFoundException:
            frame.add(name=expr.__str__(), _type=ElementaryType(member_type))
          finally:
            return frame.get(expr.__str__())
        else:  # assume is function
          fixed_full_name = self.convert_to_full_name(member_name, member_type)
          fixed_full_name = fixed_full_name.replace(" memory", "").strip()
          func = self.get_function_from_full_name(fixed_full_name)
          if not func:
            return None
          return func[0]
      else:
        # !我草, 这个分支没有被访问过?? 你的 type 全都是 str 是吧
        assert False

    def handle_TypeConversion(self, expr: TypeConversion, frame: Frame, *args):
      # 我去，不能摆
      thing = self.handle_expression(expr.expression, frame)
      if isinstance(expr._type, ElementaryType):
        if is_array(thing):
          # to get int in bytes{int}
          length = 32
          ret = IntVal(0)
          for i in range(length):
            ret = ret * 0xFF + thing[i]
          simplify(ret)
          return ret
      return thing

    def handle_IndexAccess(self, expr: IndexAccess, frame: Frame, is_left=False):
      index = self.handle_expression(expr.expression_right, frame, False)
      accessed_origin = self.handle_expression(expr.expression_left, frame, is_left)
      if not isinstance(accessed_origin, tuple):
        name = str(accessed_origin)
        body = accessed_origin
      else:
        body, name, accessed, index1 = accessed_origin
      if not is_left:
        return body
      return (body, name, body, index)

    def handle_TupleExpression(self, expr: TupleExpression, frame: Frame, *args):
      tuple_list = [self.handle_expression(e, frame) for e in expr.expressions]
      if not tuple_list:
        dn = make_z3variable(
          ElementaryType("double"), f"@{self.owner.owner.array_counter.next()}arr"
        )
        frame.add(name=str(dn)[1:], sort=dn.sort(), value=dn)
        return dn
      """
      i decided that array has only one element, which makes, having array itself becomes redundant, so you see what i did.
      """
      return tuple_list[-1]

    def handle_CallExpression(self, expr: CallExpression, frame: Frame, *args):
      if expr.called.__str__() in [
        "require(bool)",
        "require(bool,string)",
        "assert(bool)",
      ]:
        cond = self.handle_expression(expr.arguments[0], frame=frame)
        if not isinstance(cond, BoolRef):
          cond = cond != IntVal(0)
        assert isinstance(cond, BoolRef), (cond, isinstance(cond, BoolRef))
        frame.add(
          name="@pc", _type=ElementaryType("bool"), value=And(cond, frame.get("@pc"))
        )
        return
      elif expr.called.__str__() in self.config.constraints_func_names:
        log(
          "found constraints inserted", will_do=self.config.print_on_constraints_found
        )  # type: ignore
        if expr.called.__str__() == self.config.constraints_func_name_complex:
          constraints = eval(
            self.handle_expression(expr.arguments[0], frame=frame).as_string()
          )
          assert is_bool(constraints)
          frame.add(name="@pc", value=And(frame.get("@pc"), constraints))
        elif expr.called.__str__() == self.config.constraints_func_name_simple:
          cond = self.handle_expression(expr.arguments[0], frame=frame)
          if not isinstance(cond, BoolRef):
            cond = cond != IntVal(0)
          assert isinstance(cond, BoolRef), (cond, isinstance(cond, BoolRef))
          frame.add(
            name="@pc", _type=ElementaryType("bool"), value=And(cond, frame.get("@pc"))
          )
        return
      elif expr.called.__str__() == "Verification.Pause":
        breakpoint()
      else:
        if isinstance(expr.called, (NewArray, NewElementaryType)):
          """
          handle separately
          """
          return self.handle_expression(expr.called, frame=frame)
        func = self.handle_expression(expr.called, frame=frame)
        if func is None:
          return
        if isinstance(func, Event):
          # 摆了，密码吗的
          return
        assert isinstance(func, (SolidityFunction, FunctionContract)), (
          str(func),
          type(func),
        )
        ret_type = func.return_type[0] if func.return_type else ElementaryType("int")
        if isinstance(func, SolidityFunction):
          func_name = func.full_name
          real_func = self.func_provider.get_func_status(func_name)
          assert real_func is None
          # dont do solidity function
          dn = make_z3variable(ret_type, f"@{self.default_next}d")
          frame.add(name=str(dn)[1:], sort=dn.sort(), value=dn)
          return dn
        if isinstance(func, (FunctionContract, Modifier)):
          func_name = func.solidity_signature
          real_func = self.func_provider.get_func_status(func_name)
          if real_func is not None:
            # do function now.
            args = [self.handle_expression(i, frame, *args) for i in expr.arguments]
            params = [
              make_z3variable(p.type, self.owner.owner.get_name(func, p))
              for p in func.parameters
            ]
            assert len(args) == len(params)
            d = dict(zip(params, args))
            done_frame = self.owner.owner.exec_func_with_param(
              real_func, d, self.owner.owner
            )
            # summary @ret
            # TODO change this naive impl
            try:
              ret = done_frame[0].get("@ret")
            except Frame.VariableNotFoundException:
              ret = None
            if isinstance(func, Modifier):
              frame.add("@pc", value=And(frame.get("@pc"), done_frame[0].get("@pc")))
            return ret
          dn = make_z3variable(ret_type, f"@{self.default_next}d")
          frame.add(name=str(dn)[1:], sort=dn.sort(), value=dn)
          return dn
          ...
        raise NotImplementedError(expr.called)

    def handle_AssignmentOperation(
      self, expr: AssignmentOperation, frame: Frame, *args
    ):
      if isinstance(expr.expression_left, Identifier) and isinstance(
        expr.expression_left.value, Variable
      ):
        left_name = (
          self.local_variable_name(self.owner.function, expr.expression_left.value)
          if isinstance(expr.expression_left.value, LocalVariable)
          else expr.expression_left.value.name
        )
        try:
          left_expr = frame.get(left_name)
        except Frame.VariableNotFoundException:
          frame.add(left_name, _type=expr.expression_left.value.type, value=None)
          left_expr = frame.get(left_name)
        left_bool = (
          left_expr
          if isinstance(left_expr, BoolRef)
          else left_expr != 0
          if is_int(left_expr)
          else None
        )
        right_expr = self.handle_expression(expr.expression_right, frame=frame)
        if right_expr is None:
          return
        right_bool = (
          right_expr
          if isinstance(right_expr, BoolRef)
          else right_expr != 0
          if is_int(right_expr)
          else None
        )  # TODO
        res = None
        if expr.type in (
          AssignmentOperationType.ASSIGN_OR,
          AssignmentOperationType.ASSIGN_CARET,
          AssignmentOperationType.ASSIGN_AND,
        ):
          res = self._assign_ops[expr.type](left_bool, right_bool)
        else:
          res = self._assign_ops[expr.type](  # type: ignore
            left_expr, right_expr
          )  # type: ignore
        frame.add(left_name, _type=expr.expression_left.value.type, value=res)
        return res
      elif isinstance(expr.expression_left, IndexAccess):
        index_access = self.handle_expression(expr.expression_left, frame, True)
        select, name, accessed, index = index_access
        assert isinstance(name, str)
        name = frame.get_rbinding(accessed)[0]
        rhs = self.handle_expression(expr.expression_right, frame)
        frame.add(name=name, value=rhs)
        return rhs
      elif isinstance(expr.expression_left, MemberAccess):
        left_expr = self.handle_expression(expr.expression_left, frame)
        right_expr = self.handle_expression(expr.expression_right, frame)
        left_bool = (
          left_expr
          if isinstance(left_expr, BoolRef)
          else left_expr != 0
          if is_int(left_expr)
          else None
        )
        right_bool = (
          right_expr
          if isinstance(right_expr, BoolRef)
          else right_expr != 0
          if is_int(right_expr)
          else None
        )  # TODO
        res = None
        if expr.type in (
          AssignmentOperationType.ASSIGN_OR,
          AssignmentOperationType.ASSIGN_CARET,
          AssignmentOperationType.ASSIGN_AND,
        ):
          res = self._assign_ops[expr.type](left_bool, right_bool)
        else:
          res = self._assign_ops[expr.type](  # type:ignore
            left_expr, right_expr
          )  # type:ignore
        frame.add(str(expr.expression_left), value=res)
        return res
      raise NotImplementedError(type(expr.expression_left).__name__)

    def handle_ConditionalExpression(
      self, expr: ConditionalExpression, frame: Frame, *args
    ):
      cond = self.handle_expression(expr.if_expression, frame=frame)
      then = self.handle_expression(expr.then_expression, frame=frame)
      el = self.handle_expression(expr.else_expression, frame=frame)
      return If(cond, then, el)

    def handle_BinaryOperation(self, expr: BinaryOperation, frame: Frame, *args):
      op1 = self.handle_expression(expr.expression_left, frame)
      op2 = self.handle_expression(expr.expression_right, frame)
      if op1 is not None and op2 is not None:
        if expr.type in (BinaryOperationType.MODULO, BinaryOperationType.MODULO_SIGNED):
          frame.add(name="@pc", value=And(frame.get("@pc"), op2 != IntVal(0)))
        if expr.type in (
          BinaryOperationType.LEFT_SHIFT,
          BinaryOperationType.RIGHT_SHIFT,
          BinaryOperationType.AND,
          BinaryOperationType.CARET,
          BinaryOperationType.OR,
        ):
          return BV2Int(self._bin_ops[expr.type](Int2BV(op1, 256), Int2BV(op2, 256)))
        return self._bin_ops[expr.type](op1, op2)
      return op1 if op1 is not None else op2

    def handle_UnaryOperation(self, expr: UnaryOperation, frame: Frame, *args):
      op = self.handle_expression(expr.expression, frame, True)
      if isinstance(op, Tuple):
        op_right = op[0]
      else:
        op_right = op
      opr = expr.type
      match opr:
        case UnaryOperationType.BANG:
          if isinstance(op_right, BoolRef):
            return Not(op_right)
          return op_right != 0
        case UnaryOperationType.TILD:
          return ~op_right
        case UnaryOperationType.DELETE:
          assert False, "not implemented"
      if not isinstance(expr.expression, IndexAccess):
        name = (
          self.owner.owner.local_variable_name(
            self.owner.function, expr.expression.value
          )
          if isinstance(expr.expression.value, LocalVariable)
          else expr.expression.value.name
        )
      else:
        select, name, accessed, index = op
        assert isinstance(name, str)
        name = frame.get_rbinding(accessed)[0]
        op = accessed
      match opr:
        case UnaryOperationType.PLUSPLUS_PRE:
          res = op + 1
          assert expr.expression.is_lvalue, "nope"
          frame.add(name, value=res)  # type: ignore
          return res
        case UnaryOperationType.MINUSMINUS_PRE:
          res = op - 1
          assert expr.expression.is_lvalue, "nope"
          frame.add(name, value=res)  # type: ignore
          return res
        case UnaryOperationType.PLUSPLUS_POST:
          res = op + 1
          assert expr.expression.is_lvalue, "nope"
          frame.add(name, value=res)  # type: ignore
          return op
        case UnaryOperationType.MINUSMINUS_POST:
          res = op - 1
          assert expr.expression.is_lvalue, "nope"
          frame.add(name, value=res)  # type: ignore
          return op
        case UnaryOperationType.PLUS_PRE:
          return op
        case UnaryOperationType.MINUS_PRE:
          return -op

    def handle_Literal(self, expr: Literal, frame: Frame, *args):
      if isinstance(expr.type, ElementaryType):
        if expr.value in ("true", "false"):
          return BoolVal(expr.value == "true")
        x = None
        if (
          expr.type.name
          in elementary_type.Int + elementary_type.Uint + elementary_type.Byte
        ):
          x = IntVal(eval(expr.value))
        else:
          x = StringVal(expr.value)
        return x
      raise NotImplemented(expr.type.__name__)

    def handle_Identifier(self, expr: Identifier, frame: Frame, *args):
      # returns identifier in the binding, if not, make a new one
      if isinstance(expr.value, Contract):
        ...
      if isinstance(expr.value, Variable):
        name = (
          self.owner.owner.local_variable_name(expr.value.function, expr.value)
          if isinstance(expr.value, LocalVariable)
          else expr.value.name
        )
        try:
          frame.get(name)
        except Frame.VariableNotFoundException:
          frame.add(_type=expr.value.type, name=f"{name}")
        finally:
          return frame.get(name)
      if isinstance(expr.value, SolidityVariable):
        if expr.value.name in SOLIDITY_VARIABLES:
          the_type = ElementaryType(SOLIDITY_VARIABLES[expr.value.name])
          try:
            frame.get(expr.value.name)
          except Frame.VariableNotFoundException:
            frame.add(_type=the_type, name=expr.value.name)
          finally:
            return frame.get(expr.value.name)
      if isinstance(expr.value, SolidityVariableComposed):
        the_type = ElementaryType(SOLIDITY_VARIABLES_COMPOSED[expr.value.name])
        try:
          frame.get(expr.value.name)
        except Frame.VariableNotFoundException:
          frame.add(_type=the_type, name=expr.value.name)
        finally:
          return frame.get(expr.value.name)
      if isinstance(expr.value, SolidityFunction):
        # referring to the source code and found that len(list) <= 1
        ret_type = expr.value.return_type
        if len(ret_type) == 1:
          ret_type = ret_type[0]
        else:
          # this is just default =)
          ret_type = ElementaryType("int")
        return expr.value
      if isinstance(expr.value, (Modifier, FunctionContract)):
        func = expr.value
        ret_type = func.return_type[0] if func.return_type else ElementaryType("int")
        return func
      if isinstance(expr.value, Event):
        return expr.value
      raise NotImplementedError(type(expr.value))

    def visit(self, node: Node, frame: Frame):
      global global_tab
      log(
        f"\033[34m{node.expression}\033[0m",
        will_do=self.config.print_stmt,
        indent=self.config.global_tab,
      ) if node.expression else None
      self.currFrame = frame
      v = getattr(
        self, f'visit_{node.type.__str__().split(".")[1]}', self.visit_default
      )(node, self.currFrame)
      return v

    def visit_PLACEHOLDER(self, node: Node, frame: Frame):
      assert node.type is NodeType.PLACEHOLDER
      ...

    def visit_default(self, node: Node, frame: Frame):
      raise NotImplementedError(node.type)

    def visit_CONTINUE(self, node: Node, frame: Frame): ...

    def visit_ASSEMBLY(self, node: Node, frame: Frame): ...

    def visit_ENDASSEMBLY(self, node: Node, frame: Frame): ...

    def visit_ENTRYPOINT(self, node: Node, frame: Frame):
      func: FunctionContract = node.function
      for variable in func.contract.state_variables + func.parameters:
        value = None
        if variable.expression is not None:
          value = self.owner.owner.eval_expr(variable.expression)
        name = (
          self.owner.owner.local_variable_name(func, variable)
          if isinstance(variable, LocalVariable)
          else variable.name
        )
        frame.add(name=name, value=value, _type=variable.type)
      ...

    def visit_OTHER_ENTRYPOINT(self, node: Node, frame: Frame):
      self.visit_ENTRYPOINT(node, frame)

    def visit_EXPRESSION(self, node: Node, frame: Frame):
      assert node.expression, "impossible"
      result = self.handle_expression(node.expression, frame)
      return result

    def visit_RETURN(self, node: Node, frame: Frame):
      t = node.function.return_type
      if t:
        t = t[0]
      if node.expression is not None:
        result = self.handle_expression(node.expression, frame)
        # * i am so foolish, why did i forget that i can just use function's return type to help me?
        frame.add("@ret", _type=t, value=result)
      else:
        frame.add("@ret", None)

    def visit_IF(self, node: Node, frame: Frame):
      assert node.expression, "impossible"
      cond = self.handle_expression(node.expression, frame=frame)
      notcond = Not(cond)
      solver_true = Solver()
      solver_false = Solver()
      frame.simplify()
      solver_true.add(simplify(And(Not(cond), frame.get("@pc"))))
      solver_false.add(simplify(And(Not(notcond), frame.get("@pc"))))
      true_res = solver_true.check()
      false_res = solver_false.check()
      # assert not (true_res == unsat and false_res == unsat)
      if true_res == unsat:
        self.owner.next_branch = True
        frame.add("@pc", ElementaryType("bool"), And(cond, frame.get("@pc")))
      elif false_res == unsat:
        self.owner.next_branch = False
        frame.add("@pc", ElementaryType("bool"), And(notcond, frame.get("@pc")))
      else:
        # update pc and make executor execute false branch next
        self.owner.next_branch = True
        frame_replicant = deepcopy(frame)
        frame_replicant.add(
          "@pc", ElementaryType("bool"), And(notcond, frame.get("@pc"))
        )
        frame.add("@pc", ElementaryType("bool"), And(cond, frame.get("@pc")))
        # log(f'\033[32mforking!!!\033[0m')
        self.owner.queue.append(Executor.Context(node.son_false, frame_replicant))

    def visit_VARIABLE(self, node: Node, frame: Frame):
      assert node.variable_declaration, (node.expression, node.variable_declaration)
      name = self.owner.owner.local_variable_name(
        node.function, node.variable_declaration
      )
      frame.add(
        name,
        _type=node.variable_declaration.type,
        value=self.handle_expression(node.expression, frame)
        if node.expression
        else None,
        need_default=node.variable_declaration.name
        not in list(map(lambda x: x.name, node.function.parameters)),
      )
      return frame.get(name)

    def visit_ENDIF(self, node: Node, frame: Frame):
      pass

    def visit_IFLOOP(self, node: Node, frame: Frame):
      self.visit_IF(node, frame)  # * 真的吗

    def visit_STARTLOOP(self, node: Node, frame: Frame):
      # TODO: make a new frame, init it and make it child of currFrame
      new_frame = Frame(frame)
      self.currFrame = new_frame

    def visit_ENDLOOP(self, node: Node, frame: Frame):
      self.currFrame = frame.father  # back one layer of stack

  class FunctionExecutor:
    def __init__(
      self, nodelist: list[Node], entry: Node, 主人我是你的狗: "Executor"
    ) -> None:
      assert entry.type in (NodeType.ENTRYPOINT, NodeType.OTHER_ENTRYPOINT), entry.type
      self.owner = 主人我是你的狗
      self.function = entry.function
      self.curr_node = None
      self.curr_frame = Frame(None)
      self.done_frame = []
      self.constants = set()
      # init pc, not done in Frame initialization because sub frame will have its own pc
      self.curr_frame.variables["@pc"] = Bool("@pc")
      self.curr_frame.binding[self.curr_frame.variables["@pc"]] = BoolVal(True)
      self.queue = [Executor.Context(entry, self.curr_frame)]
      self.nodelist = nodelist
      self.next_branch = True
      self.visitor = Executor.NodeVisitor(self)

    @property
    def config(self) -> ConfigProvider:
      return self.owner.config

    def exec(self):
      global global_tab
      log(
        f"\033[34mdoing {self.nodelist[0].function.full_name}\033[0m",
        will_do=self.config.print_executor_process,
        indent=self.config.global_tab,
      )  # type: ignore
      self.config.global_tab += 1
      while len(self.queue) != 0:
        begin = self.queue.pop(0)
        self.next_branch = True
        self.curr_node = begin.node
        self.curr_frame = begin.frame
        self.visitor.visit(self.curr_node, self.curr_frame)
        while len(self.curr_node.sons) != 0:
          if self.curr_node.type in (NodeType.IF, NodeType.IFLOOP):
            self.curr_node = self.curr_node.sons[(1, 0)[self.next_branch]]
          else:
            self.curr_node = self.curr_node.sons[0]
          self.curr_frame = self.visitor.currFrame
          self.visitor.visit(self.curr_node, self.curr_frame)
        self.curr_frame = self.visitor.currFrame
        self.curr_frame.simplify()
        self.done_frame.append(self.curr_frame)
      self.config.global_tab -= 1

  class PureDescriptor:
    def __init__(
      self,
      name: str,
      func: FunctionContract,
      context: "FunctionExecutor",
      params,
      expr,
      pc,
    ) -> None:
      self.name = name
      self.func = func
      self.context = context
      self.params = params
      self.expr = expr
      self.pc = pc

  def __init__(
    self, contract: Contract, slither: Slither, config: ConfigProvider
  ) -> None:
    self.curr_frame = {}
    self.done_frame = {}
    self.constants = {}
    self.pure_function_expr: dict = {}
    self.slither = slither
    self.contract = contract
    self.array_counter = Counter()
    self.default_counter = Counter()
    self.func_provider = FunctionProvider(contract)
    self.summary: Summary = Summary(contract, config=config)
    self.config = config

  def local_variable_name(self, func: FunctionContract, variable: LocalVariable):
    return f"{func.name}.{str(variable)}"

  def get_function_from(self, name: str, method: str) -> List[FunctionContract]:
    result = []
    for i in self.slither.contracts:
      fun_list = i.__getattribute__(method)(name)
      if fun_list:
        result.append(fun_list)
    return result

  def get_function_from_signature(self, sig: str) -> List[FunctionContract]:
    return self.get_function_from(sig, "get_function_from_signature")

  def get_function_from_canonical_name(
    self, canonical_name: str
  ) -> List[FunctionContract]:
    return self.get_function_from(canonical_name, "get_function_from_canonical_name")

  def get_function_from_full_name(self, full_name: str) -> List[FunctionContract]:
    return self.get_function_from(full_name, "get_function_from_full_name")

  @property
  def functions(self):
    return self.contract.functions_declared

  @property
  def global_tab(self) -> int:
    return self.config.global_tab

  @global_tab.setter
  def global_tab(self, value: int):
    self._global_tab = value

  @property
  def print_summary_process(self) -> bool:
    return self.config.print_summary_process

  @property
  def constraints_func_names(self) -> Tuple[str, str]:
    return self.config.constraints_func_names

  @property
  def print_executor_process(self) -> bool:
    return self.config.print_executor_process

  def do_summary(self):
    self.summary.constants = self.constants
    for k, v in self.summary.constants.items():
      self.summary.constants[k] = reduce(
        lambda x, y: x.union(y), self.summary.constants.values()
      )
    for func in self.functions:
      log(
        f"\033[34mdoing {func.name}\033[0m",
        indent=self.global_tab,
        will_do=self.print_summary_process,
      )  # type: ignore
      self.global_tab += 1
      if (
        self.done_frame.get(func, None) is None
        or func.name in self.constraints_func_names
      ):
        if func.name not in self.constraints_func_names:
          self.done_frame[func] = self.curr_frame[func]
        else:
          continue
      self.summary.set_func_pre(
        func, reduce(Or, map(lambda x: x.get("@pc"), self.done_frame[func]))
      )
      self.summary.set_func_post(func, self.done_frame[func])
      self.global_tab -= 1

  def do_pure(self):
    log(
      "doing pure function", will_do=self.print_executor_process, indent=self.global_tab
    )
    for func in list(filter(lambda x: x.pure, self.functions)):
      if func in self.pure_function_expr:
        continue
      self.do_exec_pure_func(func)

  def do_exec(self):
    self.do_pure()
    log(
      "doing non-pure function",
      will_do=self.print_executor_process,
      indent=self.global_tab,
    )
    for func in self.functions:
      if not func.pure and not func.name in self.constraints_func_names:
        self.do_exec_non_pure_func(func)

  def do_exec_func(self, func: FunctionContract):
    assert func.entry_point
    func_exec = self.FunctionExecutor(func.nodes, func.entry_point, self)
    func_exec.exec()
    return func_exec

  def do_exec_pure_func(self, func: FunctionContract):
    log(
      "doing pure function", will_do=self.print_executor_process, indent=self.global_tab
    )
    func_exec = self.do_exec_non_pure_func(func=func)
    parameters = func.parameters
    # !TODO change this naive line
    ret = None
    try:
      ret = func_exec.done_frame[0].get("@ret")
    except Frame.VariableNotFoundException:
      ret = func_exec.done_frame[0].get(f"{func.name}.{str(func.returns[0])}")
    pure_desc = self.PureDescriptor(
      func.name, func, func_exec, parameters, ret, func_exec.done_frame[0].get("@pc")
    )
    self.pure_function_expr[func] = pure_desc

  def do_exec_non_pure_func(self, func: FunctionContract):
    func_exec = self.do_exec_func(func)
    self.constants[func] = func_exec.constants
    self.done_frame[func] = func_exec.done_frame
    self.curr_frame[func] = func_exec.curr_frame
    return func_exec

  def exec_func_with_param(self, function: FunctionContract, params: dict, owner):
    if function.pure:
      """
      directly substitute
      """
      fdesc = self.pure_function_expr.get(function, None)
      if not fdesc:
        self.do_exec_pure_func(function)
        fdesc: Executor.PureDescriptor = self.pure_function_expr[function]
      expr = substitute(
        fdesc.expr,
        list(
          map(lambda x: (Const(f"@{str(x[0])}", x[0].sort()), x[1]), params.items())
        ),
      )
      f = Frame(None)
      f.add(name="@ret", value=expr, sort=expr.sort())
      f.add(name="@pc", value=fdesc.pc, sort=fdesc.pc.sort())
      return [f]
    else:
      assert function.entry_point
      func_exec = Executor.FunctionExecutor(function.nodes, function.entry_point, owner)
      expr = func_exec.curr_frame.get("@pc")
      for k, v in params.items():
        expr = And(expr, k == v)
      for i in zip(function.parameters, params.keys()):
        expr = And(expr, make_z3variable(i[0].type, i[0].name) == i[1])
      func_exec.curr_frame.add("@pc", value=expr)
      func_exec.exec()
      return func_exec.done_frame

  def eval_expr(self, expr: Expression):
    assert self.functions[0].entry_point
    fun_exec = self.FunctionExecutor(
      self.functions[0].nodes, self.functions[0].entry_point, self
    )
    node_visit = self.NodeVisitor(fun_exec)
    return node_visit.handle_expression(expr, Frame(None))
