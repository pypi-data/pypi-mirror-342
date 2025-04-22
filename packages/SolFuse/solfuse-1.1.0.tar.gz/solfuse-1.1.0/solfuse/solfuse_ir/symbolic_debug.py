from __future__ import annotations
import pdb
import sys
from typing import Optional

from solfuse.solfuse_ir.config import ConfigProvider, default_config
from solfuse.solfuse_ir.function_engine import FunctionEngine
from . import context
from . import expr_handler
from . import handler
from . import node_handler
from . import variable_handler
from .debugger import Debugger
from .logger import log

from slither.slithir.operations import LibraryCall
import readline


class IRDebugger(Debugger):
  def pause(self, *args, **kwargs):
    cnt = log.config.global_tab
    log.config.global_tab = 0
    self.shell(*args, **kwargs)
    log.config.global_tab = cnt

  @property
  def do_function_call(self):
    return self.handler.do_function_call

  @property
  def from_engine(self):
    return self._from

  @from_engine.setter
  def from_engine(self, _from: Optional[FunctionEngine]):
    self._from = _from
    self.handler.from_engine = _from

  @property
  def done_ctx_slither_construct(self):
    return self.handler.done_ctx_slither_construct

  @property
  def done_ctx_constant_construct(self):
    return self.handler.done_ctx_constant

  @property
  def done_ctx_constructor(self):
    return self.handler.done_ctx_constructor

  @done_ctx_slither_construct.setter
  def done_ctx_slither_construct(self, ctx: context.Context):
    self.handler.done_ctx_slither_construct = ctx

  @done_ctx_constant_construct.setter
  def done_ctx_constant_construct(self, ctx: context.Context):
    self.handler.done_ctx_constant = ctx

  @done_ctx_constructor.setter
  def done_ctx_constructor(self, ctx: context.Context):
    self.handler.done_ctx_constructor = ctx

  @staticmethod
  def env(*args, **kwargs):
    argv = kwargs.get("argv")
    env = kwargs.get("env")
    if argv is None:
      argv = []
    assert isinstance(argv, list)

    if len(argv) > 0:
      from .env import SymbolNotFoundError

      for name in argv:
        log(f"{name}: ")
        log.config.global_tab += 1
        try:
          symbol = env.get(name=name)
          log(symbol)
        except SymbolNotFoundError:
          log("Not Found")
        log.config.global_tab -= 1
    else:
      log(env.binding)

  cmds = {"env": env}

  def log_ir(self, *args, **kwargs):
    ir = kwargs.get("ir")
    self.ir_cnt += 1
    log.config.global_tab += 1
    log(f"[{(self.ir_cnt)}]: {ir}", will_do=self.config.print_stmt)
    log.config.global_tab -= 1

  def __init__(
    self,
    config: ConfigProvider = default_config,
    expr_handler: handler.Handler = expr_handler.ExprHandler(),
    variable_handler: handler.Handler = variable_handler.VariableHandler(),
    _from: Optional[FunctionEngine] = None,
  ) -> None:
    from .ir_handler import IRHandler

    actual_handler = IRHandler(
      config=config, expr_handler=expr_handler, variable_handler=variable_handler
    )
    super().__init__(actual_handler, _from=_from)
    self.ir_cnt = 0
    self.config = config

  def shell(self, *args, **kwargs):
    try:
      while (cmd := input("(sym)> ").strip()) != "exit":
        argv = cmd.split()
        head, argv = argv[0], argv[1:]

        self.cmds.get(head, lambda *args, **kwargs: log(cmd))(argv=argv, **kwargs)
    except EOFError:
      pass

  def hook_before(self, *args, **kwargs):
    ir = kwargs.get("ir")
    self.log_ir(*args, **kwargs)
    match ir:
      case LibraryCall():
        if ir.destination.name == "Verification":
          match ir.function_name:
            case "Pause":
              breakpoint()
              # self.pause()
            case "Assume":
              log("WARNING: Verification.Assume Not Implemented")
              pass
            case _:
              raise NotImplementedError(ir.function.name)

  def handle_(self, *args, **kwargs):
    self.hook_before(*args, **kwargs)
    _ = self.handler.handle_(*args, **kwargs)
    self.hook_after(*args, **kwargs)
    return _


class NodeDebugger(Debugger):
  def __init__(
    self,
    _config: ConfigProvider,
    ctx_slither_construct: context.Context | None = None,
    ctx_constant: context.Context | None = None,
    ir_handler: handler.Handler = IRDebugger(),
    ctx_constructor: context.Context | None = None,
    _from: Optional[FunctionEngine] = None,
  ) -> None:
    ir_handler.from_engine = _from
    actual_handler = node_handler.NodeHandler(
      config=_config,
      ctx_slither_construct=ctx_slither_construct,
      ctx_constant=ctx_constant,
      ir_handler=ir_handler,
      ctx_constructor=ctx_constructor,
      _from=_from,
    )
    super().__init__(actual_handler=actual_handler, _from=_from)
    self.from_engine = _from
    self.node_cnt = 0
    self.config = _config
    ir_handler.config = _config

  @property
  def from_engine(self):
    return self._from

  @from_engine.setter
  def from_engine(self, _from: Optional[FunctionEngine]):
    self._from = _from
    self.handler.from_engine = _from

  @property
  def pending_calls(self):
    return self.handler.pending_calls

  @property
  def pending_arguments(self):
    return self.handler.pending_arguments

  @pending_calls.setter
  def pending_calls(self, calls):
    self.handler.pending_calls = calls

  @pending_arguments.setter
  def pending_arguments(self, args):
    self.handler.pending_arguments = args

  def clear_ir_cnt(self):
    self.handler.ir_handler.ir_cnt = 0

  def log_node(self, *args, **kwargs):
    next_node = kwargs.get("node")
    self.node_cnt += 1
    log(f"[{(self.node_cnt)}]: {next_node.type}", will_do=self.config.print_stmt)
    self.clear_ir_cnt()

  def hook_before(self, *args, **kwargs):
    self.log_node(*args, **kwargs)

  def hook_after(self, *args, **kwargs):
    return
    if not kwargs.get(self.handler.name_dispatch_kw).sons:
      log(kwargs.get("env").binding)
