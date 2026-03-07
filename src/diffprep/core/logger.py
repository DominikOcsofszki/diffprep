import logging.config
from typing import Literal

from pydantic import BaseModel, Field


class LoggerSettings(BaseModel):
    level: Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"] = "DEBUG"
    fmt: str = Field(default="%(filename)-16s:%(lineno)1d  %(message)s")
    disable_existing_loggers: bool = Field(default=False)


def build_logging_config(settings: LoggerSettings) -> dict[str, object]:
    return {
        "version": 1,
        "disable_existing_loggers": settings.disable_existing_loggers,
        "formatters": {
            "default": {
                "format": settings.fmt,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "handlers": ["console"],
            "level": settings.level,
        },
    }


def setup_logging(settings: LoggerSettings | None = None) -> None:
    logging.config.dictConfig(build_logging_config(settings or LoggerSettings()))
