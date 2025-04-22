from tempfile import TemporaryDirectory
from .common import ECHIDNA
import json
import subprocess
import os
import re
import concurrent.futures
from time import time
import signal
import sys
import argparse
import random
import math
from rich.progress import (
  Progress,
  TextColumn,
  BarColumn,
  TaskProgressColumn,
  TimeRemainingColumn,
)
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.ticker import PercentFormatter
import os
from datetime import datetime


def extract_seed_from_command(cmd):
  """从命令中提取随机数种子"""
  seed_match = re.search(r"--seed\s+(\d+)", cmd)
  if seed_match:
    return int(seed_match.group(1))
  return None


def add_seed_to_command(cmd, seed):
  """向命令添加随机数种子"""
  # 如果命令已经有种子参数，替换它
  if "--seed" in cmd:
    return re.sub(r"--seed\s+\d+", f"--seed {seed}", cmd)
  # 否则添加种子参数
  else:
    return f"{cmd} --seed {seed}"


def limit_commands(commands, limit, global_seed=None):
  """
  限制要执行的命令数量

  Args:
      commands: 命令列表
      limit: 限制数量，可以是整数或百分比字符串
      global_seed: 全局种子

  Returns:
      采样后的命令列表
  """
  if not limit or limit <= 0:
    return commands

  # 设置随机数生成器，如果全局种子指定则使用它
  if global_seed is not None:
    random.seed(global_seed)

  total_commands = len(commands)

  # 如果limit是百分比字符串（如"10%"）
  if isinstance(limit, str) and limit.endswith("%"):
    try:
      percentage = float(limit.rstrip("%"))
      limit = int(math.ceil(total_commands * percentage / 100))
    except ValueError:
      return commands

  # 确保limit不超过命令总数
  limit = min(limit, total_commands)

  # 随机采样命令
  return random.sample(commands, limit)


def prepare_commands_with_seeds(commands, global_seed=None, limit=None):
  """
  准备带有种子的命令对，并支持限制命令数量

  Args:
      commands: 原始命令数据列表
      global_seed: 全局种子值（如果指定）
      limit: 限制执行的命令数量

  Returns:
      normal_cmds: 带有种子的普通命令列表
      sm_cmds: 带有种子的state machine命令列表
      cmd_pairs: 普通命令和state machine命令的配对关系
      cmd_seeds: 命令对应的种子
  """
  # 设置随机数生成器，如果全局种子指定则使用它
  if global_seed is not None:
    random.seed(global_seed)

  # 如果需要限制命令数量，先采样原始命令列表
  if limit:
    # 处理百分比限制
    if isinstance(limit, str) and limit.endswith("%"):
      try:
        percentage = float(limit.rstrip("%"))
        limit_count = int(math.ceil(len(commands) * percentage / 100))
      except ValueError:
        limit_count = len(commands)
    else:
      # 处理数字限制
      limit_count = min(int(limit), len(commands))

    # 随机采样命令
    commands = random.sample(commands, limit_count)

  normal_cmds = []
  sm_cmds = []
  cmd_pairs = {}  # 用于存储命令之间的对应关系
  cmd_seeds = {}  # 存储每个命令使用的种子

  def transform_command(x, g):
    # return x.get(g) + " --timeout=30"
    return x.get(g) + " --disable-slither --timeout=30"

  for item in commands:
    normal_cmd = transform_command(item, "command")
    sm_cmd = transform_command(item, "command_state_machine")

    if normal_cmd and sm_cmd:
      # 尝试从命令中提取种子
      normal_seed = extract_seed_from_command(normal_cmd)
      sm_seed = extract_seed_from_command(sm_cmd)

      # 决定使用哪个种子
      seed_to_use = None
      if normal_seed is not None:
        seed_to_use = normal_seed
      elif sm_seed is not None:
        seed_to_use = sm_seed
      else:
        # 如果都没有种子，生成一个新的
        seed_to_use = random.randint(1, 1000000000)

      # 更新命令添加相同的种子
      normal_cmd = add_seed_to_command(normal_cmd, seed_to_use)
      sm_cmd = add_seed_to_command(sm_cmd, seed_to_use)

      # 存储命令和种子信息
      normal_cmds.append(normal_cmd)
      sm_cmds.append(sm_cmd)
      cmd_pairs[normal_cmd] = sm_cmd
      cmd_pairs[sm_cmd] = normal_cmd
      cmd_seeds[normal_cmd] = seed_to_use
      cmd_seeds[sm_cmd] = seed_to_use

    elif normal_cmd:
      # 如果只有普通命令，也确保它有种子
      normal_seed = extract_seed_from_command(normal_cmd)
      if normal_seed is None:
        seed_to_use = random.randint(1, 1000000000)
        normal_cmd = add_seed_to_command(normal_cmd, seed_to_use)
      else:
        seed_to_use = normal_seed

      normal_cmds.append(normal_cmd)
      cmd_seeds[normal_cmd] = seed_to_use

    elif sm_cmd:
      # 如果只有state machine命令，也确保它有种子
      sm_seed = extract_seed_from_command(sm_cmd)
      if sm_seed is None:
        seed_to_use = random.randint(1, 1000000000)
        sm_cmd = add_seed_to_command(sm_cmd, seed_to_use)
      else:
        seed_to_use = sm_seed

      sm_cmds.append(sm_cmd)
      cmd_seeds[sm_cmd] = seed_to_use

  return normal_cmds, sm_cmds, cmd_pairs, cmd_seeds


def filter_paired_commands_only(normal_cmds, sm_cmds, cmd_pairs):
  """
  过滤命令列表，只保留有配对的命令

  Args:
      normal_cmds: 普通命令列表
      sm_cmds: state machine命令列表
      cmd_pairs: 命令配对关系字典

  Returns:
      filtered_normal_cmds: 过滤后的普通命令列表
      filtered_sm_cmds: 过滤后的state machine命令列表
      filtered_count: 被过滤掉的命令数量
  """
  original_normal_count = len(normal_cmds)
  original_sm_count = len(sm_cmds)

  # 创建两个集合来快速查询哪些命令有配对
  normal_with_pair = set()
  sm_with_pair = set()

  for normal_cmd in normal_cmds:
    if normal_cmd in cmd_pairs and cmd_pairs[normal_cmd] in sm_cmds:
      normal_with_pair.add(normal_cmd)
      sm_with_pair.add(cmd_pairs[normal_cmd])

  for sm_cmd in sm_cmds:
    if sm_cmd in cmd_pairs and cmd_pairs[sm_cmd] in normal_cmds:
      sm_with_pair.add(sm_cmd)
      normal_with_pair.add(cmd_pairs[sm_cmd])

  # 过滤命令列表
  filtered_normal_cmds = [cmd for cmd in normal_cmds if cmd in normal_with_pair]
  filtered_sm_cmds = [cmd for cmd in sm_cmds if cmd in sm_with_pair]

  # 计算过滤掉的命令数量
  normal_filtered_count = original_normal_count - len(filtered_normal_cmds)
  sm_filtered_count = original_sm_count - len(filtered_sm_cmds)
  filtered_count = {
    "normal": normal_filtered_count,
    "state_machine": sm_filtered_count,
    "total": normal_filtered_count + sm_filtered_count,
  }

  return filtered_normal_cmds, filtered_sm_cmds, filtered_count


def process_command(cmd):
  """处理单个命令并返回提取的统计数据和输出"""
  with TemporaryDirectory() as tmpdirname:
    result: subprocess.CompletedProcess[bytes] = subprocess.run(
      f"{cmd}".split(),
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      cwd=tmpdirname,
    )
  output = result.stdout.decode("utf-8")
  stderr = result.stderr.decode("utf-8")

  # 检查命令退出状态
  is_error = result.returncode != 0

  # 提取最后一行包含 "calls/s" 的统计数据
  lines = output.splitlines()
  last_line = ""
  for line in lines:
    if "calls/s" in line:
      last_line = line

  if last_line:
    # 更新正则表达式以捕获reverts和revert rate信息
    pattern = r"avg gen:\s*([\d\.]+)\s*ms,\s*avg exec:\s*([\d\.]+)\s*ms,\s*total gen:\s*([\d\.]+)\s*ms,\s*total exec:\s*([\d\.]+)\s*ms,\s*calls/s:\s*([\d\.]+)(?:,\s*reverts:\s*([\d\.]+))?(?:,\s*revert rate:\s*([\d\.]+))?"
    m = re.search(pattern, last_line)
    if m:
      result_data = {
        "avg_gen": float(m.group(1)),
        "avg_exec": float(m.group(2)),
        "total_gen": float(m.group(3)),
        "total_exec": float(m.group(4)),
        "calls_per_sec": float(m.group(5)),
        "full_output": output,
        "stderr": stderr,
        "command": cmd,
        "is_error": is_error,
        "return_code": result.returncode,
      }

      # 添加reverts和revert rate数据（如果存在）
      if m.group(6) is not None:
        result_data["reverts"] = float(m.group(6))
      if m.group(7) is not None:
        result_data["revert_rate"] = float(m.group(7))

      return result_data

  # 如果无法提取统计数据或命令执行失败
  return {
    "is_error": True,
    "return_code": result.returncode,
    "full_output": output,
    "stderr": stderr,
    "command": cmd,
  }


