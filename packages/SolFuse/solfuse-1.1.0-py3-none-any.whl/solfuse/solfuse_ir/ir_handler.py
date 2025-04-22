from __future__ import annotations
from typing import Any, Callable, Iterable, Tuple, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
  from solfuse.solfuse_ir.pure_descriptor import PureDescriptor
  from solfuse.solfuse_ir.engine import Engine
  from solfuse.solfuse_ir.function_engine import FunctionEngine
from copy import deepcopy
from random import randint
from slither.core.variables.variable import Variable
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import (
  FunctionContract,
  SolidityFunction,
  Function,
  Contract,
  EnumContract,
  Enum,
  SolidityVariable,
  SolidityVariableComposed,
)
from slither.core.expressions import Identifier, Literal

from slither.core.variables import StateVariable, LocalVariable

from slither.core.solidity_types import (
  ElementaryType,
  ArrayType,
  elementary_type,
  UserDefinedType,
  MappingType,
)

from slither.slithir.operations import (
  Operation,
  Nop,
  Assignment,
  InternalDynamicCall,
  Call,
  OperationWithLValue,
  NewStructure,
  Binary,
  BinaryType,
  Send,
  Return,
  Delete,
  SolidityCall,
  NewContract,
  InternalCall,
  HighLevelCall,
  Condition,
  Unary,
  Unpack,
  UnaryType,
  Index,
  TypeConversion,
  InitArray,
  EventCall,
  LibraryCall,
  NewArray,
  Length,
  Member,
  NewElementaryType,
  LowLevelCall,
  Transfer,
)
from slither.slithir.operations.codesize import CodeSize
from slither.slithir.variables import (
  Constant,
  ReferenceVariable,
  StateIRVariable,
  TemporaryVariable,
  TupleVariable,
)
from slither.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue, LVALUE, RVALUE
from slither.core.solidity_types.type import Type

from z3 import (
  IntVal,
  BoolVal,
  StringVal,
  And,
  Or,
  If,
  simplify,
  is_string,
  Not,
  Select,
  Store,
  Int2BV,
  BV2Int,
  Datatype,
  is_bool,
  is_int,
  Int,
  IntSort,
  substitute,
  is_arith,
  Const,
  Array,
)

from .config import ConfigProvider, default_config

from .handler import Handler, ForkSelector
from .expr_handler import ExprHandler
from .variable_handler import VariableHandler
from .env import Env, SymbolNotFoundError
from .logger import log
from .utils import (
  get_real_sort,
  get_return_name,
  get_variable_default_value,
  get_variable_name,
  compute_merged_env,
  make_z3variable,
  ref_to_actual_target,
  select_z3sort,
)

import operator
from . import function_engine, symbolic_debug

ir_bin_ops = {
  BinaryType.POWER: operator.pow,
  BinaryType.MULTIPLICATION: operator.mul,
  BinaryType.DIVISION: operator.truediv,
  BinaryType.MODULO: lambda a, b: operator.mod((a), (b)),
  BinaryType.ADDITION: operator.add,
  BinaryType.SUBTRACTION: operator.sub,
  BinaryType.LEFT_SHIFT: operator.lshift,
  BinaryType.RIGHT_SHIFT: operator.rshift,
  BinaryType.AND: operator.and_,
  BinaryType.CARET: operator.xor,
  BinaryType.OR: operator.or_,
  BinaryType.LESS: operator.lt,
  BinaryType.GREATER: operator.gt,
  BinaryType.LESS_EQUAL: operator.le,
  BinaryType.GREATER_EQUAL: operator.ge,
  BinaryType.EQUAL: operator.eq,
  BinaryType.NOT_EQUAL: operator.ne,
  BinaryType.ANDAND: And,
  BinaryType.OROR: Or,
}

solidity_call_list = (
  "require(bool)",
  "require(bool,string)",
  "assert(bool)",
  "calldatasize()",
)

require_list = ("require(bool)", "require(bool,string)", "assert(bool)")

SOLIDITY_MAX_RECURSION_LIMIT = 10


