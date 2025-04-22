from __future__ import annotations
from typing import TYPE_CHECKING
from functools import reduce

from solfuse.solfuse_ir.pure_descriptor import PureDescriptor
from solfuse.solfuse_ir.context import Context
from solfuse.solfuse_ir.naive_node_handler import NaiveNodeHandler
from solfuse.solfuse_ir.utils import (
  compute_merged_env,
  make_datatype_contract_and_structure,
  select_z3sort,
)
from .logger import log
from slither.core.declarations import Contract, FunctionContract
from slither.core.solidity_types.type import Type
from slither import Slither
from .config import ConfigProvider
from .symbolic_debug import NodeDebugger
from .function_engine import FunctionEngine
from . import summary
import z3

# NodeDebugger = NaiveNodeHandler


class Engine:
  """
  `Engine` iters all functions and uses `FunctionEngine` to process them
  """

  def __init__(
    self, contract: Contract, slither: Slither, config: ConfigProvider
  ) -> None:
    self.contract: Contract = contract
    self.done_list = {}
    self.slither: Slither = slither
    self.config: ConfigProvider = config
    self.summary = summary.Summary(self.contract, self.config)
    self.done_pure: dict[FunctionContract, FunctionEngine] = {}
    self.functions = list(
      filter(
        lambda func: func.name not in self.config.constraints_func_names
        and func.contract_declarer == self.contract,
        self.contract.functions,
      )
    )

  def do_summary(self):
    for func in self.functions:
      self.summary.set_func_pre(
        func,
        reduce(
          z3.Or, map(lambda x: x.env.get("@pc")._symbolic_value, self.done_list[func])
        ),
      )
      self.summary.set_func_post(func, self.done_list[func])

  def do_pure(
    self,
    done_ctx_slither_construct: Context | None,
    done_ctx_constant_construct: Context | None,
    done_ctx_constructor: Context | None,
  ) -> None:
    itering = filter(lambda x: x.pure, self.functions)
    if not self.config.debug:
      from rich.progress import track

      itering = track(itering, description="Executing Pure Functions...")
    for func in itering:
      if func in self.done_pure:
        continue
      func_engine = FunctionEngine(
        function=func,
        node_handler=NodeDebugger(
          _config=self.config,
          ctx_slither_construct=done_ctx_slither_construct,
          ctx_constant=done_ctx_constant_construct,
          ctx_constructor=done_ctx_constructor,
        ),
        config=self.config,
      )
      done_list = func_engine.exec()
      self.done_list[func] = done_list
      merged_env = compute_merged_env(done_list)
      self.done_pure[func] = PureDescriptor(
        name=func.name,
        func=func,
        engine=func_engine,
        params=func_engine.function.parameters,
        env=merged_env,
        pc=merged_env.pc._symbolic_value,
      )

  def exec(self) -> None:
    # First execute slitherConstructorVariables and slitherConstructorConstantVariables
    slither_constructor_variables = self.contract.get_function_from_full_name(
      "slitherConstructorVariables()"
    )
    slither_constructor_constant_variables = self.contract.get_function_from_full_name(
      "slitherConstructorConstantVariables()"
    )
    contract_constructor = self.contract.constructor
    done_ctx_slither_construct = None
    done_ctx_constant_construct = None
    done_ctx_constructor = None

    if slither_constructor_constant_variables is not None:
      func_engine1 = FunctionEngine(
        function=slither_constructor_constant_variables,
        node_handler=NodeDebugger(_config=self.config),
        config=self.config,
      )
      self.done_list[slither_constructor_constant_variables] = func_engine1.exec()
      done_ctx_constant_construct = func_engine1.done_list[0]

    if slither_constructor_variables is not None:
      func_engine2 = FunctionEngine(
        function=slither_constructor_variables,
        node_handler=NodeDebugger(
          _config=self.config, ctx_constant=done_ctx_constant_construct
        ),
        config=self.config,
      )
      self.done_list[slither_constructor_variables] = func_engine2.exec()
      done_ctx_slither_construct = func_engine2.done_list[0]

    if contract_constructor is not None:
      func_engine3 = FunctionEngine(
        function=contract_constructor,
        node_handler=NodeDebugger(
          _config=self.config,
          ctx_slither_construct=done_ctx_slither_construct,
          ctx_constant=done_ctx_constant_construct,
        ),
        config=self.config,
      )
      self.done_list[contract_constructor] = func_engine3.exec()
      done_ctx_constructor = Context(
        None, compute_merged_env(func_engine3.done_list), [], [], []
      )

    self.do_pure(
      done_ctx_slither_construct=done_ctx_slither_construct,
      done_ctx_constant_construct=done_ctx_constant_construct,
      done_ctx_constructor=done_ctx_constructor,
    )

    if not self.config.debug:
      from rich.progress import track

      itering = track(
        filter(lambda x: not x.pure, self.functions),
        description="Executing Functions...",
      )
    else:
      itering = filter(lambda x: not x.pure, self.functions)

    for func in itering:
      if (
        True
        and func.contract_declarer == self.contract
        and func.full_name
        not in (
          "slitherConstructorVariables()",
          "slitherConstructorConstantVariables()",
        )
      ):
        func_engine = FunctionEngine(
          function=func,
          node_handler=NodeDebugger(
            _config=self.config,
            ctx_slither_construct=done_ctx_slither_construct,
            ctx_constant=done_ctx_constant_construct,
            ctx_constructor=done_ctx_constructor,
          ),
          config=self.config,
        )
        done_list: summary.List[Context] = func_engine.exec()
        self.done_list[func] = done_list
        # for context in done_list:
        #   for k, v in context.env.binding.items():
        #     log(f'{k} : {v}')
        # input()
