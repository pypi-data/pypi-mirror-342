"""Logger module.

This module provides logging functionality for the trading bot,
including console and file logging with rotation.

Logging levels:

NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

- DEBUG - самая подробная информация, нужна только разработчику и только для отладки,
          например значения переменных,
          какие данные получены и т.д.
- INFO - информационные сообщения, как подтверждение работы, например запуск сервиса.
- WARNING - еще не ошибка, но уже надо посмотреть - мало места на диске, мало памяти,
            много созданных объектов и т.д.
- ERROR - приложение еще работает и может работать, но что-то пошло не так.
- CRITICAL - приложение не может работать дальше.
"""

import json
import logging
import os
import sys
from logging import Logger, Formatter, StreamHandler, getLogger
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv_vault import load_dotenv

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CONFIG,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_SIZE,
    LOG_NAME,
)

# Load environment variables
load_dotenv()


def setup_logger(name: str | None = None, *, level: str | None = None) -> Logger:
    """Set up and configure the logger.

    Args:
        name (str, optional): Logger name. Defaults to None.
        level (str, optional): Logging level. Defaults to None.

    Returns:
        Logger: Configured logger instance.
    """
    # Set default logger name if not provided
    if name is None:
        name = LOG_NAME

    # Check if log config file exists
    if os.path.isfile(LOG_CONFIG):
        try:
            # Load config from JSON file
            with open(LOG_CONFIG, encoding="utf-8") as file:
                config = json.load(file)

            dictConfig(config)

            return get_logger(name)
        except FileNotFoundError as e:
            print(f"Error loading logging configuration file: {e}")

    # Create logger instance
    logger = get_logger(name)

    # Get log level from environment or config
    if level is None:
        level = os.getenv("LOG_LEVEL", LOG_LEVEL)

    # Configure logger
    logger.setLevel(getattr(logging, level) if level else LOG_LEVEL)

    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Create formatter
    formatter = Formatter(LOG_FORMAT)

    # Create console handler
    console_handler = StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create logs directory if it doesn't exist
    log_dir = Path(str.join("..", "logs"))
    log_dir.mkdir(exist_ok=True)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / LOG_FILE,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> Logger:
    """Get the logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger instance.
    """
    return getLogger(name)
