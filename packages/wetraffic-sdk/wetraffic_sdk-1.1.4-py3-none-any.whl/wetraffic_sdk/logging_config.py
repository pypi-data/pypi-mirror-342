# logging_config.py
import logging
import os

from pythonjsonlogger.json import JsonFormatter


def setup_logger(
    logger_name: str = "wetraffic.sdk",
    env_level: str = "WETRAFFIC_LOG_LEVEL",
    default_level: str = "INFO",
) -> logging.Logger:
    """
    Configure and return a JSON logger instance
    """
    # Get or create logger
    logger = logging.getLogger(logger_name)

    # Return if already configured
    if logger.handlers:
        return logger

    # Configure level from env or default
    log_level_name = os.environ.get(env_level, default_level).upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    logger.setLevel(log_level)

    # Setup handler with JSON formatter
    handler = logging.StreamHandler()
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s", timestamp=True)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
