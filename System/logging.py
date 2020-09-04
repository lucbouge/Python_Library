import sys
import logging

from .print import eprint

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
)


# https://docs.python.org/3/library/logging.html


logging_format = "{levelname}: {pathname}#{lineno} --> {msg}"  # {asctime}

logging_kwargs = {
    "level": logging.INFO,
    "style": "{",
    "format": logging_format,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    # "force": True,
}


def set_log_destination(s):
    kwargs = logging_kwargs.copy()
    if isinstance(s, str):
        eprint(f"Logging to {s}")
        kwargs["filename"] = s
        kwargs["filemode"] = "w"
    else:
        eprint("Logging to default")
        kwargs["stream"] = sys.stderr
    eprint(kwargs)
    logging.basicConfig(**kwargs)


# set_log_destination("run.log")
set_log_destination(None)
