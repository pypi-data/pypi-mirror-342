import json
import os
import sys
import re
import argparse
import shutil
import concurrent.futures
from slither import Slither
from slither.core.cfg.node import Node
from slither.core.declarations import Contract, Modifier, Function
from slither.analyses.data_dependency.data_dependency import is_dependent
from slither.core.variables.state_variable import StateVariable
from slither.core.expressions import Identifier, MemberAccess
from typing import List, Dict, Any, Set, Optional, Tuple

# 导入Rich库用于美化进度条
from rich.progress import (
  Progress,
  TextColumn,
  BarColumn,
  TimeElapsedColumn,
  TimeRemainingColumn,
  SpinnerColumn,
)
from rich.console import Console

# 定义可能的所有权相关修饰器名称（不区分大小写）
OWNERSHIP_MODIFIER_PATTERNS = [
  r"only_?owner",
  r"only_?admin",
  r"admin_?only",
  r"owner_?only",
  r"is_?owner",
  r"require_?owner",
  r"auth",
  r"authorized",
  r"requires?_?auth",
  r"admin_?role",
  r"owner_?role",
]

# 定义其他常见的访问控制修饰器模式
ACCESS_CONTROL_MODIFIER_PATTERNS = [
  r"only_?role",
  r"has_?role",
  r"with_?role",
  r"require_?role",
  r"when_?not_?paused",
  r"not_?paused",
  r"when_?paused",
  r"only_?minter",
  r"only_?burner",
  r"only_?operator",
  r"only_?delegate",
  r"only_?governor",
  r"only_?controller",
  r"only_?manager",
  r"only_?in_?state",
  r"require_?state",
  r"has_?permission",
  r"only_?whitelist",
  r"require_?whitelist",
  r"requires?_?approve",
  r"require_?not_?locked",
  r"not_?locked",
  r"not_?blacklisted",
  r"not_?banned",
  r"not_?frozen",
]

# 合并所有访问控制模式
ALL_ACCESS_CONTROL_PATTERNS = (
  OWNERSHIP_MODIFIER_PATTERNS + ACCESS_CONTROL_MODIFIER_PATTERNS
)

# 定义区块链全局变量和成员
BLOCKCHAIN_GLOBALS = [
  "msg.sender",
  "msg.value",
  "msg.data",
  "block.timestamp",
  "block.number",
  "block.difficulty",
  "block.coinbase",
  "block.gaslimit",
  "block.chainid",
  "tx.origin",
  "tx.gasprice",
  "now",  # 等同于 block.timestamp
  "blockhash",  # 函数
  "gasleft",  # 函数
]


def check_inheritance_ownership(contract: Contract) -> bool:
  """检查合约是否从名称包含Owner或Admin的合约继承"""
  for inherited in contract.inheritance:
    if "owner" in inherited.name.lower() or "admin" in inherited.name.lower():
      return True
  return False


def check_modifier_ownership(contract: Contract) -> bool:
  """检查合约是否有类似onlyOwner的修饰器"""
  # 编译正则表达式
  patterns = [
    re.compile(pattern, re.IGNORECASE) for pattern in OWNERSHIP_MODIFIER_PATTERNS
  ]

  # 检查合约自身定义的修饰器
  for modifier in contract.modifiers:
    modifier_name = modifier.name.lower()
    # 使用正则表达式匹配
    for pattern in patterns:
      if pattern.search(modifier_name):
        return True

  # 检查合约使用的修饰器（包括继承的）
  for function in contract.functions:
    for modifier in function.modifiers:
      modifier_name = modifier.name.lower()
      # 使用正则表达式匹配
      for pattern in patterns:
        if pattern.search(modifier_name):
          return True

  return False


