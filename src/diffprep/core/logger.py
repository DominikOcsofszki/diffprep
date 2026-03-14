import logging
import logging.config

from diffprep.core.configs import LoggerSettings

logger = logging.getLogger(__name__)


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


def setup_logging(settings: LoggerSettings) -> None:
    logging.config.dictConfig(build_logging_config(settings))
