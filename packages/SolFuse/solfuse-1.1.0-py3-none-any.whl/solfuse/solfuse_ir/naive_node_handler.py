from typing import Callable, List, Tuple
from .handler import ForkSelector, Handler
from .logger import log
from .env import Env
from slither.core.cfg.node import Node, NodeType
from slither.slithir.operations import Operation


class NaiveNodeHandler(Handler):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(
      name_dispatch_func=lambda node: node.type.__str__().split(".")[1],
      name_dispatch_keyword="node",
    )
    self.ir_handler = NaiveIRHandler()
    self.count = 0
    self.node_vis = {}  # prevent infinite loop

  def handle_default(
    self, node: Node, env: Env, *args, **kwargs
  ) -> Tuple[List[Node], ForkSelector, Env]:
    # allow one node to be visited at most 2 times, a naive way of handling nested call
    if self.node_vis.get(node, 0) >= 1:
      return [], ForkSelector.No, env
    self.node_vis[node] = self.node_vis.get(node, -1) + 1
    log(f"BB{{{self.name_dispatch_func(node)}}}[{self.count}]:")
    log.config.global_tab += 1
    for ir in node.irs:
      self.ir_handler.handle_(ir=ir, env=env)
    log.config.global_tab -= 1
    self.count += 1
    if Node.type in (NodeType.IF, NodeType.IFLOOP):
      # always needs to fork for full coverage, because **`naive`**
      return node.sons, ForkSelector.Yes, env
    if not node.sons:
      self.clear_count()
    return node.sons, ForkSelector.No, env

  def clear_count(self):
    self.count = 0


class NaiveIRHandler(Handler):
  def __init__(self) -> None:
    super().__init__(
      name_dispatch_func=lambda ir: type(ir).__name__.__str__().split(".")[-1],
      name_dispatch_keyword="ir",
    )

  def handle_default(self, ir: Operation, env: Env):
    log(f"{ir}")
