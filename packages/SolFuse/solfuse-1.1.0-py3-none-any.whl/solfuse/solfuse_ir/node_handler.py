import multiprocessing as mp
import queue
import random
from slither.core.cfg.node import Node, NodeType
from slither.core.declarations import FunctionContract
from slither.core.solidity_types import ElementaryType, elementary_type, ArrayType
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

from slither.core.variables import StateVariable, LocalVariable

from slither.slithir.operations import Operation, Assignment, Binary, BinaryType
from slither.slithir.variables import Constant, ReferenceVariable, StateIRVariable
from slither.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue, LVALUE, RVALUE
from typing import Callable, Optional, Tuple, List

from z3 import (
  IntVal,
  BoolVal,
  StringVal,
  BoolRef,
  Not,
  Solver,
  simplify,
  And,
  sat,
  unsat,
  is_true,
  is_false,
)

from solfuse.solfuse_ir.function_engine import FunctionEngine
from solfuse.solfuse_ir.symbol import Symbol

from .handler import Handler, ForkSelector
from .env import Env, SymbolNotFoundError
from .logger import log
from .utils import get_return_name, get_variable_default_value, get_variable_name
from .ir_handler import IRHandler
from .variable_handler import VariableHandler
from .context import Context
from solfuse.solfuse_ir import variable_handler


