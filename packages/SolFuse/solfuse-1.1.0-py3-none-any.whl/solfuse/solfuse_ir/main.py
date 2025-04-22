import argparse
from pathlib import Path

from .config import ConfigProfile, ConfigProvider, debug_config, default_config
from .logger import log, init_logger
from slither import Slither
from slither.exceptions import SlitherError
from .driver import Driver
from .engine import Engine
from .utils import custom_exception_handler, ensure_version
from z3 import Z3Exception


def do_main(
  filename: str,
  image_path: str,
  contract: str,
  solc_path: str,
  custom: bool = False,
  use_pre2: bool = False,
  debug: bool = False,
  print_stmt: bool = False,
  print_on_constraints_found: bool = False,
  print_executor_process: bool = False,
  print_summary_process: bool = False,
  print_executor_summary: bool = False,
  print_state_machine: bool = False,
  use_svg: bool = False,
  print_statistic: bool = False,
  use_proper_modifier: bool = False,
  use_state_merging: bool = False,
  die_into_pdb: bool = False,
  out_stat_file: str = "output.json",
) -> int:
  if die_into_pdb:
    import sys

    sys.excepthook = custom_exception_handler
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
  file_path: str = filename
  log(f"using solc path: {solc_path}")
  original_solc_path = solc_path
  solc_path: Path = Path(solc_path)
  # ensure corresponding solc version is present and automatically switch
  if not original_solc_path:
    try:
      version = ensure_version(file_path)
      import solcix

      solc_path = Path(solcix.installer.get_executable(version=version))
    except NotImplementedError:
      log(f"No version for file {file_path}, exiting...")
      return 114
  try:
    slither = Slither(file_path, solc=solc_path.as_posix())
  except SlitherError:
    log(f"compile {file_path} using {solc_path.as_posix()} failed")
    return 116
  contract = slither.get_contract_from_name(contract)
  if len(contract) != 1:
    log(f"Contract not unique or not found, Contract count: {len(contract)}")
    return 115
  assert len(contract) == 1, "impossible"
  contract = contract[0]
  log(f"Handling {file_path}...")
  drive = Driver(
    _engine=Engine(contract=contract, slither=slither, config=config),
    _config=config,
    file_path=file_path,
    solc_path=solc_path.resolve().as_posix(),
    image_path=image_path,
    out_stat_file=out_stat_file,
  )
  try:
    drive.run()
  except Z3Exception as e:
    if e.value in (
      "One and only one occurrence of each datatype is expected",
      "Non-empty Datatypes expected",
    ):
      return 117
    return 1
  return 0


def main():
  # prepare args
  parser = argparse.ArgumentParser()
  parser.add_argument("filename", type=str)
  parser.add_argument("image_path", type=str)
  parser.add_argument("contract", type=str)
  parser.add_argument("solc_path", type=str)
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
  parser.add_argument("--use_proper_modifier", action="store_true", default=False)
  parser.add_argument("--use_state_merging", default=False, action="store_true")
  parser.add_argument("--die_into_pdb", default=False, action="store_true")
  parser.add_argument("--out_stat_file", type=str, default="output.json")

  args: argparse.Namespace = parser.parse_args()
  do_main(
    filename=args.filename,
    image_path=args.image_path,
    contract=args.contract,
    solc_path=args.solc_path,
    custom=args.custom,
    use_pre2=args.use_pre2,
    debug=args.debug,
    print_stmt=args.print_stmt,
    print_on_constraints_found=args.print_on_constraints_found,
    print_executor_process=args.print_executor_process,
    print_summary_process=args.print_summary_process,
    print_executor_summary=args.print_executor_summary,
    print_state_machine=args.print_state_machine,
    use_svg=args.use_svg,
    print_statistic=args.print_statistic,
    use_proper_modifier=args.use_proper_modifier,
    use_state_merging=args.use_state_merging,
    die_into_pdb=args.die_into_pdb,
    out_stat_file=args.out_stat_file,
  )

  # # set custom exception handler based on args
  # if args.die_into_pdb:
  #   import sys

  #   sys.excepthook = custom_exception_handler

  # # prepare config
  # config = ConfigProvider(
  #   ConfigProfile(
  #     debug=args.debug,
  #     print_stmt=args.print_stmt,
  #     print_on_constraints_found=args.print_on_constraints_found,
  #     print_executor_process=args.print_executor_process,
  #     print_summary_process=args.print_summary_process,
  #     print_state_machine=args.print_state_machine,
  #     use_pre2=args.use_pre2,
  #     use_state_merging=args.use_state_merging,
  #     use_proper_modifier=args.use_proper_modifier,
  #   )
  # )
  # if not args.custom:
  #   config = debug_config if args.debug else default_config

  # # prepare logger
  # init_logger(config=config)

  # # prepare program
  # file_path: str = args.filename
  # log(f"using solc path: {args.solc_path}")
  # solc_path: Path = Path(args.solc_path)
  # # ensure corresponding solc version is present and automatically switch
  # if not args.solc_path:
  #   try:
  #     version = ensure_version(file_path)
  #     import solcix

  #     solc_path = Path(solcix.installer.get_executable(version=version))
  #   except NotImplementedError:
  #     log(f"No version for file {file_path}, exiting...")
  #     exit(code=114)
  # try:
  #   slither = Slither(file_path, solc=solc_path.as_posix())
  # except SlitherError:
  #   log(f"compile {file_path} using {solc_path.as_posix()} failed")
  #   exit(116)
  # contract = slither.get_contract_from_name(args.contract)
  # if len(contract) != 1:
  #   log(f"Contract not unique or not found, Contract count: {len(contract)}")
  #   exit(115)
  # assert len(contract) == 1, "impossible"
  # contract = contract[0]
  # log(f"Handling {file_path}...")
  # drive = Driver(
  #   _engine=Engine(contract=contract, slither=slither, config=config),
  #   _config=config,
  #   file_path=file_path,
  #   solc_path=solc_path.resolve().as_posix(),
  #   image_path=args.image_path,
  #   out_stat_file=args.out_stat_file,
  # )
  # try:
  #   drive.run()
  # except Z3Exception as e:
  #   if e.value in (
  #     "One and only one occurrence of each datatype is expected",
  #     "Non-empty Datatypes expected",
  #   ):
  #     exit(117)
  #   raise e
