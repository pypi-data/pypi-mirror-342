from pathlib import Path
from re import split
from subprocess import DEVNULL, PIPE
from rich import progress
from rich.progress import Progress, SpinnerColumn, TextColumn
from .modify_constructors import modify_one_contract
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import os  # 新增
import argparse  # 新增


def process_item(item):
  src_file_path = item["src_file_path"]
  json_file_path = item["json_file_path"]
  contract = item["contract"]
  command = item["command"]
  with open(json_file_path) as jf:
    thing = json.load(jf)
    no_elementary_cnt = int(thing["constructor_fail_reason"] != "")
  output_path = modify_one_contract(
    solidity_file=src_file_path, contract_name=contract, args_json=json_file_path
  )
  modify_command = f"python -m solfuse.tools.modify_constructors {src_file_path} {contract} {json_file_path}"
  new_item = {**item}
  new_item["modify_command"] = modify_command
  if not isinstance(output_path, Path):
    return "modifying_failed", {**new_item, "error": output_path}, no_elementary_cnt
  splited_command = command.split()
  new_command = " ".join(
    [splited_command[0], output_path.as_posix(), *splited_command[2:]]
  )
  new_command_state_machine = " ".join(
    [new_command, "--state-machine-json-file", json_file_path]
  )

  modifyed_item = item
  modifyed_item["src_file_path"] = output_path.as_posix()
  modifyed_item["command"] = new_command
  modifyed_item["command_state_machine"] = new_command_state_machine

  import tempfile

  with tempfile.TemporaryDirectory(dir="/tmp") as tempfilename:
    p = subprocess.run(
      args=f"{new_command} --disable-slither --timeout 1".split(),
      stderr=DEVNULL,
      stdout=DEVNULL,
      cwd=tempfilename,
    )

  if p.returncode != 0:
    return (
      "still_error_no_arg",
      {**modifyed_item, "error": str(p.stderr)},
      no_elementary_cnt,
    )
  else:
    return "fine", modifyed_item, no_elementary_cnt


def main():
  fine = []
  still_error_no_arg = []
  modifying_failed = []
  no_elementary_cnt = 0

  # 新增：从参数中获取输入与输出路径
  parser_arg = argparse.ArgumentParser(
    description="修改 Solidity 构造函数：移除参数列表，并添加状态变量初始化"
  )
  parser_arg.add_argument(
    "--no_arg_json",
    type=str,
    default="/home/hengdiye/tmp/slithIR_examples/solfuse/error_no_arg.json",
    help="指定 no_arg_json 的文件位置",
  )
  parser_arg.add_argument(
    "--fine_json",
    type=str,
    default="/home/hengdiye/tmp/slithIR_examples/solfuse/fine.json",
    help="指定 fine_json 的文件位置",
  )
  parser_arg.add_argument(
    "--output_dir", type=str, default=".", help="指定所有输出 JSON 的文件夹"
  )
  args = parser_arg.parse_args()

  # 将输出目录确保存在，并切换工作目录到该目录
  os.makedirs(args.output_dir, exist_ok=True)
  # 读取输入的no_arg_json来自参数
  no_arg_json = args.no_arg_json

  with open(no_arg_json, mode="r") as no_args:
    data = json.load(no_args)
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      task = progress.add_task(
        "[green]Fixing Echidna no-argument errors...", total=len(data)
      )
      with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_item, item) for item in data]
        for future in as_completed(futures):
          result_type, result_item, cnt = future.result()
          no_elementary_cnt += cnt
          if result_type == "fine":
            fine.append(result_item)
          elif result_type == "still_error_no_arg":
            still_error_no_arg.append(result_item)
          elif result_type == "modifying_failed":
            modifying_failed.append(result_item)
          progress.advance(task)

  print(f"{len(fine)} fine")
  print(f"{len(still_error_no_arg)} error in fuzzing")
  print(f"{len(modifying_failed)} failed to modify")

  # 修改读取 fine.json 的位置，从输出目录读取
  fine_json_path = os.path.join(args.output_dir, "fine.json")
  with open(fine_json_path, mode="r") as fj:
    thing = json.load(fj)
    fine.extend(thing)
  with open(os.path.join(args.output_dir, "fine_fixing.json"), "w") as ff:
    json.dump(fine, ff, ensure_ascii=False, indent=2)
  with open(os.path.join(args.output_dir, "err_still.json"), "w") as es:
    json.dump(still_error_no_arg, es, ensure_ascii=False, indent=2)
  with open(os.path.join(args.output_dir, "modifying_failed.json"), mode="w") as mf:
    json.dump(modifying_failed, mf, ensure_ascii=False, indent=2)
  print(len(fine))


if __name__ == "__main__":
  main()