class NodeHandler(Handler):
  def __init__(
    self,
    config,
    ctx_slither_construct: Context | None = None,
    ctx_constant: Context | None = None,
    ir_handler: Handler = IRHandler(),
    ctx_constructor: Context | None = None,
    _from: Optional[FunctionEngine] = None,
  ) -> None:
    super().__init__(
      name_dispatch_func=lambda node: node.type.__str__().split(".")[1],
      name_dispatch_keyword="node",
      _from=_from,
    )
    self.config = config
    self.ir_handler = ir_handler
    self.from_engine = _from
    self.ir_handler.from_engine = _from
    self.ctx_slither_construct: Context | None = ctx_slither_construct
    self.ctx_constant: Context | None = ctx_constant
    self.ctx_constructor: Context | None = ctx_constructor
    self.ir_handler.done_ctx_slither_construct = ctx_slither_construct
    self.ir_handler.done_ctx_constant = ctx_constant
    self.ir_handler.done_ctx_constructor = ctx_constructor
    self.pending_calls: List[FunctionContract] = []
    self.pending_arguments: List[List] = []
    # ? current just hard coded, may be changed to configurable later
    self.max_loop_times = 1
    ...  # TODO should add other members

  @property
  def from_engine(self):
    return self._from

  @from_engine.setter
  def from_engine(self, _from: Optional[FunctionEngine]):
    self._from = _from
    self.ir_handler.from_engine = _from

  def handle_OTHER_ENTRYPOINT(
    self, node: Node, env: Env, arguments: List | None = None, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return self.handle_ENTRYPOINT(
      node=node, env=env, arguments=arguments, *args, **kwargs
    )
    # return (node.sons, ForkSelector.No, env)

  def handle_ENTRYPOINT(
    self,
    node: Node,
    env: Env,
    arguments: List | None = None,
    origin_call=True,
    pending_calls: List[FunctionContract] = [],
    pending_arguments: List[List] = [],
    *args,
    **kwargs,
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    self.pending_calls = pending_calls
    self.pending_arguments = pending_arguments
    """Prepare all state variables, function params for the function. Do this by predefining symbols in the Env.

    Args:
        node (Node): should be Entry Point of a function
        env (Env): should be only containing pc

    Returns:
        Tuple[List[Node], ForkSelector, Env]: nodes to execute next, wether to fork, and modified env.
    """
    func: FunctionContract = node.function

    # Step 0: attempting compute initialized state variables through executing slitherConstructorVariables and slitherConstructorConstantVariables

    # Step 1: make symbol for state variables
    for state in func.contract.state_variables_ordered:
      # TODO currently only assign default value
      # TODO should changed to evaluate expression or default value after other parts finished
      try:
        env.get(get_variable_name(state))
      except SymbolNotFoundError:
        name: str | None = get_variable_name(variable=state)
        symbolic_value = None
        try:
          if state.is_declared_by(func.contract):
            if (
              state.initialized and state.is_constant and self.ctx_constant is not None
            ):
              symbolic_value: Symbol = self.ctx_constant.env.get(
                name=name
              )._symbolic_value
            elif state.initialized and self.ctx_slither_construct is not None:
              symbolic_value: Symbol = self.ctx_slither_construct.env.get(
                name=name
              )._symbolic_value
          if self.ctx_constructor is not None:
            # pass
            symbolic_value: Symbol = self.ctx_constructor.env.get(
              name=name
            )._symbolic_value
        except SymbolNotFoundError:
          pass

        # * Adding constraints for constant state variables, to make them always appear in pre condition.
        # * Not doing so will make predefined state variables lose their value in final state machine construction, when called inside another function call, thus cause precision loss
        # *
        # * The reason why such occasion will make predefined state variable disappear is because those added value appear inside post condition,
        # * but when solving two function's connection, I use pre condition of func1 (pre2),  post condition of func1(post), and pre condition of func2 (pre),
        # * substituting the variables appearing in pre with variables defined in post, without doing so to pre2, and check if pre and pre2 can be satisfied.
        # * The reason I do not substitute pre2 is that pre2 often gets violated by post, by not substituting I can reduce such case happening and preserve as much precison as possible.
        # *
        # * This method should be reasonable, but when pre should contradict with pre2 because they disagree on a predefined state variable, the actual value of state variable will be missing in pre2, causing an unsat turning into a sat.
        # *
        # * To make code shorter, I first add a None symbolic expr, creating a dummy variable to use in the equation, then add the true (if present) symbolic expr back in.
        # if self.ctx_constant is not None:
        # log(self.ctx_constant.env)
        # input()

        env.add(name=name, soltype=state.type, value=state)
        if symbolic_value is not None and state.is_constant:
          env.add(
            name="@pc",
            soltype=env.get("@pc")._type,
            symbolic_value=simplify(
              And(
                env.get("@pc")._symbolic_value,
                env.get(name=name)._symbolic_value == symbolic_value,
              )
            ),
          )
        env.add(
          name=name, soltype=state.type, value=state, symbolic_value=symbolic_value
        )

    # Step 2: make symbol for parameters, include symbolic expresion if have any arguments
    pend_args = self.pending_arguments[0]
    need_fill_argument = False
    if arguments is not None and len(arguments) == len(func.parameters):
      # assert len(arguments) == len(func.parameters), (
      #   f"Expected {len(func.parameters)}, got {len(arguments)}"
      # )
      need_fill_argument = True
    if not need_fill_argument and pend_args is not None and len(pend_args) > 0:
      pend_args_symbolic = list(
        map(
          lambda x: self.ir_handler.variable_handler.handle_(variable=x, env=env),
          pend_args,
        )
      )
      arguments = pend_args_symbolic
      need_fill_argument = True
    log(f"Pending arguments: {pend_args}")
    log(f"Arguments: {arguments}")
    for param, arg in zip(
      func.parameters,
      arguments
      if (arguments is not None and len(arguments) == len(func.parameters))
      else func.parameters,
    ):
      name = get_variable_name(param)
      env.add(
        name=name,
        soltype=param.type,
        value=param,
        symbolic_value=arg if need_fill_argument else None,
      )

    # Step 3: make return variable (if any) for the function

    cnt = 0
    for ret in func.returns:
      name = get_return_name(ret, cnt)
      cnt += 1
      if ret.name:
        name = get_variable_name(variable=ret)
      env.add(name=name, soltype=ret.type, value=ret)
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_EXPRESSION(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    """I think EXPRESSION node is just a wrapper for expression, so just iter through its irs should be fine.

    Args:
        node (Node): Should be EXPRESSION node
        env (Env): environment

    Returns:
        Tuple[List[Node], ForkSelector, Env]
    """
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_RETURN(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_VARIABLE(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    # ? need to define variable for ir
    # write an `or` here because Slither fucking give me a None type variable
    env.add(
      name=get_variable_name(node.variable_declaration),
      soltype=node.variable_declaration.type or ElementaryType("uint256"),
      value=node.variable_declaration,
    )
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env, assign_local=True)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  @staticmethod
  def solve_IF(expr, is_true, queue: mp.Queue):
    solve = Solver()
    solve.add(expr)
    queue.put((is_true, solve.check()))

  def handle_IF(
    self,
    node: Node,
    env: Env,
    delegate_from_loop=False,
    loop_times=0,
    *args,
    **kwargs,
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    result = None
    for ir in node.irs:
      # * CONDITION IR is guarenteed to be the last ir visited, so result will be the actual condtion
      result = self.ir_handler.handle_(ir=ir, env=env)
    if len(node.irs) == 0:
      """
      Slither sometimes will not produce any ir for IF expression, for god knows what reason.
      Wipe ass for them.
      """
      result = BoolVal(True)
    elif not isinstance(result, BoolRef):
      result = BoolVal(random.choice([True, True]))
    cond = simplify(result)

    # if node.son_true.type == NodeType.THROW:
    #   selector = ForkSelector.Yes
    #   selector.payload = cond
    #   return ([node.son_true, node.son_false], selector, env)
    notcond = simplify(Not(cond))
    env.simplify()

    true_expr = simplify(And(Not(cond), env.get("@pc")._symbolic_value))
    false_expr = simplify(And(Not(notcond), env.get("@pc")._symbolic_value))

    processes: List[mp.Process] = []
    q = mp.Queue()
    for selector, expr in [(True, true_expr), (False, false_expr)]:
      p = mp.Process(target=self.solve_IF, args=(expr, selector, q))
      processes.append(p)

    for p in processes:
      p.start()

    true_res, false_res = sat, sat
    for _ in range(len(processes)):
      try:
        is_true, res = q.get(timeout=0.2)
      except queue.Empty:
        continue
      if is_true:
        true_res = res
      else:
        false_res = res

    for p in processes:
      if p.is_alive():
        p.terminate()

    # solver_true = Solver()
    # solver_false = Solver()
    # # ! TODO change to more precise version
    # solver_true.add(simplify(And(Not(cond), env.get('@pc')._symbolic_value)))
    # solver_false.add(
    #     simplify(And(Not(notcond), env.get('@pc')._symbolic_value)))
    # true_res = solver_true.check()
    # false_res = solver_false.check()
    log(f"loop? : {delegate_from_loop} {loop_times} {self.max_loop_times}")
    if (delegate_from_loop and loop_times > self.max_loop_times) or false_res == unsat:
      log(f"loop_times: {loop_times}")
      son_false = list(filter(lambda x: x.type is NodeType.ENDLOOP, node.sons))
      if len(son_false) == 0:
        son_false = [node.son_false]
      return (
        son_false,
        ForkSelector.No,
        env,
        self.pending_calls[:],
        self.pending_arguments[:],
      )
    elif true_res == unsat:
      return (
        [node.son_true],
        ForkSelector.No,
        env,
        self.pending_calls[:],
        self.pending_arguments[:],
      )
    # * add cond as payload for the scheduler to patch path conditions
    # if node.son_true.type == NodeType.THROW:
    #   selector = ForkSelector.Yes
    #   selector.payload = cond
    #   return (node.sons, selector, env)
    selector = ForkSelector.Yes
    selector.payload = cond
    return (node.sons, selector, env, self.pending_calls[:], self.pending_arguments[:])

  def handle_ENDIF(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_STARTLOOP(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_IFLOOP(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    if getattr(node, "loop_times", None) is None:
      node.loop_times = 0
    node.loop_times += 1
    return self.handle_IF(
      node=node, env=env, delegate_from_loop=True, loop_times=node.loop_times
    )

  def handle_ENDLOOP(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_PLACEHOLDER(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    if not self.config.use_proper_modifier:
      return (
        node.sons,
        ForkSelector.No,
        env,
        self.pending_calls[:],
        self.pending_arguments[:],
      )
    self.pending_calls.pop(0)
    self.pending_arguments.pop(0)
    function = self.pending_calls[0]
    function_argument = self.pending_arguments[0]
    arglist = function_argument
    if len(self.pending_arguments) > 1:
      arglist = list(
        map(
          lambda x: self.ir_handler.handler.variable_handler.handle_(
            variable=x, env=env
          ),
          function_argument,
        )
      )
    merged_env = self.ir_handler.do_function_call(
      function=function,
      function_from=node.function,
      arglist=arglist,
      env=env,
      config=self.config,
      done_ctx_constant=self.ir_handler.done_ctx_constant,
      done_ctx_constructor=self.ir_handler.done_ctx_constructor,
      done_ctx_slither_construct=self.ir_handler.done_ctx_slither_construct,
      from_modifier=True,
      *args,
      **kwargs,
    )

    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_ASSEMBLY(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_ENDASSEMBLY(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_CONTINUE(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_BREAK(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_THROW(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    # * occuring a throw means reverting, so add condition to pc
    if (cond := getattr(node, "to_throw_cond", None)) is not None:
      if all(
        map(
          lambda x: x.type in (NodeType.ENTRYPOINT, NodeType.OTHER_ENTRYPOINT),
          node.fathers,
        )
      ) or not is_true(cond):
        origin_pc = env.pc
        if is_true(cond):
          env.add(
            name="@pc",
            soltype=origin_pc._type,
            value=origin_pc._value,
            symbolic_value=simplify(Not(cond)),
          )
        else:
          env.add(
            name="@pc",
            soltype=origin_pc._type,
            value=origin_pc._value,
            symbolic_value=simplify(
              And(simplify(Not(cond)), origin_pc._symbolic_value)
            ),
          )
    assert not node.sons
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_TRY(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )

  def handle_CATCH(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env, list, list]:
    return (
      node.sons,
      ForkSelector.No,
      env,
      self.pending_calls[:],
      self.pending_arguments[:],
    )