def process_command_with_retry(cmd, max_retries=0):
  """
  处理单个命令并返回提取的统计数据和输出，支持重试失败的命令

  Args:
      cmd: 要执行的命令
      max_retries: 最大重试次数（默认为0，不重试）

  Returns:
      dict: 命令执行结果，包含统计数据和重试信息
  """
  retry_count = 0
  result_data = None

  # 最多尝试 max_retries + 1 次（原始执行 + 重试）
  while retry_count <= max_retries:
    try:
      with TemporaryDirectory() as tmpdirname:
        result: subprocess.CompletedProcess[bytes] = subprocess.run(
          f"{cmd}".split(),
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          cwd=tmpdirname,
        )
      output = result.stdout.decode("utf-8")
      stderr = result.stderr.decode("utf-8")

      # 检查命令退出状态
      is_error = result.returncode != 0

      # 提取最后一行包含 "calls/s" 的统计数据
      lines = output.splitlines()
      last_line = ""
      for line in lines:
        if "calls/s" in line:
          last_line = line

      if last_line:
        # 更新正则表达式以捕获reverts和revert rate信息
        pattern = r"avg gen:\s*([\d\.]+)\s*ms,\s*avg exec:\s*([\d\.]+)\s*ms,\s*total gen:\s*([\d\.]+)\s*ms,\s*total exec:\s*([\d\.]+)\s*ms,\s*calls/s:\s*([\d\.]+)(?:,\s*reverts:\s*([\d\.]+))?(?:,\s*revert rate:\s*([\d\.]+))?"
        m = re.search(pattern, last_line)
        if m:
          result_data = {
            "avg_gen": float(m.group(1)),
            "avg_exec": float(m.group(2)),
            "total_gen": float(m.group(3)),
            "total_exec": float(m.group(4)),
            "calls_per_sec": float(m.group(5)),
            "full_output": output,
            "stderr": stderr,
            "command": cmd,
            "is_error": is_error,
            "return_code": result.returncode,
            "retry_count": retry_count,
          }

          # 添加reverts和revert rate数据（如果存在）
          if m.group(6) is not None:
            result_data["reverts"] = float(m.group(6))
          if m.group(7) is not None:
            result_data["revert_rate"] = float(m.group(7))

          # 如果成功提取到数据，则跳出循环
          break

      # 如果无法提取统计数据或命令执行失败
      result_data = {
        "is_error": True,
        "return_code": result.returncode,
        "full_output": output,
        "stderr": stderr,
        "command": cmd,
        "retry_count": retry_count,
      }

      # 如果执行成功（即使无法提取数据），则跳出循环
      if not is_error:
        break

      # 否则，增加重试计数并继续
      retry_count += 1

    except Exception as exc:
      result_data = {
        "is_error": True,
        "exception": str(exc),
        "command": cmd,
        "retry_count": retry_count,
      }
      retry_count += 1

  return result_data


def save_intermediate_results(
  stats, completed_cmds, output_path, elapsed_time, total_commands
):
  """保存中间结果到文件"""
  # 计算已完成命令的统计数据
  result_stats = {}
  if stats["avg_gen"]:  # 确保有数据再计算
    avg_avg_gen = sum(stats["avg_gen"]) / len(stats["avg_gen"])
    avg_avg_exec = sum(stats["avg_exec"]) / len(stats["avg_exec"])
    total_gen_sum = sum(stats["total_gen"])
    total_exec_sum = sum(stats["total_exec"])
    avg_calls_per_sec = sum(stats["calls_per_sec"]) / len(stats["calls_per_sec"])

    # 创建结果字典
    result_stats = {
      "status": "intermediate",
      "progress": {
        "completed": len(completed_cmds),
        "total": total_commands,
        "percent": round(len(completed_cmds) / total_commands * 100, 1)
        if total_commands > 0
        else 0,
      },
      "command_count": len(stats["avg_gen"]),
      "avg_gen_time": round(avg_avg_gen, 2),
      "avg_exec_time": round(avg_avg_exec, 2),
      "total_gen_time": round(total_gen_sum, 2),
      "total_exec_time": round(total_exec_sum, 2),
      "avg_calls_per_sec": round(avg_calls_per_sec, 2),
      "elapsed_time_seconds": round(elapsed_time, 2),
      "completed_commands": completed_cmds,
      "raw_data": stats,  # 包含原始数据以便进一步分析
    }

  # 确保目录存在
  os.makedirs(os.path.dirname(output_path), exist_ok=True)

  # 保存到文件
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result_stats, f, indent=2, ensure_ascii=False)


def run_commands(
  cmds,
  stats,
  completed_cmds,
  detailed_results,
  error_cmds=None,
  max_workers=None,
  save_interval=10,
  intermediate_json=None,
  total_commands=0,
  console=None,
  start_time=None,
  cmd_seeds=None,
  max_retries=0,  # 新增参数：最大重试次数
):
  """
  执行一组命令并收集统计数据，支持重试失败的命令

  Args:
      cmds: 要执行的命令列表
      stats: 用于存储统计数据的字典
      completed_cmds: 已完成命令的列表
      detailed_results: 用于存储每个命令详细结果的字典
      error_cmds: 用于存储出错命令的列表
      max_workers: 最大线程数
      save_interval: 中间结果保存间隔
      intermediate_json: 中间结果文件路径
      total_commands: 总命令数量（用于进度显示）
      console: Rich控制台对象
      start_time: 开始时间
      cmd_seeds: 命令对应的种子字典
      max_retries: 命令失败后的最大重试次数

  Returns:
      更新后的stats, completed_cmds, detailed_results和error_cmds
  """
  if console is None:
    console = Console()

  if start_time is None:
    start_time = time()

  if error_cmds is None:
    error_cmds = []

  if cmd_seeds is None:
    cmd_seeds = {}

  # 记录重试信息的统计数据
  retry_stats = {
    "commands_retried": 0,
    "total_retries": 0,
    "successful_retries": 0,
  }

  # 过滤掉已完成的命令
  cmds_to_run = [
    cmd for cmd in cmds if cmd not in completed_cmds and cmd not in error_cmds
  ]

  console.print(f"[bold green]准备运行 {len(cmds_to_run)} 个命令，使用多线程执行...[/]")
  if max_retries > 0:
    console.print(f"[bold blue]失败命令将最多重试 {max_retries} 次[/]")

  # 使用线程池执行命令，并展示美观的进度条
  with Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TaskProgressColumn(),
    "•",
    TimeRemainingColumn(),
  ) as progress:
    task_id = progress.add_task("[cyan]处理命令...", total=len(cmds_to_run))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
      # 提交所有任务，使用带重试的命令处理函数
      future_to_cmd = {
        executor.submit(process_command_with_retry, cmd, max_retries): cmd
        for cmd in cmds_to_run
      }

      # 收集结果
      processed = 0
      for future in concurrent.futures.as_completed(future_to_cmd):
        cmd = future_to_cmd[future]
        try:
          data = future.result()
          processed += 1
          progress.update(task_id, advance=1)

          # 添加使用的种子信息到结果中
          if cmd in cmd_seeds:
            data["seed_used"] = cmd_seeds[cmd]

          # 更新重试统计信息
          if "retry_count" in data and data["retry_count"] > 0:
            retry_stats["commands_retried"] += 1
            retry_stats["total_retries"] += data["retry_count"]
            if not data.get("is_error", False):
              retry_stats["successful_retries"] += 1
              progress.console.print(
                f"[bold green]命令 '{cmd}' 在重试 {data['retry_count']} 次后成功执行[/]"
              )

          if data:
            if data.get("is_error", False):
              # 命令出错，添加到错误列表
              error_cmds.append(cmd)
              detailed_results[cmd] = data

              # 根据是否尝试过重试来显示不同的错误消息
              if data.get("retry_count", 0) > 0:
                progress.console.print(
                  f"[bold red]命令 '{cmd}' 执行出错，尝试重试 {data['retry_count']} 次后仍然失败 (返回码: {data.get('return_code', 'N/A')})[/]"
                )
              else:
                progress.console.print(
                  f"[bold red]命令 '{cmd}' 执行出错 (返回码: {data.get('return_code', 'N/A')})[/]"
                )
            elif "avg_gen" in data:
              # 命令成功执行，且提取到了统计数据
              stats["avg_gen"].append(data["avg_gen"])
              stats["avg_exec"].append(data["avg_exec"])
              stats["total_gen"].append(data["total_gen"])
              stats["total_exec"].append(data["total_exec"])
              stats["calls_per_sec"].append(data["calls_per_sec"])

              # 添加reverts和revert_rate数据（如果存在）
              if "reverts" in data and "reverts" in stats:
                stats["reverts"].append(data["reverts"])
              if "revert_rate" in data and "revert_rate" in stats:
                stats["revert_rate"].append(data["revert_rate"])

              completed_cmds.append(cmd)
              detailed_results[cmd] = data

          # 定期保存中间结果
          if intermediate_json and processed % save_interval == 0:
            elapsed = time() - start_time
            save_intermediate_results(
              stats, completed_cmds, intermediate_json, elapsed, total_commands
            )
            progress.console.print(
              f"[dim]保存中间结果... 已完成: {len(completed_cmds)}/{total_commands}, 出错: {len(error_cmds)}[/]"
            )

        except Exception as exc:
          console.print(f"[bold red]命令 '{cmd}' 生成了异常: {exc}[/]")
          error_cmds.append(cmd)
          detailed_results[cmd] = {
            "is_error": True,
            "exception": str(exc),
            "command": cmd,
            "retry_count": 0,
          }

  # 显示重试统计信息
  if max_retries > 0:
    console.print(
      f"[bold blue]重试统计: {retry_stats['commands_retried']} 个命令尝试重试，"
      f"共 {retry_stats['total_retries']} 次重试，"
      f"{retry_stats['successful_retries']} 次重试成功[/]"
    )

  # 将重试统计信息添加到stats中
  stats["retry_stats"] = retry_stats

  return stats, completed_cmds, detailed_results, error_cmds


def calculate_stats_summary(stats):
  """计算统计数据的摘要"""
  if not stats["avg_gen"]:
    return {}

  summary = {
    "command_count": len(stats["avg_gen"]),
    "avg_gen_time": round(sum(stats["avg_gen"]) / len(stats["avg_gen"]), 2),
    "avg_exec_time": round(sum(stats["avg_exec"]) / len(stats["avg_exec"]), 2),
    "total_gen_time": round(sum(stats["total_gen"]), 2),
    "total_exec_time": round(sum(stats["total_exec"]), 2),
    "avg_calls_per_sec": round(
      sum(stats["calls_per_sec"]) / len(stats["calls_per_sec"]), 2
    ),
  }

  # 添加reverts和revert_rate摘要（如果存在）
  if "reverts" in stats and stats["reverts"]:
    summary["avg_reverts"] = round(sum(stats["reverts"]) / len(stats["reverts"]), 2)
    summary["total_reverts"] = round(sum(stats["reverts"]), 0)

  if "revert_rate" in stats and stats["revert_rate"]:
    summary["avg_revert_rate"] = round(
      sum(stats["revert_rate"]) / len(stats["revert_rate"]), 4
    )

  return summary


