from typing import Any, Iterator
from dataclasses import dataclass
from slither.core.cfg.node import Node
from slither.core.declarations import Function
from .env import Env
from enum import Enum


class ForkStatus(Enum):
  No = 0
  YesTrue = 1
  YesFalse = 2


@dataclass
class Context:
  node: Node
  env: Env
  fork_stack: list[ForkStatus]
  pending_calls: list[Function]
  pending_arguments: list[Any]

  def __iter__(self) -> Iterator[Node | Env]:
    return iter(
      (self.node, self.env, self.fork_stack, self.pending_calls, self.pending_arguments)
    )
