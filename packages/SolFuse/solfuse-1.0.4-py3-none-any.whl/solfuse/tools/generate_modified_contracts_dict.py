#!/usr/bin/env python3

import json
import os
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# 尝试导入原始合约字典
try:
  from .cgt_id_and_contract_dict import id_and_contract as original_dict
except ImportError:
  original_dict = {}

try:
  from .state_machine_id_and_contract_dict import (
    state_machine_id_and_contract as state_dict,
  )
except ImportError:
  state_dict = {}


def generate_modified_contracts_dict(
  report_file: str, use_state_machine: bool = False
) -> Dict[str, str]:
  """
  基于移除约束报告，生成修改后的合约字典

  参数:
      report_file: 包含移除约束报告的JSON文件路径
      use_state_machine: 是否使用state_machine_id_and_contract字典

  返回:
      包含修改后文件名和原合约名的映射字典
  """
  # 加载完整字典
  full_dict = {}
  full_dict.update(original_dict)

  if use_state_machine:
    full_dict.update(state_dict)

  # 读取移除约束报告
  if not os.path.exists(report_file):
    print(f"错误: 找不到报告文件 {report_file}")
    return {}

  with open(report_file, "r", encoding="utf-8") as f:
    try:
      report_data = json.load(f)
    except json.JSONDecodeError:
      print(f"错误: 无法解析JSON文件 {report_file}")
      return {}

  # 创建修改后的字典
  modified_dict = original_dict

  for entry in report_data:
    # 检查是否成功且移除了约束
    if (
      entry.get("success", False)
      and entry.get("removed_constraints", 0) > 0
      and "output_file" in entry
      and "file_path" in entry
      and "contract_name" in entry
    ):
      # 获取原始文件路径和输出文件路径
      original_file = entry["file_path"]
      output_file = entry["output_file"]
      contract_name = entry["contract_name"]

      # 提取修改后的文件名（不含路径）
      original_file_path = Path(original_file)
      output_file_path = Path(output_file)

      # 获取新文件的stem（文件名不含扩展名）
      new_file_stem = output_file_path.stem

      # 将修改后的文件stem和合约名加入新字典
      modified_dict[new_file_stem] = contract_name
      modified_dict.pop(original_file_path.stem)

  return modified_dict


def main():
  parser = argparse.ArgumentParser(description="生成修改后的合约映射字典")
  parser.add_argument("report_file", help="移除约束报告的JSON文件路径")
  parser.add_argument(
    "--output",
    "-o",
    default="modified_contracts_dict.py",
    help="输出Python文件路径 (默认: modified_contracts_dict.py)",
  )
  parser.add_argument(
    "--use_state_machine",
    action="store_true",
    help="是否包含state_machine_id_and_contract字典",
  )

  args = parser.parse_args()

  # 生成修改后的字典
  modified_dict = generate_modified_contracts_dict(
    args.report_file, use_state_machine=args.use_state_machine
  )

  if not modified_dict:
    print("未找到符合条件的修改后合约")
    return

  # 保存到Python文件
  with open(args.output, "w", encoding="utf-8") as f:
    f.write("# 此文件由generate_modified_contracts_dict.py自动生成\n\n")
    f.write("modified_contracts_dict = {\n")

    # 按键排序并写入
    for key in sorted(modified_dict.keys()):
      f.write(f'    "{key}": "{modified_dict[key]}",\n')

    f.write("}\n")

  print(f"修改后的合约字典已生成，包含 {len(modified_dict)} 个合约")
  print(f"已保存至: {args.output}")


if __name__ == "__main__":
  main()
