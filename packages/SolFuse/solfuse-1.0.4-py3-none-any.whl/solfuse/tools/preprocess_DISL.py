from datasets import load_dataset
from rich.console import Console
from rich.panel import Panel
import argparse
import os
import json
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, TaskID
from typing import Dict, List, Optional, Tuple
import time
import tempfile
from pathlib import Path


def parse_thing_version(thing):
  """从合约提取的metadata中获取编译器版本"""
  raw_version = thing["compiler_version"]
  start = raw_version.find("v") + 1

  def eat_digit(i):
    while i < len(raw_version) and raw_version[i].isdigit():
      i += 1
    return i

  num_cnt = 3
  end = start
  while num_cnt > 0:
    end = eat_digit(end)
    num_cnt -= 1
    if num_cnt > 0:
      end += 1
  return raw_version[start:end]


def split_version(version):
  """将版本号拆分为元组以便比较"""
  return tuple(map(int, version.split(".")))


def get_compiler_path(version: str) -> Optional[str]:
  """使用solcix安装并获取编译器路径"""
  try:
    # 安装 solc
    import solcix

    # 确保安装对应版本的编译器
    solcix.install_solc(version, verbose=False)

    # 获取编译器路径
    solc_path = Path(solcix.installer.get_executable(version=version))
    if solc_path is None or not os.path.exists(solc_path):
      return None

    return solc_path.as_posix()
  except Exception as e:
    print(f"获取编译器路径失败: {str(e)}")
    return None


def process_contract_with_version(args, contract_info):
  """处理合约并安装编译器，返回处理结果"""
  try:
    contract_address = contract_info["address"]
    version = contract_info["version"]
    contract_name = contract_info["contract_name"]

    # 获取编译器路径
    compiler_path = get_compiler_path(version)
    if not compiler_path:
      return {
        "status": "failed",
        "address": contract_address,
        "reason": f"无法获取编译器路径: {version}",
      }

    # 获取合约名称
    # contract_name_match = re.search(r"contract\s+(\w+)", source_code)
    # contract_name = contract_name_match.group(1) if contract_name_match else "Unknown"

    return {
      "status": "success",
      "address": contract_address,
      "file_path": os.path.join(
        args.output_dir, "source_code", f"{contract_address}.sol"
      ),
      "contract_name": contract_name,
      "compiler_version": version,
      "compiler_path": compiler_path,
    }
  except Exception as e:
    return {
      "status": "failed",
      "address": contract_address if "contract_address" in locals() else "unknown",
      "reason": str(e),
    }


