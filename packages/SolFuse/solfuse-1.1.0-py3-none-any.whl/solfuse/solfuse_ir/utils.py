from __future__ import annotations
from locale import currency
from pathlib import Path
import pdb
import traceback
import disjoint_set
import solcix
from functools import reduce
from typing import TYPE_CHECKING, Dict, List, Tuple
from slither.core.solidity_types import (
  ElementaryType,
  elementary_type,
  Type,
  ArrayType,
  MappingType,
  UserDefinedType,
  TypeInformation,
  FunctionType,
)

if TYPE_CHECKING:
  from solfuse.solfuse_ir.env import Env
  from solfuse.solfuse_ir.context import Context
from . import symbol
from slither.slithir.variables import ReferenceVariable
from slither.core.variables import Variable, LocalVariable, StateVariable
from z3 import (
  BoolVal,
  IntVal,
  RealVal,
  StringVal,
  SortRef,
  BoolSort,
  StringSort,
  IntSort,
  RealSort,
  ArraySort,
  Bool,
  Int,
  String,
  Array,
  Real,
  Const,
  EnumSort,
  Datatype,
  If,
  simplify,
  Sort,
  Or,
  Function,
  RecFunction,
  Solver,
)
from slither.core.declarations.structure import Structure
from slither.core.declarations import StructureContract, EnumContract, FunctionContract
from slither.core.declarations.enum import Enum
from slither.core.declarations.contract import Contract
from slither.core.cfg.node import Node, NodeType
from . import logger

log = logger.log


def custom_exception_handler(type, value, tb):
  # Print the exception details
  traceback.print_exception(type, value, tb)
  # Start pdb debugger at the point where exception occurred
  pdb.post_mortem(tb)


def ensure_version(file: str):
  file_path = Path(file)
  assert file_path.is_file()
  try:
    if solcix.resolve_version_from_solidity(file_path.as_posix()):
      version = solcix.install_solc_from_solidity(file_path)
      # solcix.manage.switch_local_version(version=version, always_install=True)
      return version
    else:
      return None
  except:
    pass
    # raise NotImplementedError(file)


def get_variable_name(variable: Variable):
  name = variable.name
  if isinstance(variable, (LocalVariable, StateVariable)):
    name = variable.canonical_name
  return name


def get_return_name(variable: Variable, cnt: int):
  ret_name_template = "@return"
  if variable and variable.name:
    return get_variable_name(variable=variable)
  if variable and variable.name == "":
    # shoule be "xxx." but without variable name following the dot, so we use it to connect our template ret_name
    return f"{get_variable_name(variable=variable)}{ret_name_template}{cnt}"
  return f"{ret_name_template}{cnt}"


def compute_merged_expr_env(done_env: List[Context], variable_name: str):
  if variable_name == "@pc":
    return reduce(
      lambda x, y: simplify(Or(x, y)), map(lambda x: x.env.pc._symbolic_value, done_env)
    )
  return _compute_merged_expr(
    list(map(lambda x: x.env.pc._symbolic_value, done_env)),
    list(map(lambda x: x.env.get(variable_name)._symbolic_value, done_env)),
  )


def _compute_merged_expr(pc_list: list, symbolic_variable_list: list):
  assert len(pc_list) == len(symbolic_variable_list)
  if len(pc_list) == 1:
    return symbolic_variable_list[0]
  # TODO: maybe we can do this proper
  if isinstance(symbolic_variable_list[0], FunctionContract):
    return symbolic_variable_list[0]
  try:
    return simplify(
      If(
        pc_list[0],
        symbolic_variable_list[0],
        _compute_merged_expr(pc_list[1:], symbolic_variable_list[1:]),
      )
    )
  except:
    return symbolic_variable_list[0]


def compute_merged_disjoint_set(done_env: List[Context]):
  new_disjoint_set = disjoint_set.DisjointSet()
  for env in done_env:
    # log(repr(env.env.ref_disjoint_set))
    for x, root in env.env.ref_disjoint_set:
      new_root = new_disjoint_set.find(x)
      new_disjoint_set.union(new_root, root)
  # log(repr(new_disjoint_set))
  # input()
  return new_disjoint_set


