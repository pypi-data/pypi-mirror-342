from .common import ECHIDNA as ECHIDNA_EXE_DEFAULT
import json
import tempfile
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import track
import argparse  # 新增
import os  # 新增

care_error = "echidna: Constructor arguments are required:"


def run_echidna_verify(filepath: str, contract: str, solc_path: str, echidna_exe: str):
  with tempfile.TemporaryDirectory(dir="/tmp") as tmpdirname:
    p = subprocess.run(
      args=f"{echidna_exe} {filepath} --contract {contract} --test-mode exploration --format text --crytic-args --solc={solc_path} --timeout 1 --disable-slither".split(),
      stderr=subprocess.PIPE,
      stdout=subprocess.DEVNULL,
      cwd=tmpdirname,
    )
  return p


def process_item(item):
  filepath = item["src_file_path"]
  contract = item["contract"]
  solc_path = item["solc_path"]

  if "solc-0.4" in solc_path:
    solc_path = "/home/hengdiye/.solcix/artifacts/solc-0.4.25/solc-0.4.25"
    item["solc_path"] = solc_path

  # 使用全局ECHIDNA_EXE传入
  result = run_echidna_verify(
    filepath=filepath,
    contract=contract,
    solc_path=solc_path,
    echidna_exe=ECHIDNA_EXE_DEFAULT,
  )
  # 使用 join 组合 stderr 行，形成完整的错误信息
  errorout = "\n".join(result.stderr.decode().splitlines())
  command = " ".join(result.args[:-3])
  command_state_machine = " ".join(
    [command, "--state-machine-json-file", item["json_file_path"]]
  )
  item_updated = {
    **item,
    "command": command,
    "command_state_machine": command_state_machine,
  }
  if result.returncode != 0:
    if care_error in errorout:
      return "error_no_arg", item_updated
    else:
      return "other_error", {**item_updated, "error": errorout}
  else:
    return "fine", item_updated


def main():
  # 新增：参数解析
  parser = argparse.ArgumentParser(description="过滤可运行的 Echidna 测试")
  parser.add_argument(
    "--positive_files_json",
    type=str,
    default="/home/hengdiye/tmp/slithIR_examples/solfuse/positive_files.json",
    help="指定 positive_files.json 文件位置",
  )
  global ECHIDNA_EXE_DEFAULT
  parser.add_argument(
    "--echidna_exe",
    type=str,
    default=ECHIDNA_EXE_DEFAULT,
    help="指定 echidna 可执行文件路径",
  )
  parser.add_argument(
    "--output_dir", type=str, default=".", help="指定所有输出 JSON 文件的目录"
  )
  args = parser.parse_args()

  # 更新全局变量
  ECHIDNA_EXE_DEFAULT = args.echidna_exe

  fine = []
  error_no_arg = []
  other_error = []

  # 修改读取 positive_files.json位置
  with open(args.positive_files_json, "r") as positive_files:
    data = json.load(positive_files)

  # 使用 ThreadPoolExecutor 并发处理所有任务
  futures = []
  with ThreadPoolExecutor() as executor:
    for item in data:
      futures.append(executor.submit(process_item, item))

    # 利用 as_completed 遍历所有完成的 Future，同时利用 track 进度条显示
    for future in track(
      as_completed(futures), total=len(futures), description="Processing"
    ):
      result_type, result_item = future.result()
      if result_type == "fine":
        fine.append(result_item)
      elif result_type == "error_no_arg":
        error_no_arg.append(result_item)
      elif result_type == "other_error":
        other_error.append(result_item)

  # 输出 JSON 文件到指定文件夹
  os.makedirs(args.output_dir, exist_ok=True)
  with open(os.path.join(args.output_dir, "fine.json"), "w", encoding="utf8") as f:
    json.dump(fine, f, indent=2, ensure_ascii=False)
  with open(
    os.path.join(args.output_dir, "error_no_arg.json"), "w", encoding="utf8"
  ) as f:
    json.dump(error_no_arg, f, indent=2, ensure_ascii=False)
  with open(
    os.path.join(args.output_dir, "other_error.json"), "w", encoding="utf8"
  ) as f:
    json.dump(other_error, f, indent=2, ensure_ascii=False)

  print("fine:", len(fine))
  print("error_no_arg:", len(error_no_arg))
  print("other_error:", len(other_error))
  print("Fixing error_no_arg.json")


if __name__ == "__main__":
  main()
