from pathlib import Path
from statistics import mean
import msparser
from rich import pretty, progress

pretty.install()


def total_memory(x):
  return x["mem_heap"] + x["mem_heap_extra"]


def get_peak_memory_snapshot(data):
  snapshot = max(data["snapshots"], key=total_memory)
  snapshot["total"] = snapshot["mem_heap"] + snapshot["mem_heap_extra"]
  return snapshot


def get_mean_memory_consumption(data):
  return mean(map(total_memory, data["snapshots"]))


def get_dir_compute_func_for(reduce_func, single_compute_func):
  return lambda dir: reduce_func(
    map(
      lambda x: single_compute_func(msparser.parse_file(x)),
      filter(lambda x: x.is_file(), Path(dir).iterdir()),
    )
  )


def get_memory_stats_dir(dir):
  mean_cons = get_dir_compute_func_for(mean, get_mean_memory_consumption)(dir)
  peak_cons = get_dir_compute_func_for(
    lambda l: total_memory(max(l, key=total_memory)),
    lambda x: get_peak_memory_snapshot(x),
  )(dir)
  return mean_cons, peak_cons


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("dir", type=str)

  parser = parser.parse_args()

  dir = parser.dir

  mean_cons, peak_cons = get_memory_stats_dir(dir)

  print(f"Average Memory Consumption: {mean_cons/1024/1024} MiBs")
  print(f"File Count: {len(list(filter(lambda x: x.is_file(), Path(dir).iterdir())))}")
  print(
    f"Average Overall Memory Consumption:{mean_cons /1024/1024 * len(list(filter(lambda x: x.is_file(), Path(dir).iterdir())))} MiBs"
  )
  print(f"Peak Memory Consumption Single Process: {peak_cons/1024/1024} MiBs")
