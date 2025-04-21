"""Модуль для централизованной настройки логирования с использованием structlog.

Предоставляет структурированное логирование для всего приложения.
"""

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog


def _configure_logging() -> structlog.stdlib.BoundLogger:
    """Настройка системы логирования с учётом ОС и переменной окружения APP_LOG_DIR."""
    logging.getLogger("fast_bitrix24").setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    env_dir = os.getenv("APP_LOG_DIR")
    if env_dir:
        log_dir = Path(env_dir)
    else:
        system = platform.system()
        if system == "Windows":
            base = Path(
                os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"),
            )
            log_dir = base / "b24-mcp" / "logs"
        else:
            log_dir = Path("/var/log/myapp")
            if not os.access(log_dir, os.W_OK):
                log_dir = (
                    Path(
                        os.getenv(
                            "XDG_STATE_HOME",
                            Path.home() / ".local" / "state",
                        ),
                    )
                    / "b24-mcp"
                    / "logs"
                )

    log_file = log_dir / "app.log"

    log_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    root_logger.addHandler(file_handler)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if any("tests" in arg for arg in sys.argv):
        console_handler = logging.StreamHandler(sys.stdout)
        root_logger.addHandler(console_handler)

        structlog.configure(
            processors=[
                *shared_processors,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        structlog.configure(
            processors=[
                *shared_processors,
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(ensure_ascii=False),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    return structlog.get_logger()


logger = _configure_logging()


def configure_log_level(level: str) -> None:
    """Настройка уровня логирования.

    :param level: уровень логирования ("DEBUG", "INFO" и т.д.)
    """
    logging.getLogger().setLevel(level)
