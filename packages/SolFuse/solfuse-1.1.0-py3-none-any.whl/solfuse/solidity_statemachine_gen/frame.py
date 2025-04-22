from io import StringIO

from slither.core.solidity_types.elementary_type import ElementaryType
from slither.core.source_mapping.source_mapping import SourceMapping
from z3 import *

from .indent_print import indent_print
from .utils import VarGenerator
from .variable_type import make_z3variable, get_variable_default_value


class Frame:
  class VariableNotFoundException(Exception):
    pass

  class ExprNotFoundException(Exception):
    pass

  def __init__(self, father):
    self.variables = {}
    self.binding = {}
    # rbinding means reverse binding. sometimes need to get name based on expr. what a mess.
    # rbinding maps a expr to (name: str, variable: z3 expr) pair.
    self.rbinding = {}
    self.vargen = VarGenerator()
    self.father = father

  def print_to_file(self, s):
    indent_print("Frame:", file=s)
    for name in self.variables.keys():
      indent_print(f"{name}:", indent=1, file=s)
      indent_print(self.get(name), indent=2, file=s)

  def __str__(self):
    s = StringIO()
    self.print_to_file(s)
    return s.getvalue()

  def simplify(self):
    for k, v in self.binding.items():
      if not isinstance(v, SourceMapping):
        self.binding[k] = simplify(v)

  def ensure_variable(self, name: str, _type=None, sort=None, wontadd=False):
    if self.variables.get(name, None) is not None:
      return self.variables[name]
    else:
      if wontadd:
        return None
      self.variables[name] = self.make_variable_from_type_or_sort(name, _type, sort)
      return self.variables[name]

  def make_variable_from_type_or_sort(self, name, _type, sort):
    if sort is not None:
      return Const(name, sort)
    return make_z3variable(_type, name)

  def add(self, name, _type=None, value=None, sort=None, need_default=False):
    if _type is None:
      _type = ElementaryType("int")
    variable = None
    reg = self
    while (variable is None) and reg.father:
      variable = reg.ensure_variable(name, _type, sort, wontadd=True)
      reg = reg.father
    if variable is None:
      variable = reg.ensure_variable(name, _type, sort)
    if value is None:
      if (
        need_default
        and _type is not None
        and isinstance(_type, ElementaryType)
        and _type.name != "bool"
      ):
        reg.binding[variable] = get_variable_default_value(_type)
      else:
        reg.binding[variable] = self.make_variable_from_type_or_sort(
          f"@{name}", _type, sort
        )
    else:
      reg.binding[variable] = value
    # to maintain reverse binding's correctness. this rbinding will become big rapidly, i mean, giant.
    reg.binding[variable] = simplify(reg.binding[variable])
    reg.rbinding[reg.binding[variable]] = (name, variable)

  def get_rbinding(self, variable):
    if self.rbinding.get(variable, None) is not None:
      return self.rbinding[variable]
    if self.father:
      return self.father.get_rbinding(variable)
    raise self.ExprNotFoundException

  def get(self, name):
    variable = self.ensure_variable(name, wontadd=True)
    if variable is None or self.binding.get(variable, None) is None:
      if self.father is not None:
        return self.father.get(name)
      raise self.VariableNotFoundException(name)
    return self.binding[variable]