def compare_stats(normal_stats, sm_stats):
  """比较两种方法的统计数据，计算差异和提升百分比"""
  if not normal_stats or not sm_stats:
    return {}

  comparison = {}
  for key in normal_stats:
    if key == "command_count":
      comparison[key] = {
        "normal": normal_stats[key],
        "state_machine": sm_stats[key],
        "difference": sm_stats[key] - normal_stats[key],
      }
    else:
      normal_val = normal_stats[key]
      sm_val = sm_stats[key]

      # 计算差异和百分比变化
      diff = sm_val - normal_val

      # 对于不同指标确定改进方向:
      # - 时间指标（avg_gen、avg_exec等）: 负值代表改进（更快）
      # - calls/s: 正值代表改进（更高效）
      # - reverts和revert_rate: 负值代表改进（更少的revert）
      is_improvement = False
      if key == "avg_calls_per_sec":
        is_improvement = diff > 0  # 调用频率更高是改进
      elif key in ["avg_reverts", "total_reverts", "avg_revert_rate"]:
        is_improvement = diff < 0  # revert次数或比率更低是改进
      else:
        is_improvement = diff < 0  # 其他时间指标，更小是改进

      if normal_val != 0:
        percent = (diff / normal_val) * 100
      else:
        percent = 0

      comparison[key] = {
        "normal": normal_val,
        "state_machine": sm_val,
        "difference": diff,
        "percent_change": round(percent, 2),
        "is_improvement": is_improvement,
      }

  return comparison


def save_comparison_markdown(
  comparison,
  normal_summary,
  sm_summary,
  total_runtime,
  output_path,
  global_seed=None,
  skip_only_owners=False,
  min_transition_rate=None,
  max_transition_rate=None,
):
  """
  将比较结果保存为Markdown格式

  Args:
      comparison: 比较结果字典
      normal_summary: 普通命令统计摘要
      sm_summary: state machine命令统计摘要
      total_runtime: 总运行时间（秒）
      output_path: 输出文件路径
      global_seed: 全局种子（如果使用）
      skip_only_owners: 是否跳过了只有owner能操作的合约
      min_transition_rate: 状态机转换率的最小阈值（如果设置）
      max_transition_rate: 状态机转换率的最大阈值（如果设置）
  """
  # 生成标题，根据参数添加附加信息
  title = "Echidna 执行统计比较结果"
  subtitle_parts = []

  if skip_only_owners:
    subtitle_parts.append("剔除onlyOwner样例")

  # 添加状态机转换率限制信息
  if min_transition_rate is not None and max_transition_rate is not None:
    subtitle_parts.append(
      f"将状态机转换率限制在{min_transition_rate}~{max_transition_rate}%之间"
    )
  elif min_transition_rate is not None:
    subtitle_parts.append(f"状态机转换率大于{min_transition_rate}%")
  elif max_transition_rate is not None:
    subtitle_parts.append(f"状态机转换率小于{max_transition_rate}%")

  # 完整标题
  if subtitle_parts:
    full_title = f"{title}（{', '.join(subtitle_parts)}）"
  else:
    full_title = title

  markdown_content = [
    f"# {full_title}",
    f"\n## 执行时间\n\n总运行时间: {total_runtime:.2f} 秒",
  ]

  # 添加种子信息（如果有）
  if global_seed is not None:
    markdown_content.append(f"\n## 全局种子\n\n使用全局随机种子: {global_seed}")

  markdown_content.append("\n## 普通命令执行统计\n")

  # 添加普通命令统计表格
  markdown_content.append("| 指标 | 值 |")
  markdown_content.append("| ---- | ---- |")
  for key, value in normal_summary.items():
    if key in ("avg_gen_time", "avg_exec_time", "total_gen_time", "total_exec_time"):
      markdown_content.append(f"| {key.replace('_', ' ').title()} (ms) | {value} |")
    elif key in ("avg_revert_rate"):
      markdown_content.append(f"| {key.replace('_', ' ').title()} | {value:.4f} |")
    else:
      markdown_content.append(f"| {key.replace('_', ' ').title()} | {value} |")

  # 添加State Machine命令统计表格
  markdown_content.append("\n## State Machine命令执行统计\n")
  markdown_content.append("| 指标 | 值 |")
  markdown_content.append("| ---- | ---- |")
  for key, value in sm_summary.items():
    if key not in ("command_count", "avg_calls_per_sec"):
      markdown_content.append(f"| {key.replace('_', ' ').title()} (ms) | {value} |")
    else:
      markdown_content.append(f"| {key.replace('_', ' ').title()} | {value} |")
  # 添加比较结果表格
  markdown_content.append("\n## 对比分析\n")
  markdown_content.append("| 指标 | 普通命令 | State Machine | 差异 | 变化百分比 |")
  markdown_content.append("| ---- | ---- | ---- | ---- | ---- |")

  for key, values in comparison.items():
    if key not in ("command_count"):
      # 根据是否有改进选择符号
      percent_change = values["percent_change"]
      if values["is_improvement"]:
        percent_text = (
          f"+{percent_change}%" if percent_change > 0 else f"{percent_change}%"
        )
      else:
        percent_text = f"{percent_change}%"

      # 对不同类型的指标使用不同的单位或格式
      if key in ("avg_gen_time", "avg_exec_time", "total_gen_time", "total_exec_time"):
        title = f"{key.replace('_', ' ').title()} (ms)"
      elif key in ("avg_revert_rate"):
        title = f"{key.replace('_', ' ').title()}"
        # 确保revert_rate以小数格式显示
        normal_val = (
          f"{values['normal']:.4f}"
          if isinstance(values["normal"], float)
          else values["normal"]
        )
        sm_val = (
          f"{values['state_machine']:.4f}"
          if isinstance(values["state_machine"], float)
          else values["state_machine"]
        )
        diff_val = (
          f"{values['difference']:.4f}"
          if isinstance(values["difference"], float)
          else values["difference"]
        )
        markdown_content.append(
          f"| {title} | {normal_val} | {sm_val} | {diff_val} | {percent_text} |"
        )
        continue
      else:
        title = f"{key.replace('_', ' ').title()}"

      markdown_content.append(
        f"| {title} | {values['normal']} | {values['state_machine']} | "
        f"{values['difference']} | {percent_text} |"
      )
    else:
      markdown_content.append(
        f"| {key.replace('_', ' ').title()} | "
        f"{values['normal']} | {values['state_machine']} | "
        f"{values['difference']} | N/A |"
      )

  # 保存为文件
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(markdown_content))


def analyze_command_performance(normal_detailed, sm_detailed, cmd_pairs, cmd_seeds):
  """
  分析每个命令的表现，找出State Machine较差和较好的样例

  Args:
      normal_detailed: 普通命令的详细结果
      sm_detailed: state machine命令的详细结果
      cmd_pairs: 命令配对关系
      cmd_seeds: 命令对应的种子

  Returns:
      worse_samples: State Machine表现较差的样例列表
      better_samples: State Machine表现较好的样例列表
  """
  worse_samples = []
  better_samples = []

  # 对比已完成的命令对
  for normal_cmd, normal_data in normal_detailed.items():
    # 跳过错误的命令
    if normal_data.get("is_error", False):
      continue

    # 查找对应的state machine命令
    if normal_cmd in cmd_pairs:
      sm_cmd = cmd_pairs[normal_cmd]
      if sm_cmd in sm_detailed and not sm_detailed[sm_cmd].get("is_error", False):
        sm_data = sm_detailed[sm_cmd]

        # 获取使用的种子
        seed = cmd_seeds.get(normal_cmd) or normal_data.get("seed_used")

        # 创建评估结果
        evaluation = {
          "normal_command": normal_cmd,
          "sm_command": sm_cmd,
          "seed_used": seed,
          "normal_results": normal_data,
          "sm_results": sm_data,
          "comparison": {},
        }

        # 比较关键指标
        is_worse = False
        is_better = False

        # 计算关键指标的差异
        metrics_to_compare = [
          "avg_gen",
          "avg_exec",
          "total_gen",
          "total_exec",
          "calls_per_sec",
        ]

        # 如果存在revert相关指标，也进行比较
        if "reverts" in normal_data and "reverts" in sm_data:
          metrics_to_compare.append("reverts")
        if "revert_rate" in normal_data and "revert_rate" in sm_data:
          metrics_to_compare.append("revert_rate")

        for key in metrics_to_compare:
          # 如果某个指标不存在于其中一个数据中，则跳过
          if key not in normal_data or key not in sm_data:
            continue

          normal_val = normal_data[key]
          sm_val = sm_data[key]
          diff = sm_val - normal_val
          percent = (diff / normal_val) * 100 if normal_val != 0 else 0

          # 判断是改进还是退步
          # 对不同指标有不同的判断标准:
          # - calls_per_sec，值越大越好
          # - reverts和revert_rate，值越小越好
          # - 其他时间指标，值越小越好
          if key == "calls_per_sec":
            is_improvement = diff > 0
          elif key in ["reverts", "revert_rate"]:
            is_improvement = diff < 0
          else:
            is_improvement = diff < 0

          evaluation["comparison"][key] = {
            "normal": normal_val,
            "state_machine": sm_val,
            "difference": diff,
            "percent_change": round(percent, 2),
            "is_improvement": is_improvement,
          }

          # 根据指标重要性判断整体表现
          if key == "calls_per_sec":
            if diff < -10:  # calls/s减少超过10%认为是明显退步
              is_worse = True
            elif diff > 10:  # calls/s增加超过10%认为是明显改进
              is_better = True
          elif key == "revert_rate":
            # revert率降低超过10%认为是明显改进，增加超过10%认为是明显退步
            if diff > 0.10:  # revert率增加超过10%点
              is_worse = True
            elif diff < -0.10:  # revert率减少超过10%点
              is_better = True
          elif key == "reverts":
            # 如果reverts数量变化显著，也要考虑
            if normal_val > 0:
              percent = diff / normal_val * 100
              if percent > 20:  # reverts增加超过20%
                is_worse = True
              elif percent < -20:  # reverts减少超过20%
                is_better = True

        # 对总执行时间的评估
        total_time_normal = normal_data["total_gen"] + normal_data["total_exec"]
        total_time_sm = sm_data["total_gen"] + sm_data["total_exec"]
        time_diff_percent = (
          ((total_time_sm - total_time_normal) / total_time_normal * 100)
          if total_time_normal > 0
          else 0
        )

        if time_diff_percent > 15:  # 总时间增加超过15%认为是明显退步
          is_worse = True
        elif time_diff_percent < -15:  # 总时间减少超过15%认为是明显改进
          is_better = True

        # 根据分析结果归类
        if is_worse and not is_better:
          worse_samples.append(evaluation)
        elif is_better and not is_worse:
          better_samples.append(evaluation)

  return worse_samples, better_samples