def check_access_control_modifiers(contract: Contract) -> bool:
  """
  检查合约是否使用了访问控制修饰器（包括所有权和其他类型的访问控制）
  """
  # 编译正则表达式
  patterns = [
    re.compile(pattern, re.IGNORECASE) for pattern in ALL_ACCESS_CONTROL_PATTERNS
  ]

  # 检查合约自身定义的修饰器
  for modifier in contract.modifiers:
    modifier_name = modifier.name.lower()
    # 使用正则表达式匹配
    for pattern in patterns:
      if pattern.search(modifier_name):
        return True

  # 检查合约使用的修饰器（包括继承的）
  for function in contract.functions:
    for modifier in function.modifiers:
      modifier_name = modifier.name.lower()
      # 使用正则表达式匹配
      for pattern in patterns:
        if pattern.search(modifier_name):
          return True

  return False


def check_global_variable_dependency(node: Node, contract: Contract) -> bool:
  """检查节点是否依赖于区块链全局变量"""

  def check_expression(expr):
    """递归检查表达式中的全局变量"""
    if expr is None:
      return False

    # 将表达式转换为字符串进行检查
    expr_str = str(expr)

    # 检查表达式字符串是否包含全局变量
    for global_var in BLOCKCHAIN_GLOBALS:
      if global_var in expr_str:
        return True

    # 检查表达式的子表达式
    if hasattr(expr, "expressions"):
      for sub_expr in expr.expressions:
        if check_expression(sub_expr):
          return True

    # 检查左右表达式（如二元操作）
    if hasattr(expr, "left") and check_expression(expr.left):
      return True
    if hasattr(expr, "right") and check_expression(expr.right):
      return True

    # 检查条件表达式
    if hasattr(expr, "condition") and check_expression(expr.condition):
      return True
    if hasattr(expr, "then_expression") and check_expression(expr.then_expression):
      return True
    if hasattr(expr, "else_expression") and check_expression(expr.else_expression):
      return True

    # 检查函数调用的参数
    if hasattr(expr, "arguments"):
      for arg in expr.arguments:
        if check_expression(arg):
          return True

    # 检查数组访问
    if hasattr(expr, "array") and check_expression(expr.array):
      return True
    if hasattr(expr, "index") and check_expression(expr.index):
      return True

    # 检查成员访问
    if hasattr(expr, "expression") and check_expression(expr.expression):
      return True

    return False

  # 检查节点的主表达式
  if hasattr(node, "expression") and check_expression(node.expression):
    return True

  # 检查条件表达式
  if hasattr(node, "condition") and check_expression(node.condition):
    return True

  # 检查值表达式（赋值等）
  if hasattr(node, "value") and check_expression(node.value):
    return True

  # 检查变量初始化表达式
  if (
    hasattr(node, "variable")
    and hasattr(node.variable, "expression")
    and check_expression(node.variable.expression)
  ):
    return True

  return False


def check_blockchain_dependent_modifiers(contract: Contract) -> Tuple[bool, List[str]]:
  """
  检查合约中是否有依赖区块链全局变量的修饰器，如msg.sender, block.timestamp等

  Returns:
      元组: (是否有依赖全局变量的修饰器, 依赖全局变量的修饰器名称列表)
  """
  has_global_modifiers = False
  global_dependent_modifiers = []

  # 找出合约中所有修饰器
  all_modifiers = contract.modifiers

  # 遍历每个修饰器，检查其是否依赖于区块链全局变量
  for modifier in all_modifiers:
    for node in modifier.nodes:
      # 检查节点中的代码是否依赖全局变量
      if check_global_variable_dependency(node, contract):
        has_global_modifiers = True
        if modifier.name not in global_dependent_modifiers:
          global_dependent_modifiers.append(modifier.name)

  # 检查合约函数使用的修饰器（包括继承的）
  for function in contract.functions:
    for modifier_call in function.modifiers:
      modifier_name = modifier_call.name
      # 检查该修饰器是否存在于继承链中
      for inherited_contract in [contract] + list(contract.inheritance):
        for inherited_modifier in inherited_contract.modifiers:
          if inherited_modifier.name == modifier_name:
            for node in inherited_modifier.nodes:
              if check_global_variable_dependency(node, contract):
                has_global_modifiers = True
                if modifier_name not in global_dependent_modifiers:
                  global_dependent_modifiers.append(modifier.name)

  return has_global_modifiers, global_dependent_modifiers