class IRHandler(Handler):
  def __init__(
    self,
    expr_handler: Handler = ExprHandler(),
    variable_handler: Handler = VariableHandler(),
    config: ConfigProvider = default_config,
  ) -> None:
    super().__init__(name_dispatch_keyword="ir")
    self.expr_handler = expr_handler
    self.variable_handler = variable_handler
    self.config = config
    self.done_ctx_slither_construct = None
    self.done_ctx_constant = None
    self.done_ctx_constructor = None

  @property
  def from_engine(self):
    return self._from

  @from_engine.setter
  def from_engine(self, value):
    self._from = value
    self.expr_handler.from_engine = value
    self.variable_handler.from_engine = value

  @staticmethod
  def get_sym_ref(val: Variable, env: Env):
    if isinstance(val, Function):
      return val
    sym_ref = None
    name = get_variable_name(val)
    # * compute sym_ref
    if isinstance(val, ReferenceVariable):
      try:
        sym_ref = env.ref_to_actual_target(name)
      except:
        pass
      if sym_ref is None:
        points_to_origin = val.points_to_origin
        if points_to_origin is None:
          return sym_ref
        points_to_origin_name = get_variable_name(points_to_origin)
        points_to_origin_value = env.get(points_to_origin_name)
        sym_ref = points_to_origin_value._symbolic_value
    return sym_ref

  def handle_Assignment(
    self, ir: Assignment, env: Env, assign_local: bool = False, *args, **kwargs
  ):
    lval = ir.lvalue
    l_name = get_variable_name(lval)
    rval = ir.rvalue
    rval_evaled = self.variable_handler.handle_(variable=rval, env=env)
    # * update function table

    try:
      expr = env.get(get_variable_name(lval))
      if isinstance(rval_evaled, Function):
        env.functable[expr._symbolic_value] = rval_evaled
    except SymbolNotFoundError:
      pass

    if (
      isinstance(lval.type, ElementaryType)
      and lval.type.name == "address"
      and isinstance(rval.type, UserDefinedType)
      and isinstance(rval.type.type, Contract)
    ):
      addr = getattr(env.get(get_variable_name(rval)), "_address", None)
      env.add(name=l_name, soltype=lval.type, value=lval, symbolic_value=addr)
      return

    should_modify_address = (
      isinstance(rval.type, ElementaryType) and rval.type.name == "address"
    ) or (
      isinstance(rval.type, UserDefinedType)
      and isinstance(rval.type.type, Contract)
      and is_int(rval_evaled)
    )

    # * compute sym_ref
    sym_ref = self.get_sym_ref(rval, env)

    if not should_modify_address:
      env.add(
        name=l_name,
        soltype=lval.type,
        value=lval,
        symbolic_value=rval_evaled,
        sym_ref=sym_ref,
      )
    else:
      val = None
      try:
        val = env.get(name=l_name)._symbolic_value
      except SymbolNotFoundError:
        pass
      env.add(
        name=l_name,
        soltype=lval.type,
        value=lval,
        symbolic_value=val,
        address=rval_evaled,
        sym_ref=sym_ref,
      )

  def handle_Binary(self, ir: Binary, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    variable_left = ir.variable_left
    variable_right = ir.variable_right

    # assert not isinstance(lvalue, ReferenceVariable)  # ! TODO: expand later
    # ? I think there is no need to modify the infomation of lvalue in binary operation
    # ? because the reference relationship never changes
    assert isinstance(variable_left, RVALUE)
    assert isinstance(variable_right, RVALUE)

    value_left = self.variable_handler.handle_(variable=variable_left, env=env)
    value_right = self.variable_handler.handle_(variable=variable_right, env=env)
    if ir.type in (
      BinaryType.LEFT_SHIFT,
      BinaryType.RIGHT_SHIFT,
      BinaryType.AND,
      BinaryType.CARET,
      BinaryType.OR,
    ):
      result = BV2Int(
        ir_bin_ops[ir.type](Int2BV(value_left, 256), Int2BV(value_right, 256))
      )
    else:
      # TODO: for variables cast to address or some kind. temporary solution, needs proper treat later.
      if not (value_left.sort() == value_right.sort()) and (
        not is_int(value_left) or not is_int(value_right)
      ):
        rand_val_1 = Int(f"@randint_{str(abs(hash(value_left)))}")
        rand_val_2 = Int(f"@randint_{str(abs(hash(value_right)))}")
        if not is_int(value_left) and not is_int(value_right):
          result = ir_bin_ops[ir.type](rand_val_1, rand_val_2)
        elif not is_int(value_left):
          result = ir_bin_ops[ir.type](rand_val_1, value_right)
        else:
          result = ir_bin_ops[ir.type](value_left, rand_val_1)
      else:
        result = ir_bin_ops[ir.type](value_left, value_right)

    sym_ref = self.get_sym_ref(lvalue, env)
    result = simplify(result)
    env.add(
      name=l_name,
      soltype=lvalue.type,
      value=lvalue,
      symbolic_value=result,
      sym_ref=sym_ref,
    )
    return result
    self.handle_default(ir=ir, env=env)

  def handle_Transfer(self, ir: Transfer, env: Env, *args, **kwargs):
    # TODO: Do I need to handle Transfer, really? Needs figure out.
    return
    self.handle_default(ir=ir, env=env)

  def handle_Return(self, ir: Return, env: Env, *args, **kwargs):
    # assert len(ir.values) <= 1, "TODO: Extend to multiple return values"
    if len(ir.values) == 0:
      return
    # ret_val: Variable = ir.values[0]
    # assert len(ir.node.function.returns) == len(ir.values), "WUT?"
    if len(ir.node.function.returns) == len(ir.values):
      for cnt, (ret_dec, ret_val) in enumerate(
        zip(ir.node.function.returns, ir.values)
      ):
        assert isinstance(ret_val, RVALUE), "TODO: Extend to other class"
        ret_symbol = self.variable_handler.handle_(variable=ret_val, env=env)
        env.add(
          name=get_return_name(ret_dec, cnt),
          soltype=ret_dec.type,
          value=ret_dec,
          symbolic_value=ret_symbol,
        )
      return ret_val  # ? this line is written arbitarily, the return value should never have been used so probably fine
    else:
      # * Should wipe ass for slither and match the return type. for example if return type is uint[4] but 4 values are returned instead, I should make an array and return it.
      match len(ir.node.function.returns):
        case 0:
          return
        case 1:
          match ir.node.function.return_type[0]:
            case ArrayType() as a:
              assert eval(a.length_value.value) == len(ir.values), (
                "TODO: Handle other occasion"
              )
              env.add(
                name=get_return_name(ir.node.function.returns[0], 0)[1:],
                value=ir.node.function.returns[0],
                soltype=ir.node.function.returns[0].type,
              )
              return_symbol = env.get(
                name=get_return_name(ir.node.function.returns[0], 0)[1:]
              )
              return_expr = return_symbol._symbolic_value
              for cnt, value in enumerate(ir.values):
                assert isinstance(value, RVALUE), "TODO: Extend to other class"
                ret_symbol = self.variable_handler.handle_(variable=value, env=env)
                return_expr = Store(return_expr, cnt, ret_symbol)
              env.add(
                name=get_return_name(ir.node.function.returns[0], 0),
                soltype=return_symbol._type,
                value=return_symbol._value,
                symbolic_value=return_expr,
              )
              return
        case _:
          match len(ir.values):
            case 1:
              # value = ir.values[0]
              # target_name = get_variable_name(value.name)
              # assert isinstance(value, TupleVariable), "Handle otherwise"
              # return_type = select_z3sort(
              #     _type=(target_name, *ir.node.function.return_type))
              return
            case _:
              return_exprs = list(
                map(
                  lambda x: self.variable_handler.handle_(variable=x, env=env),
                  ir.values,
                )
              )
              return_types = ir.node.function.return_type
              return_variables = ir.node.function.returns
              return_names = list(
                map(lambda x: get_return_name(x[1], x[0]), enumerate(return_variables))
              )
              ret_val_cnt = 0
              # iterate through return_types to consume all return_values, simple pattern matching
              for cnt, t in enumerate(return_types):
                env.add(name=return_names[cnt], value=return_variables[cnt], soltype=t)
                return_expr = env.get(return_names[cnt])._symbolic_value
                if isinstance(t, ArrayType):
                  length = t.length_value
                  if length is None:
                    raise NotImplementedError(
                      return_variables,
                      ir.values,
                      "Cannot Handle array of arbitary length",
                    )
                  length = int(length.value)
                  for i in range(length):
                    return_expr = Store(return_expr, i, return_exprs[ret_val_cnt + i])
                  ret_val_cnt += length
                  env.add(
                    name=return_names[cnt],
                    value=return_variables[cnt],
                    soltype=t,
                    symbolic_value=return_expr,
                  )
                else:
                  env.add(
                    name=return_names[cnt],
                    soltype=t,
                    value=return_variables[cnt],
                    symbolic_value=return_exprs[ret_val_cnt],
                  )
                  ret_val_cnt += 1
              if ret_val_cnt != len(ir.values):
                raise NotImplementedError(
                  return_variables, ir.values, "Not the case intended to handle"
                )
              # return_symbol = env.get(name=name0)
              # return_expr0 = return_symbol._symbolic_value
              # for i in range(16):
              #   return_expr0 = Store(return_expr0, i, return_exprs[i])
              # env.add(name=name, soltype=return_symbol._type,
              #         value=return_symbol._value, symbolic_value=return_expr0)

              # env.add(name=get_return_name(
              #     ir.node.function.retruns[1], 1), soltype=return_type2, value=ir.node.function.returns[1], symbolic_value=return_exprs[-1])
              return
              raise NotImplementedError(ir.node.function.returns, ir.values)
    self.handle_default(ir=ir, env=env)

  def handle_SolidityCall(self, ir: SolidityCall, env: Env, *args, **kwargs):
    func: SolidityFunction = ir.function
    # assert func.name in solidity_call_list, (func.name, func.return_type, func)

    match func.name:
      case a if a in require_list:
        cond: Variable = self.variable_handler.handle_(
          variable=ir.arguments[0], env=env
        )
        env.add_pc(cond)
        # env.add(
        #   name="@pc",
        #   soltype=env.get("@pc")._type,
        #   symbolic_value=simplify(a=And(env.get("@pc")._symbolic_value, cond)),
        # )
        return
      case _:
        # TODO: handle multiple return types
        assert len(func.return_type) <= 1, "TODO: handle multiple return types"
        if len(func.return_type) == 1:
          rtype = func.return_type[0]
          lvalue = ir.lvalue
          l_name = get_variable_name(lvalue)
          env.add(name=l_name, soltype=rtype, value=lvalue)
          return
        else:
          lvalue = ir.lvalue
          if lvalue and lvalue.type:
            l_name = get_variable_name(lvalue)
            env.add(name=l_name, soltype=lvalue.type, value=lvalue)
          return
        raise NotImplementedError(func.name)
    self.handle_default(ir=ir, env=env)

  @staticmethod
  def do_fake_function_call(return_type: List[Type], returns: List[Type], env: Env):
    merged_env = deepcopy(env)
    return_name_list = []
    if return_type:
      assert len(returns) == 0 or len(return_type) == len(returns), "Handle else"
      return_name_list = list(
        map(
          lambda x: (get_return_name(variable=x[1], cnt=x[0]), x[1]),
          enumerate(returns or [None] * len(return_type)),
        )
      )
    for ret in return_name_list:
      assert ret[1], "Return type should not be None"
      # * Need default for Solidity's implicit return mechanism
      merged_env.add(name=ret[0], soltype=ret[1].type, value=ret[1], need_default=True)
    return merged_env

  def do_function_call(
    function: FunctionContract,
    function_from: FunctionContract,
    env: Env,
    arglist: List[Any],
    config: ConfigProvider,
    done_ctx_constant,
    done_ctx_slither_construct,
    done_ctx_constructor,
    from_engine: FunctionEngine,
    *args,
    **kwargs,
  ):
    assert function is not None, "TODO: handle Tuple[str, str] case"
    if function in from_engine.done_pure:
      env.add_pc(from_engine.done_pure[function].pc)
      return from_engine.done_pure[function].env
    # assert len(function.returns) <= 1, "TODO: handle multiple return"
    if function.entry_point is None:
      return IRHandler.do_fake_function_call(
        return_type=function.return_type, returns=function.returns, env=env
      )
    call_from = function_from
    call_origin = from_engine.call_origin or function

    """
    Python 3.11.10 (default, Feb  2 2022, 07:45:15) is what i currently on when writhing following code and this comment.
    
    This version of Python seems to think all IRDebugger() constructed by the default argument is the same, causing self.from_engine got overwritten when constructing new instance of FunctionEngine. 
    
    Explicitly construct IRDebugger to bypass this issue.
    """
    ih = symbolic_debug.IRDebugger(config=config)
    nh = symbolic_debug.NodeDebugger(
      _config=config,
      ctx_slither_construct=done_ctx_slither_construct,
      ctx_constructor=done_ctx_constructor,
      ctx_constant=done_ctx_constant,
      ir_handler=ih,
    )
    func_engine = function_engine.FunctionEngine(
      function=function,
      node_handler=nh,
      config=config,
      call_from=call_from,
      call_origin=call_origin,
      from_modifier=kwargs.get("from_modifier", False),
      done_pure=from_engine.done_pure,
    )
    func_engine.call_cnt = deepcopy(from_engine.call_cnt)
    func_engine.call_cnt[function.canonical_name] = (
      func_engine.call_cnt.get(function.canonical_name, 0) + 1
    )
    from_engine.call_cnt[function.canonical_name] = (
      from_engine.call_cnt.get(function.canonical_name, 0) + 1
    )
    if function == call_origin:
      log(
        f"Recursion detected on {function.canonical_name} for {func_engine.call_cnt.get(function.canonical_name, 0)} times"
      )

    if func_engine.call_cnt[function.canonical_name] > SOLIDITY_MAX_RECURSION_LIMIT:
      return IRHandler.do_fake_function_call(
        return_type=function.return_type, returns=function.returns, env=env
      )

    function.called_from = function_from
    func_engine.env = env

    func_engine.set_arguments(arguments=arglist)

    log.config.global_tab += 1
    done_list = func_engine.exec()
    log.config.global_tab -= 1
    func_engine.call_cnt[function.canonical_name] -= 1
    if done_list:
      try:
        merged_env = compute_merged_env(done_env=done_list)
        return merged_env
      except SymbolNotFoundError:
        # ? Should never reach here
        assert False, "SymbolNotFoundError"
        breakpoint()
    else:
      assert False

  @staticmethod
  def resolve_return_name_list(
    return_type: List[Type],
    returns: List[Variable],
  ):
    return_name_list = []
    if return_type:
      assert len(returns) == 0 or len(return_type) == len(returns), "Handle else"
      return_name_list = list(
        map(
          lambda x: (get_return_name(variable=x[1], cnt=x[0]), x[1]),
          enumerate(returns or [None] * len(return_type)),
        )
      )
    return return_name_list

  @staticmethod
  def do_post_function_call(
    return_type: List[Type],
    returns: List[Variable],
    merged_env: Env,
    env: Env,
    lval: Variable,
    param_list: List = [],
    pure: bool = False,
  ):
    return_name_list = IRHandler.resolve_return_name_list(
      return_type=return_type,
      returns=returns,
    )
    if not return_name_list and not lval:
      # * if return name does not exists, that means
      # * 1. functon actually does not return anything, OR
      # * 2. slither has no idea what this function is doing
      # * The second occasion is marked by the fact that lval is still present.
      # * So still need to add a dummy variable for lval even if return_name does not exist.
      return

    # if pure function, substitute merged_env
    if pure:
      for k, v in merged_env.binding.items():
        merged_env.binding[k]._symbolic_value = substitute(
          v._symbolic_value,
          list(map(lambda x: (Const(f"@{x[0]}", x[1].sort()), x[1]), param_list)),
        )

    if len(return_name_list) == 1:
      return_val = merged_env.get(name=return_name_list[0][0])
      target_name = get_variable_name(variable=lval)
      env.add(
        name=target_name,
        soltype=lval.type,
        value=lval,
        symbolic_value=return_val._symbolic_value,
        need_default=True,
      )
    else:
      target_name = get_variable_name(variable=lval)
      variable_sort = select_z3sort(_type=(target_name, *lval.type))
      construct_params = []
      for cnt, return_name in enumerate(return_name_list):
        return_val = merged_env.get(name=return_name[0])
        symbolic_value = return_val._symbolic_value
        if isinstance(lval.type[cnt], UserDefinedType) and isinstance(
          lval.type[cnt].type, Enum
        ):
          e, item_list = select_z3sort(lval.type[cnt])
          if not is_arith(symbolic_value):
            # can convert to enum directly
            symbolic_value = item_list[symbolic_value.as_long()]
          else:
            # make a ite expression to convert to enum
            base = item_list[0]
            for i in range(1, len(item_list)):
              base = If(symbolic_value == IntVal(i), item_list[i], base)
            # symbolic_value = Const(return_name[0], get_real_sort(select_z3sort(lval.type[cnt])))
            symbolic_value = base
        construct_params.append(symbolic_value)
        env.add(
          name=return_val._name,
          soltype=return_val._type,
          value=return_val._value,
          symbolic_value=return_val._symbolic_value,
          need_default=True,
        )
      variable = variable_sort.cons(*construct_params)
      env.add(
        name=target_name,
        soltype=lval.type,
        value=lval,
        symbolic_value=variable,
        need_default=True,
      )

  def handle_InternalCall(self, ir: InternalCall, env: Env, *args, **kwargs):
    if ir.is_modifier_call and self.config.use_proper_modifier:
      return
    arglist = list(
      map(lambda x: self.variable_handler.handle_(variable=x, env=env), ir.arguments)
    )
    function = ir.function
    merged_env = IRHandler.do_function_call(
      function=function,
      function_from=ir.node.function,
      env=env,
      arglist=arglist,
      config=self.config,
      done_ctx_constant=self.done_ctx_constant,
      done_ctx_constructor=self.done_ctx_constructor,
      done_ctx_slither_construct=self.done_ctx_slither_construct,
      from_engine=self.from_engine,
      *args,
      **kwargs,
    )
    if ir.is_modifier_call:
      new_pc = simplify(merged_env.get("@pc")._symbolic_value)
      env.add(
        name="@pc",
        soltype=env.get("@pc")._type,
        symbolic_value=simplify(And(new_pc, env.get("@pc")._symbolic_value)),
      )

    self.do_post_function_call(
      returns=function.returns,
      return_type=function.return_type,
      merged_env=merged_env,
      env=env,
      lval=ir.lvalue,
      param_list=zip(map(lambda x: get_variable_name(x), ir.arguments), arglist),
      pure=function.pure,
    )
    return
    self.handle_default(ir=ir, env=env)

  def handle_HighLevelCall(self, ir: HighLevelCall, env: Env, *args, **kwargs):
    function = ir.function
    lval = ir.lvalue
    match function:
      case FunctionContract() | Function():
        # assert len(function.returns) <= 1, "TODO: handle multiple return"
        arglist = list(
          map(
            lambda x: self.variable_handler.handle_(variable=x, env=env), ir.arguments
          )
        )
        merged_env = IRHandler.do_function_call(
          function=function,
          function_from=ir.node.function,
          env=env,
          arglist=arglist,
          config=self.config,
          done_ctx_constant=self.done_ctx_constant,
          done_ctx_constructor=self.done_ctx_constructor,
          done_ctx_slither_construct=self.done_ctx_slither_construct,
          from_engine=self.from_engine,
          *args,
          **kwargs,
        )
        self.do_post_function_call(
          return_type=function.return_type,
          returns=function.returns,
          merged_env=merged_env,
          env=env,
          lval=ir.lvalue,
          param_list=zip(map(lambda x: get_variable_name(x), ir.arguments), arglist),
          pure=function.pure,
        )
        return
      case StateVariable():
        #! TODO: try to get state variable value (of other contract), if any
        env.add(name=get_variable_name(lval), soltype=lval.type, value=lval)
        return
        # return self.variable_handler.handle_(variable=function, env=env)
        # assert False, "TODO: Implement this"
      case _:
        raise NotImplementedError(function)
    self.handle_default(ir=ir, env=env)

  def handle_Condition(self, ir: Condition, env: Env, *args, **kwargs):
    value = ir.value
    if isinstance(value, Constant):
      return BoolVal(value.value)
    return env.get(name=get_variable_name(value))._symbolic_value
    self.handle_default(ir=ir, env=env)

  def handle_Unary(self, ir: Unary, env: Env, *args, **kwargs):
    target = ir.lvalue
    assert target is not None, "Needs to be FIXed"
    operand = ir.rvalue

    l_name = get_variable_name(target)

    value = self.variable_handler.handle_(variable=operand, env=env)

    match ir.type:
      case UnaryType.BANG:
        if not is_bool(value):
          target_value = value._symbolic_value != 0
        target_value = simplify(Not(value))
      case UnaryType.TILD:
        target_value = BV2Int(~Int2BV(value, 256), 256)
      case _:
        assert False, "Impossible Unary Type"

    env.add(name=l_name, soltype=target.type, value=target, symbolic_value=target_value)
    return target_value
    self.handle_default(ir=ir, env=env)

  def handle_Index(self, ir: Index, env: Env, *args, **kwargs):
    variable_left = ir.variable_left
    variable_right = ir.variable_right
    result = ir.lvalue
    assert result is not None, "handle None occasion!"
    l_name = get_variable_name(variable=result)
    sym_left = self.variable_handler.handle_(variable=variable_left, env=env)
    sym_right = self.variable_handler.handle_(variable=variable_right, env=env)
    # handle bytes access
    if (
      isinstance(variable_left.type, ElementaryType)
      and variable_left.type.name in elementary_type.Byte
    ):
      sz = 256
      #   try:
      #     sz = variable_left.type.size
      #   except:
      #     sz = 32 * 8
      if is_string(sym_left):
        result_value = sym_left[sym_right]
      else:
        result_value = simplify(
          simplify(
            BV2Int(
              (Int2BV(sym_left, sz) >> simplify((Int2BV(sym_right, 256) << 3))) & 0xFF,
              sz,
            )
          )
        )
    elif (
      isinstance(variable_right.type, ElementaryType)
      and variable_right.type.name == "string"
      and isinstance(variable_left.type, MappingType)
      and not (
        isinstance(variable_left.type.type_from, ElementaryType)
        and variable_left.type.type_from.name == "string"
      )
    ):
      # TODOL: change this implementation of convert to string using hash, i think it will fail eventually
      sym_right = IntVal(hash(sym_right.as_string()))
      result_value = sym_left[sym_right]
    elif (
      isinstance(variable_left.type, MappingType)
      and isinstance(variable_left.type.type_from, ElementaryType)
      and variable_left.type.type_from.name == "address"
      and isinstance(variable_right.type, UserDefinedType)
      and isinstance(variable_right.type.type, Contract)
    ):
      sym_right = IntVal(hash(variable_right))
      result_value = sym_left[sym_right]
    elif (
      isinstance(variable_left.type, (ArrayType, MappingType))
      and is_int(sym_right)
      and isinstance(variable_right.type, UserDefinedType)
      and isinstance(variable_right.type.type, Enum)
    ):
      # convert sym_right into enum
      enum_type = variable_right.type.type
      _, enum_item_list = select_z3sort(enum_type)
      if not is_arith(sym_right):
        # can convert to enum directly
        sym_right = enum_item_list[sym_right.as_long()]
      else:
        # make a ite expression to convert to enum
        base = enum_item_list[0]
        for i in range(1, len(enum_item_list)):
          base = If(sym_right == IntVal(i), enum_item_list[i], base)
        # symbolic_value = Const(return_name[0], get_real_sort(select_z3sort(lval.type[cnt])))
        sym_right = base
      result_value = sym_left[sym_right]
    else:
      sym_right_addr = IntVal(hash(variable_right))
      try:
        result_value = sym_left[sym_right]
      except Exception:
        result_value = sym_left[sym_right_addr]
    # result.sym_right = sym_right
    # result.sym_left = sym_left
    env.add(
      name=l_name,
      soltype=result.type,
      value=result,
      symbolic_value=result_value,
      sym_ref=result_value,
    )
    return result_value
    self.handle_default(ir=ir, env=env)

  def handle_TypeConversion(self, ir: TypeConversion, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    variable = ir.variable
    l_name = get_variable_name(lvalue)
    rtype = ir.type
    # ! TODO: May need to change this naive implementation!!
    symbolic_value = self.variable_handler.handle_(variable=ir.variable, env=env)

    # log(variable.type)
    # log(variable.type.__str__())
    # log(rtype.__str__())

    if (
      isinstance(variable.type, UserDefinedType)
      and isinstance(variable.type.type, Contract)
      and isinstance(rtype, ElementaryType)
      and rtype.name == "address"
    ):
      # ! Temporary patch for address cast
      symbolic_value_address = None
      try:
        symbol = env.get(name=l_name)
        address = symbol._address
        if address is not None:
          symbolic_value_address = IntVal(address)
      except Exception:
        pass
      if symbolic_value_address is None:
        symbolic_value = Int(f"@randint_{str(abs(hash(symbolic_value)))}")
      else:
        symbolic_value = symbolic_value_address
      log(symbolic_value)
    elif (
      isinstance(variable.type, ElementaryType)
      and variable.type.name in (elementary_type.Uint + elementary_type.Int)
      and isinstance(rtype, ElementaryType)
      and rtype.name == "string"
    ):
      symbolic_value = IntVal(symbolic_value.as_long())
    elif (
      isinstance(variable.type, ElementaryType)
      and variable.type.name in elementary_type.Byte
      and isinstance(rtype, ElementaryType)
      and rtype.name == "string"
    ):
      symbolic_value = StringVal(str(hash(symbolic_value)))

    env.add(name=l_name, soltype=rtype, value=lvalue, symbolic_value=symbolic_value)
    return env.get(name=l_name)._symbolic_value
    self.handle_default(ir=ir, env=env)

  def handle_InitArray(self, ir: InitArray, env: Env, *args, **kwargs):
    init_values = ir.init_values
    lvalue = ir.lvalue
    ltype = lvalue.type
    l_name = get_variable_name(lvalue)
    rvalue = None
    sym_ref = None

    def same_array_type_loose(x, y):
      return isinstance(x, ArrayType) and isinstance(y, ArrayType) and x.type == y.type

    if len(init_values) == 1 and same_array_type_loose(ltype, init_values[0].type):
      # ? wipe ass for slither
      match init_values[0]:
        case TemporaryVariable() as t:
          rvalue = self.variable_handler.handle_(variable=t, env=env)
        case Constant() as c:
          rvalue = self.variable_handler.handle_(variable=c, env=env)
        case ReferenceVariable() as r:
          rvalue = self.variable_handler.handle_(variable=r, env=env)
        case _:
          assert False, f"Not Implemented for {init_values[0].__class__}"
    else:
      env.add(name=l_name, soltype=lvalue.type, value=lvalue)
      rvalue = env.get(name=l_name)._symbolic_value
      for i, value in enumerate(init_values):
        match value:
          case TemporaryVariable():
            rvalue = simplify(
              Store(rvalue, i, self.variable_handler.handle_(variable=value, env=env))
            )
          case Constant():
            rvalue = simplify(
              Store(rvalue, i, self.variable_handler.handle_(variable=value, env=env))
            )
          case LocalVariable():
            rvalue = simplify(
              Store(rvalue, i, self.variable_handler.handle_(variable=value, env=env))
            )
          case StateVariable() | ReferenceVariable():
            rvalue = simplify(
              Store(rvalue, i, self.variable_handler.handle_(variable=value, env=env))
            )
          case SolidityVariableComposed():
            rvalue = simplify(
              Store(rvalue, i, self.variable_handler.handle_(variable=value, env=env))
            )
          case list():
            array_expr = Array(f"@array_{randint(0, 1000000)}", IntSort(), IntSort())
            for i, v in enumerate(value):
              array_expr = Store(array_expr, i, v)
            rvalue = simplify(Store(rvalue, i, array_expr))
          case _:
            assert False, f"Not Implemented for {value.__class__}"

    env.add(
      name=l_name,
      soltype=lvalue.type,
      value=lvalue,
      symbolic_value=rvalue,
      sym_ref=sym_ref,
    )
    return env.get(name=l_name)._symbolic_value
    self.handle_default(ir=ir, env=env)

  def handle_EventCall(self, ir: EventCall, env: Env, *args, **kwargs):
    return
    self.handle_default(ir=ir, env=env)

  def handle_LowLevelCall(self, ir: LowLevelCall, env: Env, *args, **kwargs):
    result: TupleVariable | Variable = ir.lvalue
    # ? Maybe I should model TupleVariable as a dataclass, for, tuple can have different types on different positions, i am so screwed
    # TODO: I have no idea how low level calls are done, nor does slither know, so probably i just return random variable now. Maybe needs further implementation.
    if isinstance(result, TupleVariable):
      result_name = get_variable_name(variable=result)
      env.add(name=result_name, soltype=(result_name, *result.type), value=result)
      return
    else:
      # * You know why I need this branch when LowLevelCall says lvalue must be either TupleVariable or TupleSSAVariable and I do not use SSA?
      # * BECASE `assert isinstance(result, TupleVariable)` FAILED!!! AUTHOR OF SLITHER IS A CHEATER!!!
      result_name = get_variable_name(variable=result)
      env.add(name=result_name, soltype=result.type, value=result)
      return
    self.handle_default(ir=ir, env=env)

  def handle_Unpack(self, ir: Unpack, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(variable=lvalue)
    _tuple = ir.tuple
    _tuple_symbolic = env.get(name=get_variable_name(_tuple))._symbolic_value
    _tuple_sort = select_z3sort((get_variable_name(_tuple), *_tuple.type))
    _index = ir.index  # ! HOW COULD SLITHER JUST REUSE THIS INDEX FIELD???

    getter = getattr(_tuple_sort, f"index{_index}", None)
    assert getter is not None

    lvalue_expr = getter(_tuple_symbolic)

    env.add(name=l_name, soltype=lvalue.type, value=lvalue, symbolic_value=lvalue_expr)
    return
    self.handle_default(ir=ir, env=env)

  def handle_LibraryCall(self, ir: LibraryCall, env: Env, *args, **kwargs):
    if ir.destination.name == "Verification":
      match ir.function_name.value:
        case "Pause":
          return
        case "Assume":
          arg0name = get_variable_name(ir.arguments[0])
          env.add_pc(ref_to_actual_target(env.get(arg0name), env))
          # env.add(
          #   "@pc",
          #   soltype=env.get("@pc")._type,
          #   symbolic_value=simplify(
          #     And(
          #       env.get("@pc")._symbolic_value,
          #       ref_to_actual_target(env.get(arg0name), env),
          #     )
          #   ),
          # )
          return
        case _:
          raise NotImplementedError(ir.function_name)
    else:
      function = ir.function
      arglist = list(
        map(lambda x: self.variable_handler.handle_(variable=x, env=env), ir.arguments)
      )

      merged_env = IRHandler.do_function_call(
        function=function,
        function_from=ir.node.function,
        env=env,
        arglist=arglist,
        config=self.config,
        done_ctx_constant=self.done_ctx_constant,
        done_ctx_constructor=self.done_ctx_constructor,
        done_ctx_slither_construct=self.done_ctx_slither_construct,
        from_engine=self.from_engine,
        *args,
        **kwargs,
      )
      self.do_post_function_call(
        return_type=function.return_type,
        returns=function.returns,
        env=env,
        merged_env=merged_env,
        lval=ir.lvalue,
        param_list=zip(map(lambda x: get_variable_name(x), ir.arguments), arglist),
        pure=function.pure,
      )
      # return_name = ''
      # if function.return_type:
      #   # handle named return
      #   return_name = get_return_name(
      #       variable=function.return_values[0] if function.return_values else None, cnt=0)
      # lval = ir.lvalue

      # if not return_name and not lval:
      #   return  # no need to add variable for function that return nothing
      # try:
      #   return_val = merged_env.get(name=return_name)
      # except SymbolNotFoundError:
      #   return_val = merged_env.get(get_return_name(None, cnt=0))
      # target_name = get_variable_name(lval)
      # env.add(name=target_name, soltype=lval.type, value=lval,
      #         symbolic_value=return_val._symbolic_value)
      return
    self.handle_default(ir=ir, env=env)

  def handle_NewArray(self, ir: NewArray, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    assert lvalue is not None
    l_name = get_variable_name(lvalue)
    assert l_name is not None
    env.add(name=l_name, soltype=ir.array_type, value=lvalue)
    return
    # log(env.get(name=l_name))
    self.handle_default(ir=ir, env=env)

  def handle_Length(self, ir: Length, env: Env, *args, **kwargs):
    lvalue: ReferenceVariable = ir._lvalue
    assert lvalue is not None
    lname = get_variable_name(lvalue)
    arr: Union[StateVariable, LocalVariable] = ir.value
    match arr.type:
      case ArrayType():
        assert isinstance(arr.type, ArrayType), "Handle what?"
        length = arr.type.length_value
        length_eval = None
        if length:
          assert isinstance(length, Literal)
          match length.value:
            case int() | str():
              length_eval = IntVal(length.value)
            case _:
              assert False, "str cannot be length"
        env.add(
          name=lname, soltype=lvalue.type, value=lvalue, symbolic_value=length_eval
        )
        return
      case ElementaryType() as e:
        if e.name.startswith("byte"):
          if e.is_dynamic:
            env.add(name=lname, soltype=lvalue.type, value=lvalue)
          else:
            env.add(
              name=lname,
              soltype=lvalue.type,
              value=lvalue,
              symbolic_value=IntVal(e.size),
            )
          return
        else:
          pass
    self.handle_default(ir=ir, env=env)

  def handle_NewElementaryType(self, ir: NewElementaryType, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    env.add(name=l_name, soltype=lvalue.type, value=lvalue)
    return
    self.handle_default(ir=ir, env=env)

  def handle_NewStructure(self, ir: NewStructure, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    env.add(name=l_name, soltype=lvalue.type, value=lvalue)
    return
    self.handle_default(ir=ir, env=env)

  def handle_Member(self, ir: Member, env: Env, *args, **kwargs):
    vleft = ir.variable_left
    vright = ir.variable_right
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    match vleft:
      case (
        LocalVariable() | ReferenceVariable() | StateVariable() | TemporaryVariable()
      ):
        if isinstance(vleft.type, ElementaryType) and vleft.type.name == "address":
          match vright.value:
            case str() as s:
              match s:
                case "call":
                  # TODO: change dummy implementation
                  env.add(name=l_name, soltype=vleft.type, value=lvalue)
                  return
                case _:
                  raise NotImplementedError(s)
            case _:
              raise NotImplementedError(vright.value)
        elif vleft.type is None:
          return
        else:
          # * Use select_z3sort to get Sort from cache
          # * z3 constructs variables using SortRef, but drops all attributes for some reason
          # * so getting from sort of symbolic expr does not work.

          vleft_symbol = env.get(get_variable_name(vleft))
          vleft_symbol_expr = ref_to_actual_target(vleft_symbol, env)
          attribute = getattr(select_z3sort(vleft.type), vright.value, None)
          symbolic_value = None

          if attribute is None:
            # * possibly a function, needs special handling
            attribute = getattr(
              select_z3sort(vleft.type), f"@function_{vright.value}", None
            )
            if attribute is not None:
              symbolic_value = attribute(vleft_symbol_expr)
              if (t := env.functable.get(symbolic_value, None)) is not None:
                symbolic_value = t
            else:
              match vright.value:
                case str() as s:
                  match s:
                    case "balance":
                      pass
                    case "transfer":
                      raise NotImplementedError("Implement Me")
                    case _:  # ! This is a function call
                      pass
                      # possibly directly access function declared in Contract
                      assert isinstance(vleft.type.type, Contract)
                      symbolic_value = list(
                        filter(
                          lambda x: x.name == vright.value, vleft.type.type.functions
                        )
                      )
                      assert len(symbolic_value) == 1
                      symbolic_value = symbolic_value[0]
                case _:
                  raise NotImplementedError(vright.value)
            env.add(
              name=l_name,
              soltype=lvalue.type or vright.type,
              value=lvalue or vright,
              symbolic_value=symbolic_value,
            )
            return
          assert attribute is not None, "Should Be Impossible"
          member_access = attribute(vleft_symbol_expr)
          env.add(
            name=l_name,
            soltype=lvalue.type,
            value=lvalue,
            symbolic_value=member_access,
            sym_ref=member_access,
          )
          return
      case EnumContract() | Enum():
        enum_type, item_list = select_z3sort(
          vleft.contract.get_enum_from_name(vleft.name)
        )
        # Convert Enum Item into IntVal, assign to attribute
        attribute = IntVal(
          list(filter(lambda x: str(x[1]) == vright.value, enumerate(item_list)))[0][0]
        )
        assert attribute is not None, "Should Be Impossible"
        # enum_access = attribute(vleft_symbol_expr)
        env.add(
          name=l_name,
          soltype=lvalue.type,
          value=lvalue,
          symbolic_value=attribute,
          sym_ref=attribute,
        )
        return
      case Contract():
        """
        I have no idea how to handle this, so just add the variable to the environment
        """
        env.add(name=l_name, soltype=lvalue.type, value=lvalue)
        return
      case SolidityVariableComposed():
        """
        I have no idea how to handle this, so just add the variable to the environment
        """
        env.add(name=l_name, soltype=vleft.type, value=lvalue)
        return
      case _:
        raise NotImplementedError(type(vleft))
    self.handle_default(ir=ir, env=env)

  def handle_CodeSize(self, ir: CodeSize, env: Env, *args, **kwargs):
    """
    Copy pasted from solidity source code as explaination:

    extcodesize checks the size of the code stored in an address, and
    address returns the current address. Since the code is still not
    deployed when running a constructor, any checks on its code size will
    yield zero, making it an effective way to detect if a contract is
    under construction or not.
    """

    # Step1: statically check if the call is from a constructor, if true, means size check should return zero, if false, return something non-zero
    called_from: FunctionContract = ir.node.function
    should_return_zero: bool = called_from.is_constructor
    while (not should_return_zero) and (
      getattr(called_from, "called_from", None) is not None
    ):
      called_from = called_from.called_from
      should_return_zero: bool = called_from.is_constructor

    # Step2: prepare variables and do the assign. If not should_return_zero, make a random number to return, since I have no idea how to calculate code size
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)

    if should_return_zero and ir.value.name == "self":
      env.add(name=l_name, soltype=lvalue.type, value=lvalue, symbolic_value=IntVal(0))
      return
    else:
      import random

      env.add(
        name=l_name,
        soltype=lvalue.type,
        value=lvalue,
        symbolic_value=IntVal(random.randint(1, 114514)),
      )
      return
    self.handle_default(ir=ir, env=env)

  def handle_Send(self, ir: Send, env: Env, *args, **kwargs):
    # TODO: Do I really need to handle Send operation？ Needs to figure out maybe.
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    env.add(
      name=l_name, soltype=lvalue.type, value=lvalue, symbolic_value=None, address=None
    )
    return
    self.handle_default(ir=ir, env=env)

  def handle_Delete(self, ir: Delete, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    env.add(name=l_name, soltype=lvalue.type, value=lvalue, need_default=True)
    return
    self.handle_default(ir=ir, env=env)

  def handle_NewContract(self, ir: NewContract, env: Env, *args, **kwargs):
    lvalue = ir.lvalue
    l_name = get_variable_name(lvalue)
    address = IntVal(randint(0, 2**256))
    env.add(name=l_name, soltype=ir.contract_name, value=lvalue, address=address)
    return
    self.handle_default(ir=ir, env=env)

  def handle_InternalDynamicCall(
    self, ir: InternalDynamicCall, env: Env, *args, **kwargs
  ):
    func = env.ref_to_actual_target(get_variable_name(ir.function))
    func_type = ir.function_type
    arglist = list(
      map(lambda x: self.variable_handler.handle_(variable=x, env=env), ir.arguments)
    )
    return_type = func_type.return_type
    returns = func_type.return_values
    if isinstance(func, Function):
      return_type = func.return_type
      returns = func.returns
    if isinstance(func, Function):
      merged_env = IRHandler.do_function_call(
        function=func,
        function_from=ir.node.function,
        env=env,
        arglist=arglist,
        config=self.config,
        done_ctx_constant=self.done_ctx_constant,
        done_ctx_constructor=self.done_ctx_constructor,
        done_ctx_slither_construct=self.done_ctx_slither_construct,
        from_engine=self.from_engine,
        *args,
        **kwargs,
      )
    else:
      merged_env = self.do_fake_function_call(
        return_type=return_type, returns=returns, env=env
      )
    self.do_post_function_call(
      return_type=return_type,
      returns=returns,
      merged_env=merged_env,
      env=env,
      lval=ir.lvalue,
      param_list=zip(map(lambda x: get_variable_name(x), ir.arguments), arglist),
      pure=False,
    )
    return
    self.handle_default(ir=ir, env=env)

  def handle_Nop(self, ir: Nop, env: Env, *args, **kwargs):
    return
    self.handle_default(ir=ir, env=env)
