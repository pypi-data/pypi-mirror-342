#!/usr/bin/env python3

import argparse
import os
import sys
from typing import List, Dict, Set, Tuple
import re

from slither import Slither
from slither.core.cfg.node import Node
from slither.core.expressions.call_expression import CallExpression
from slither.core.solidity_types import ElementaryType
from slither.slithir.variables.state_variable import StateVariable
from slither.core.declarations.solidity_variables import (
  SolidityVariableComposed,
  SolidityFunction,
)

# 设置 tree-sitter
try:
  from tree_sitter import Language, Parser
except ImportError:
  print("请安装 tree-sitter: pip install tree-sitter")
  sys.exit(1)


def is_global_var_constraint(node: Node) -> bool:
  """
  检查节点是否包含全局区块链变量约束
  """
  if not node.contains_require_or_assert():
    return False

  # 获取 require 语句
  expression = node.expression
  if isinstance(expression, CallExpression) and (
    "require" in str(expression.called) or "assert" in str(expression.called)
  ):
    # 检查所有参数
    for arg in expression.arguments:
      arg_str = str(arg)

      # 使用 Slither 的全局变量检查
      # 检查是否包含任何 SolidityVariableComposed 类型的变量
      # for var in arg:
      if isinstance(arg, SolidityVariableComposed):
        # msg.sender, block.timestamp 等全局变量
        return True
      elif isinstance(arg, SolidityFunction):
        # gasleft() 等全局函数
        return True

      # 检查字符串表示中常见的全局变量模式作为额外保障
      for pattern in ["msg.", "block.", "tx.", "gasleft"]:
        if pattern in arg_str:
          return True

  return False


def find_require_constraints(slither: Slither) -> List[Dict]:
  """
  找到所有包含全局变量约束的 require 语句
  """
  require_nodes = []

  for contract in slither.contracts:
    for function in contract.functions + contract.modifiers:
      for node in function.nodes:
        if is_global_var_constraint(node):
          require_nodes.append(
            {
              "contract": contract.name,
              "function": function.name,
              "node": node,
              "line": node.source_mapping.lines[0],
              "expression": str(node.expression),
            }
          )

  return require_nodes


def setup_tree_sitter():
  """
  设置 tree-sitter Solidity 解析器
  """
  # 注意：需要提前构建 tree-sitter-solidity 语言库
  LANGUAGE_PATH = os.path.expanduser("~/.tree-sitter-langs/solidity.so")

  if not os.path.exists(LANGUAGE_PATH):
    print(f"未找到 tree-sitter Solidity 语言库: {LANGUAGE_PATH}")
    print(
      "请安装 tree-sitter-solidity: https://github.com/JoranHonig/tree-sitter-solidity"
    )
    sys.exit(1)

  SOL_LANGUAGE = Language(LANGUAGE_PATH, "solidity")
  parser = Parser()
  parser.set_language(SOL_LANGUAGE)

  return parser


def remove_require_statements(file_path: str, require_nodes: List[Dict]) -> str:
  """
  使用 tree-sitter 移除指定的 require 语句
  """
  with open(file_path, "r", encoding="utf-8") as f:
    source_code = f.read()

  # 按行号排序（倒序，从后往前删除，避免行号变化）
  require_nodes.sort(key=lambda x: x["line"], reverse=True)

  # 将源代码拆分为行
  lines = source_code.split("\n")

  for req in require_nodes:
    line_idx = req["line"] - 1
    line = lines[line_idx]

    # 确定要删除的完整语句（包括跨越多行的情况）
    stmt_start = line_idx
    stmt_end = line_idx

    # 向上查找语句开始
    open_braces = line.count("{")
    close_braces = line.count("}")
    if "require(" in line and ";" in line:
      # 单行 require 语句
      lines[line_idx] = re.sub(r"require\([^;]+;", "", lines[line_idx])
    else:
      # 多行 require 语句，需要查找完整语句
      # 先检查语句是否已开始
      if "require(" in line:
        # 记录行号并向下查找分号
        current = line_idx
        while current < len(lines) and ";" not in lines[current]:
          current += 1

        if current < len(lines):
          # 找到分号，删除从 require 到分号的整个语句
          for i in range(line_idx, current + 1):
            lines[i] = ""

  # 合并代码并移除空行
  modified_code = "\n".join(filter(lambda l: l.strip() or l.isspace(), lines))
  return modified_code


def main():
  parser = argparse.ArgumentParser(description="移除 Solidity 代码中包含全局变量的约束")
  parser.add_argument("solidity_file", help="Solidity 源代码文件路径")
  parser.add_argument("--solc", default="solc", help="solc 可执行文件路径 (默认: solc)")
  parser.add_argument(
    "--output", "-o", help="输出文件路径 (默认: 原文件名_no_constraints.sol)"
  )

  args = parser.parse_args()

  solidity_file = args.solidity_file
  solc_path = args.solc

  if not os.path.isfile(solidity_file):
    print(f"错误：找不到 Solidity 文件: {solidity_file}")
    sys.exit(1)

  try:
    print(f"使用 Slither 分析文件: {solidity_file}")
    slither = Slither(solidity_file, solc=solc_path)

    # 找到所有全局变量约束
    require_nodes = find_require_constraints(slither)

    if not require_nodes:
      print("未发现包含全局变量约束的 require 语句")
      sys.exit(0)

    print(f"发现 {len(require_nodes)} 处全局变量约束:")
    for i, req in enumerate(require_nodes, 1):
      print(
        f"{i}. 合约 {req['contract']} 中的函数 {req['function']} 第 {req['line']} 行: {req['expression']}"
      )

    # 移除 require 语句
    modified_code = remove_require_statements(solidity_file, require_nodes)

    # 保存修改后的代码
    if args.output:
      output_file = args.output
    else:
      base, ext = os.path.splitext(solidity_file)
      output_file = f"{base}_no_constraints{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
      f.write(modified_code)

    print(f"已成功移除约束并保存到: {output_file}")

  except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


if __name__ == "__main__":
  main()
