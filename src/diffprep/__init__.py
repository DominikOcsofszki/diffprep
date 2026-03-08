import logging

from diffprep.core import get_settings
from diffprep.core.logger import setup_logging

setup_logging(get_settings().logger_settings)

logger = logging.getLogger(__name__)
logger.debug("Logging is ready")
