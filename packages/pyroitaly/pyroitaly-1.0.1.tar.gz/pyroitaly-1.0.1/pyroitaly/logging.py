#  PyroItaly - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present ItalyMusic <https://github.com/ItalyMusic>
#  Copyright (C) 2025-present ItalyMusic <https://github.com/ItalyMusic>
#
#  This file is part of PyroItaly.
#
#  PyroItaly is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroItaly is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroItaly.  If not, see <http://www.gnu.org/licenses/>.

"""
PyroItaly Logging System

This module provides an enhanced logging system for PyroItaly using loguru.
It offers better formatting, log rotation, and more detailed error reporting.
"""

import os
import sys
import traceback
from typing import Dict, Any, Optional, Union, List, Callable

from loguru import logger

# Remove default logger
logger.remove()

# Default log format
DEFAULT_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class LoguruHandler:
    """Enhanced logging handler using loguru
    
    This class provides a more powerful logging system with better formatting,
    log rotation, and more detailed error reporting.
    """
    
    def __init__(self):
        """Initialize the logging handler"""
        self._loggers = {}
        self._default_level = "INFO"
        self._configured = False
    
    def configure(
        self,
        level: str = "INFO",
        log_to_console: bool = True,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None,
        rotation: str = "20 MB",
        retention: str = "1 week",
        format: str = DEFAULT_LOG_FORMAT,
        backtrace: bool = True,
        diagnose: bool = True,
    ) -> None:
        """Configure the logging system
        
        Args:
            level: Minimum log level to display
            log_to_console: Whether to log to console
            log_to_file: Whether to log to file
            log_file_path: Path to log file (if log_to_file is True)
            rotation: When to rotate logs (size or time)
            retention: How long to keep logs
            format: Log format string
            backtrace: Whether to show backtrace for errors
            diagnose: Whether to show variable values in tracebacks
        """
        self._default_level = level
        
        # Configure loguru
        if log_to_console:
            logger.add(
                sys.stderr,
                level=level,
                format=format,
                backtrace=backtrace,
                diagnose=diagnose,
            )
        
        if log_to_file:
            if not log_file_path:
                log_file_path = os.path.join(os.getcwd(), "pyroitaly.log")
            
            logger.add(
                log_file_path,
                level=level,
                format=format,
                rotation=rotation,
                retention=retention,
                backtrace=backtrace,
                diagnose=diagnose,
            )
        
        self._configured = True
    
    def get_logger(self, name: str) -> "logger":
        """Get a logger instance for a specific module
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Configured logger instance
        """
        if name not in self._loggers:
            self._loggers[name] = logger.bind(name=name)
        
        return self._loggers[name]
    
    @property
    def is_configured(self) -> bool:
        """Check if the logging system is configured
        
        Returns:
            True if configured, False otherwise
        """
        return self._configured


# Create a global instance
log_handler = LoguruHandler()


def get_logger(name: str) -> "logger":
    """Get a logger instance for a specific module
    
    This is the main function to get a logger in PyroItaly.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    # Configure with defaults if not already configured
    if not log_handler.is_configured:
        log_handler.configure()
    
    return log_handler.get_logger(name)


class PyroItalyError(Exception):
    """Base exception class for PyroItaly
    
    All PyroItaly exceptions inherit from this class.
    """
    
    def __init__(self, message: str = None):
        self.message = message or "An error occurred in PyroItaly"
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation of the error
        
        Returns:
            Error message
        """
        return self.message


class ConnectionError(PyroItalyError):
    """Exception raised for connection-related errors
    
    This exception is raised when there are issues with the connection
    to Telegram servers.
    """
    
    def __init__(self, message: str = None):
        super().__init__(message or "Failed to connect to Telegram servers")


class AuthenticationError(PyroItalyError):
    """Exception raised for authentication-related errors
    
    This exception is raised when there are issues with authentication
    or authorization.
    """
    
    def __init__(self, message: str = None):
        super().__init__(message or "Authentication failed")


class SessionError(PyroItalyError):
    """Exception raised for session-related errors
    
    This exception is raised when there are issues with the session
    management.
    """
    
    def __init__(self, message: str = None):
        super().__init__(message or "Session error occurred")


class APIError(PyroItalyError):
    """Exception raised for API-related errors
    
    This exception is raised when there are issues with the Telegram API
    responses or requests.
    """
    
    def __init__(self, message: str = None, code: int = None):
        self.code = code
        message_with_code = f"API error {code}: {message}" if code else message
        super().__init__(message_with_code or "Telegram API error")


class TimeoutError(PyroItalyError):
    """Exception raised for timeout-related errors
    
    This exception is raised when operations timeout.
    """
    
    def __init__(self, message: str = None):
        super().__init__(message or "Operation timed out")


class PluginError(PyroItalyError):
    """Exception raised for plugin-related errors
    
    This exception is raised when there are issues with plugins.
    """
    
    def __init__(self, message: str = None, plugin_name: str = None):
        self.plugin_name = plugin_name
        message_with_plugin = f"Plugin '{plugin_name}': {message}" if plugin_name else message
        super().__init__(message_with_plugin or "Plugin error occurred")


def format_exception(exc: Exception) -> str:
    """Format an exception with traceback for logging
    
    Args:
        exc: Exception to format
        
    Returns:
        Formatted exception string with traceback
    """
    tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return "".join(tb)
