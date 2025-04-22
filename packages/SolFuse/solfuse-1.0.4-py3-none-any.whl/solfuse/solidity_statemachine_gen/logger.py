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
    self._config = value

  def __call__(self, *args, indent=0, width=2, will_do=True):
    assert self.config is not None, "not initialized"

    if not self.debug or not will_do:
      return
    indent_print(*args, indent=indent, width=width)

  @property
  def debug(self) -> bool:
    return self.config.debug


log = Logger()


def init_logger(config: ConfigProvider):
  log.config = config