def find_low_performance_samples(detailed_results, cmd_seeds, threshold=800.0):
  """
  查找执行效率特别低的样例（calls/sec值特别小的样例）

  Args:
      detailed_results: 命令的详细结果字典
      cmd_seeds: 命令对应的种子字典
      threshold: calls/sec的阈值，低于此值被认为是低效率样例

  Returns:
      low_perf_samples: 低效率样例列表
  """
  low_perf_samples = []

  for cmd, data in detailed_results.items():
    # 跳过错误的命令
    if data.get("is_error", False):
      continue

    # 检查calls_per_sec值是否低于阈值
    if "calls_per_sec" in data and data["calls_per_sec"] < threshold:
      sample_info = {
        "command": cmd,
        "seed_used": cmd_seeds.get(cmd) or data.get("seed_used"),
        "calls_per_sec": data["calls_per_sec"],
        "avg_gen": data.get("avg_gen"),
        "avg_exec": data.get("avg_exec"),
        "total_gen": data.get("total_gen"),
        "total_exec": data.get("total_exec"),
      }

      # 提取合约名称
      contract_match = re.search(r"--contract\s+(\w+)", cmd)
      if contract_match:
        sample_info["contract_name"] = contract_match.group(1)

      # 提取文件路径
      file_path_match = re.search(r"echidna\s+([^\s]+)\s+", cmd)
      if file_path_match:
        sample_info["file_path"] = file_path_match.group(1)

      low_perf_samples.append(sample_info)

  # 按照calls_per_sec从小到大排序
  low_perf_samples.sort(key=lambda x: x["calls_per_sec"])

  return low_perf_samples


def filter_high_revert_reduction_samples(
  normal_detailed, sm_detailed, cmd_pairs, cmd_seeds, threshold=20.0
):
  """
  过滤 revert 率减少超过指定阈值百分比的样例

  Args:
      normal_detailed: 普通命令的详细结果字典
      sm_detailed: state machine命令的详细结果字典
      cmd_pairs: 命令配对关系
      cmd_seeds: 命令对应的种子字典
      threshold: revert率减少的阈值百分比，超过此值的样例将被统计

  Returns:
      high_reduction_samples: revert率减少幅度大的样例列表
      stats_summary: 这些样例的统计数据摘要
  """
  high_reduction_samples = []
  stats = {
    "avg_gen": [],
    "avg_exec": [],
    "total_gen": [],
    "total_exec": [],
    "calls_per_sec": [],
    "reverts": [],
    "revert_rate": [],
    "reduction_percent": [],
  }

  for normal_cmd, normal_data in normal_detailed.items():
    # 跳过错误的命令
    if normal_data.get("is_error", False):
      continue

    # 查找对应的state machine命令
    if normal_cmd in cmd_pairs:
      sm_cmd = cmd_pairs[normal_cmd]
      if sm_cmd in sm_detailed and not sm_detailed[sm_cmd].get("is_error", False):
        sm_data = sm_detailed[sm_cmd]

        # 检查是否有revert_rate数据
        if "revert_rate" in normal_data and "revert_rate" in sm_data:
          normal_revert_rate = normal_data["revert_rate"]
          sm_revert_rate = sm_data["revert_rate"]

          # 只有当普通命令的revert率大于0时才有意义计算减少比例
          if normal_revert_rate > 0:
            # 计算revert率减少的百分比
            reduction = (normal_revert_rate - sm_revert_rate) / normal_revert_rate * 100

            # 如果减少幅度超过阈值
            if reduction > threshold:
              sample_info = {
                "normal_command": normal_cmd,
                "sm_command": sm_cmd,
                "seed_used": cmd_seeds.get(normal_cmd) or normal_data.get("seed_used"),
                "normal_revert_rate": normal_revert_rate,
                "sm_revert_rate": sm_revert_rate,
                "reduction_percent": reduction,
                "avg_gen": sm_data.get("avg_gen"),
                "avg_exec": sm_data.get("avg_exec"),
                "total_gen": sm_data.get("total_gen"),
                "total_exec": sm_data.get("total_exec"),
                "calls_per_sec": sm_data.get("calls_per_sec"),
                "reverts": sm_data.get("reverts"),
              }

              high_reduction_samples.append(sample_info)

              # 收集统计数据（使用state machine的数据）
              stats["avg_gen"].append(sm_data.get("avg_gen", 0))
              stats["avg_exec"].append(sm_data.get("avg_exec", 0))
              stats["total_gen"].append(sm_data.get("total_gen", 0))
              stats["total_exec"].append(sm_data.get("total_exec", 0))
              stats["calls_per_sec"].append(sm_data.get("calls_per_sec", 0))
              stats["reverts"].append(sm_data.get("reverts", 0))
              stats["revert_rate"].append(sm_data.get("revert_rate", 0))
              stats["reduction_percent"].append(reduction)

  # 计算统计数据的平均值
  stats_summary = {
    "avg_gen_time": round(
      sum(stats["avg_gen"]) / len(stats["avg_gen"]) if stats["avg_gen"] else 0, 2
    ),
    "avg_exec_time": round(
      sum(stats["avg_exec"]) / len(stats["avg_exec"]) if stats["avg_exec"] else 0, 2
    ),
    "total_gen_time": round(sum(stats["total_gen"]) if stats["total_gen"] else 0, 2),
    "total_exec_time": round(sum(stats["total_exec"]) if stats["total_exec"] else 0, 2),
    "avg_calls_per_sec": round(
      sum(stats["calls_per_sec"]) / len(stats["calls_per_sec"])
      if stats["calls_per_sec"]
      else 0,
      2,
    ),
    "avg_reverts": round(
      sum(stats["reverts"]) / len(stats["reverts"]) if stats["reverts"] else 0, 2
    ),
    "avg_revert_rate": round(
      sum(stats["revert_rate"]) / len(stats["revert_rate"])
      if stats["revert_rate"]
      else 0,
      4,
    ),
    "avg_reduction_percent": round(
      sum(stats["reduction_percent"]) / len(stats["reduction_percent"])
      if stats["reduction_percent"]
      else 0,
      2,
    ),
    "max_reduction_percent": max(stats["reduction_percent"]),
  }

  return high_reduction_samples, stats_summary


def load_low_perf_samples(filepath):
  """
  从文件中加载已知的低性能样例

  Args:
      filepath: 低性能样例JSON文件路径

  Returns:
      low_perf_commands: 低性能命令的集合，如果文件不存在或无法加载则返回空集合
      original_data: 原始低性能样例数据，用于后续合并
  """
  low_perf_commands = set()
  original_data = None

  if not filepath or not os.path.exists(filepath):
    return low_perf_commands, original_data

  try:
    with open(filepath, "r", encoding="utf-8") as f:
      data = json.load(f)

    # 保存原始数据用于后续合并
    original_data = data

    # 收集普通命令中的低性能样例
    if "normal_command_samples" in data:
      for sample in data["normal_command_samples"]:
        if "command" in sample:
          low_perf_commands.add(" ".join(sample["command"].split()[:-2]))

    # 收集state machine命令中的低性能样例
    if "state_machine_samples" in data:
      for sample in data["state_machine_samples"]:
        if "command" in sample:
          low_perf_commands.add(" ".join(sample["command"].split()[:-2]))

    return low_perf_commands, original_data

  except Exception as e:
    print(f"警告: 无法加载低性能样例文件 {filepath}: {e}")
    return low_perf_commands, None


def merge_low_perf_samples(existing_data, new_data):
  """
  合并现有和新的低性能样例数据

  Args:
      existing_data: 现有的低性能样例数据
      new_data: 新的低性能样例数据

  Returns:
      merged_data: 合并后的数据
  """
  if not existing_data:
    return new_data

  # 创建合并后的数据结构
  merged_data = {
    "global_seed": new_data.get("global_seed"),
    "threshold": min(
      existing_data.get("threshold", float("inf")),
      new_data.get("threshold", float("inf")),
    ),
    "normal_command_samples": [],
    "state_machine_samples": [],
  }

  # 用于检查重复的命令集合
  normal_commands = set()
  sm_commands = set()

  # 添加现有的普通命令样例
  if "normal_command_samples" in existing_data:
    for sample in existing_data["normal_command_samples"]:
      if "command" in sample:
        cmd_key = " ".join(sample["command"].split()[:-2])
        normal_commands.add(cmd_key)
        merged_data["normal_command_samples"].append(sample)

  # 添加新的普通命令样例（如果不重复）
  if "normal_command_samples" in new_data:
    for sample in new_data["normal_command_samples"]:
      if "command" in sample:
        cmd_key = " ".join(sample["command"].split()[:-2])
        if cmd_key not in normal_commands:
          normal_commands.add(cmd_key)
          merged_data["normal_command_samples"].append(sample)

  # 添加现有的state machine命令样例
  if "state_machine_samples" in existing_data:
    for sample in existing_data["state_machine_samples"]:
      if "command" in sample:
        cmd_key = " ".join(sample["command"].split()[:-2])
        sm_commands.add(cmd_key)
        merged_data["state_machine_samples"].append(sample)

  # 添加新的state machine命令样例（如果不重复）
  if "state_machine_samples" in new_data:
    for sample in new_data["state_machine_samples"]:
      if "command" in sample:
        cmd_key = " ".join(sample["command"].split()[:-2])
        if cmd_key not in sm_commands:
          sm_commands.add(cmd_key)
          merged_data["state_machine_samples"].append(sample)

  # 更新计数
  merged_data["normal_count"] = len(merged_data["normal_command_samples"])
  merged_data["state_machine_count"] = len(merged_data["state_machine_samples"])

  return merged_data


def load_only_owners(filepath):
  """
  从JSON文件中加载只有owner能操作的合约列表

  Args:
      filepath: only_owners JSON文件路径

  Returns:
      owner_only_commands: owner_only命令列表，如果文件不存在或无法加载则返回空列表
  """
  owner_only_commands = []

  if not filepath or not os.path.exists(filepath):
    return owner_only_commands

  try:
    with open(filepath, "r", encoding="utf-8") as f:
      data = json.load(f)

    # 提取命令列表
    for item in data:
      if "command_state_machine" in item:
        cmd = item.get("command_state_machine", "")
        if cmd:
          # 提取核心部分，忽略额外参数
          core_cmd = " ".join(
            cmd.split()[:4]
          )  # 通常前四个部分包含echidna路径和合约路径
          owner_only_commands.append(core_cmd)

    return owner_only_commands

  except Exception as e:
    print(f"警告: 无法加载only_owners文件 {filepath}: {e}")
    return []


