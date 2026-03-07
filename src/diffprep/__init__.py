import logging

from diffprep.core.logger import LoggerSettings, setup_logging

setup_logging(LoggerSettings())

logger = logging.getLogger(__name__)
logger.debug("Logging is ready")
