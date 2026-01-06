from __future__ import annotations


import os
import logging
from logging.handlers import RotatingFileHandler
from logging import basicConfig, getLogger, DEBUG
from typing import TypeAlias

from datetime import datetime

LoggerT: TypeAlias = logging.Logger


def configure_logger(logger_name: str) -> LoggerT:
    """Configures logger.

    Uses env variable LOG_LEVEL_NAME:
     - CRITICAL = 50
     - FATAL = 50
     - ERROR = 40
     - WARNING = 30
     - INFO = 20
     - DEBUG = 10

    Args:
        logger_name: Logger name.

    Returns:
        Logger object.
    """
    log_level_matrix = {"CRITICAL": 50, "FATAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10}

    log_level_name = os.getenv("LOG_LEVEL_NAME") or "DEBUG"
    log_level_value = log_level_matrix[log_level_name]

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level_value)

    log_dir = get_root_dir() + "/logs"
    log_path = log_dir + f"/{logger_name}.log"

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logger_handler = RotatingFileHandler(log_path, maxBytes=100 * 1024 * 1024, backupCount=20)
    logger_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger


def get_timestamp():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M%S")
    return year + month + day + time + now.strftime(".%f")

def get_root_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


class LogProvider:
    logger = None

    def __new__(cls):
        if cls.logger is None:
            log_dir = get_root_dir() + "/logs"
            log_path = f"{log_dir}/Log.txt"
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            format_ = "{asctime} {levelname} {message}"
            basicConfig(filename=log_path, level=DEBUG, format=format_, style="{")
            cls.logger = getLogger()
        return cls.logger
