from copy import deepcopy
import json
from enum import Enum
from random import shuffle
from rich.progress import (
  Progress,
  SpinnerColumn,
  MofNCompleteColumn,
  TextColumn,
  TimeElapsedColumn,
)
import time
import statistics
import multiprocessing
from pathlib import Path
import subprocess
import sys
from sys import stderr, stdout, version
from typing import List, Literal, Self
from rich.progress import track
import solcix
from .buggy_files import buggy
from .failed import failed
import solfuse.solfuse_ir.utils
import os


class ErrorCode(Enum):
  FAILED = 1
  TIMEOUT = 124
  CONTRACT_NOT_UNIQUE = 115
  COMPILE_ERROR = 116
  MUTUALLY_RECURSIVE_TYPE = 117

  @classmethod
  def _missing_(self, value):
    return ErrorCode.FAILED


def parse_and_calculate_statistics(json_files):
  total_deleted_paths = {}  # 总的删除路径数
  total_transition_reduction_rate = 0
  count = 0
  positive_reduction_count = 0  # 统计转换减少率大于0的样例个数
  positive_reduction_rates = []  # 存储转换减少率大于0的样例的转换减少率
  positive_deleted_paths_per_length = {}  # 存储每个长度的删除路径数列表
  positive_files = []
  black_hole_cnt = 0
  black_hole_avg = 0
  black_hole_max = 0
  black_hole_min = 0
  black_hole_total = 0

  for json_file in json_files:
    if not os.path.exists(json_file):
      continue  # 如果文件不存在，跳过
    try:
      with open(json_file, "r") as f:
        data = json.load(f)
        # 提取删除路径数
        deleted_paths = data.get("deleted_paths", {})
        src_file_path = data.get("file_path", "")
        solc_path = data.get("solc_path", "")
        contract = data.get("contract")
        black_hole = data.get("black_holes", [])
        # 提取状态机转换减少率
        state_comparison = data.get("state_comparison", {})
        transition_reduction_rate = state_comparison.get("transition_reduction_rate", 0)
        if transition_reduction_rate > 0:
          # 对于转换减少率大于0的样例，收集删除路径数
          positive_files.append(
            {
              "src_file_path": src_file_path,
              "json_file_path": json_file,
              "solc_path": solc_path,
              "contract": contract,
            }
          )
          black_hole_cnt += 1
          black_hole_total += len(black_hole)
          black_hole_avg += len(black_hole)
          black_hole_max = max(black_hole_max, len(black_hole))
          black_hole_min = min(black_hole_min, len(black_hole))
          for key, value in deleted_paths.items():
            # 累加总的删除路径数
            total_deleted_paths[key] = total_deleted_paths.get(key, 0) + value
            # 在对应列表中添加删除路径数
            if key not in positive_deleted_paths_per_length:
              positive_deleted_paths_per_length[key] = []
            positive_deleted_paths_per_length[key].append(value)
          positive_reduction_rates.append(transition_reduction_rate)
          positive_reduction_count += 1
        else:
          # 即使转换减少率不大于0，也要累加总的删除路径数
          for key, value in deleted_paths.items():
            total_deleted_paths[key] = total_deleted_paths.get(key, 0) + value
        total_transition_reduction_rate += transition_reduction_rate
        count += 1
    except Exception as e:
      print(f"解析文件 {json_file} 时发生错误：{e}")
      continue

  # 计算平均值（仅针对转换率大于0的样例）
  if positive_reduction_count > 0:
    average_deleted_paths = {
      key: sum(values) / positive_reduction_count
      for key, values in positive_deleted_paths_per_length.items()
    }
    average_transition_reduction_rate = (
      total_transition_reduction_rate / positive_reduction_count
    )
  else:
    average_deleted_paths = {}
    average_transition_reduction_rate = 0

  # 计算中位数、最大值、最小值（按长度区分，仅针对转换减少率大于0的样例）
  median_deleted_paths_per_length = {}
  max_deleted_paths_per_length = {}
  min_deleted_paths_per_length = {}
  for key, values in positive_deleted_paths_per_length.items():
    median_deleted_paths_per_length[key] = statistics.median(values)
    max_deleted_paths_per_length[key] = max(values)
    min_deleted_paths_per_length[key] = min(values)

  # 计算转换减少率的中位数、最大值、最小值
  if positive_reduction_count > 0:
    median_transition_reduction_rate = statistics.median(positive_reduction_rates)
    max_transition_reduction_rate = max(positive_reduction_rates)
    min_transition_reduction_rate = min(positive_reduction_rates)
  else:
    median_transition_reduction_rate = 0
    max_transition_reduction_rate = 0
    min_transition_reduction_rate = 0

  black_hole_avg /= black_hole_cnt if black_hole_cnt > 0 else 1

  # 输出结果
  print("\n===== 测试结果统计 =====")
  print(f"处理的样例个数: {count}")
  print("平均删除路径数:")
  for key, value in average_deleted_paths.items():
    print(f"{key}: {value:.2f}")
  print(f"平均状态机转换减少率: {average_transition_reduction_rate:.2f}%")
  print(f"状态机转换减少率大于0的样例个数: {positive_reduction_count}")
  print("\n删除路径数按长度统计（仅针对转换减少率大于0的样例）：")
  for key in positive_deleted_paths_per_length.keys():
    median_value = median_deleted_paths_per_length.get(key, 0)
    max_value = max_deleted_paths_per_length.get(key, 0)
    min_value = min_deleted_paths_per_length.get(key, 0)
    print(f"{key} - 中位数: {median_value}, 最大值: {max_value}, 最小值: {min_value}")
  print(f"存在黑洞黑洞样例个数: {black_hole_total}")
  print(f"平均黑洞个数: {black_hole_avg}")
  print(f"最大黑洞个数: {black_hole_max}")
  print(f"最小黑洞个数: {black_hole_min}")
  print("\n转换减少率统计（仅针对转换减少率大于0的样例）：")
  print(
    f"转换减少率 - 中位数: {median_transition_reduction_rate:.2f}%, 最大值: {max_transition_reduction_rate:.2f}%, 最小值: {min_transition_reduction_rate:.2f}%"
  )

  return positive_files