def generate_sorted_performance_comparison(
  normal_detailed, sm_detailed, cmd_pairs, cmd_seeds, output_json
):
  """
  按照不同性能指标对比普通命令和state machine命令，并排序输出

  Args:
      normal_detailed: 普通命令的详细结果
      sm_detailed: state machine命令的详细结果
      cmd_pairs: 命令配对关系
      cmd_seeds: 命令对应的种子
      output_json: 输出JSON文件路径

  Returns:
      sorted_results: 排序后的结果字典
  """
  metrics = [
    "avg_gen",
    "avg_exec",
    "total_gen",
    "total_exec",
    "calls_per_sec",
    "reverts",
    "revert_rate",
  ]
  sorted_results = {metric: [] for metric in metrics}

  # 收集配对命令的性能数据
  for normal_cmd, normal_data in normal_detailed.items():
    # 跳过错误的命令
    if normal_data.get("is_error", False):
      continue

    # 查找对应的state machine命令
    if normal_cmd in cmd_pairs:
      sm_cmd = cmd_pairs[normal_cmd]
      if sm_cmd in sm_detailed and not sm_detailed[sm_cmd].get("is_error", False):
        sm_data = sm_detailed[sm_cmd]

        # 获取使用的种子
        seed = cmd_seeds.get(normal_cmd) or normal_data.get("seed_used")

        # 提取合约名称和文件路径
        contract_name = "Unknown"
        file_path = "Unknown"

        contract_match = re.search(r"--contract\s+(\w+)", normal_cmd)
        if contract_match:
          contract_name = contract_match.group(1)

        file_path_match = re.search(r"echidna\s+([^\s]+)\s+", normal_cmd)
        if file_path_match:
          file_path = file_path_match.group(1).split("/")[-1]  # 只保留文件名

        # 为每个指标创建比较结果
        for metric in metrics:
          normal_val = normal_data[metric]
          sm_val = sm_data[metric]
          diff = sm_val - normal_val

          # 计算百分比变化
          if normal_val != 0:
            percent_change = (diff / normal_val) * 100
          else:
            percent_change = 0

          # 判断是改进还是退步
          # 对calls_per_sec，值越大越好；对其他时间指标，值越小越好
          is_improvement = (metric == "calls_per_sec" and diff > 0) or (
            metric != "calls_per_sec" and diff < 0
          )

          comparison_item = {
            "contract_name": contract_name,
            "file_path": file_path,
            "normal_cmd": normal_cmd,
            "sm_cmd": sm_cmd,
            "seed": seed,
            "normal_value": normal_val,
            "sm_value": sm_val,
            "difference": diff,
            "percent_change": round(percent_change, 2),
            "is_improvement": is_improvement,
          }

          sorted_results[metric].append(comparison_item)

  # 对每个指标按性能提升从大到小排序
  for metric in metrics:
    if metric == "calls_per_sec":
      # 对calls_per_sec，按百分比变化从大到小排序（正值表示提升）
      sorted_results[metric] = sorted(
        sorted_results[metric], key=lambda x: -x["percent_change"]
      )
    else:
      # 对时间指标，按百分比变化从小到大排序（负值表示提升）
      sorted_results[metric] = sorted(
        sorted_results[metric], key=lambda x: x["percent_change"]
      )

  # 保存排序结果到JSON文件
  with open(output_json, "w", encoding="utf-8") as f:
    json.dump(sorted_results, f, indent=2, ensure_ascii=False)

  return sorted_results


def plot_performance_comparisons(
  sorted_results,
  output_dir,
  skip_only_owners=False,
  min_transition_rate=None,
  max_transition_rate=None,
):
  """
  为每项性能指标生成散点图

  Args:
      sorted_results: 排序后的性能比较结果
      output_dir: 图表输出目录
      skip_only_owners: 是否跳过了只有owner能操作的合约
      min_transition_rate: 状态机转换率的最小阈值（如果设置）
      max_transition_rate: 状态机转换率的最大阈值（如果设置）
  """
  # 确保输出目录存在
  os.makedirs(output_dir, exist_ok=True)

  # 设置matplotlib只使用英文字体，避免中文字体警告
  plt.rcParams["font.family"] = "sans-serif"
  plt.rcParams["font.sans-serif"] = [
    "DejaVu Sans",
    "Arial",
    "Helvetica",
    "Liberation Sans",
  ]
  plt.rcParams["axes.unicode_minus"] = False  # 正确显示减号

  # 生成时间戳以区分不同批次的图表
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

  # 为每个性能指标绘制散点图
  metrics = ["avg_gen", "avg_exec", "total_gen", "total_exec", "calls_per_sec"]

  # 使用纯英文的指标名称
  metric_names = {
    "avg_gen": "Average Generation Time (ms)",
    "avg_exec": "Average Execution Time (ms)",
    "total_gen": "Total Generation Time (ms)",
    "total_exec": "Total Execution Time (ms)",
    "calls_per_sec": "Calls per Second",
  }

  # 生成参数信息的英文子标题
  subtitle_parts = []

  if skip_only_owners:
    subtitle_parts.append("OnlyOwner Excluded")

  # 添加状态机转换率限制信息
  if min_transition_rate is not None and max_transition_rate is not None:
    subtitle_parts.append(
      f"Transition Rate: {min_transition_rate}%-{max_transition_rate}%"
    )
  elif min_transition_rate is not None:
    subtitle_parts.append(f"Transition Rate > {min_transition_rate}%")
  elif max_transition_rate is not None:
    subtitle_parts.append(f"Transition Rate < {max_transition_rate}%")

  # 生成英文子标题
  subtitle = ""
  if subtitle_parts:
    subtitle = f" ({', '.join(subtitle_parts)})"

  for metric in metrics:
    # 创建新的图表
    plt.figure(figsize=(12, 8))

    # 提取数据点
    data = sorted_results[metric]
    indices = np.arange(len(data))

    # 分离改进和退步的数据点
    improved_indices = [i for i, item in enumerate(data) if item["is_improvement"]]
    regressed_indices = [i for i, item in enumerate(data) if not item["is_improvement"]]

    improved_percents = [data[i]["percent_change"] for i in improved_indices]
    regressed_percents = [data[i]["percent_change"] for i in regressed_indices]

    # 绘制散点图
    plt.scatter(
      improved_indices,
      improved_percents,
      color="green",
      label="better",
      alpha=0.7,
      s=30,
    )
    plt.scatter(
      regressed_indices, regressed_percents, color="red", label="worse", alpha=0.7, s=30
    )

    # 绘制水平零线
    plt.axhline(y=0, color="black", linestyle="-", linewidth=1)

    # 添加标签和标题，使用纯英文并添加参数信息
    plt.title(
      f"State Machine vs Normal: {metric_names[metric]} Difference{subtitle}",
      fontsize=16,
    )
    plt.xlabel(
      "Commands (sorted by performance improvement)",
      fontsize=14,
    )
    plt.ylabel(
      "Performance Change (%)",
      fontsize=14,
    )
    plt.grid(True, linestyle="--", alpha=0.7)

    # 格式化y轴为百分比
    plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=1))

    # 添加图例
    plt.legend(
      fontsize=12,
    )

    # 紧凑布局
    plt.tight_layout()

    # 保存图表
    output_path = os.path.join(
      output_dir, f"{timestamp}_{metric}_performance_comparison.png"
    )
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Generated chart: {output_path}")

  # 生成汇总统计图表
  plt.figure(figsize=(14, 10))

  # 重置字体设置，确保使用英文字体
  plt.rcParams["font.family"] = "sans-serif"
  plt.rcParams["font.sans-serif"] = [
    "DejaVu Sans",
    "Arial",
    "Helvetica",
    "Liberation Sans",
  ]

  # 为每个指标计算改进率
  improvement_rates = []
  metric_labels = []

  for metric in metrics:
    data = sorted_results[metric]
    if not data:  # 如果没有数据，跳过
      continue

    improved_count = sum(1 for item in data if item["is_improvement"])
    total_count = len(data)
    improvement_rate = improved_count / total_count * 100 if total_count > 0 else 0

    improvement_rates.append(improvement_rate)
    metric_labels.append(metric_names[metric])

  # 绘制条形图
  bars = plt.bar(metric_labels, improvement_rates, color="skyblue")

  # 在条形上添加百分比标签
  for bar, rate in zip(bars, improvement_rates):
    plt.text(
      bar.get_x() + bar.get_width() / 2,
      bar.get_height() + 1,
      f"{rate:.1f}%",
      ha="center",
      va="bottom",
      fontsize=10,
    )

  plt.title(
    f"State Machine vs Normal: Performance Improvement Rates{subtitle}",
    fontsize=16,
  )
  plt.ylabel(
    "Improvement Rate (%)",
    fontsize=14,
  )
  plt.ylim(0, 100)  # 设定y轴范围从0到100%
  plt.grid(True, linestyle="--", alpha=0.7, axis="y")

  # 保存汇总图表
  summary_output_path = os.path.join(
    output_dir, f"{timestamp}_improvement_rates_summary.png"
  )
  plt.savefig(summary_output_path, dpi=300)
  plt.close()

  print(f"Generated summary chart: {summary_output_path}")


def filter_low_transition_rate_samples(commands, threshold=3.0):
  """
  过滤掉状态机转换率低于阈值的样例

  Args:
      commands: 原始命令数据列表
      threshold: 转换率阈值，低于此值的样例将被过滤（默认3%）

  Returns:
      filtered_commands: 过滤后的命令列表
      filtered_count: 被过滤掉的命令数量
  """
  filtered_commands = []
  filtered_count = 0

  for item in commands:
    # 获取状态机JSON文件路径
    json_file_path = item.get("json_file_path")

    # 如果没有JSON文件路径，则保留此命令
    if not json_file_path or not os.path.exists(json_file_path):
      filtered_commands.append(item)
      continue

    try:
      # 读取JSON文件
      with open(json_file_path, "r", encoding="utf-8") as f:
        state_machine_data = json.load(f)

      # 获取状态机转换率
      transition_rate = state_machine_data.get("state_comparison", {}).get(
        "transition_reduction_rate", 0
      )

      # 如果转换率大于等于阈值，则保留此命令
      if transition_rate >= threshold:
        filtered_commands.append(item)
      else:
        filtered_count += 1

    except Exception as e:
      # 如果读取失败，则保留此命令
      print(f"警告: 无法读取状态机文件 {json_file_path}: {e}")
      filtered_commands.append(item)

  return filtered_commands, filtered_count


