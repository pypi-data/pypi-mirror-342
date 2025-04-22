#!/usr/bin/env python3

import argparse
import os
import sys
import time
import multiprocessing
from pathlib import Path
import json
from typing import List, Dict, Tuple, Optional
from rich.progress import (
  Progress,
  SpinnerColumn,
  TextColumn,
  MofNCompleteColumn,
  TimeElapsedColumn,
  BarColumn,
)

import solcix
import solfuse.solfuse_ir.utils

from .remove_solidity_constraints import (
  find_require_constraints,
  remove_require_statements,
)
from slither import Slither

# 导入可能的映射字典
try:
  from .cgt_id_and_contract_dict import id_and_contract as cgt_dict
except ImportError:
  cgt_dict = {}

try:
  from .state_machine_id_and_contract_dict import (
    state_machine_id_and_contract as state_dict,
  )
except ImportError:
  state_dict = {}


def discover_compiler(args: Tuple[Path, Dict, bool]) -> Dict:
  """
  为单个文件发现适合的编译器版本

  参数:
      args: 包含 (file, id_and_contract, quiet) 的元组

  返回:
      包含文件路径、合约名称、编译器路径等信息的字典
  """
  file, id_and_contract, quiet = args

  result = {
    "file": file,
    "success": False,
    "contract_name": id_and_contract.get(file.stem),
    "error": None,
  }

  try:
    # 确定编译器版本
    version = solfuse.solfuse_ir.utils.ensure_version(file=file)
    if version is None:
      result["error"] = "无法确定编译器版本"
      return result

    # 获取编译器路径
    solc_path = solcix.installer.get_executable(version=version)
    result["solc_path"] = solc_path
    result["success"] = True

  except Exception as e:
    result["error"] = str(e)

  return result


def process_file(args: Tuple[str, str, str, bool]) -> Dict:
  """
  处理单个Solidity文件，移除全局变量约束

  参数:
      args: 包含 (file_path, contract_name, solc_path, quiet) 的元组

  返回:
      包含处理结果信息的字典
  """
  file_path, contract_name, solc_path, quiet = args

  result = {
    "file_path": str(file_path),
    "contract_name": contract_name,
    "solc_path": solc_path,
    "success": False,
    "removed_constraints": 0,
    "error": None,
  }

  try:
    if not quiet:
      print(f"处理文件: {file_path}")

    # 使用Slither分析文件
    slither = Slither(file_path, solc=solc_path)

    # 找到所有全局变量约束
    require_nodes = find_require_constraints(slither)
    result["removed_constraints"] = len(require_nodes)

    if not require_nodes:
      if not quiet:
        print(f"文件 {file_path} 未发现全局变量约束")
      result["success"] = True
      return result

    # 移除require语句
    modified_code = remove_require_statements(file_path, require_nodes)

    # 保存修改后的代码
    base, ext = os.path.splitext(file_path)
    output_file = f"{base}_no_constraints{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
      f.write(modified_code)

    result["output_file"] = output_file
    result["success"] = True

  except Exception as e:
    result["error"] = str(e)
    if not quiet:
      print(f"处理 {file_path} 时出错: {e}")

  return result


