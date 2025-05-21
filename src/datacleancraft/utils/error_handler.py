"""
error_handler.py: Centralized error handling utilities.
"""

import sys
import functools
import logging

logger = logging.getLogger(__name__)

class PipelineError(Exception):
    """Custom exception class for pipeline-related errors."""
    pass


def handle_exception(func=None, *, fatal=False):
    """
    Decorator to handle exceptions uniformly across the pipeline.
    
    Can be used both with and without parentheses:
    - @handle_exception
    - @(fatal=True)
    """
    if func is None:
        return lambda func: handle_exception(func, fatal=fatal)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.error(f"[ErrorHandler] An error occurred in {func.__name__}: {str(exc)}", exc_info=True)
            if fatal:
                logger.critical("[ErrorHandler] Fatal error encountered. Exiting pipeline.", exc_info=True)
                sys.exit(1)
            return None
    return wrapper
