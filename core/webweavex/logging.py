from __future__ import annotations

import logging

_LOGGER_NAME = "webweavex"
_FORMAT = "[WebWeaveX] %(asctime)s %(levelname)s %(name)s %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def _configure_base_logger() -> logging.Logger:
  logger = logging.getLogger(_LOGGER_NAME)
  if logger.handlers:
    return logger
  logger.setLevel(logging.INFO)
  handler = logging.StreamHandler()
  handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATEFMT))
  logger.addHandler(handler)
  logger.propagate = False
  return logger


def get_logger(name: str) -> logging.Logger:
  """Return a configured logger for WebWeaveX modules."""
  base_logger = _configure_base_logger()
  if name == _LOGGER_NAME:
    return base_logger
  if name.startswith(f"{_LOGGER_NAME}.") or name == _LOGGER_NAME:
    return logging.getLogger(name)
  return base_logger.getChild(name)
