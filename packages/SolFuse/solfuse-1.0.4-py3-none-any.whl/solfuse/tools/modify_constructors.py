from enum import Enum
from pathlib import Path
import sys
import argparse
import json
import re
from typing import List, Tuple
from tree_sitter import Node
from tree_sitter_language_pack import get_parser

from solfuse.solfuse_ir import indent_print


def generate_unique_name(original, contract_node, source_code):
  """
  根据目标合约中的已有标识符生成唯一的名称：
  初始 candidate 为 "_" + original；若存在冲突，则在后面添加 _<counter> 后缀。
  """
  contract_text = source_code[contract_node.start_byte : contract_node.end_byte]
  candidate = "_" + original
  counter = 0
  pattern = r"\b{}\b".format(re.escape(candidate))
  while re.search(pattern, contract_text):
    counter += 1
    candidate = "_" + original + "_" + str(counter)
    pattern = r"\b{}\b".format(re.escape(candidate))
  return candidate


def delete_all_comments(source_code):
  class ScanningState(Enum):
    NORMAL = 0
    SLASH = 1
    BLOCK_COMMENT = 2
    LINE_COMMENT = 3
    MAYBE_EXITING_BLOCK_COMMENT = 4
    STRING = 5

  state = ScanningState.NORMAL
  start = 0
  modifications: List[Tuple[int, int, str]] = []
  for i, c in enumerate(source_code):
    match c:
      case "/":
        match state:
          case ScanningState.NORMAL:
            state = ScanningState.SLASH
          case ScanningState.SLASH:
            state = ScanningState.LINE_COMMENT
            start = i - 1
          case ScanningState.MAYBE_EXITING_BLOCK_COMMENT:
            state = ScanningState.NORMAL
            modifications.append((start, i + 1, ""))
          case ScanningState.BLOCK_COMMENT:
            pass
          case ScanningState.LINE_COMMENT:
            pass
          case ScanningState.STRING:
            pass
        continue
      case "*":
        match state:
          case ScanningState.NORMAL:
            pass
          case ScanningState.SLASH:
            state = ScanningState.BLOCK_COMMENT
            start = i - 1
          case ScanningState.BLOCK_COMMENT:
            state = ScanningState.MAYBE_EXITING_BLOCK_COMMENT
          case ScanningState.LINE_COMMENT:
            pass
          case ScanningState.MAYBE_EXITING_BLOCK_COMMENT:
            pass
          case ScanningState.STRING:
            pass
        continue
      case "\n":
        match state:
          case ScanningState.LINE_COMMENT:
            state = ScanningState.NORMAL
            modifications.append((start, i + 1, ""))
          case _:
            pass
        continue
      case '"':
        match state:
          case ScanningState.NORMAL:
            state = ScanningState.STRING
          case ScanningState.STRING:
            state = ScanningState.NORMAL
          case _:
            pass
        continue
      case _:  # 其他字符
        match state:
          case ScanningState.SLASH:
            state = ScanningState.NORMAL
          case ScanningState.BLOCK_COMMENT:
            pass
          case ScanningState.LINE_COMMENT:
            pass
          case ScanningState.MAYBE_EXITING_BLOCK_COMMENT:
            state = ScanningState.BLOCK_COMMENT
          case _:
            pass
        continue
  modifications.sort(key=lambda x: x[0], reverse=True)
  for start, end, replacement in modifications:
    source_code = source_code[:start] + replacement + source_code[end:]
  return source_code


