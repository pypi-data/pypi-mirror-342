from typing import Optional, overload

from solfuse.solfuse_ir.function_engine import FunctionEngine
from .handler import Handler


class Debugger(Handler):
  """Generic Debugger class for symbolic engine. Do debug by wrapping an acutal handler do the heavy-lifting work and run hook functions before and after every actual handle happens.

  Args:
      Handler (Handler): A functional handler that do the actual work.
  """

  def __init__(self, actual_handler: Handler, _from: Optional[FunctionEngine]) -> None:
    self.handler = actual_handler
    super().__init__(
      name_dispatch_func=actual_handler.name_dispatch_func,
      name_dispatch_keyword=actual_handler.name_dispatch_kw,
      _from=_from,
    )

  @property
  def from_engine(self):
    return super().from_engine

  @from_engine.getter
  def from_engine(self):
    return super().from_engine

  @from_engine.setter
  def from_engine(self, _from: Optional[FunctionEngine]):
    self._from = _from
    self.handler.from_engine = _from

  def hook_before(self, *args, **kwargs):
    pass

  def hook_after(self, *args, **kwargs):
    pass

  def handle_(self, *args, **kwargs):
    self.hook_before(*args, **kwargs)
    _ = self.handler.handle_(*args, **kwargs)
    self.hook_after(*args, **kwargs)
    return _