def compute_merged_ref_mappings(
  done_env: List[Context], merged_disjoint_set: disjoint_set.DisjointSet
):
  new_ref_to_symbolic_value = {}
  new_symbolic_value_to_ref = {}

  for x, root in merged_disjoint_set:
    # filter that those env that do not contain root
    filtered_env = list(filter(lambda c: root in c.env.ref_disjoint_set, done_env))
    expr_list = list(
      map(
        lambda x: x.env.ref_to_symbolic_value[x.env.ref_disjoint_set[root]],
        filtered_env,
      )
    )
    pc_list = list(map(lambda x: x.env.pc._symbolic_value, filtered_env))
    merged_expr = _compute_merged_expr(
      pc_list=pc_list, symbolic_variable_list=expr_list
    )
    new_ref_to_symbolic_value[root] = merged_expr
    new_symbolic_value_to_ref[merged_expr] = root

  return new_ref_to_symbolic_value, new_symbolic_value_to_ref


def compute_on_chain_info(done_env: List[Context]):
  result = {}
  from z3 import Optimize, sat, unsat

  for env in map(lambda x: x.env, done_env):
    for k, v in env.binding.items():
      if v._is_on_chain:
        solver = Solver()
        solver.add(env.pc._symbolic_value)
        # solver.add(v._symbolic_value)
        if solver.check() == sat:
          result[k] = solver.model().eval(v._symbolic_value)
        else:
          result[k] = None

  # for env in map(lambda x: x.env, done_env):
  #   for k, v in env.binding.items():
  #     if v._is_on_chain:
  #       min_optimizer, max_optimizer = Optimize(), Optimize()
  #       min_optimizer.add(env.pc._symbolic_value)
  #       max_optimizer.add(env.pc._symbolic_value)
  #       min_obj = min_optimizer.minimize(v._symbolic_value)
  #       max_obj = max_optimizer.maximize(v._symbolic_value)
  #       min_result = min_optimizer.check()
  #       max_result = max_optimizer.check()
  #       if min_result == max_result and min_result is sat:
  #         min_value = min_obj.lower()
  #         max_value = max_obj.upper()
  #         result[k] = (min_value, max_value)
  #       else:
  #         result[k] = ()
  return result


def compute_merged_env(done_env: List[Context]):
  import solfuse.solfuse_ir.env

  result_env = solfuse.solfuse_ir.env.Env()
  merged_disjoint_set = compute_merged_disjoint_set(done_env=done_env)
  result_env.ref_disjoint_set = merged_disjoint_set
  result_env.ref_to_symbolic_value, result_env.symbolic_value_to_ref = (
    compute_merged_ref_mappings(
      done_env=done_env, merged_disjoint_set=merged_disjoint_set
    )
  )
  for e in done_env:
    for k, v in e.env.binding.items():
      # filter out the env that do not contain this variable name
      filtered_env = list(filter(lambda x: k in x.env.binding, done_env))
      merged_expr = compute_merged_expr_env(
        done_env=filtered_env, variable_name=v._name
      )
      result_env.add(
        name=k, soltype=v._type, value=v._value, symbolic_value=merged_expr
      )
      result_env.get(k)._is_on_chain = v._is_on_chain
  return result_env


global_sort_cache: Dict[Type, SortRef] = {}
global_datatype_cache: Dict[Type, Datatype] = {}


def get_real_sort(t):
  if isinstance(t, Tuple):
    return t[0]
  return t


def make_datatypes_and_sorts(t: List, created_types=[]):
  all_datatypes = []
  all_sorts = []
  for t1 in t:
    thing = select_z3datatype(t1, created_types)
    if isinstance(thing, Datatype):
      all_datatypes.append((t1, thing))
      all_sorts.append(None)
    elif isinstance(thing, SortRef):
      all_sorts.append(thing)
    elif isinstance(thing, Tuple):
      # all_datatypes.append((t1, thing[0]))
      all_sorts.append(thing[0])

  # refresh from cache
  for cnt, t1 in enumerate(all_datatypes):
    if global_datatype_cache[t1[0]] is not t1[1]:
      all_datatypes[cnt] = (t1[0], global_datatype_cache[t1[0]])
  return all_datatypes, all_sorts


def fill_hole_in_all_sorts(all_sorts, to_fill):
  cnt_datatype = 0
  for cnt, t2 in enumerate(all_sorts):
    if t2 is None:
      all_sorts[cnt] = to_fill[cnt_datatype][1]
      cnt_datatype += 1
  return all_sorts


def make_all_sorts(t: List):
  all_datatypes, all_sorts = make_datatypes_and_sorts(t)

  all_sorts_created_from_datatype = create_all_datatype_and_update_type_cache(
    list(map(lambda x: x[1], all_datatypes)), list(map(lambda x: x[0], all_datatypes))
  )

  all_sorts_created_from_datatype = list(
    zip(list(map(lambda x: x[0], all_datatypes)), list(all_sorts_created_from_datatype))
  )

  return fill_hole_in_all_sorts(all_sorts, all_sorts_created_from_datatype)
  # cnt_datatype = 0
  # for cnt, t2 in enumerate(all_sorts):
  #   if t2 is None:
  #     all_sorts[cnt] = all_sorts_created_from_datatype[cnt_datatype]
  #     cnt_datatype += 1

  # return all_sorts


