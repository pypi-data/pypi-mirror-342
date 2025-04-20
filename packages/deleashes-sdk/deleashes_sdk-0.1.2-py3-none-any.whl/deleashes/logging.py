"""
Logging module for Deleashes SDK.
"""

import logging

# Create a logger for the Deleashes SDK
logger = logging.getLogger("deleashes")


def get_logger():
    """
    Returns the Deleashes SDK logger.

    Examples:
        >>> import logging
        >>> from deleashes.logging import get_logger
        >>> 
        >>> # Configure the logger
        >>> logger = get_logger()
        >>> handler = logging.StreamHandler()
        >>> handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        >>> logger.addHandler(handler)
        >>> logger.setLevel(logging.INFO)
    """
    return logger


# By default, don't show any logs unless configured by the user
logger.setLevel(logging.WARNING)
