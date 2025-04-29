# logger.py: Standard logging setup
"""
Logger setup for datacleancraft.
"""

import logging
import sys
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure logger.

    Args:
        name (str): Logger name.

    Returns:
        Logger object.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

"""
logger.py - Centralized logger configuration for the DataCleanCraft package.
"""


def setup_logger(
    name: str = "datacleancraft",
    level: int = logging.INFO,
    log_to_file: bool = False,
    log_dir: str = "logs",
) -> logging.Logger:
    """
    Set up and return a configured logger.

    Args:
        name (str): Name of the logger.
        level (int): Logging level.
        log_to_file (bool): Whether to log to a file in addition to console.
        log_dir (str): Directory to save log files if log_to_file is True.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate logs if root logger has handlers

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_to_file:
            log_dir_path = Path(log_dir)
            log_dir_path.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_dir_path / f"{name}.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

# Default logger for immediate use
default_logger = setup_logger()
