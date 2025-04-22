from curses.ascii import isascii
import json
import os
from pathlib import Path


# 读取 positive_files_state_machine.json
def transform_positive_files():
  # 获取脚本所在目录
  script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
  print("HERE?")
  # 读取正例文件
  try:
    with open(script_dir / "positive_files.json", "r", encoding="utf-8") as f:
      positive_files = json.load(f)["contracts"]
  except FileNotFoundError:
    print("Error: positive_files.json not found")
    return
  except json.JSONDecodeError:
    print("Error: Invalid JSON format in positive_files.json")
    return

  # 创建输出目录
  # output_dir = Path("/home/hengdiye/datasets/cgt/source/")
  # output_dir.mkdir(parents=True, exist_ok=True)

  # 统计计数器
  processed_contracts = 0
  saved_files = 0

  # 新建字典，不使用现有字典
  contract_address_to_name_map = {}
  solc_dict = {}

  # 遍历并处理每个合约
  for item in positive_files:
    if (
      "address" not in item
      or "contract_name" not in item
      or "compiler_path" not in item
    ):
      continue

    contract_address = item["address"].lower()
    contract_name: str = item["contract_name"]
    if not (contract_name.isascii() and contract_name.isalnum()):
      print(f"Invalid contract name: {contract_name}")
      continue
    solc_path = item["compiler_path"]
    # source_code = item["source_code"]

    # # 移除 0x 前缀
    # if contract_address.startswith("0x"):
    #   contract_address = contract_address[2:]

    # 添加到新字典
    if contract_address and contract_name:
      contract_address_to_name_map[contract_address] = contract_name
      processed_contracts += 1

    # 添加到 solc 字典
    if contract_address and solc_path:
      solc_dict[contract_address] = solc_path

    # # 保存源代码到文件
    # if contract_address and source_code:
    #   output_file = output_dir / f"{contract_address}.sol"
    #   with open(output_file, "w", encoding="utf-8") as f:
    #     f.write(source_code)
    #   saved_files += 1

  # 将新字典写入到新文件
  new_dict_file = script_dir / "new_big_id_and_contract_dict.py"
  with open(new_dict_file, "w", encoding="utf-8") as f:
    f.write("new_big_id_and_contract: dict[str, str] = {\n")
    for key, value in sorted(contract_address_to_name_map.items()):
      f.write(f'  "{key}": "{value}",\n')
    f.write("}\n")
    f.write("new_big_id_and_contract_solc: dict[str, str] = {\n")
    for key, value in sorted(solc_dict.items()):
      f.write(f'  "{key}": "{value}",\n')
    f.write("}\n")

  # print(
  #   f"Created new dictionary with {processed_contracts} contracts in state_machine_id_and_contract_dict.py"
  # )
  # print(f"Source code saved for {saved_files} files at {output_dir}")


if __name__ == "__main__":
  transform_positive_files()
