from pathlib import Path
from typing import Unpack

import loguru
from environs import env

from liblaf.grapes import environ
from liblaf.grapes.logging.filters import Filter, default_filter
from liblaf.grapes.typed import PathLike


def jsonl_handler(
    fpath: PathLike | None = None,
    filter_: Filter | None = None,
    **kwargs: Unpack["loguru.FileHandlerConfig"],
) -> "loguru.HandlerConfig":
    if fpath is None:
        fpath = env.path(environ.LOGGING_JSONL, default=Path("run.log.jsonl"))
    filter_ = default_filter(filter_)
    return {"sink": fpath, "filter": filter_, "serialize": True, "mode": "w", **kwargs}