def main():
  console = Console()

  # 添加命令行参数
  parser = argparse.ArgumentParser(description="过滤 DISL 数据集中符合特定条件的合约")
  parser.add_argument("--workers", type=int, default=4, help="并行工作线程数量")
  parser.add_argument(
    "--max_contracts", type=int, default=1000000, help="要处理的最大合约数量"
  )
  parser.add_argument(
    "--output", type=str, default="positive_files.json", help="输出JSON文件路径"
  )
  parser.add_argument(
    "--dataset_path",
    type=str,
    default="/home/hengdiye/datasets/DISL/data/decomposed",
    help="DISL 数据集路径",
  )
  parser.add_argument(
    "--output_dir",
    type=str,
    default="/home/hengdiye/datasets/DISL/extracted_contracts",
    help="提取合约的输出目录",
  )
  parser.add_argument(
    "--min_version",
    type=str,
    default="0.4.25",
    help="最低支持的编译器版本",
  )
  args = parser.parse_args()

  # 显示任务概述
  console.print(
    Panel.fit(
      "[bold green]DISL 合约过滤工具[/bold green]\n"
      f"将处理最多 [bold]{args.max_contracts}[/bold] 个合约\n"
      f"使用 [bold]{args.workers}[/bold] 个并行工作线程\n"
      f"结果将保存到 [bold]{args.output}[/bold]\n"
      f"提取的合约将保存到 [bold]{args.output_dir}[/bold]\n"
      f"最低支持的编译器版本: [bold]{args.min_version}[/bold]"
    )
  )

  # 加载数据集
  console.print("[bold blue]正在加载数据集...[/bold blue]")
  dataset = load_dataset(args.dataset_path)
  total_contracts = len(dataset["train"])
  console.print(f"数据集共包含 [bold]{total_contracts}[/bold] 个合约")

  # 确保输出目录和source_code目录存在
  os.makedirs(args.output_dir, exist_ok=True)
  source_code_dir = os.path.join(args.output_dir, "source_code")
  os.makedirs(source_code_dir, exist_ok=True)

  # 限制处理的最大合约数
  contracts_to_process = min(args.max_contracts, total_contracts)
  console.print(f"将处理前 [bold]{contracts_to_process}[/bold] 个合约")

  # 统计信息
  processed_contracts = 0
  saved_files = 0
  skipped_contracts = 0
  min_version_tuple = split_version(args.min_version)

  # 用于跟踪已处理的合约地址
  processed_addresses = set()

  # 预处理：从数据集中提取符合条件的合约
  console.print("[bold blue]正在筛选符合版本要求的合约...[/bold blue]")
  filtered_contracts = []
  version_mismatch = 0

  with Progress() as progress:
    filter_task = progress.add_task("[cyan]筛选合约...", total=contracts_to_process)

    for i, item in enumerate(dataset["train"]):
      if i >= contracts_to_process:
        break

      try:
        contract_address = item["contract_address"]

        # 检查是否已处理过此地址
        if contract_address in processed_addresses:
          processed_contracts += 1
          skipped_contracts += 1
          progress.update(filter_task, advance=1)
          continue

        # 解析版本并检查是否满足最低版本要求
        try:
          version = parse_thing_version(item)
          if split_version(version) < min_version_tuple:
            version_mismatch += 1
            progress.update(filter_task, advance=1)
            continue
        except Exception:
          version_mismatch += 1
          progress.update(filter_task, advance=1)
          continue

        processed_addresses.add(contract_address)

        # 同时保存到按地址组织的文件夹和统一的source_code文件夹
        try:
          # 创建地址对应的目录
          contract_dir = os.path.join(args.output_dir, contract_address)
          if os.path.exists(contract_dir):
            shutil.rmtree(contract_dir)
          os.makedirs(contract_dir)

          # 获取文件名和源码
          file_name = os.path.basename(item["file_path"])
          source_code = item["source_code"]

          # 保存到地址目录
          contract_file_path = os.path.join(contract_dir, file_name)
          with open(contract_file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

          # 保存到source_code目录（以地址命名）
          source_code_file_path = os.path.join(
            source_code_dir, f"{contract_address}.sol"
          )
          with open(source_code_file_path, "w", encoding="utf-8") as f:
            f.write(source_code)

          # 添加到待处理列表
          filtered_contracts.append(
            {
              "address": contract_address,
              "version": version,
              "source_code": source_code,
              "file_path": file_name,
              "contract_name": Path(item["file_path"]).stem,
            }
          )

          saved_files += 1
        except Exception as e:
          console.print(
            f"[bold red]保存文件失败 {contract_address}: {str(e)}[/bold red]"
          )

        processed_contracts += 1
        progress.update(filter_task, advance=1)
      except Exception as e:
        console.print(f"[bold red]处理合约失败 {i}: {str(e)}[/bold red]")
        continue

  console.print(f"共筛选出 [bold]{len(filtered_contracts)}[/bold] 个符合版本要求的合约")
  console.print(f"版本不符合要求的合约: [bold]{version_mismatch}[/bold]")

  # 多线程处理编译器安装和路径获取
  console.print("[bold blue]正在并行安装编译器...[/bold blue]")

  compiler_results = []

  with Progress() as progress:
    compiler_task = progress.add_task(
      "[cyan]安装编译器...", total=len(filtered_contracts)
    )

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
      # 提交处理任务
      futures = {
        executor.submit(process_contract_with_version, args, contract): contract
        for contract in filtered_contracts
      }

      # 收集结果
      for future in as_completed(futures):
        result = future.result()
        compiler_results.append(result)
        progress.update(compiler_task, advance=1)

  # 统计编译器处理结果
  successful_contracts = [r for r in compiler_results if r["status"] == "success"]
  failed_contracts = [r for r in compiler_results if r["status"] == "failed"]

  console.print(f"编译器成功安装: [bold green]{len(successful_contracts)}[/bold green]")
  console.print(f"编译器安装失败: [bold red]{len(failed_contracts)}[/bold red]")

  # 保存处理结果到JSON
  with open(args.output, "w", encoding="utf-8") as f:
    result_data = {
      "total_processed": processed_contracts,
      "total_saved": saved_files,
      "unique_addresses": len(processed_addresses),
      "skipped_duplicates": skipped_contracts,
      "version_mismatch": version_mismatch,
      "compiler_success": len(successful_contracts),
      "compiler_failed": len(failed_contracts),
      "contracts": successful_contracts,
    }

    json.dump(result_data, f, indent=2)

  # 显示完成信息
  completion_message = (
    "[bold green]完成![/bold green]\n"
    f"共处理 [bold]{processed_contracts}[/bold] 个合约\n"
    f"唯一合约地址数: [bold]{len(processed_addresses)}[/bold]\n"
    f"跳过的重复地址: [bold]{skipped_contracts}[/bold]\n"
    f"版本不符要求的: [bold]{version_mismatch}[/bold]\n"
    f"成功保存的文件: [bold]{saved_files}[/bold]\n"
    f"有效编译器路径: [bold]{len(successful_contracts)}[/bold]\n"
    f"编译器安装失败: [bold]{len(failed_contracts)}[/bold]\n"
    f"结果已保存到 [bold]{args.output}[/bold]\n"
    f"合约文件已保存到 [bold]{args.output_dir}[/bold]"
  )

  console.print(Panel.fit(completion_message))


if __name__ == "__main__":
  main()