def check_owner_variable(contract: Contract) -> bool:
  """检查合约是否有owner相关的状态变量"""
  for state_var in contract.state_variables:
    if "owner" in state_var.name.lower() or "admin" in state_var.name.lower():
      return True
  return False


def check_ownership_functions(contract: Contract) -> bool:
  """检查合约是否包含所有权相关的函数"""
  ownership_function_patterns = [
    r"transfer_?ownership",
    r"set_?owner",
    r"change_?owner",
    r"renounce_?ownership",
  ]
  patterns = [
    re.compile(pattern, re.IGNORECASE) for pattern in ownership_function_patterns
  ]

  for function in contract.functions:
    function_name = function.name.lower()
    for pattern in patterns:
      if pattern.search(function_name):
        return True

  return False


def extract_solc_path(command: str) -> Optional[str]:
  """从命令字符串中提取solc路径"""
  if not command:
    return None

  # 查找 --solc= 参数
  match = re.search(r"--solc=([^\s]+)", command)
  if match:
    return match.group(1)

  # 兼容 --crytic-args --solc=路径 的格式
  match = re.search(r"--crytic-args\s+--solc=([^\s]+)", command)
  if match:
    return match.group(1)

  return None


def analyze_contract_for_access_control(
  file_path: str, contract_name: str, solc_path: Optional[str] = None
) -> Dict[str, Any]:
  """分析合约是否包含访问控制特征，并返回分析结果"""
  result = {
    "file_path": file_path,
    "contract_name": contract_name,
    "has_ownership": False,
    "has_state_dependent_modifiers": False,
    "has_blockchain_dependent_modifiers": False,
    "state_dependent_modifiers": [],
    "blockchain_dependent_modifiers": [],
    "details": {},
    "error": None,
    "solc_path_used": solc_path,
  }

  try:
    # 使用Slither分析合约，如果指定了solc路径则使用指定的solc
    slither_kwargs = {}
    if solc_path:
      slither_kwargs["solc"] = solc_path

    slither = Slither(file_path, **slither_kwargs)

    # 找到指定的合约
    contract = None
    for c in slither.contracts:
      if c.name == contract_name:
        contract = c
        break

    if contract is None:
      result["error"] = f"Contract {contract_name} not found in {file_path}"
      return result

    # 检查各种所有权特征
    has_inheritance = check_inheritance_ownership(contract)
    has_modifier = check_modifier_ownership(contract)
    has_owner_var = check_owner_variable(contract)
    has_ownership_functions = check_ownership_functions(contract)

    # 检查访问控制修饰器
    has_access_control = check_access_control_modifiers(contract)

    # 检查依赖状态变量的修饰器 - 替换为区块链全局变量检测
    try:
      has_blockchain_modifiers, blockchain_modifiers = (
        check_blockchain_dependent_modifiers(contract)
      )
      # 为了向后兼容，仍然设置状态依赖变量
      has_state_modifiers, state_modifiers = (
        has_blockchain_modifiers,
        blockchain_modifiers,
      )
    except Exception as e:
      print(f"检查区块链全局变量依赖时出错: {e}")
      has_blockchain_modifiers, blockchain_modifiers = False, []
      has_state_modifiers, state_modifiers = False, []

    # 不再需要单独检查区块链全局变量依赖，因为上面已经检查过了

    # 更新结果
    result["has_state_dependent_modifiers"] = has_blockchain_modifiers  # 保持向后兼容
    result["state_dependent_modifiers"] = blockchain_modifiers  # 保持向后兼容
    result["has_blockchain_dependent_modifiers"] = has_blockchain_modifiers
    result["blockchain_dependent_modifiers"] = blockchain_modifiers
    result["has_ownership"] = (
      has_inheritance or has_modifier or has_owner_var or has_ownership_functions
    )
    result["details"] = {
      "inherits_ownership": has_inheritance,
      "has_ownership_modifier": has_modifier,
      "has_owner_variable": has_owner_var,
      "has_ownership_functions": has_ownership_functions,
      "has_access_control_modifiers": has_access_control,
    }

  except Exception as e:
    result["error"] = str(e)

  return result