def run_testcase(args, quiet: bool = False):
  if quiet:
    exit(
      subprocess.run(
        args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
      ).returncode
    )
  # exit(subprocess.run(args, stdout=subprocess.DEVNULL).returncode)
  exit(subprocess.run(args).returncode)


def copy_files_to_directory(files, target_dir: Path | str):
  import os
  import shutil

  # Check if the target directory exists, if not, create it
  if not os.path.exists(target_dir):
    os.makedirs(target_dir)

  # Copy each file to the target directory
  for file in files:
    if os.path.exists(Path(target_dir) / (file.name)):
      continue
    shutil.copy(file, target_dir)
    # print(f"Copied {file} to {target_dir}")


def make_success_or_fail_file(target_dir: Path, success: bool):
  fail_file = target_dir / "fail"
  success_file = target_dir / "success"
  if success:
    if fail_file.exists():
      fail_file.unlink()
    success_file.touch()
  else:
    if success_file.exists():
      success_file.unlink()
    fail_file.touch()


if __name__ == "__main__":
  import argparse
  import os

  parser = argparse.ArgumentParser()
  parser.add_argument("dir", type=str)
  parser.add_argument("--cont", "-c", action="store_true", default=False)
  parser.add_argument("--die_into_pdb", default=False, action="store_true")
  parser.add_argument("-f", "--file", type=str, default="")
  parser.add_argument("-t", "--timeout", type=str, default="1m")
  parser.add_argument("--use_timeout", default=False, action="store_true")
  parser.add_argument("-q", "--quiet", action="store_true", default=False)
  parser.add_argument("--iter_fail", default=False, action="store_true")
  parser.add_argument("--buggy_file", type=str, default="./buggy.py")
  parser.add_argument("--failed_file", type=str, default="./failed.py")
  parser.add_argument("--list_buggy", action="store_true", default=False)
  parser.add_argument("--list_failed", action="store_true", default=False)
  parser.add_argument("--iter_count", type=int, default=-1)
  parser.add_argument("--clear_flags", action="store_true")
  parser.add_argument("--ignore_fail", action="store_true")
  parser.add_argument("--ignore_buggy", action="store_true")
  parser.add_argument("--use_new_big_id_and_contract", action="store_true")
  parser.add_argument(
    "--output_dir", type=str, default=".", help="指定 positive_files.json 输出的文件夹"
  )
  parser.add_argument(
    "--use_json", action="store_true", default=False, help="使用 JSON 文件作为输入"
  )
  parser.add_argument(
    "--no_include_state_machine",
    action="store_true",
    default=False,
    help="如果设置，则不将 state_machine_id_and_contract 合并到 id_and_contract 中",
  )
  parser.add_argument(
    "--only_state_machine",
    action="store_true",
    default=False,
    help="如果设置，则只使用 state_machine_id_and_contract",
  )

  parser = parser.parse_args()

  count = parser.iter_count

  fail_out = stdout
  if parser.list_failed:
    fail_out = open(parser.failed_file, mode="w")
    fail_out.write("failed = [\n")
    fail_out.flush()

  # * output to a file for me to paste into buggy_files.py
  with open(parser.buggy_file, mode="w") as buggyf:
    buggyf.write(f"buggy = {{\n")
    buggyf.flush()
    if parser.cont:
      import random

      random.seed(time.time())
    if not parser.cont:
      sys.excepthook = solfuse.solfuse_ir.utils.custom_exception_handler
    solc_dict = None
    dir = parser.dir
    # from .cgt_id_and_contract_dict import id_and_contract
    from .state_machine_id_and_contract_dict import (
      state_machine_id_and_contract,
    )

    # from .modified_contracts_dict import modified_contracts_dict as id_and_contract
    from .cgt_id_and_contract_dict import id_and_contract as id_and_contract
    from .new_big_id_and_contract_dict import (
      new_big_id_and_contract,
      new_big_id_and_contract_solc,
    )

    if parser.use_new_big_id_and_contract:
      id_and_contract = new_big_id_and_contract
      solc_dict = new_big_id_and_contract_solc
    elif parser.only_state_machine:
      id_and_contract = state_machine_id_and_contract
    elif not parser.no_include_state_machine:
      id_and_contract.update(state_machine_id_and_contract)

    current_process_list: List[multiprocessing.Process] = []
    current_process_cnt = 0
    run_cnt = 0
    success_cnt = 0
    mutually_recursive_error = 0
    if parser.file:
      itering = [Path(parser.file)]
    else:
      itering = list(
        filter(
          lambda x: x.is_file()
          and (
            (x.stem in id_and_contract.keys())
            and x.name
            not in (set() if parser.ignore_buggy else buggy).union(
              {} if parser.ignore_fail else failed
            )
          ),
          Path(dir).iterdir(),
        )
      )
      if parser.iter_fail:
        itering = list(filter(lambda x: x.name in failed, itering))
    if count > 0:
      itering = itering[:count]

    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      MofNCompleteColumn(),
      TimeElapsedColumn(),
    ) as progress:
      json_files = []  # 用于保存所有生成的 JSON 文件路径
      pid_to_file: dict[int, Path] = {}
      if not parser.cont:
        progress.stop()
      task_testing = progress.add_task(
        description="[yellow]Testing...", total=len(itering)
      )
      success_testing = progress.add_task("[green]Success", total=len(itering))
      timeout_testing = progress.add_task("[red]Timeout", total=len(itering))
      current_process_testing = progress.add_task(
        "[green]Current Running", total=multiprocessing.cpu_count()
      )
      for file in itering:
        if file.is_file():
          import shutil
          import os

          # * Step 1: make a directory containing (1) file being tested; (2) .solcix file to guide version; (3) success/fail dummy file to speed up testing.
          target_dir = file.parent / file.stem
          os.makedirs(name=target_dir, exist_ok=True)
          copy_files_to_directory(files=[file], target_dir=target_dir)

          timestamp = time.strftime("%Y%m%d")
          output_file = os.path.join(
            target_dir, f"output_{timestamp}_{os.path.basename(file)}.json"
          )
          json_files.append(output_file)

          success_file = target_dir / "success"
          fail_file = target_dir / "fail"
          if parser.clear_flags:
            if success_file.exists():
              success_file.unlink()
            if fail_file.exists():
              fail_file.unlink()
          else:
            if success_file.exists():
              progress.update(success_testing, advance=1)
              continue

          # * Step 2: Prepare compiler
          if solc_dict is not None:
            solc_path = solc_dict.get(file.stem)
            if solc_path is None:
              print(f"{file.name}, # no compiler", file=buggyf)
              buggyf.flush()
              progress.update(task_testing, advance=1)
              continue
          else:
            version = solfuse.solfuse_ir.utils.ensure_version(file=file)
            try:
              if version is None:
                raise Exception(f"No version for file {file.name}, exiting...")
              solc_path = solcix.installer.get_executable(version=version)
            except:
              print(f"{file.name}, # no compiler", file=buggyf)
              buggyf.flush()
              progress.update(task_testing, advance=1)
              continue

          # * Step 3: Run program
          args = [
            "python",
            "-m",
            "solfuse.solfuse_ir",
            file.as_posix(),
            "/home/hengdiye/tmp/slithIR_examples/solfuse/images",
            id_and_contract[f"{file.stem}"],
            solc_path,
          ]
          if parser.use_timeout:
            args = ["timeout", parser.timeout] + args
          if not parser.cont:
            args.append("-d")
          if parser.die_into_pdb:
            args.append("--die_into_pdb")
          args.append("--out_stat_file")
          args.append(output_file)
          quiet = parser.quiet
          # if parser.use_timeout:
          process = multiprocessing.Process(target=run_testcase, args=[args, quiet])
          # else:
          # process = multiprocessing.Process(target=run_testcase, args=[['python', '-m', 'solfuse.solfuse_ir',
          # file.as_posix(), '/home/hengdiye/tmp/slithIR_examples/solfuse/images',  id_and_contract[f'{file.stem}'], solc_path] + (['-d'] if not parser.cont else []) + (['--die_into_pdb'] if parser.die_into_pdb else [])])
          while current_process_cnt >= multiprocessing.cpu_count():
            current_process_list_copy = []
            shrinked = False
            shuffle(current_process_list)
            for p in current_process_list:
              if p.exitcode is not None and not shrinked:
                p.join()
                progress.update(current_process_testing, advance=-1)
                current_process_cnt -= 1
                shrinked = True
                f, tgt_dir = pid_to_file[p.pid]
                make_success_or_fail_file(tgt_dir, success=p.exitcode == 0)
                if p.exitcode:
                  if not parser.cont:
                    exit(p.exitcode)
                  match ErrorCode(p.exitcode):
                    case ErrorCode.TIMEOUT:  # timeout
                      print(f'"{f.name}", # timeout', file=buggyf)
                      progress.update(timeout_testing, advance=1)
                    case ErrorCode.COMPILE_ERROR:
                      print(f'"{f.name}", # compile error', file=buggyf)
                    case ErrorCode.CONTRACT_NOT_UNIQUE:
                      print(f'"{f.name}", # with not unique contract', file=buggyf)
                    case ErrorCode.FAILED:
                      print(f'"{f.name}", ', file=fail_out, flush=True)
                    case ErrorCode.MUTUALLY_RECURSIVE_TYPE:
                      print(f'"{f.name}" failed with mutually recursive type')
                      mutually_recursive_error += 1
                  buggyf.flush()
                  fail_out.flush()
                else:
                  success_cnt += 1
                  progress.update(success_testing, advance=1)
                progress.update(task_testing, advance=1)
              else:
                current_process_list_copy.append(p)
            current_process_list = current_process_list_copy
          process.start()
          pid_to_file[process.pid] = file, deepcopy(target_dir)
          progress.update(current_process_testing, advance=1)
          current_process_list.append(process)
          run_cnt += 1
          current_process_cnt += 1
          if not parser.cont:
            process.join()
            progress.update(current_process_testing, advance=-1)
            current_process_cnt -= 1
            if not process.exitcode:
              progress.update(success_testing, advance=1)
              success_cnt += 1
            progress.update(task_id=task_testing, advance=1)
      for p in current_process_list:
        p.join()
        progress.update(task_testing, advance=1)
        progress.update(current_process_testing, advance=-1)
        f, tgt_dir = pid_to_file[p.pid]
        make_success_or_fail_file(tgt_dir, success=p.exitcode == 0)
        if not p.exitcode:
          success_cnt += 1
          progress.update(success_testing, advance=1)
        else:
          match ErrorCode(p.exitcode):
            case ErrorCode.TIMEOUT:  # timeout
              print(f"{f.name}, # timeout", file=buggyf)
              progress.update(timeout_testing, advance=1)
            case ErrorCode.COMPILE_ERROR:
              print(f"{f.name}, # compile error", file=buggyf)
            case ErrorCode.CONTRACT_NOT_UNIQUE:
              print(f"{f.name}, # with not unique contract", file=buggyf)
            case ErrorCode.FAILED:
              print(f'"{f.name}", ', file=fail_out)
            case ErrorCode.MUTUALLY_RECURSIVE_TYPE:
              print(f'"{f.name}" failed with mutually recursive type')
              print(f'"{f.name}", ', file=fail_out)
              mutually_recursive_error += 1
          buggyf.flush()
          fail_out.flush()
  if not parser.list_buggy:
    os.remove(parser.buggy_file)
  else:
    with open(parser.buggy_file, mode="a") as buggyf:
      buggyf.write("}\n")
  fail_out.write("]\n")
  if parser.list_failed:
    fail_out.close()
  print(f"{success_cnt} / {run_cnt} suceeded")
  print(f"{mutually_recursive_error} files failed with mutually recursive type")
  positive_files = parse_and_calculate_statistics(json_files)
  os.makedirs(parser.output_dir, exist_ok=True)
  output_path = os.path.join(parser.output_dir, "positive_files.json")
  with open(output_path, "w", encoding="utf8") as pf:
    json.dump(positive_files, pf, indent=2)
