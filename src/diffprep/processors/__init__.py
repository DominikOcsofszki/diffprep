import importlib
import logging
import pkgutil

from ._registry import (
    Processor,
    get_processor,
    register_processor,
    validate_registered_processors,
)

logger = logging.getLogger(__name__)


def _load_processors() -> None:
    modules = [
        mod.name
        for mod in pkgutil.iter_modules(__path__)
        if not mod.name.startswith("_")
    ]
    logger.debug("Discovered processor modules: %s", modules)

    for name in modules:
        module_name = f"{__name__}.{name}"
        logger.debug("Loading processor module: %s", module_name)
        importlib.import_module(module_name)


_load_processors()
logger.debug("Validating registered processors")
validate_registered_processors()

__all__ = ["Processor", "get_processor", "register_processor"]
