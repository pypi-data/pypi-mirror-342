from typing import Callable
from enum import Enum


class ForkSelector(Enum):
  """
  Selector Enum to mark if needs to fork next.
  `ForkSelector.Yes` means that Engine needs to fork, that is, first execute `son_true` (`son[0]`), then execute `son_false` (`son[1]`).
  `ForkSelector.No` means no need to fork.
  """

  Yes = 0
  No = 1


class Handler:
  def __init__(
    self,
    name_dispatch_func: Callable = lambda _: type(_).__name__.split(".")[-1],
    name_dispatch_keyword: str = "obj",
    _from=None,
    *args,
    **kwargs,
  ) -> None:
    """Generic Handler for different kinds of object of the same type. Typical usage: handle different types of CFG Nodes, statements, or expressions.

    Args:
        name_dispatch_func (Callable): function to dispatch different types of object to functions with different names, usually by getting type name of an object and then perform string tricks.
        name_dispatch_keyword (str): parameter name of that object in the function signature, used to extract the object from kwargs.
    """
    self.name_dispatch_func: Callable = name_dispatch_func
    self.name_dispatch_kw: str = name_dispatch_keyword
    self._from = _from

  @property
  def from_engine(self):
    return self._from

  @from_engine.setter
  def from_engine(self, _from):
    self._from = _from

  @from_engine.getter
  def from_engine(self):
    return self._from

  def handle_default(self, *args, **kwargs):
    raise NotImplementedError(
      f"{self.name_dispatch_kw.upper()}[{self.name_dispatch_func(kwargs.get(self.name_dispatch_kw, None))}]: {kwargs.get(self.name_dispatch_kw, None).__str__()}"
    )

  def handle_(self, *args, **kwargs):
    return getattr(
      self,
      f"handle_{self.name_dispatch_func(kwargs.get(self.name_dispatch_kw, None))}",
      self.handle_default,
    )(*args, **kwargs)
