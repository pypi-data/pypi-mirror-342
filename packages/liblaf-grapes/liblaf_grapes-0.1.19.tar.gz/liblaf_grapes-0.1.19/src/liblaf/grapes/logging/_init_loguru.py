import logging
from collections.abc import Sequence

import loguru
from environs import env
from loguru import logger

from ._intercept import setup_loguru_logging_intercept
from ._level import DEFAULT_LEVELS, add_level
from ._std import clear_handlers
from .filters import Filter
from .handler import file_handler, jsonl_handler, rich_handler


def init_loguru(
    level: int | str = logging.NOTSET,
    filter_: Filter | None = None,
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
) -> None:
    """Initialize the Loguru logger with specified configurations.

    Args:
        level: The logging level.
        filter_: A filter to apply to the logger.
        handlers: A sequence of handler configurations.
        levels: A sequence of level configurations.
    """
    if handlers is None:
        handlers: list[loguru.HandlerConfig] = [
            rich_handler(level=level, filter_=filter_)
        ]
        if env.path("LOGGING_FILE", default=None):
            handlers.append(file_handler(level=level, filter_=filter_))
        if env.path("LOGGING_JSONL", default=None):
            handlers.append(jsonl_handler(level=level, filter_=filter_))
    logger.configure(handlers=handlers)
    for lvl in levels or DEFAULT_LEVELS:
        add_level(**lvl)
    setup_loguru_logging_intercept(level=level)
    clear_handlers()