def filter_transition_rate_samples(commands, min_threshold=3.0, max_threshold=None):
  """
  根据状态机转换率过滤样例，过滤掉转换率低于最小阈值或高于最大阈值的样例

  Args:
      commands: 原始命令数据列表
      min_threshold: 最小转换率阈值，低于此值的样例将被过滤（默认3%）
      max_threshold: 最大转换率阈值，高于此值的样例将被过滤（默认None，表示不设上限）

  Returns:
      filtered_commands: 过滤后的命令列表
      filtered_count: 被过滤掉的命令数量和原因
  """
  filtered_commands = []
  filtered_count = {"low_rate": 0, "high_rate": 0, "total": 0}

  for item in commands:
    # 获取状态机JSON文件路径
    json_file_path = item.get("json_file_path")

    # 如果没有JSON文件路径，则保留此命令
    if not json_file_path or not os.path.exists(json_file_path):
      filtered_commands.append(item)
      continue

    try:
      # 读取JSON文件
      with open(json_file_path, "r", encoding="utf-8") as f:
        state_machine_data = json.load(f)

      # 获取状态机转换率
      transition_rate = state_machine_data.get("state_comparison", {}).get(
        "transition_reduction_rate", 0
      )

      # 检查转换率是否在允许范围内
      is_within_range = True

      # 判断是否低于最小阈值
      if min_threshold is not None and transition_rate < min_threshold:
        is_within_range = False
        filtered_count["low_rate"] += 1

      # 判断是否高于最大阈值
      if max_threshold is not None and transition_rate > max_threshold:
        is_within_range = False
        filtered_count["high_rate"] += 1

      if is_within_range:
        filtered_commands.append(item)
      else:
        filtered_count["total"] += 1

    except Exception as e:
      # 如果读取失败，则保留此命令
      print(f"警告: 无法读取状态机文件 {json_file_path}: {e}")
      filtered_commands.append(item)

  return filtered_commands, filtered_count


