from datasets import load_dataset
from slither import Slither
from solfuse.solfuse_ir.utils import ensure_version
import tempfile
from pathlib import Path
import json
import argparse
import concurrent.futures
from rich.progress import (
  Progress,
  TextColumn,
  BarColumn,
  TaskProgressColumn,
  TimeRemainingColumn,
)
from rich.console import Console
from rich.panel import Panel
import random
from functools import partial
import sys
from solfuse.custom_detectors import (
  state_machine_modifiers_detector,
  looser_state_machine_detector,
)


def normalize_source_code(source_code):
  return source_code.encode("utf-8").decode("unicode_escape")


def parse_thing_version(thing):
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
  return tuple(map(int, version.split(".")))


def process_item(thing, min_version=(0, 4, 25)):
  """处理单个合约，如果满足条件则返回规范化的源代码，否则返回 None"""
  try:
    # 解析版本
    thing_version = parse_thing_version(thing)
    if split_version(thing_version) < min_version:
      return None
    # 写入临时文件
    with tempfile.NamedTemporaryFile(suffix=".sol", mode="w", encoding="utf-8") as f:
      f.write(thing["source_code"])
      f.seek(0)

      # 安装 solc
      import solcix

      solcix.install_solc(thing_version, verbose=False)
      solc_path = Path(solcix.installer.get_executable(version=thing_version))
      if solc_path is None:
        return None

      # 使用 Slither 分析
      s1 = Slither(f.name, solc=solc_path.as_posix())
      s2 = Slither(f.name, solc=solc_path.as_posix())

      # 使用探测器检测
      detects = (
        state_machine_modifiers_detector.GeneralizedStateMachineWithModifiersDetector(
          s1
        ),
        looser_state_machine_detector.LooseStateMachineDetector(s2),
      )
      if any(list(map(lambda d: d._detect(), detects))):
        return thing
  except Exception as e:
    # 将详细错误输出到日志，但不中断处理
    with open("errors.log", "w") as log:
      log.write(f"处理合约时出错: {str(e)}\n")

  return None


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
  args = parser.parse_args()

  # 显示任务概述
  console.print(
    Panel.fit(
      "[bold green]DISL 合约过滤工具[/bold green]\n"
      f"将处理最多 [bold]{args.max_contracts}[/bold] 个合约\n"
      f"使用 [bold]{args.workers}[/bold] 个并行工作线程\n"
      f"结果将保存到 [bold]{args.output}[/bold]"
    )
  )

  # 加载数据集
  console.print("[bold blue]正在加载数据集...[/bold blue]")
  dataset = load_dataset(args.dataset_path)
  total_contracts = len(dataset["train"])
  console.print(f"数据集共包含 [bold]{total_contracts}[/bold] 个合约")

  # 预处理：过滤掉版本低的合约
  valid_contracts = []
  with Progress(
    TextColumn("[bold blue]{task.description}[/bold blue]"),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn(),
  ) as progress:
    task = progress.add_task(
      "[cyan]预处理合约...", total=min(total_contracts, args.max_contracts * 3)
    )

    for cnt, thing in enumerate(dataset["train"]):
      progress.update(task, advance=1)
      if cnt >= args.max_contracts * 3:
        break

      try:
        thing_version = parse_thing_version(thing)
        if split_version(thing_version) >= (0, 4, 25):
          valid_contracts.append(thing)
          if len(valid_contracts) >= args.max_contracts:
            break
      except Exception:
        continue

  console.print(
    f"预处理完成，找到 [bold green]{len(valid_contracts)}[/bold green] 个版本符合要求的合约"
  )

  # 使用线程池并行处理
  positive_files = []
  with Progress(
    TextColumn("[bold green]{task.description}[/bold green]"),
    BarColumn(complete_style="green"),
    TaskProgressColumn(),
    TimeRemainingColumn(),
  ) as progress:
    task = progress.add_task("[yellow]分析合约...", total=len(valid_contracts))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
      futures = []

      # 提交所有任务
      for item in valid_contracts:
        futures.append(executor.submit(process_item, item))

      # 收集结果
      for future in concurrent.futures.as_completed(futures):
        progress.update(task, advance=1)
        try:
          result = future.result()
          if result:
            positive_files.append(result)
            console.print(
              f"[green]找到符合条件的合约，当前共 {len(positive_files)} 个[/green]"
            )
        except Exception as e:
          console.print(f"[bold red]处理失败: {str(e)}[/bold red]")

  # 显示结果统计
  console.print(f"\n[bold]分析完成！[/bold]")
  console.print(f"共处理了 [bold]{len(valid_contracts)}[/bold] 个合约")
  console.print(f"找到 [bold green]{len(positive_files)}[/bold green] 个符合条件的合约")

  # 将结果写入 JSON 文件
  with open(args.output, "w") as f:
    json.dump(positive_files, f, indent=2, ensure_ascii=False)
  console.print(f"[bold green]结果已保存到 {args.output}[/bold green]")


if __name__ == "__main__":
  main()
