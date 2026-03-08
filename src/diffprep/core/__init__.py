import logging
from functools import lru_cache

from diffprep.core.logger import setup_logging

from .configs import (
    JsonSettings,
    NormalizeSettings,
    Settings,
    XmlSettings,
)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    setup_logging(settings.logger_settings)
    logging.debug("Settings initialized: \n%s\n", settings.model_dump_json(indent=4))
    return settings


__all__ = [
    "JsonSettings",
    "NormalizeSettings",
    "Settings",
    "XmlSettings",
    "get_settings",
]
