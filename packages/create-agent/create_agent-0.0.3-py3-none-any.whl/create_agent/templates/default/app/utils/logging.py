import logging
import sys
from contextlib import contextmanager

import colorlog

from app.config import settings

# Create a logger
logger = logging.getLogger("{{ package_name }}")

# Set logging level from settings
log_level = getattr(logging, settings.LOG_LEVEL)
logger.setLevel(log_level)

# Create a console handler
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(log_level)

# Create a formatter
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

# Add formatter to handler
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)


@contextmanager
def log_context(context_name: str):
    """Context manager for logging."""
    logger.debug(f"Starting {context_name}")
    try:
        yield
    except Exception as e:
        logger.error(f"Error in {context_name}: {str(e)}", exc_info=True)
        raise
    finally:
        logger.debug(f"Finished {context_name}") 