def modify_one_contract(solidity_file, contract_name, args_json, verbose=False):
  outfile = sys.stdout if verbose else open("/dev/null", "w")
  # 读取 Solidity 源码，使用 bytes 供 tree_sitter 解析，同时保留字符串形式用于文本操作
  with open(solidity_file, "rb") as f:
    source_code_bytes = f.read()
  source_code = source_code_bytes.decode("utf8")
  source_code = delete_all_comments(source_code)
  # 创建 parser 并解析
  solidity_parser = get_parser("solidity")
  tree = solidity_parser.parse(source_code_bytes)
  root_node: Node = tree.root_node
  source_code_bytes = bytes(source_code, encoding="utf8")
  tree = solidity_parser.parse(source_code_bytes)
  root_node = tree.root_node
  node_text = None
  # 定位目标合约，寻找类型为 contract_declaration 的节点，其 identifier 与目标名称匹配
  contract_node = None
  for child in root_node.children:
    if child.type == "contract_declaration":
      for n in child.children:
        if n.type == "identifier":
          node_text = source_code_bytes[n.start_byte : n.end_byte].decode("utf8")
          if node_text == contract_name:
            contract_node = child
            break
      if contract_node:
        break
  if not contract_node:
    return f"目标合约未找到: {contract_name} : {node_text}"
    return None

  # 在合约中寻找构造函数节点（这里假定类型为 constructor_definition）
  constructor_node = None
  contract_body_node = contract_node.child_by_field_name("body")
  for child in contract_body_node.children:
    if child.type == "constructor_definition":
      constructor_node = child
      break
    if child.type == "function_definition":
      for c in child.children:
        if c.type == "function" and c.next_sibling.type == "identifier":
          function_name_node = c.next_sibling
          function_name = source_code[
            function_name_node.start_byte : function_name_node.end_byte
          ]
          if function_name == contract_name:
            constructor_node = child
  if not constructor_node:
    return f"构造函数未找到: {solidity_file}:{contract_name}"
    return None

  modifications = []  # 记录文本修改 (start, end, replacement)
  # 1. 定位构造函数参数列表节点，并提取参数信息
  # 此处通过 children 索引获取左右括号节点
  lparam = None
  rparam = None
  for n in constructor_node.children:
    if n.type == "(":
      lparam = n
  if lparam is None:
    return "构造函数参数列表开头未找到"
    return None
  rparam = lparam
  while rparam.type != ")" and rparam.next_sibling is not None:
    rparam = rparam.next_sibling
  assert lparam.type == "(" and rparam.type == ")"
  if lparam.next_sibling is rparam:
    indent_print.indent_print("构造函数参数列表为空", file=outfile)
    return solidity_file

  # 参数列表的文本，例如 "(uint a, address b)"
  params_text = source_code[lparam.start_byte : rparam.end_byte]
  params_inside = params_text.strip()[1:-1].strip()  # 去除左右括号
  param_list = []  # 每项为 (参数类型, 参数名)
  if params_inside:
    for param in params_inside.split(","):
      param = param.strip()
      parts = param.split()
      if len(parts) >= 2:
        param_type = " ".join(parts[:-1])
        param_name = parts[-1]
        param_list.append((param_type, param_name))

  # 解析传入的构造函数参数值, 从 JSON 中取 "constructor_arguments" 字段
  with open(args_json) as f:
    parsed_args = json.load(f)
  if "constructor_arguments" not in parsed_args:
    return "JSON 中未包含 constructor_arguments 字段"
    # return None
  arg_values = parsed_args["constructor_arguments"]

  # 检查构造函数参数列表中的所有参数都在提供的 JSON 中
  for _, param_name in param_list:
    if param_name not in arg_values:
      return f"缺少构造函数参数: {param_name}"
      # breakpoint()
      # return None

  # 记录修改1：移除构造函数参数列表（替换为 "()"）
  modifications.append((lparam.start_byte, rparam.end_byte, "()"))

  # 2. 修改构造函数体，利用 generate_unique_name 为每个参数生成唯一新名称，并替换构造函数体中原有参数引用
  body_node = constructor_node.child_by_field_name("body")
  if not body_node:
    return "构造函数体未找到"
  body_text = source_code[body_node.start_byte : body_node.end_byte]
  new_body_text = body_text

  # 建立原参数与唯一新名称的映射关系
  rename_map = {}
  for _, param_name in param_list:
    unique_name = generate_unique_name(param_name, contract_node, source_code)
    rename_map[param_name] = unique_name
    new_body_text = re.sub(
      r"\b{}\b".format(re.escape(param_name)), unique_name, new_body_text
    )
  modifications.append((body_node.start_byte, body_node.end_byte, new_body_text))

  # 3. 在合约体内添加新的状态变量声明，使用新的唯一名称和对应的参数值
  contract_body_node = contract_node.child_by_field_name("body")
  if not contract_body_node:
    return "合约体未找到"
  insert_position = contract_body_node.start_byte + 1
  state_declarations = "\n"
  for param_type, param_name in param_list:
    new_name = rename_map[param_name]
    arg_value = arg_values[param_name]
    if isinstance(arg_value, str):
      arg_str = f'"{arg_value}"'
    else:
      arg_str = str(arg_value)
    if arg_str in ("True", "False"):
      arg_str = arg_str.lower()
    state_declarations += f"    {param_type if not param_type.startswith('string') else 'string'} public {new_name} = {param_type.split()[0] if not param_type.startswith('string') else ''}({arg_str});\n"

  # 修改构造函数中所有调用父类构造函数的表达式，将参数列表替换为 "()"
  modifications.append((insert_position, insert_position, state_declarations))
  modifications_modifier = modify_modifier_calls(
    source_code, constructor_node, rename_map
  )
  modifications.extend(modifications_modifier)
  # 按照偏移量从后到前应用所有修改，避免影响后续偏移量
  modifications.sort(key=lambda x: x[0], reverse=True)
  modified_source = source_code
  for start, end, replacement in modifications:
    modified_source = modified_source[:start] + replacement + modified_source[end:]

  # 修改所有调用指定合约构造函数的表达式，将构造函数参数列表移除（替换为空）
  modified_source = modify_constructor_calls(
    modified_source, solidity_parser, contract_name
  )

  # 输出修改后的 Solidity 文件，文件名前加 "Modified_"
  origin_path = Path(solidity_file)
  output_path = origin_path.parent / ("Modified_" + origin_path.name)
  with open(output_path, "w", encoding="utf8") as f:
    f.write(modified_source)
  indent_print.indent_print(
    f"修改后的 Solidity 文件已保存至 {output_path}", file=outfile
  )
  return output_path


