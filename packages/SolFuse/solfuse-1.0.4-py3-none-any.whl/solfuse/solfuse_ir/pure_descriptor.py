from __future__ import annotations
from typing import TYPE_CHECKING, List
from attr import dataclass

if TYPE_CHECKING:
  from solfuse.solfuse_ir.function_engine import FunctionEngine
  from solfuse.solfuse_ir.env import Env
  from slither.core.declarations import FunctionContract
  from slither.slithir.variables import LocalVariable
  from z3 import (
    BoolRef,
    BitVecRef,
    ArrayRef,
  )


@dataclass
class PureDescriptor:
  name: str
  func: FunctionContract
  engine: FunctionEngine
  params: List[LocalVariable]
  env: Env
  pc: BoolRef