def make_datatype_tuple(t: Tuple):
  # means a tuple, make a special type for each TupleVariable, _type[0] is the type name, [1:] is types a tuple contains
  _type_name, _type = t[0], t[1:]

  all_sorts_in_tuple = make_all_sorts(_type)
  new_type = Datatype(_type_name)
  new_type.declare(
    "cons", *list(map(lambda x: (f"index{x[0]}", x[1]), enumerate(all_sorts_in_tuple)))
  )
  return new_type


def update_global_sort_cache(_type, new_datatype):
  global_sort_cache[_type] = new_datatype
  if isinstance(_type, UserDefinedType):
    global_sort_cache[_type.type] = new_datatype


def create_datatype_and_update_type_cache(new_datatype, _type):
  from z3 import CreateDatatypes

  new_datatype = CreateDatatypes(new_datatype)
  assert len(new_datatype) == 1
  new_datatype = new_datatype[0]
  update_global_sort_cache(_type, new_datatype)
  return new_datatype


def create_all_datatype_and_update_type_cache(new_datatypes, _types):
  from z3 import CreateDatatypes

  if not new_datatypes:
    return ()
  new_datatypes = CreateDatatypes(*new_datatypes)
  for cnt, t in enumerate(new_datatypes):
    if isinstance(t, Tuple):
      update_global_sort_cache(_types[cnt], t[0])
    else:
      update_global_sort_cache(_types[cnt], t)
  return new_datatypes


def make_sort_elementary(_type: ElementaryType):
  if _type.name == "bool":
    return BoolSort()
  elif _type.name == "string":
    return StringSort()
  elif _type.name == "address":
    return IntSort()
  elif _type.name in elementary_type.Int + elementary_type.Uint + elementary_type.Byte:
    return IntSort()
  elif _type.name in elementary_type.Fixed + elementary_type.Ufixed:
    return RealSort()
  else:
    raise NotImplementedError(_type)


def make_datatype_enum(_type: Enum):
  return EnumSort(name=_type.canonical_name, values=_type.values)


def make_sort_enum(_type: Enum):
  enum_sort, item_list = make_datatype_enum(_type)
  global_sort_cache[_type] = (enum_sort, item_list)
  return enum_sort, item_list


def make_datatype_structure(
  _type: Structure, user_defined_type: UserDefinedType = None, created_types=[]
):
  data_type = Datatype(_type.name)
  data_type.declare("nil")
  if user_defined_type:
    global_datatype_cache[user_defined_type] = data_type
    global_datatype_cache[_type] = data_type
  else:
    global_datatype_cache[_type] = data_type
  # all_names = list(map(lambda x: x[0] if not isinstance(
  #     x[1].type, FunctionType) else f'@function_{x[0]}', _type.elems.items()))
  # all_datatypes, all_sorts = make_datatypes_and_sorts(
  # map(lambda x: x[1].type, _type.elems.items()), created_types)
  # all_sorts = fill_hole_in_all_sorts(all_sorts, all_datatypes)
  # all_sorts = make_all_sorts(map(lambda x: x[1].type, _type.elems.items()))
  # assert len(all_names) == len(all_sorts)
  # field_list = list(zip(all_names, all_sorts))
  field_list = list(
    map(
      lambda x: (
        x[0] if not isinstance(x[1].type, FunctionType) else f"@function_{x[0]}",
        get_real_sort(t=select_z3sort(x[1].type)),
      ),
      _type.elems.items(),
    )
  )
  data_type.declare("cons", *field_list)

  return data_type


def need_to_create_datatype(_type: Type):
  return (
    isinstance(_type, Structure)
    or isinstance(_type, StructureContract)
    or isinstance(_type, Contract)
    or (isinstance(_type, UserDefinedType) and need_to_create_datatype(_type.type))
    or (isinstance(_type, ArrayType) and need_to_create_datatype(_type.type))
    or (
      isinstance(_type, MappingType)
      and (
        need_to_create_datatype(_type.type_from)
        or need_to_create_datatype(_type.type_to)
      )
    )
  )


def make_datatype_contract_single(
  queue_datatype,
  _type: Contract,
  user_defined_type: UserDefinedType = None,
  created_types=[],
):
  data_type = Datatype(_type.name)

  all_names = list(
    map(
      lambda x: x[0]
      if not isinstance(x[1].type, FunctionType)
      else f"@function_{x[0]}",
      _type.variables_as_dict.items(),
    )
  )
  for name, variable in _type.variables_as_dict.items():
    if need_to_create_datatype(variable.type):
      new_datatype = Datatype(name=variable.name)
      new_datatype.declare("nil")
    else:
      pass


