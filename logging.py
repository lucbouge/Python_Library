import logging
from logging import (
    basicConfig,
    info,
    warning,
    error,
    critical,
    exception,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    EXCEPTION,
)


# https://docs.python.org/3/library/logging.html


logging_format = "{levelname}: {pathname}#{lineno} --> {msg}"  # {asctime}

basicConfig(
    level=logging.INFO,
    style="{",
    format=logging_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="run.log",
    filemode="w",
)