def remove_access_control_modifiers(contract_content: str) -> str:
  """
  移除合约中的所有访问控制修饰符

  Args:
    contract_content: 合约源代码字符串

  Returns:
    移除了访问控制修饰符的合约代码
  """
  # 基于已定义的修饰符模式创建正则模式
  modifier_patterns = []
  for pattern in ALL_ACCESS_CONTROL_PATTERNS:
    # 转换为不区分大小写的正则表达式，匹配完整单词
    modifier_patterns.append(rf"\b{pattern}\b")

  modified_content = contract_content

  # 处理函数定义中的修饰符
  # 场景1: function xxx() public onlyOwner { ... }
  for pattern in modifier_patterns:
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern})(\s*\{{|\s+|\()",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  # 场景2: function xxx() public onlyOwner(arg1, arg2) { ... } 或 onlyOwner(arg)
  for pattern in modifier_patterns:
    # 匹配任意参数数量的修饰符调用，包括单参数
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern}\([^)]*\))(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  # 场景3: 多个修饰符以逗号分隔，如: function xxx() public onlyOwner, nonReentrant { ... }
  for pattern in modifier_patterns:
    # 修饰符在前面
    regex = re.compile(rf"(\s*)({pattern})\s*,\s*([^{{,]+)(\s*\{{)", re.IGNORECASE)
    modified_content = regex.sub(r"\1\3\4", modified_content)

    # 修饰符在后面
    regex = re.compile(rf"([^{{,]+)\s*,\s*({pattern})(\s*\{{)", re.IGNORECASE)
    modified_content = regex.sub(r"\1\3", modified_content)

  # 场景4: 处理returns声明之前的修饰符
  for pattern in modifier_patterns:
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern})(\s+returns)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  # 场景5: 处理带参数的修饰符和returns组合
  for pattern in modifier_patterns:
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern}\([^)]*\))(\s+returns)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  # 新增场景6: 处理带参数的修饰符与其他修饰符之间的逗号
  for pattern in modifier_patterns:
    # 处理带参数修饰符后面跟着逗号的情况
    regex = re.compile(
      rf"({pattern}\([^)]*\))\s*,\s*([^{{,]+)(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\2\3", modified_content)

    # 处理带参数修饰符前面有逗号的情况
    regex = re.compile(
      rf"([^{{,]+)\s*,\s*({pattern}\([^)]*\))(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  return modified_content


def remove_specific_modifiers(
  contract_content: str, modifiers_to_remove: List[str]
) -> str:
  """
  移除合约中指定的修饰符

  Args:
    contract_content: 合约源代码字符串
    modifiers_to_remove: 要移除的修饰符名称列表

  Returns:
    移除了指定修饰符的合约代码
  """
  if not modifiers_to_remove:
    return contract_content

  modified_content = contract_content

  for modifier in modifiers_to_remove:
    # 转义可能的正则表达式特殊字符
    pattern = re.escape(modifier)

    # 场景1: function xxx() public modifierName { ... }
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern})(\s*\{{|\s+|\()",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

    # 场景2: function xxx() public modifierName(arg1, arg2) { ... } 或 modifierName(arg)
    # 修复：确保单参数和多参数修饰符都被完全移除
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern}\([^)]*\))(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

    # 场景3: 多个修饰符以逗号分隔
    # 修饰符在前面
    regex = re.compile(rf"(\s*)({pattern})\s*,\s*([^{{,]+)(\s*\{{)", re.IGNORECASE)
    modified_content = regex.sub(r"\1\3\4", modified_content)

    # 修饰符在后面
    regex = re.compile(rf"([^{{,]+)\s*,\s*({pattern})(\s*\{{)", re.IGNORECASE)
    modified_content = regex.sub(r"\1\3", modified_content)

    # 场景4: 处理returns声明之前的修饰符
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern})(\s+returns)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

    # 场景5: 处理带参数的修饰符和returns组合
    regex = re.compile(
      rf"(function\s+\w+\s*\([^)]*\)\s*(?:public|external|internal|private)?\s*)({pattern}\([^)]*\))(\s+returns)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

    # 场景6: 处理带参数的修饰符加逗号的情况，比如 modifierName(arg1, arg2), otherModifier 或 modifierName(arg), otherModifier
    regex = re.compile(
      rf"({pattern}\([^)]*\))\s*,\s*([^{{,]+)(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\2\3", modified_content)

    # 场景7: 处理两个修饰符之间的逗号，比如 otherModifier, modifierName(arg1, arg2) 或 otherModifier, modifierName(arg)
    regex = re.compile(
      rf"([^{{,]+)\s*,\s*({pattern}\([^)]*\))(\s*\{{|\s+)",
      re.IGNORECASE,
    )
    modified_content = regex.sub(r"\1\3", modified_content)

  return modified_content


def save_modified_contract(original_path: str, content: str) -> str:
  """
  保存修改后的合约到新文件

  Args:
    original_path: 原始合约文件路径
    content: 修改后的合约内容

  Returns:
    新保存的文件路径
  """
  # 获取原始文件名和目录
  file_dir = os.path.dirname(original_path)
  file_name = os.path.basename(original_path)
  deowned_dir = os.path.join(file_dir, "deowned")

  # 创建deowned目录，如果不存在
  os.makedirs(deowned_dir, exist_ok=True)

  # 新文件路径
  new_file_name = f"DeOwner_{file_name}"
  new_file_path = os.path.join(deowned_dir, new_file_name)

  # 保存新文件
  with open(new_file_path, "w", encoding="utf-8") as f:
    f.write(content)

  print(f"保存修改后的合约: {new_file_path}")
  return new_file_path


def _update_single_item(
  item: Dict[str, Any], modified_paths: Dict[str, str]
) -> Dict[str, Any]:
  """
  更新单个JSON项目中的文件路径

  Args:
    item: 原始JSON项目
    modified_paths: 映射原始路径到新路径的字典

  Returns:
    更新了路径的JSON项目
  """
  src_file_path = item.get("src_file_path")
  if src_file_path and src_file_path in modified_paths:
    # 创建新的项目对象
    new_item = item.copy()

    # 更新源文件路径
    new_item["src_file_path"] = modified_paths[src_file_path]

    # 更新command中的文件路径 - 假设文件路径是第一个参数
    if "command" in new_item and new_item["command"]:
      parts = new_item["command"].split()
      for i, part in enumerate(parts):
        # 检查参数是否是文件路径（跳过选项参数）
        if not part.startswith("-") and os.path.basename(part) == os.path.basename(
          src_file_path
        ):
          parts[i] = modified_paths[src_file_path]
          break
      new_item["command"] = " ".join(parts)

    # 更新command_state_machine中的文件路径 - 假设文件路径是第一个参数
    if "command_state_machine" in new_item and new_item["command_state_machine"]:
      parts = new_item["command_state_machine"].split()
      for i, part in enumerate(parts):
        # 检查参数是否是文件路径（跳过选项参数）
        if not part.startswith("-") and os.path.basename(part) == os.path.basename(
          src_file_path
        ):
          parts[i] = modified_paths[src_file_path]
          break
      new_item["command_state_machine"] = " ".join(parts)

    return new_item
  else:
    # 如果文件路径不在修改列表中，保留原始项
    return item


def update_json_paths(
  items: List[Dict[str, Any]], modified_paths: Dict[str, str]
) -> List[Dict[str, Any]]:
  """
  使用多线程更新JSON条目中的文件路径

  Args:
    items: 原始JSON条目列表
    modified_paths: 映射原始路径到新路径的字典

  Returns:
    更新了路径的JSON条目列表
  """
  # 设置最大线程数，可根据系统资源调整
  max_workers = min(32, os.cpu_count() or 4)  # 使用CPU核心数的倍数作为线程数
  updated_items = []

  # 如果没有需要修改的路径或者只有很少的项目，使用单线程处理
  if not modified_paths or len(items) < 10:
    return [_update_single_item(item, modified_paths) for item in items]

  # 使用线程池并行处理
  with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # 提交所有任务到线程池
    futures = {
      executor.submit(_update_single_item, item, modified_paths): i
      for i, item in enumerate(items)
    }

    # 预先分配结果列表大小
    updated_items = [None] * len(items)

    # 处理完成的任务结果
    for future in concurrent.futures.as_completed(futures):
      item_index = futures[future]
      try:
        # 获取处理结果并保持原始顺序
        updated_items[item_index] = future.result()
      except Exception as exc:
        print(f"处理项目 #{item_index} 时发生错误: {exc}")
        # 错误情况下保留原始项
        updated_items[item_index] = items[item_index]

  return updated_items


def read_contract_content(file_path: str) -> Tuple[str, bool]:
  """
  读取合约文件内容

  Args:
    file_path: 合约文件路径

  Returns:
    元组: (合约内容, 是否成功读取)
  """
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      return f.read(), True
  except Exception as e:
    print(f"读取合约文件失败: {file_path}, 错误: {e}")
    return "", False


def analyze_single_contract(
  item: Dict[str, Any],
  item_index: int,
  total_items: int,
  progress_task=None,
  progress=None,
) -> Dict[str, Any]:
  """分析单个合约的辅助函数，用于多线程处理"""
  src_file_path = item.get("src_file_path")
  contract_name = item.get("contract")
  command = item.get("command") or item.get("command_state_machine", "")

  if not src_file_path or not contract_name:
    if progress and progress_task:
      progress.update(
        progress_task,
        advance=1,
        description=f"[red]错误: 项目 #{item_index} 缺少文件路径或合约名称",
      )
    else:
      print(f"警告: 项目 #{item_index} 缺少文件路径或合约名称")
    return {"original_item": item, "analysis": {"error": "缺少文件路径或合约名称"}}

  if not os.path.exists(src_file_path):
    if progress and progress_task:
      progress.update(
        progress_task, advance=1, description=f"[red]错误: 文件 {src_file_path} 不存在"
      )
    else:
      print(f"警告: 文件 {src_file_path} 不存在")
    return {"original_item": item, "analysis": {"error": "文件不存在"}}

  # 提取solc路径
  solc_path = extract_solc_path(command)

  # 更新进度条描述
  if progress and progress_task:
    progress.update(
      progress_task,
      description=f"分析: {contract_name} ({item_index + 1}/{total_items})",
    )

  # 分析合约，传入solc路径
  analysis_result = analyze_contract_for_access_control(
    src_file_path, contract_name, solc_path
  )

  # 如果有错误，更新进度条
  if analysis_result["error"]:
    if progress and progress_task:
      progress.update(
        progress_task,
        description=f"[yellow]警告: {contract_name} - {analysis_result['error']}",
      )
    else:
      print(f"警告: 分析 {src_file_path} 时出错: {analysis_result['error']}")

  result = {"original_item": item, "analysis": analysis_result}

  # 完成任务进度
  if progress and progress_task:
    progress.update(progress_task, advance=1)

  return result


def process_contract_modification(
  contract_info: Dict[str, Any],
  analysis_result: Dict[str, Any],
  progress_task=None,
  progress=None,
  index=None,
  total=None,
) -> Tuple[str, str, str]:
  """
  处理单个合约的修改，移除访问控制修饰符

  Args:
      contract_info: 合约信息字典
      analysis_result: 合约分析结果
      progress_task: Rich进度条任务ID
      progress: Rich进度条对象
      index: 当前处理索引
      total: 总数量

  Returns:
      元组: (原始文件路径, 新文件路径, 合约名称)
  """
  src_file_path = contract_info.get("src_file_path")
  contract_name = contract_info.get("contract")

  # 更新进度条描述
  if progress and progress_task and index is not None and total is not None:
    progress.update(
      progress_task, description=f"修改: {contract_name} ({index + 1}/{total})"
    )

  # 读取合约内容
  content, read_success = read_contract_content(src_file_path)
  if not read_success:
    if progress and progress_task:
      progress.update(progress_task, description=f"[red]读取失败: {contract_name}")
      progress.update(progress_task, advance=1)
    return src_file_path, "", contract_name

  # 先移除所有通用访问控制修饰符
  modified_content = remove_access_control_modifiers(content)

  # 然后移除已识别的特定依赖状态的修饰符
  if analysis_result.get("state_dependent_modifiers"):
    if progress and progress_task:
      progress.update(progress_task, description=f"移除状态依赖修饰符: {contract_name}")
    else:
      print(
        f"移除状态依赖修饰符: {', '.join(analysis_result['state_dependent_modifiers'])}"
      )
    modified_content = remove_specific_modifiers(
      modified_content, analysis_result["state_dependent_modifiers"]
    )

  # 移除依赖区块链全局变量的修饰符
  if analysis_result.get("blockchain_dependent_modifiers"):
    if progress and progress_task:
      progress.update(
        progress_task, description=f"移除全局变量依赖修饰符: {contract_name}"
      )
    else:
      print(
        f"移除区块链全局变量依赖修饰符: {', '.join(analysis_result['blockchain_dependent_modifiers'])}"
      )
    modified_content = remove_specific_modifiers(
      modified_content, analysis_result["blockchain_dependent_modifiers"]
    )

  # 保存修改后的合约
  new_file_path = save_modified_contract(src_file_path, modified_content)

  if progress and progress_task:
    progress.update(progress_task, description=f"[green]处理完成: {contract_name}")
    progress.update(progress_task, advance=1)
  else:
    print(
      f"已处理合约: {contract_name}, 原路径: {src_file_path}, 新路径: {new_file_path}"
    )

  return src_file_path, new_file_path, contract_name


def process_contracts_in_parallel(
  contracts_to_process: List[Tuple[Dict[str, Any], Dict[str, Any]]],
) -> Dict[str, str]:
  """
  并行处理多个合约的修改

  Args:
      contracts_to_process: 需要处理的合约列表，每项包含 (合约信息, 分析结果)

  Returns:
      字典: 映射原始路径到新路径
  """
  modified_paths = {}
  max_workers = min(32, os.cpu_count() or 4)

  total_contracts = len(contracts_to_process)

  # 使用Rich创建一个美观的进度条
  console = Console()
  console.print(
    f"[bold blue]使用 {max_workers} 个线程处理 {total_contracts} 个合约修改[/]"
  )

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console,
  ) as progress:
    mod_task = progress.add_task("[cyan]修改合约...", total=total_contracts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
      # 提交所有修改任务到线程池
      futures = {
        executor.submit(
          process_contract_modification,
          contract_info,
          analysis_result,
          mod_task,
          progress,
          i,
          total_contracts,
        ): i
        for i, (contract_info, analysis_result) in enumerate(contracts_to_process)
      }

      # 处理完成的任务结果
      for future in concurrent.futures.as_completed(futures):
        try:
          src_path, new_path, contract_name = future.result()
          if new_path:  # 只有当成功处理时才添加路径映射
            modified_paths[src_path] = new_path
        except Exception as exc:
          item_index = futures[future]
          progress.update(mod_task, description=f"[red]错误: 项目 #{item_index}")

  return modified_paths


def collect_access_control_contracts(input_json_path: str, output_json_path: str):
  """从输入JSON收集具有访问控制特征的合约并输出结果"""
  try:
    # 创建控制台对象
    console = Console()

    # 读取输入JSON
    console.print("[bold blue]读取输入JSON文件...[/]")
    with open(input_json_path, "r") as f:
      items = json.load(f)

    access_control_contracts = []
    results = []
    contracts_to_modify = []  # 存储需要修改的合约信息和分析结果

    total_items = len(items)
    console.print(f"[bold green]找到 {total_items} 个合约项待分析[/]")

    # 设置最大线程数，可根据系统资源调整
    max_workers = min(32, os.cpu_count() or 4)
    console.print(f"[bold blue]使用 {max_workers} 个线程进行分析[/]")

    # 使用Rich的Progress创建漂亮的进度条
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      BarColumn(),
      TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
      TimeElapsedColumn(),
      TimeRemainingColumn(),
      console=console,
    ) as progress:
      # 添加分析任务进度条
      analysis_task = progress.add_task("[cyan]分析合约...", total=total_items)

      # 使用线程池并行分析合约
      with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有分析任务到线程池
        futures = {
          executor.submit(
            analyze_single_contract, item, i, total_items, analysis_task, progress
          ): i
          for i, item in enumerate(items)
        }

        # 处理完成的任务结果
        for future in concurrent.futures.as_completed(futures):
          item_index = futures[future]
          try:
            result = future.result()
            results.append(result)

            # 如果有访问控制特性，添加到集合中并收集待处理列表
            item = result["original_item"]
            analysis = result["analysis"]

            if (
              analysis.get("has_ownership", False)
              or analysis.get("has_state_dependent_modifiers", False)
              or analysis.get("has_blockchain_dependent_modifiers", False)
            ):
              access_control_contracts.append(item)
              contract_name = item.get("contract")

              # 在进度条下方打印发现信息
              console.print(f"[yellow]找到访问控制特征: {contract_name}[/]")

              # 保存到待处理列表
              contracts_to_modify.append((item, analysis))

          except Exception as exc:
            progress.update(
              analysis_task,
              description=f"[red]错误: 处理项目 #{item_index} 时出错: {exc}",
            )

    # 打印分析结果总结
    console.print(
      f"[bold green]分析完成! 找到 {len(access_control_contracts)} 个具有访问控制特征的合约[/]"
    )

    if contracts_to_modify:
      # 并行处理合约修改
      console.print(
        f"[bold blue]\n开始并行处理 {len(contracts_to_modify)} 个需要修改的合约...[/]"
      )
      modified_paths = process_contracts_in_parallel(contracts_to_modify)

      # 保存所有分析结果（更详细）
      console.print("[bold blue]保存分析结果...[/]")
      with open(output_json_path.replace(".json", "_full_analysis.json"), "w") as f:
        json.dump(results, f, indent=2)

      # 保存具有访问控制特征的合约列表
      with open(output_json_path, "w") as f:
        json.dump(access_control_contracts, f, indent=2)

      # 生成去除访问控制的JSON文件
      deownered_output_path = output_json_path.replace(".json", "_deaccesscontrol.json")
      console.print("[bold blue]更新JSON路径...[/]")
      updated_items = update_json_paths(items, modified_paths)
      with open(deownered_output_path, "w") as f:
        json.dump(updated_items, f, indent=2)

      console.print(f"[bold green]\n处理完成! 共处理了 {len(modified_paths)} 个合约[/]")
      console.print(f"[green]结果已保存至: {output_json_path}[/]")
      console.print(
        f"[green]详细分析结果已保存至: {output_json_path.replace('.json', '_full_analysis.json')}[/]"
      )
      console.print(
        f"[green]去除访问控制的JSON文件已保存至: {deownered_output_path}[/]"
      )
    else:
      console.print("[bold yellow]没有找到需要修改的合约。[/]")

  except Exception as e:
    Console().print(f"[bold red]错误: {e}[/]")
    sys.exit(1)


def main():
  # 参数解析
  parser = argparse.ArgumentParser(
    description="收集具有访问控制特征的合约，并去除访问控制修饰符"
  )
  parser.add_argument("--input", "-i", required=True, help="输入JSON文件路径")
  parser.add_argument("--output", "-o", required=True, help="输出JSON文件路径")

  args = parser.parse_args()

  # 执行收集
  collect_access_control_contracts(args.input, args.output)


if __name__ == "__main__":
  main()
