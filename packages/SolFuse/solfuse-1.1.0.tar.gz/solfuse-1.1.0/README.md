# SolFuse

A Tool to generate state-machine indicating invalid call-chain from Solidity source code.

## Usage

```text
usage: solfuse [-h] [--custom] [--use_pre2] [--debug] [--print_stmt] [--print_on_constraints_found] [--print_executor_process] [--print_summary_process] [--print_executor_summary] [--print_state_machine] [--use_svg] [--print_statistic]
               [--use_proper_modifier] [--use_state_merging] [--die_into_pdb] [--out_stat_file OUT_STAT_FILE]
               filename image_path contract solc_path

positional arguments:
  filename
  image_path
  contract
  solc_path

options:
  -h, --help            show this help message and exit
  --custom, -c
  --use_pre2, -p
  --debug, -d
  --print_stmt
  --print_on_constraints_found
  --print_executor_process
  --print_summary_process
  --print_executor_summary
  --print_state_machine
  --use_svg
  --print_statistic, -s
  --use_proper_modifier
  --use_state_merging
  --die_into_pdb
  --out_stat_file OUT_STAT_FILE
```