def batch_run_echidna(
  output_json=None,
  max_workers=None,
  save_interval=10,
  resume=True,
  compare_state_machine=True,
  global_seed=None,
  limit=None,
  low_perf_threshold=2000.0,  # 默认阈值改为2000.0
  skip_low_perf=False,
  low_perf_json=None,
  skip_only_owners=False,
  only_owners_json=None,
  max_retries=0,  # 新增参数：最大重试次数
  min_transition_rate=3.0,  # 新增参数：状态机转换率最小阈值
  max_transition_rate=None,  # 新增参数：状态机转换率的最大阈值
):
  """
  批量运行echidna命令并收集统计数据，支持暂存中间结果

  Args:
      output_json: 输出JSON文件的路径，默认为None
      max_workers: 最大线程数，默认为None（根据系统自动选择）
      save_interval: 每执行多少个命令保存一次中间结果，默认为10
      resume: 是否从上次中断的地方继续执行，默认为True
      compare_state_machine: 是否比较普通命令和state machine命令，默认为True
      global_seed: 全局随机数种子，确保每次运行结果一致
      limit: 限制运行的命令数量，可以是具体数字或百分比字符串(如"10%")
      low_perf_threshold: calls/sec的阈值，低于此值被认为是低效率样例
      skip_low_perf: 是否跳过已知的低性能样例
      low_perf_json: 包含低性能样例信息的JSON文件路径
      skip_only_owners: 是否跳过只有owner能操作的合约
      only_owners_json: 包含只有owner能操作合约信息的JSON文件路径
      max_retries: 命令失败后的最大重试次数，默认为0（不重试）
      min_transition_rate: 状态机转换率的最小阈值，低于此值的样例将被过滤（默认3%）
      max_transition_rate: 状态机转换率的最大阈值，高于此值的样例将被过滤（默认None，表示不设上限）
  """
  console = Console()
  start_time = time()

  # 生成时间戳，用于所有输出文件
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

  # 设置默认输出路径
  if output_json is None:
    base_path = (
      "/home/hengdiye/tmp/slithIR_examples/solfuse/scripts/results/echidna_stats"
    )
    output_json = f"{base_path}_{timestamp}.json"
  else:
    # 为自定义输出路径添加时间戳
    # 分离文件名和扩展名
    output_base, output_ext = os.path.splitext(output_json)
    output_json = f"{output_base}_{timestamp}{output_ext}"

  # 设置Markdown输出路径
  output_markdown = output_json.replace(".json", ".md")

  # 设置样例分析结果输出路径
  output_better_json = output_json.replace(".json", "_better_samples.json")
  output_worse_json = output_json.replace(".json", "_worse_samples.json")

  # 设置低性能样例结果输出路径
  output_low_perf_json = output_json.replace(".json", "_low_performance_samples.json")

  # 如果未指定低性能样例文件路径，则默认使用输出路径
  if low_perf_json is None and skip_low_perf:
    low_perf_json = output_low_perf_json

  # 设置出错样例结果输出路径
  output_error_json = output_json.replace(".json", "_error_samples.json")

  # 设置高revert率样例结果输出路径
  output_high_revert_json = output_json.replace(".json", "_high_revert_samples.json")

  # 设置revert率减少幅度较大的样例结果输出路径
  output_high_reduction_json = output_json.replace(
    ".json", "_high_revert_reduction_samples.json"
  )

  # 确保输出目录存在
  os.makedirs(os.path.dirname(output_json), exist_ok=True)

  # 中间结果文件路径
  intermediate_json = output_json.replace(".json", "_intermediate.json")

  console.print(f"[bold cyan]运行时间戳: {timestamp}[/]")
  console.print(f"[bold cyan]所有输出文件将使用此时间戳，以避免覆盖现有文件[/]")
  console.print(f"[bold cyan]主输出文件: {output_json}[/]")

  # 创建统计数据存储结构 - 普通命令
  normal_stats = {
    "avg_gen": [],
    "avg_exec": [],
    "total_gen": [],
    "total_exec": [],
    "calls_per_sec": [],
    "reverts": [],  # 新增：存储revert次数
    "revert_rate": [],  # 新增：存储revert比例
  }

  # 详细结果存储
  normal_detailed = {}
  sm_detailed = {}

  # 创建统计数据存储结构 - state machine命令
  sm_stats = {
    "avg_gen": [],
    "avg_exec": [],
    "total_gen": [],
    "total_exec": [],
    "calls_per_sec": [],
    "reverts": [],  # 新增：存储revert次数
    "revert_rate": [],  # 新增：存储revert比例
  }

  # 已完成的命令列表
  normal_completed = []
  sm_completed = []

  # 出错的命令列表
  normal_errors = []
  sm_errors = []

  # 加载命令列表
  json_path = (
    "/home/hengdiye/tmp/slithIR_examples/solfuse/scripts/tmp/new_big/fine_fixing.json"
  )
  # json_path = "/home/hengdiye/tmp/slithIR_examples/solfuse/only_owners_deownered.json"
  # json_path = (
  #   "/home/hengdiye/tmp/slithIR_examples/solfuse/only_owners_deaccesscontrol.json"
  # )
  with open(json_path, "r", encoding="utf-8") as f:
    commands = json.load(f)

  # 如果指定了状态机转换率阈值，过滤命令列表
  if min_transition_rate > 0 or max_transition_rate is not None:
    filtered_commands, filtered_count = filter_transition_rate_samples(
      commands, min_transition_rate, max_transition_rate
    )

    # 展示过滤信息
    filter_info = []
    if filtered_count["low_rate"] > 0:
      filter_info.append(
        f"{filtered_count['low_rate']} 个转换率低于 {min_transition_rate}% 的样例"
      )
    if filtered_count["high_rate"] > 0:
      filter_info.append(
        f"{filtered_count['high_rate']} 个转换率高于 {max_transition_rate}% 的样例"
      )

    if filter_info:
      console.print(
        f"[bold yellow]已过滤 {filtered_count['total']} 个样例：{', '.join(filter_info)}[/]"
      )

    commands = filtered_commands

  # 如果指定了limit参数，显示限制信息
  if limit:
    if isinstance(limit, str) and limit.endswith("%"):
      console.print(f"[bold yellow]限制运行命令数量: 原始命令的 {limit}[/]")
    else:
      console.print(f"[bold yellow]限制运行命令数量: {limit} 条命令[/]")

  # 设置默认的only_owners文件路径
  if only_owners_json is None and skip_only_owners:
    only_owners_json = "/home/hengdiye/tmp/slithIR_examples/solfuse/only_owners.json"

  # 准备带有种子的命令
  normal_cmds, sm_cmds, cmd_pairs, cmd_seeds = prepare_commands_with_seeds(
    commands, global_seed, limit
  )

  # 如果指定了跳过只有owner能操作的合约，过滤命令列表
  if skip_only_owners and only_owners_json:
    owner_only_commands = load_only_owners(only_owners_json)
    if owner_only_commands:
      # 过滤普通命令
      original_normal_count = len(normal_cmds)
      filtered_normal_cmds = []

      for cmd in normal_cmds:
        should_keep = True
        for owner_cmd in owner_only_commands:
          if owner_cmd in cmd:
            should_keep = False
            break
        if should_keep:
          filtered_normal_cmds.append(cmd)

      normal_cmds = filtered_normal_cmds
      filtered_normal_count = original_normal_count - len(normal_cmds)

      # 过滤state machine命令
      original_sm_count = len(sm_cmds)
      filtered_sm_cmds = []

      for cmd in sm_cmds:
        should_keep = True
        for owner_cmd in owner_only_commands:
          if owner_cmd in cmd:
            should_keep = False
            break
        if should_keep:
          filtered_sm_cmds.append(cmd)

      sm_cmds = filtered_sm_cmds
      filtered_sm_count = original_sm_count - len(sm_cmds)

      # 更新配对关系和种子信息
      cmd_pairs = {
        k: v for k, v in cmd_pairs.items() if k in normal_cmds or k in sm_cmds
      }
      cmd_seeds = {
        k: v for k, v in cmd_seeds.items() if k in normal_cmds or k in sm_cmds
      }

      # 输出过滤信息
      if filtered_normal_count > 0 or filtered_sm_count > 0:
        console.print(
          f"[bold yellow]已过滤 {filtered_normal_count} 个普通命令和 {filtered_sm_count} 个State Machine命令（只有owner能操作的合约）[/]"
        )

  # 如果指定了跳过低性能样例，加载已知的低性能样例并过滤命令列表
  if skip_low_perf and low_perf_json:
    low_perf_commands, original_data = load_low_perf_samples(low_perf_json)
    if low_perf_commands:
      # 过滤普通命令
      original_normal_count = len(normal_cmds)
      normal_cmds = [
        cmd
        for cmd in normal_cmds
        if " ".join(cmd.split()[:-2]) not in low_perf_commands
      ]
      filtered_normal_count = original_normal_count - len(normal_cmds)

      # 过滤state machine命令
      original_sm_count = len(sm_cmds)
      sm_cmds = [
        cmd for cmd in sm_cmds if " ".join(cmd.split()[:-2]) not in low_perf_commands
      ]
      filtered_sm_count = original_sm_count - len(sm_cmds)

      # 更新配对关系和种子信息
      cmd_pairs = {
        k: v for k, v in cmd_pairs.items() if k in normal_cmds or k in sm_cmds
      }
      cmd_seeds = {
        k: v for k, v in cmd_seeds.items() if k in normal_cmds or k in sm_cmds
      }

      # 输出过滤信息
      if filtered_normal_count > 0 or filtered_sm_count > 0:
        console.print(
          f"[bold yellow]已过滤 {filtered_normal_count} 个普通命令和 {filtered_sm_count} 个State Machine命令（低性能样例）[/]"
        )

  # 在其他过滤完成后，只保留配对的命令
  original_normal_count = len(normal_cmds)
  original_sm_count = len(sm_cmds)
  normal_cmds, sm_cmds, filtered_count = filter_paired_commands_only(
    normal_cmds, sm_cmds, cmd_pairs
  )

  # 输出过滤信息
  if filtered_count["total"] > 0:
    console.print(
      f"[bold yellow]已过滤 {filtered_count['normal']} 个普通命令和 {filtered_count['state_machine']} 个State Machine命令（无法配对的命令）[/]"
    )

  # 更新命令配对关系和种子信息，确保只包含保留的命令
  cmd_pairs = {k: v for k, v in cmd_pairs.items() if k in normal_cmds or k in sm_cmds}
  cmd_seeds = {k: v for k, v in cmd_seeds.items() if k in normal_cmds or k in sm_cmds}

  total_normal = len(normal_cmds)
  total_sm = len(sm_cmds)
  total_commands = total_normal + total_sm

  console.print(
    f"[bold green]已准备 {total_normal} 个普通命令和 {total_sm} 个 state machine 命令[/]"
  )
  if global_seed is not None:
    console.print(f"[bold cyan]使用全局种子: {global_seed}[/]")

  # 检查是否存在中间结果，如果存在且resume=True则加载
  if resume and os.path.exists(intermediate_json):
    try:
      with open(intermediate_json, "r", encoding="utf-8") as f:
        intermediate_data = json.load(f)

      # 检查中间结果是否与当前限制条件兼容（命令数量相同）
      can_resume = True
      if (
        limit is not None
        and "normal" in intermediate_data
        and "state_machine" in intermediate_data
      ):
        saved_normal_count = len(
          intermediate_data["normal"].get("completed_commands", [])
        ) + len(intermediate_data["normal"].get("error_commands", []))
        saved_sm_count = len(
          intermediate_data["state_machine"].get("completed_commands", [])
        ) + len(intermediate_data["state_machine"].get("error_commands", []))

        # 如果保存的命令数量与当前准备的命令数量不一致，不进行恢复
        if saved_normal_count > total_normal or saved_sm_count > total_sm:
          can_resume = False
          console.print(
            "[bold red]中间结果与当前限制条件不兼容（保存的命令数量多于当前设置），不进行恢复[/]"
          )

      if (
        can_resume
        and "status" in intermediate_data
        and intermediate_data["status"] == "intermediate"
      ):
        if "normal" in intermediate_data:
          normal_completed = intermediate_data["normal"].get("completed_commands", [])
          normal_stats = intermediate_data["normal"].get("raw_data", normal_stats)
          normal_detailed = intermediate_data["normal"].get("detailed_results", {})
          normal_errors = intermediate_data["normal"].get("error_commands", [])

        if "state_machine" in intermediate_data:
          sm_completed = intermediate_data["state_machine"].get(
            "completed_commands", []
          )
          sm_stats = intermediate_data["state_machine"].get("raw_data", sm_stats)
          sm_detailed = intermediate_data["state_machine"].get("detailed_results", {})
          sm_errors = intermediate_data["state_machine"].get("error_commands", [])

        console.print(
          f"[bold yellow]从上次中断处恢复，已完成 {len(normal_completed) + len(sm_completed)}/{total_commands} 个命令，"
          f"出错 {len(normal_errors) + len(sm_errors)} 个命令[/]"
        )
    except Exception as e:
      console.print(f"[bold red]加载中间结果失败: {e}[/]")

  # 定义信号处理函数来优雅地处理中断
  def signal_handler(sig, frame):
    console.print("\n[bold yellow]接收到中断信号，正在保存中间结果...[/]")

    # 创建包含两种命令类型的中间结果
    combined_results = {
      "status": "intermediate",
      "limit_used": limit,
      "normal": {
        "completed_commands": normal_completed,
        "raw_data": normal_stats,
        "detailed_results": normal_detailed,
        "error_commands": normal_errors,
      },
      "state_machine": {
        "completed_commands": sm_completed,
        "raw_data": sm_stats,
        "detailed_results": sm_detailed,
        "error_commands": sm_errors,
      },
      "cmd_pairs": cmd_pairs,
      "cmd_seeds": cmd_seeds,
      "global_seed": global_seed,
    }

    # 保存到文件
    os.makedirs(os.path.dirname(intermediate_json), exist_ok=True)
    with open(intermediate_json, "w", encoding="utf-8") as f:
      json.dump(combined_results, f, indent=2, ensure_ascii=False)

    console.print(f"[bold green]中间结果已保存至: [/][blue]{intermediate_json}[/]")
    sys.exit(0)

  # 注册信号处理器
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  # 首先执行普通命令
  console.print("\n[bold cyan]===== 执行普通命令 =====[/]")
  normal_stats, normal_completed, normal_detailed, normal_errors = run_commands(
    normal_cmds,
    normal_stats,
    normal_completed,
    normal_detailed,
    error_cmds=normal_errors,
    max_workers=max_workers,
    save_interval=save_interval,
    intermediate_json=intermediate_json,
    total_commands=total_commands,
    console=console,
    start_time=start_time,
    cmd_seeds=cmd_seeds,
    max_retries=max_retries,  # 传递重试参数
  )

  # 接着执行state machine命令（如果需要比较）
  if compare_state_machine and sm_cmds:
    console.print("\n[bold cyan]===== 执行State Machine命令 =====[/]")
    sm_stats, sm_completed, sm_detailed, sm_errors = run_commands(
      sm_cmds,
      sm_stats,
      sm_completed,
      sm_detailed,
      error_cmds=sm_errors,
      max_workers=max_workers,
      save_interval=save_interval,
      intermediate_json=intermediate_json,
      total_commands=total_commands,
      console=console,
      start_time=start_time,
      cmd_seeds=cmd_seeds,
      max_retries=max_retries,  # 传递重试参数
    )

  # 计算总运行时间
  total_runtime = time() - start_time

  # 计算两种方法的统计摘要
  normal_summary = calculate_stats_summary(normal_stats)
  sm_summary = calculate_stats_summary(sm_stats)

  # 比较两种方法的结果
  comparison = {}
  if compare_state_machine and normal_summary and sm_summary:
    comparison = compare_stats(normal_summary, sm_summary)

  # 创建最终结果字典
  result_stats = {
    "status": "completed",
    "parallel_runtime_seconds": round(total_runtime, 2),
    "global_seed_used": global_seed,
    "limit_used": limit,
    "max_retries_used": max_retries,
    "seeds": {
      "used_seeds": list(set(cmd_seeds.values())),  # 所有使用的独特种子列表
      "cmd_seeds": cmd_seeds,  # 保存每个命令使用的种子
    },
    "normal": {
      **normal_summary,
      "raw_data": normal_stats,
      "error_count": len(normal_errors),
    },
  }

  if compare_state_machine and sm_cmds:
    result_stats["state_machine"] = {
      **sm_summary,
      "raw_data": sm_stats,
      "error_count": len(sm_errors),
    }

    if comparison:
      result_stats["comparison"] = comparison

  # 创建并保存出错样例详细信息
  error_samples = {
    "global_seed": global_seed,
    "normal": {
      cmd: normal_detailed[cmd] for cmd in normal_errors if cmd in normal_detailed
    },
    "state_machine": {cmd: sm_detailed[cmd] for cmd in sm_errors if cmd in sm_detailed},
    "cmd_seeds": {
      cmd: cmd_seeds.get(cmd) for cmd in set(normal_errors).union(set(sm_errors))
    },
  }

  # 保存出错样例到文件
  with open(output_error_json, "w", encoding="utf-8") as f:
    json.dump(error_samples, f, indent=2, ensure_ascii=False)

  console.print(
    f"[bold green]出错样例详细信息已保存至:[/] [blue]{output_error_json}[/]"
  )

  # 使用Rich创建美观的表格展示统计结果
  console.print("\n[bold green]===== 执行统计结果 =====[/]")

  # 显示使用的全局种子和限制条件
  if global_seed is not None:
    console.print(f"[bold cyan]使用全局种子: [/][green]{global_seed}[/]")

  if limit:
    console.print(f"[bold cyan]命令限制条件: [/][yellow]{limit}[/]")

  # 显示使用的独特种子数量
  unique_seeds = len(set(cmd_seeds.values()))
  console.print(f"[bold cyan]使用的独特种子数量: [/][green]{unique_seeds}[/]")

  # 普通命令结果表格
  if normal_summary:
    normal_table = Table(title="普通命令执行统计")
    normal_table.add_column("指标", style="cyan")
    normal_table.add_column("值", style="green")

    for key, value in normal_summary.items():
      normal_table.add_row(key.replace("_", " ").title(), f"{value}")

    # 添加出错统计
    normal_table.add_row("出错命令数", f"[red]{len(normal_errors)}[/]")

    console.print(Panel(normal_table, border_style="blue"))

  # State Machine命令结果表格
  if sm_summary:
    sm_table = Table(title="State Machine命令执行统计")
    sm_table.add_column("指标", style="cyan")
    sm_table.add_column("值", style="green")

    for key, value in sm_summary.items():
      sm_table.add_row(key.replace("_", " ").title(), f"{value}")

    # 添加出错统计
    sm_table.add_row("出错命令数", f"[red]{len(sm_errors)}[/]")

    console.print(Panel(sm_table, border_style="blue"))

  # 比较结果表格
  if comparison:
    compare_table = Table(title="普通命令 vs State Machine命令比较")
    compare_table.add_column("指标", style="cyan")
    compare_table.add_column("普通命令", style="yellow")
    compare_table.add_column("State Machine", style="yellow")
    compare_table.add_column("差异", style="magenta")
    compare_table.add_column("变化百分比", style="magenta")

    for key, values in comparison.items():
      if key != "command_count":
        # 根据是否有改进选择颜色
        diff_style = "green" if values["is_improvement"] else "red"
        percent_text = f"{values['percent_change']}%"
        if values["is_improvement"]:
          percent_text = (
            f"[green]+{percent_text}[/]"
            if values["percent_change"] > 0
            else f"[green]{percent_text}[/]"
          )
        else:
          percent_text = f"[red]{percent_text}[/]"

        compare_table.add_row(
          key.replace("_", " ").title(),
          f"{values['normal']}",
          f"{values['state_machine']}",
          f"[{diff_style}]{values['difference']}[/]",
          percent_text,
        )
      else:
        # 命令数量单独处理，没有改进概念
        compare_table.add_row(
          key.replace("_", " ").title(),
          f"{values['normal']}",
          f"{values['state_machine']}",
          f"{values['difference']}",
          "N/A",
        )

    console.print(Panel(compare_table, title="[bold]比较分析[/]", border_style="blue"))

  # 分析每个样例的表现
  if compare_state_machine and normal_detailed and sm_detailed:
    console.print("\n[bold cyan]===== 分析样例表现 =====[/]")
    worse_samples, better_samples = analyze_command_performance(
      normal_detailed, sm_detailed, cmd_pairs, cmd_seeds
    )

    # 添加全局种子信息到样例分析结果
    worse_samples_with_seeds = {
      "global_seed": global_seed,
      "samples": worse_samples,
      "count": len(worse_samples),
    }

    better_samples_with_seeds = {
      "global_seed": global_seed,
      "samples": better_samples,
      "count": len(better_samples),
    }

    # 保存表现较差的样例
    with open(output_worse_json, "w", encoding="utf-8") as f:
      json.dump(worse_samples_with_seeds, f, indent=2, ensure_ascii=False)
    console.print(
      f"[bold yellow]发现 {len(worse_samples)} 个State Machine表现较差的样例，已保存至:[/] [blue]{output_worse_json}[/]"
    )

    # 保存表现较好的样例
    with open(output_better_json, "w", encoding="utf-8") as f:
      json.dump(better_samples_with_seeds, f, indent=2, ensure_ascii=False)
    console.print(
      f"[bold green]发现 {len(better_samples)} 个State Machine表现较好的样例，已保存至:[/] [blue]{output_better_json}[/]"
    )

    # 创建并保存排序后的性能比较结果
    console.print("\n[bold magenta]===== 生成排序后的性能比较结果 =====[/]")
    sorted_results_json = output_json.replace(".json", "_sorted_comparison.json")
    sorted_results = generate_sorted_performance_comparison(
      normal_detailed, sm_detailed, cmd_pairs, cmd_seeds, sorted_results_json
    )
    console.print(
      f"[bold green]排序后的性能比较结果已保存至:[/] [blue]{sorted_results_json}[/]"
    )

    # 生成性能比较的散点图
    console.print("\n[bold magenta]===== 生成性能比较散点图 =====[/]")
    charts_dir = os.path.join(
      os.path.dirname(output_json), f"performance_charts_{timestamp}"
    )
    plot_performance_comparisons(
      sorted_results,
      charts_dir,
      skip_only_owners=skip_only_owners,  # 传递是否跳过onlyOwner参数
      min_transition_rate=min_transition_rate,  # 传递最小转换率
      max_transition_rate=max_transition_rate,  # 传递最大转换率
    )
    console.print(f"[bold green]性能比较散点图已保存至:[/] [blue]{charts_dir}[/]")

  # 查找低性能样例
  console.print("\n[bold yellow]===== 分析低性能样例 =====[/]")

  # 收集普通命令中的低性能样例
  normal_low_perf = find_low_performance_samples(
    normal_detailed, cmd_seeds, low_perf_threshold
  )

  # 收集state machine命令中的低性能样例（如果启用了比较）
  sm_low_perf = []
  if compare_state_machine:
    sm_low_perf = find_low_performance_samples(
      sm_detailed, cmd_seeds, low_perf_threshold
    )

  # 合并所有低性能样例
  new_low_perf_samples = {
    "global_seed": global_seed,
    "threshold": low_perf_threshold,
    "normal_command_samples": normal_low_perf,
    "normal_count": len(normal_low_perf),
    "state_machine_samples": sm_low_perf,
    "state_machine_count": len(sm_low_perf),
  }

  # 检查是否存在现有的低性能样例文件，如果有则合并
  existing_low_perf_commands, existing_low_perf_data = load_low_perf_samples(
    output_low_perf_json
  )

  if existing_low_perf_data:
    console.print("[bold yellow]在现有的低性能样例基础上添加新发现的低性能样例[/]")
    merged_low_perf_samples = merge_low_perf_samples(
      existing_low_perf_data, new_low_perf_samples
    )
    low_perf_samples = merged_low_perf_samples
  else:
    low_perf_samples = new_low_perf_samples

  # 保存低性能样例到文件
  with open(output_low_perf_json, "w", encoding="utf-8") as f:
    json.dump(low_perf_samples, f, indent=2, ensure_ascii=False)

  console.print(
    f"[bold yellow]总计: {low_perf_samples['normal_count']} 个普通命令低性能样例，"
    f"{low_perf_samples['state_machine_count']} 个State Machine低性能样例，已保存至:[/] [blue]{output_low_perf_json}[/]"
  )

  # 查找revert率减少幅度较大的样例
  console.print("\n[bold green]===== 分析revert率减少幅度较大的样例 =====[/]")
  high_reduction_samples, high_reduction_stats = filter_high_revert_reduction_samples(
    normal_detailed, sm_detailed, cmd_pairs, cmd_seeds, threshold=20.0
  )

  # 输出revert率减少幅度较大的样例列表
  with open(output_high_reduction_json, "w", encoding="utf-8") as f:
    json.dump(
      {
        "threshold": 20.0,
        "samples": high_reduction_samples,
        "stats_summary": high_reduction_stats,
      },
      f,
      indent=2,
      ensure_ascii=False,
    )

  console.print(
    f"[bold green]发现 {len(high_reduction_samples)} 个revert率减少超过20%的样例，已保存至:[/] [blue]{output_high_reduction_json}[/]"
  )

  # 输出这些样例的统计摘要
  high_reduction_table = Table(title="revert率减少幅度较大样例统计摘要")
  high_reduction_table.add_column("指标", style="cyan")
  high_reduction_table.add_column("值", style="green")

  for key, value in high_reduction_stats.items():
    high_reduction_table.add_row(key.replace("_", " ").title(), f"{value}")

  console.print(Panel(high_reduction_table, border_style="blue"))

  # 保存最终结果到 JSON 文件
  with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result_stats, f, indent=2, ensure_ascii=False)

  console.print(f"[bold green]统计数据已保存至:[/] [blue]{output_json}[/]")

  # 保存比较结果为Markdown
  if comparison:
    save_comparison_markdown(
      comparison,
      normal_summary,
      sm_summary,
      total_runtime,
      output_markdown,
      global_seed,
      skip_only_owners=skip_only_owners,  # 传递是否跳过onlyOwner参数
      min_transition_rate=min_transition_rate,  # 传递最小转换率
      max_transition_rate=max_transition_rate,  # 传递最大转换率
    )
    console.print(
      f"[bold green]比较结果已保存为Markdown格式:[/] [blue]{output_markdown}[/]"
    )

  # 如果所有任务已完成，删除中间结果文件
  if (
    os.path.exists(intermediate_json)
    and len(normal_completed) + len(normal_errors) == total_normal
    and (not compare_state_machine or len(sm_completed) + len(sm_errors) == total_sm)
  ):
    try:
      os.remove(intermediate_json)
      console.print("[dim]所有命令已完成，中间结果文件已删除[/]")
    except:
      pass

  return result_stats


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="批量运行echidna命令并收集统计数据")
  parser.add_argument("--output", "-o", help="输出JSON文件路径")
  parser.add_argument("--workers", "-w", type=int, help="最大线程数")
  parser.add_argument(
    "--interval",
    "-i",
    type=int,
    default=10,
    help="中间结果保存间隔（完成多少个命令保存一次）",
  )
  parser.add_argument("--no-resume", action="store_true", help="不从上次中断处恢复")
  parser.add_argument("--no-sm", action="store_true", help="不执行state machine命令")
  parser.add_argument("--seed", type=int, help="全局随机数种子")
  parser.add_argument(
    "--limit", "-l", help="限制运行的命令数量，可以是具体数字或百分比（如'10%'）"
  )
  parser.add_argument(
    "--low-perf",
    type=float,
    default=2000.0,  # 修改默认阈值为2000.0
    help="设置低性能样例的calls/sec阈值（默认2000.0）",
  )
  parser.add_argument(
    "--skip-low-perf",
    action="store_true",
    help="跳过已知的低性能样例",
  )
  parser.add_argument(
    "--low-perf-json",
    help="包含低性能样例信息的JSON文件路径",
  )
  parser.add_argument(
    "--skip-only-owners",
    action="store_true",
    help="跳过只有owner能操作的合约",
  )
  parser.add_argument(
    "--only-owners-json",
    help="包含只有owner能操作合约信息的JSON文件路径",
  )
  parser.add_argument(
    "--retries", type=int, default=0, help="命令失败后的最大重试次数（默认为0，不重试）"
  )
  parser.add_argument(
    "--min-transition-rate",
    type=float,
    default=3.0,
    help="过滤掉状态机转换率低于此阈值的样例（默认3%）",
  )
  parser.add_argument(
    "--max-transition-rate",
    type=float,
    help="过滤掉状态机转换率高于此阈值的样例",
  )

  args = parser.parse_args()

  # 处理limit参数
  limit_value = args.limit
  if limit_value and not limit_value.endswith("%"):
    try:
      limit_value = int(limit_value)
    except ValueError:
      print(f"警告：无效的limit值 '{limit_value}'，将使用所有命令")
      limit_value = None

  batch_run_echidna(
    output_json=args.output,
    max_workers=args.workers,
    save_interval=args.interval,
    resume=not args.no_resume,
    compare_state_machine=not args.no_sm,
    global_seed=args.seed,
    limit=limit_value,
    low_perf_threshold=args.low_perf,
    skip_low_perf=args.skip_low_perf,
    low_perf_json=args.low_perf_json,
    skip_only_owners=args.skip_only_owners,
    only_owners_json=args.only_owners_json,
    max_retries=args.retries,  # 使用命令行传入的重试次数
    min_transition_rate=args.min_transition_rate,  # 使用命令行传入的最小转换率阈值
    max_transition_rate=args.max_transition_rate,  # 传递最大转换率阈值
  )
