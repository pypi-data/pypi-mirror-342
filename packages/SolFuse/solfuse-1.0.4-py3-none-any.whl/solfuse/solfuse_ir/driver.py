import datetime
from pathlib import Path
from . import config
from . import engine
from . import state_machine
from .logger import log
import time
import os
import json


class Driver:
  def __init__(
    self,
    _engine: engine.Engine,
    _config: config.ConfigProvider,
    file_path: str,
    solc_path: str,
    image_path: str = ".",
    out_stat_file="output.json",
  ) -> None:
    self.engine: engine.Engine = _engine
    self.config: config.ConfigProvider = _config
    self.state_machine = None
    self.image_path = image_path
    self.file_path = file_path
    self.out_stat_file = out_stat_file
    self.solc_path = solc_path

  def run(self) -> None:
    # 开始时间
    start_time = time.time()

    # 执行引擎
    self.engine.exec()
    exec_time = time.time()

    # 生成摘要
    self.engine.do_summary()
    summary_time = time.time()
    log(self.engine.summary.chain_info)
    # 构建状态机（剪裁前）
    self.state_machine = state_machine.StateMachine(
      summary=self.engine.summary, config=self.config
    )

    self.state_machine.build()
    build_time = time.time()
    self.state_machine.export_to_dot_reject(folder=self.image_path)
    # log(self.engine.summary)

    # 执行剪裁操作并统计被删除的路径数
    deleted_paths = {}
    path_lengths = [1, 2, 3]  # 您可以根据需要调整路径长度
    for length in path_lengths:
      count = self.state_machine.statistic_deleted_edge(length)
      deleted_paths[f"length_{length}"] = count

    # 获取剪裁后的状态机数据
    pruned_state_machine_dict = self.state_machine.to_dict()

    # 统计剪裁前的转换数量
    original_transition_count = len(self.state_machine.states) ** 2

    # 统计剪裁后的转换数量
    pruned_transition_count = original_transition_count - sum(
      len(v) for v in pruned_state_machine_dict["transitions_reject"].values()
    )

    end_time = time.time()

    # 计算转换数量的变化
    transition_count_diff = original_transition_count - pruned_transition_count
    transition_reduction_rate = (
      (transition_count_diff / original_transition_count) * 100
      if original_transition_count > 0
      else 0
    )

    # 收集时间数据
    timing_data = {
      "engine_exec_time": exec_time - start_time,
      "summary_time": summary_time - exec_time,
      "state_machine_build_time": build_time - summary_time,
      "total_run_time": end_time - start_time,
    }

    # 输出日志
    log(f"Engine 执行时间: {timing_data['engine_exec_time']} 秒", will_do=True)
    log(f"摘要生成时间: {timing_data['summary_time']} 秒", will_do=True)
    log(f"状态机构建时间: {timing_data['state_machine_build_time']} 秒", will_do=True)
    log(f"总运行时间: {timing_data['total_run_time']} 秒", will_do=True)
    log(
      f"转换数量 - 剪裁前: {original_transition_count}, 剪裁后: {pruned_transition_count}, 减少了 {transition_count_diff} 个，减幅 {transition_reduction_rate:.2f}%",
      will_do=True,
    )
    for length in path_lengths:
      count = deleted_paths[f"length_{length}"]
      log(f"被删除的{length}长度路径数: {count}", will_do=True)

    black_holes = self.state_machine.find_black_holes()
    assert len(black_holes) == 0, f"发现黑洞: {black_holes}"

    # 整合数据
    data = {
      "file_path": Path(self.file_path).resolve().as_posix(),
      "timing": timing_data,
      "deleted_paths": deleted_paths,
      "state_comparison": {
        "original_transition_count": original_transition_count,
        "pruned_transition_count": pruned_transition_count,
        "transition_count_diff": transition_count_diff,
        "transition_reduction_rate": transition_reduction_rate,
      },
      "state_machine": pruned_state_machine_dict,
      "black_holes": black_holes,
      "contract": self.engine.contract.name,
      "solc_path": self.solc_path,
      "constructor_arguments": self.engine.summary.construct_params,
      "constructor_fail_reason": self.engine.summary.construct_fail_reason,
      "parameter_ranges": dict(
        map(lambda x: (x[0].name, x[1]), self.engine.summary._post_range.items())
      ),
      "on_chain_info": self.state_machine.summary.chain_info,
    }
    log(self.state_machine.summary.chain_info)
    output_file = os.path.join(self.image_path, self.out_stat_file)
    try:
      with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
      log(f"数据已导出到 {output_file}", will_do=True)
    except IOError as e:
      log(f"导出 JSON 文件时发生错误: {e}", will_do=True)
