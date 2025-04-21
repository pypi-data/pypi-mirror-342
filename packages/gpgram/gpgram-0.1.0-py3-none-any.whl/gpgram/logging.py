"""
Logging module for Gpgram.

This module provides advanced logging capabilities using Loguru.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

from loguru import logger

# Remove default handler
logger.remove()

# Default format for console logging
DEFAULT_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Default format for file logging
FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"


def setup_logging(
    level: str = "INFO",
    console: bool = True,
    console_format: str = DEFAULT_FORMAT,
    file: Optional[Union[str, Path]] = None,
    file_level: str = "DEBUG",
    file_format: str = FILE_FORMAT,
    file_rotation: str = "10 MB",
    file_retention: str = "1 month",
    file_compression: str = "zip",
    json: bool = False,
    **kwargs
) -> None:
    """
    Set up logging for Gpgram.
    
    Args:
        level: Minimum level for console logging
        console: Whether to log to console
        console_format: Format for console logging
        file: Path to log file
        file_level: Minimum level for file logging
        file_format: Format for file logging
        file_rotation: When to rotate the log file
        file_retention: How long to keep log files
        file_compression: Compression format for rotated log files
        json: Whether to use JSON format for file logging
        **kwargs: Additional arguments to pass to logger.configure()
    """
    config = {
        "handlers": [],
        "extra": {"app_name": "gpgram"},
    }
    
    # Add console handler
    if console:
        config["handlers"].append({
            "sink": sys.stderr,
            "level": level,
            "format": console_format,
            "colorize": True,
        })
    
    # Add file handler
    if file:
        file_config = {
            "sink": file,
            "level": file_level,
            "format": file_format,
            "rotation": file_rotation,
            "retention": file_retention,
            "compression": file_compression,
        }
        
        if json:
            file_config["serialize"] = True
        
        config["handlers"].append(file_config)
    
    # Update with additional kwargs
    config.update(kwargs)
    
    # Configure logger
    logger.configure(**config)


def get_logger(name: str) -> "logger":
    """
    Get a logger with the given name.
    
    Args:
        name: Name of the logger
    
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Set up default logging
setup_logging()
