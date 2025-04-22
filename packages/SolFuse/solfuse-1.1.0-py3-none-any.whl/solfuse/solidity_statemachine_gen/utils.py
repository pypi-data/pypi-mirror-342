import time
from pathlib import Path


def merge_dict2(A: dict, B: dict, VA, VB, f):
  return {
    VA[k]: (
      f(A.get(VA[k]), B.get(VB[k]), k)
      if k in VA.keys() and k in VB.keys()
      else A.get(VA[k], B.get(VB[k]))
    )
    for k in VA.keys() | VB.keys()
  }


def merge_dict(A: dict, B: dict, f):
  return {
    k: f(A.get(k), B.get(k), k)
    if k in A.keys() and k in B.keys()
    else A.get(k, B.get(k))
    for k in A.keys() | B.keys()
  }


class VarGenerator:
  """
  deepcopy does not like generator.
  impl this class to make deepcopy happy.
  """

  def __init__(self) -> None:
    self.counter = Counter()

  def next(self) -> str:
    return f"@v{self.counter.next()}"


class Counter:
  def __init__(self) -> None:
    self.cnt = 0

  def next(self) -> int:
    self.cnt += 1
    return self.cnt - 1


def run_for_this_seconds(t: float):
  time.sleep(t)
  return t