def batch_process_files(
  dir_path: str,
  output_dir: str = None,
  max_workers: int = None,
  quiet: bool = False,
  use_state_machine: bool = False,
) -> List[Dict]:
  """
  批量处理目录中的所有Solidity文件，移除全局变量约束
  """
  if max_workers is None:
    max_workers = multiprocessing.cpu_count()

  # 合并合约字典
  id_and_contract = {}
  id_and_contract.update(cgt_dict)

  if use_state_machine:
    id_and_contract.update(state_dict)

  # 创建输出目录
  if output_dir:
    os.makedirs(output_dir, exist_ok=True)

  # 查找所有适合处理的Solidity文件
  all_files = []
  dir_path_obj = Path(dir_path)

  # 查找sol文件
  for file in dir_path_obj.glob("*.sol"):
    # 确保文件是实际文件而不是符号链接
    file_path = file.resolve()
    if file_path.is_file() and file.stem in id_and_contract:
      all_files.append(file_path)

  if not all_files:
    print(f"目录 {dir_path} 中没有找到匹配的Solidity文件")
    return []

  print(f"找到 {len(all_files)} 个Solidity文件")

  # 使用多线程查找编译器版本
  compiler_discovery_args = [(file, id_and_contract, quiet) for file in all_files]
  discover_results = []

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
  ) as progress:
    compiler_task = progress.add_task(
      "[blue]检测编译器版本...", total=len(compiler_discovery_args)
    )

    # 使用多线程查找编译器
    with multiprocessing.Pool(processes=max_workers) as pool:
      for result in pool.imap_unordered(discover_compiler, compiler_discovery_args):
        progress.update(compiler_task, advance=1)
        discover_results.append(result)

  # 筛选成功找到编译器的文件
  successful_discoveries = [r for r in discover_results if r["success"]]
  failed_discoveries = [r for r in discover_results if not r["success"]]

  print(f"\n编译器检测完成: {len(successful_discoveries)}/{len(all_files)} 个文件成功")
  if failed_discoveries:
    print(f"无法确定编译器版本的文件: {len(failed_discoveries)} 个")
    if not quiet:
      for fail in failed_discoveries[:5]:  # 只显示前5个
        print(f"  - {fail['file'].name}: {fail['error']}")
      if len(failed_discoveries) > 5:
        print(f"  ... 以及其他 {len(failed_discoveries) - 5} 个文件")

  # 准备处理参数
  process_args = [
    (d["file"].as_posix(), d["contract_name"], d["solc_path"].as_posix(), quiet)
    for d in successful_discoveries
  ]

  results = []
  success_count = 0
  fail_count = 0

  # 使用进度条显示处理情况
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
  ) as progress:
    process_task = progress.add_task("[yellow]处理文件...", total=len(process_args))
    success_task = progress.add_task("[green]成功处理", total=len(process_args))
    fail_task = progress.add_task("[red]处理失败", total=len(process_args))

    # 创建进程池并处理文件
    with multiprocessing.Pool(processes=max_workers) as pool:
      for result in pool.imap_unordered(process_file, process_args):
        progress.update(process_task, advance=1)

        if result["success"]:
          success_count += 1
          progress.update(success_task, advance=1)
        else:
          fail_count += 1
          progress.update(fail_task, advance=1)

        results.append(result)

  # 输出统计信息
  total_removed = sum(r.get("removed_constraints", 0) for r in results)

  print(
    f"\n处理完成: {success_count}/{len(results)} 个文件成功处理, {fail_count} 个失败"
  )
  print(f"共移除 {total_removed} 个全局变量约束")

  # 找出成功移除约束的文件数量
  files_with_constraints = sum(
    1 for r in results if r.get("removed_constraints", 0) > 0
  )
  print(f"有 {files_with_constraints} 个文件包含全局变量约束并被成功修改")

  # 如果指定了输出目录，保存结果报告
  if output_dir:
    report_path = os.path.join(output_dir, "constraints_removal_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
      json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"详细报告已保存至: {report_path}")

  return results


def main():
  parser = argparse.ArgumentParser(description="批量移除Solidity代码中的全局变量约束")
  parser.add_argument("dir", help="包含Solidity文件的目录")
  parser.add_argument("--output_dir", "-o", help="输出目录，用于保存报告和日志")
  parser.add_argument(
    "--max_workers",
    "-w",
    type=int,
    default=None,
    help="最大工作进程数，默认使用CPU核心数",
  )
  parser.add_argument("--quiet", "-q", action="store_true", help="静默模式，减少输出")
  parser.add_argument(
    "--no_state_machine",
    action="store_true",
    help="不使用state_machine_id_and_contract字典",
  )

  args = parser.parse_args()

  start_time = time.time()

  batch_process_files(
    dir_path=args.dir,
    output_dir=args.output_dir,
    max_workers=args.max_workers,
    quiet=args.quiet,
    use_state_machine=not args.no_state_machine,
  )

  elapsed_time = time.time() - start_time
  print(f"总运行时间: {elapsed_time:.2f} 秒")


if __name__ == "__main__":
  main()