def make_datatype_contract(
  _type: Contract, user_defined_type: UserDefinedType = None, created_types=[]
):
  data_type = Datatype(_type.name)
  data_type.declare("nil")
  if user_defined_type:
    global_datatype_cache[user_defined_type] = data_type
  else:
    global_datatype_cache[_type] = data_type

  all_names = list(
    map(
      lambda x: x[0]
      if not isinstance(x[1].type, FunctionType)
      else f"@function_{x[0]}",
      _type.variables_as_dict.items(),
    )
  )
  all_datatypes, all_sorts = make_datatypes_and_sorts(
    map(lambda x: x[1].type, _type.variables_as_dict.items()), created_types
  )
  # created_types.extend(all_datatypes)
  all_sorts = fill_hole_in_all_sorts(all_sorts, all_datatypes)
  # all_sorts = make_all_sorts(
  #     map(lambda x: x.type, _type.variables_as_dict.values()))
  assert len(all_names) == len(all_sorts)
  variable_list = list(zip(all_names, all_sorts))
  # variable_list = list(
  #     map(lambda x: (x[0] if not isinstance(x[1].type, FunctionType) else f'@function_{x[0]}', get_real_sort(select_z3sort(x[1].type))), _type.variables_as_dict.items()))
  data_type.declare("cons", *variable_list)

  # for cnt, (t, d) in enumerate(all_datatypes):
  #   if user_defined_type == t:
  #     all_datatypes[cnt][1] = data_type
  #   elif _type == t:
  #     all_datatypes[cnt][1] = data_type

  if user_defined_type:
    global_datatype_cache[user_defined_type] = data_type
    update_created_types(created_types, data_type, user_defined_type)
    # created_types.append((user_defined_type, data_type))
  else:
    update_created_types(created_types, data_type, _type)
    # created_types.append((_type, data_type))
    global_datatype_cache[_type] = data_type
  return data_type


def update_created_types(created_types, new_datatype, _type):
  type_exists = False
  for cnt, (t, d) in enumerate(created_types):
    if _type == t:
      type_exists = True
      # created_types[cnt] = (_type, new_datatype)
  if not type_exists:
    created_types.append((_type, new_datatype))
  return created_types


def make_sort_user_defined(_type: UserDefinedType, created_types=[]):
  if (t := global_sort_cache.get(_type.type)) is not None:  # prevent redefining
    return t
  match _type.type:
    case Enum() | EnumContract() as e:
      enum_sort, item_list = make_sort_enum(e)
      global_sort_cache[_type] = (enum_sort, item_list)
      return enum_sort, item_list
    case Structure() | StructureContract() as s:
      data_type = make_datatype_structure(
        s, user_defined_type=_type, created_types=created_types
      )
      # created_types.append((_type, data_type))
      # update_created_types(created_types, data_type, _type)
      return create_datatype_and_update_type_cache(data_type, _type)
    case Contract() as c:
      data_type = make_datatype_contract(
        c, user_defined_type=_type, created_types=created_types
      )
      # print(list(map(lambda x: x[0].__str__(), created_types)))
      # created_types = list(set(created_types))
      # print(list(map(lambda x: x[0].__str__(), created_types)))
      create_all_datatype_and_update_type_cache(
        list(map(lambda x: x[1], created_types)),
        list(map(lambda x: x[0], created_types)),
      )
      return global_sort_cache[_type]
      # return create_datatype_and_update_type_cache(data_type, _type)
  raise NotImplementedError(f"UserDefinedType: {_type}")


def make_datatype_contract_and_structure(
  _type: Structure | StructureContract | Contract,
  user_defined_type=None,
  created_types=[],
):
  if (t := global_datatype_cache.get(_type)) is not None:
    # created_types.append((_type, t))
    update_created_types(created_types, t, _type)
    return t
  if isinstance(_type, Structure) or isinstance(_type, StructureContract):
    return make_datatype_structure(
      _type=_type, user_defined_type=user_defined_type, created_types=created_types
    )
  if isinstance(_type, Contract):
    return make_datatype_contract(
      _type, user_defined_type=user_defined_type, created_types=created_types
    )
  raise NotImplementedError(f"UserDefinedType: {_type}")


