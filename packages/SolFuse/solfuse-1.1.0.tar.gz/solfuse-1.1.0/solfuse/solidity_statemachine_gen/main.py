import argparse
from fileinput import filename
import time
from functools import reduce

from slither.slither import Slither

from .config import default_config, debug_config, ConfigProvider, ConfigProfile
from .executor import Executor
from .logger import init_logger
from .logger import log
from .state_machine import StateMachine


def do_main(
  filename: str,
  contract_name: str,
  image_path: str,
  contract: str,
  custom: bool,
  use_pre2: bool,
  debug: bool,
  print_stmt: bool,
  print_on_constraints_found: bool,
  print_executor_process: bool,
  print_summary_process: bool,
  print_executor_summary: bool,
  print_state_machine: bool,
  use_svg: bool,
  print_statistic: bool,
) -> None:
  # prepare config
  config = ConfigProvider(
    ConfigProfile(
      debug=debug,
      print_stmt=print_stmt,
      print_on_constraints_found=print_on_constraints_found,
      print_executor_process=print_executor_process,
      print_summary_process=print_summary_process,
      print_state_machine=print_state_machine,
      use_pre2=use_pre2,
    )
  )
  if not custom:
    config = debug_config if debug else default_config

  # prepare logger
  init_logger(config=config)

  # prepare program
  start = time.perf_counter()

  slither = Slither(filename)
  contract = slither.get_contract_from_name(contract_name)

  analyze_time = time.perf_counter()

  assert len(contract) == 1, "impossible"
  contract = contract[0]
  # run
  executor = Executor(contract=contract, slither=slither, config=config)
  executor.do_exec()

  exec_time = time.perf_counter()

  log("doing summary", will_do=config.print_summary_process)  # type: ignore
  executor.do_summary()
  log(executor.summary, will_do=config.print_executor_summary)  # type: ignore
  sm = StateMachine(summary=executor.summary, config=config)
  sm.build()
  sm.print_simple()
  sm.export_to_dot_reject(image_path, use_svg=use_svg)

  finalize_time = time.perf_counter()
  if print_statistic:
    print("")
    import pathlib

    print(f"name: {pathlib.Path(filename).stem}")
    total = finalize_time - start
    analyze = analyze_time - start
    exec = exec_time - analyze_time
    generate = finalize_time - exec_time
    print(f"time used total: {total}")
    print(f"time used on analyzing contract: {analyze} -- {((analyze) / total) * 100}%")
    print(f"time used on execution: {exec} -- {((exec) / total) * 100}%")
    print(
      f"time used on generating state machine:{generate} -- {(generate / total) * 100}%"
    )
    print(f"functions processed: {len(sm.functions)}")
    print(
      "lines of code: {}".format(
        list(slither.source_code.values())[0].count("\r\n") + 1
      )
    )
    print(
      f"eliminated transitions: {sum(map(lambda x: len(x), sm.transitions_reject.values()))}"
    )
    print(f"eliminated 1-paths: {sm.statistic_deleted_edge(1)}")
    print(f"eliminated 2-paths: {sm.statistic_deleted_edge(2)}")
    print(f"eliminated 3-paths: {sm.statistic_deleted_edge(3)}")


def main() -> None:
  # prepare args
  parser = argparse.ArgumentParser()
  parser.add_argument("filename", type=str)
  parser.add_argument("image_path", type=str)
  parser.add_argument("contract", type=str)
  parser.add_argument("--custom", "-c", action="store_true", default=False)
  parser.add_argument("--use_pre2", "-p", action="store_true", default=False)
  parser.add_argument("--debug", "-d", action="store_true", default=False)
  parser.add_argument("--print_stmt", action="store_true", default=False)
  parser.add_argument(
    "--print_on_constraints_found", action="store_true", default=False
  )
  parser.add_argument("--print_executor_process", action="store_true", default=False)
  parser.add_argument("--print_summary_process", action="store_true", default=False)
  parser.add_argument("--print_executor_summary", action="store_true", default=False)
  parser.add_argument("--print_state_machine", action="store_true", default=False)
  parser.add_argument("--use_svg", action="store_true", default=False)
  parser.add_argument("--print_statistic", "-s", action="store_true", default=False)
  args: argparse.Namespace = parser.parse_args()

  # prepare config
  config = ConfigProvider(
    ConfigProfile(
      debug=args.debug,
      print_stmt=args.print_stmt,
      print_on_constraints_found=args.print_on_constraints_found,
      print_executor_process=args.print_executor_process,
      print_summary_process=args.print_summary_process,
      print_state_machine=args.print_state_machine,
      use_pre2=args.use_pre2,
    )
  )
  if not args.custom:
    config = debug_config if args.debug else default_config

  # prepare logger
  init_logger(config=config)

  # prepare program
  start = time.perf_counter()
  filename: str = args.filename

  slither = Slither(filename)
  contract = slither.get_contract_from_name(args.contract)

  analyze_time = time.perf_counter()

  assert len(contract) == 1, "impossible"
  contract = contract[0]
  # run
  executor = Executor(contract=contract, slither=slither, config=config)
  executor.do_exec()

  exec_time = time.perf_counter()

  log("doing summary", will_do=config.print_summary_process)  # type: ignore
  executor.do_summary()
  log(executor.summary, will_do=config.print_executor_summary)  # type: ignore
  sm = StateMachine(summary=executor.summary, config=config)
  sm.build()
  sm.print_simple()
  sm.export_to_dot_reject(args.image_path, use_svg=args.use_svg)

  finalize_time = time.perf_counter()

  if args.print_statistic:
    print("")
    import pathlib

    print(f"name: {pathlib.Path(filename).stem}")
    total = finalize_time - start
    analyze = analyze_time - start
    exec = exec_time - analyze_time
    generate = finalize_time - exec_time
    print(f"time used total: {total}")
    print(f"time used on analyzing contract: {analyze} -- {((analyze) / total) * 100}%")
    print(f"time used on execution: {exec} -- {((exec) / total) * 100}%")
    print(
      f"time used on generating state machine:{generate} -- {(generate / total) * 100}%"
    )
    print(f"functions processed: {len(sm.functions)}")
    print(
      "lines of code: {}".format(
        list(slither.source_code.values())[0].count("\r\n") + 1
      )
    )
    print(
      f"eliminated transitions: {sum(map(lambda x: len(x), sm.transitions_reject.values()))}"
    )
    print(f"eliminated 1-paths: {sm.statistic_deleted_edge(1)}")
    print(f"eliminated 2-paths: {sm.statistic_deleted_edge(2)}")
    print(f"eliminated 3-paths: {sm.statistic_deleted_edge(3)}")


if __name__ == "__main__":
  main()
