import logging

logger = logging.getLogger(__name__)


def initialize_logging(level=logging.INFO):
    logging.basicConfig()
    logger.setLevel(level)