def select_z3datatype(
  _type: Type | List[Type] | TypeInformation, created_types=[]
) -> Datatype | SortRef:
  if (t := global_datatype_cache.get(_type)) is not None:
    update_created_types(created_types, t, _type)
    # created_types.append((_type, t))
    return t
  match _type:
    case tuple():
      t = make_datatype_tuple(_type)
      global_datatype_cache[_type] = t
      update_created_types(created_types, t, _type)
      # created_types.append((_type, t))
      return t
    case UserDefinedType():
      match _type.type:
        case Structure() | StructureContract() | Contract() as s:
          t = make_datatype_contract_and_structure(
            s, user_defined_type=_type, created_types=created_types
          )
          # created_types.append((_type, t))
          update_created_types(created_types, t, _type)
          global_datatype_cache[_type] = t
          # global_datatype_cache[_type.type] = t
          return t
        case _:
          return select_z3sort(_type)
    # case Enum():
    #   return make_datatype_enum(_type)
    case Structure() | Contract():
      t = make_datatype_contract_and_structure(_type, created_types=created_types)
      # created_types.append((_type, t))
      update_created_types(created_types, t, _type)
      global_datatype_cache[_type] = t
      return t
    case _:
      return select_z3sort(_type)


def select_z3sort(_type: Type | List[Type] | TypeInformation) -> SortRef:
  if isinstance(_type, TypeInformation):
    return select_z3sort(_type.type)
  if (t := global_sort_cache.get(_type)) is not None:
    # log(f"CACHE HIT FOR {_type}")
    return t
  match _type:
    case tuple():
      return create_datatype_and_update_type_cache(
        make_datatype_tuple(_type), _type[1:]
      )
    case ElementaryType():
      return make_sort_elementary(_type)
    case ArrayType():
      return ArraySort(IntSort(), get_real_sort(select_z3sort(_type.type)))
    case MappingType():
      return ArraySort(
        get_real_sort(select_z3sort(_type=_type.type_from)),
        get_real_sort(select_z3sort(_type=_type.type_to)),
      )
    case UserDefinedType():
      return make_sort_user_defined(_type)
    case FunctionType():
      # Dummy sort
      return RealSort()
    # * Some variable will directly use UserdefinedType.type as their type, wipe ass for them
    case Enum():
      e, i = make_sort_enum(_type)
      global_sort_cache[_type] = (e, i)
      return e, i
    case Structure() | Contract():
      return create_datatype_and_update_type_cache(
        make_datatype_contract_and_structure(_type), _type
      )
  raise NotImplementedError(f"Type: {_type}")


def get_variable_default_value(_type: Type):
  assert isinstance(_type, ElementaryType)
  if _type.name == "bool":
    return BoolVal(False)
  if _type.name == "string":
    return StringVal("")
  if _type.name in elementary_type.Int + elementary_type.Uint + elementary_type.Byte + [
    "address"
  ]:
    return IntVal(0)
  if _type.name in elementary_type.Fixed + elementary_type.Ufixed:
    return RealVal(0)


def get_variable_default_range(_type: Type):
  if isinstance(_type, Enum):
    srt, item_list = select_z3sort(_type)
    return (0, len(item_list) - 1)
  if _type is None or not isinstance(_type, ElementaryType):
    return None
  if _type.name == "bool":
    return None

  if _type.name == "string":
    return None  # why in the hell i need this?

  if _type.name == "address":
    return (0, 1 << (8 * 20) - 1)

  if _type.name in elementary_type.Int:
    return (-(1 << (int(_type.name[3:]) - 1)), (1 << (int(_type.name[3:]) - 1)) - 1)

  if _type.name in elementary_type.Uint:
    return (0, (1 << (int(_type.name[4:]))) - 1)
  return None


def make_z3variable(_type: Type, name: str):
  if isinstance(_type, List):
    _type = tuple(_type)
  srt = select_z3sort(_type)
  if isinstance(srt, Tuple):
    return Const(name, IntSort())
  return Const(name, sort=srt)


def ref_to_actual_target(v: symbol.Symbol, ctx: Env):
  # if not isinstance(v._value, ReferenceVariable) or getattr(v._value, 'sym_right', None) is None:
  return ctx.ref_to_actual_target(v._name)
  # value: ReferenceVariable = v._value
  # product = ctx.get(name=get_variable_name(
  # variable=value.points_to))._symbolic_value[value.sym_right]
  # product = value.sym_right
  # while isinstance(value, ReferenceVariable):
  #   if product is None:
  #     product = ctx.get(name=get_variable_name(
  #         variable=value.points_to))._symbolic_value[value.sym_right]
  #   else:
  #     product = ctx.get(name=get_variable_name(
  #         variable=value.points_to))._symbolic_value[product]
  #   value = value.points_to
  # return product