def modify_constructor_calls(source_code, solidity_parser, contract_name):
  """
  修改所有调用指定合约构造函数的表达式，将构造函数参数列表移除（替换为空）
  假定调用格式为 new ContractName(arguments)
  """
  tree = solidity_parser.parse(source_code.encode("utf8"))
  root_node = tree.root_node
  query_text = """
    (
      call_expression
       function: (expression (new_expression name: (type_name (user_defined_type (identifier))))) @call_expression
    )
    """
  query = solidity_parser.language.query(query_text)
  modifications_calls = []
  matches = query.matches(root_node)

  for cnt, match in matches:
    lst: list[Node] = match.get("call_expression")
    for node in lst:
      node_text = source_code[node.start_byte : node.end_byte]
      if " ".join(node_text.split()) != f"new {contract_name}":
        continue
      if node.next_named_sibling.type == "call_argument":
        call_arg = node.next_named_sibling
        start_byte = call_arg.start_byte
        end_byte = call_arg.end_byte
        while (
          call_arg.next_named_sibling
          and call_arg.next_named_sibling.type == "call_argument"
        ):
          call_arg = call_arg.next_named_sibling
          end_byte = call_arg.end_byte
        modifications_calls.append((start_byte, end_byte, ""))

  modifications_calls.sort(key=lambda x: x[0], reverse=True)
  modified_source = source_code
  for start, end, replacement in modifications_calls:
    modified_source = modified_source[:start] + replacement + modified_source[end:]
  return modified_source


def modify_modifier_calls(source_code, constructor_node: Node, rename_map):
  """
  (modifier_invocation (identifier) (call_argument (expression (identifier)))
  """
  modifications_super = []
  # 遍历 constructor_node 的所有子节点，查找父类构造函数调用
  for child in constructor_node.children:
    if child.type == "modifier_invocation":
      args_node = list(filter(lambda x: x.type == "call_argument", child.children))
      for arg in args_node:
        arg_text = source_code[arg.start_byte : arg.end_byte]
        modifications_super.append(
          (
            arg.start_byte,
            arg.end_byte,
            rename_map.get(arg_text, arg_text),
          )
        )
  modifications_super.sort(key=lambda x: x[0], reverse=True)
  # print(modifications_super)
  return modifications_super
  modified_source = source_code
  for start, end, replacement in modifications_super:
    modified_source = modified_source[:start] + replacement + modified_source[end:]
  return modified_source


def main():
  # dummy main: 仅解析参数并调用 extract 出来的函数
  parser_arg = argparse.ArgumentParser(
    description="修改 Solidity 构造函数：移除参数列表，并添加状态变量初始化"
  )
  parser_arg.add_argument("solidity_file", help="Solidity 源码文件路径")
  parser_arg.add_argument("contract_name", help="目标合约名称")
  parser_arg.add_argument("args_json", help="构造函数参数对应的 JSON 文件路径")
  args = parser_arg.parse_args()
  return modify_one_contract(args.solidity_file, args.contract_name, args.args_json)


if __name__ == "__main__":
  main()
