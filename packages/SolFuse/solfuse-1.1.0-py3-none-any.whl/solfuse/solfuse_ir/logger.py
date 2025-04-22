from typing import Union

from .config import ConfigProvider
from .indent_print import indent_print


class Logger:
  def __init__(self) -> None:
    self._config = None

  @property
  def config(self) -> Union[None, ConfigProvider]:
    return self._config

  @config.setter
  def config(self, value: ConfigProvider):
    assert isinstance(value, ConfigProvider), "U make me eat what?"
    self._config: ConfigProvider = value

  def __call__(self, *args, indent=-1, width=2, will_do=False):
    assert self.config is not None, "not initialized"

    if not self.debug and not will_do:
      return
    indent_print(
      *args,
      indent=indent if indent >= 0 else self.config.global_tab if self.config else 0,
      width=width,
    )

  @property
  def debug(self) -> bool:
    return self.config.debug


log = Logger()


def init_logger(config: ConfigProvider):
  log.config = config
