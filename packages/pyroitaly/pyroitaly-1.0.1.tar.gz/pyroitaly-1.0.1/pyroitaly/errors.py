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
PyroItaly Error Handling System

This module provides a comprehensive error handling system for PyroItaly,
with detailed error messages, error codes, and suggestions for resolution.
"""

import inspect
import os
import sys
import traceback
from typing import Dict, Any, Optional, Union, List, Callable, Type, TypeVar

from .logging import get_logger

logger = get_logger(__name__)

# Type variable for error classes
E = TypeVar('E', bound='PyroItalyError')


class ErrorInfo:
    """Information about an error, including code, description, and resolution
    
    This class provides detailed information about errors that can occur
    in PyroItaly, including error codes, descriptions, and suggestions
    for resolution.
    """
    
    def __init__(
        self,
        code: str,
        description: str,
        resolution: Optional[str] = None,
        docs_url: Optional[str] = None
    ):
        """Initialize error information
        
        Args:
            code: Error code (e.g., "AUTH_001")
            description: Description of the error
            resolution: Suggested resolution steps
            docs_url: URL to documentation about this error
        """
        self.code = code
        self.description = description
        self.resolution = resolution
        self.docs_url = docs_url
    
    def __str__(self) -> str:
        """String representation of the error information
        
        Returns:
            Formatted error information string
        """
        result = f"[{self.code}] {self.description}"
        
        if self.resolution:
            result += f"\n\nResolution: {self.resolution}"
        
        if self.docs_url:
            result += f"\n\nFor more information, see: {self.docs_url}"
        
        return result


# Error registry to store all error types and their information
ERROR_REGISTRY: Dict[str, ErrorInfo] = {}


def register_error(
    error_class: Type[E],
    code: str,
    description: str,
    resolution: Optional[str] = None,
    docs_url: Optional[str] = None
) -> Type[E]:
    """Register an error class with its information
    
    This decorator registers an error class with its code, description,
    and resolution information.
    
    Args:
        error_class: Error class to register
        code: Error code (e.g., "AUTH_001")
        description: Description of the error
        resolution: Suggested resolution steps
        docs_url: URL to documentation about this error
        
    Returns:
        The original error class
    """
    error_info = ErrorInfo(code, description, resolution, docs_url)
    ERROR_REGISTRY[error_class.__name__] = error_info
    
    # Add error info to the class
    error_class.error_info = error_info
    
    return error_class


class PyroItalyError(Exception):
    """Base exception class for PyroItaly
    
    All PyroItaly exceptions inherit from this class.
    """
    
    # Default error info
    error_info = ErrorInfo(
        code="PYRO_000",
        description="An unknown error occurred in PyroItaly",
        resolution="Check the logs for more details"
    )
    
    def __init__(self, message: Optional[str] = None, **kwargs):
        """Initialize the error
        
        Args:
            message: Custom error message
            **kwargs: Additional error context
        """
        self.message = message or self.error_info.description
        self.context = kwargs
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation of the error
        
        Returns:
            Formatted error string with code, message, and context
        """
        result = f"[{self.error_info.code}] {self.message}"
        
        if self.context:
            result += "\n\nContext:"
            for key, value in self.context.items():
                result += f"\n- {key}: {value}"
        
        if self.error_info.resolution:
            result += f"\n\nResolution: {self.error_info.resolution}"
        
        if self.error_info.docs_url:
            result += f"\n\nFor more information, see: {self.error_info.docs_url}"
        
        return result
    
    @classmethod
    def from_exception(cls, exc: Exception, **kwargs) -> 'PyroItalyError':
        """Create a PyroItalyError from another exception
        
        Args:
            exc: Original exception
            **kwargs: Additional error context
            
        Returns:
            PyroItalyError instance
        """
        return cls(str(exc), original_exception=type(exc).__name__, **kwargs)


@register_error(
    error_class=PyroItalyError,
    code="PYRO_000",
    description="An unknown error occurred in PyroItaly",
    resolution="Check the logs for more details",
    docs_url="https://docs.pyroitaly.org/errors/PYRO_000"
)
class UnknownError(PyroItalyError):
    """Exception raised for unknown errors
    
    This exception is raised when an unknown error occurs in PyroItaly.
    """
    pass


@register_error(
    error_class=PyroItalyError,
    code="CONN_001",
    description="Failed to connect to Telegram servers",
    resolution="Check your internet connection and try again",
    docs_url="https://docs.pyroitaly.org/errors/CONN_001"
)
class ConnectionError(PyroItalyError):
    """Exception raised for connection-related errors
    
    This exception is raised when there are issues with the connection
    to Telegram servers.
    """
    pass


@register_error(
    error_class=PyroItalyError,
    code="CONN_002",
    description="Connection timed out",
    resolution="Check your internet connection and try again",
    docs_url="https://docs.pyroitaly.org/errors/CONN_002"
)
class TimeoutError(PyroItalyError):
    """Exception raised for timeout-related errors
    
    This exception is raised when operations timeout.
    """
    pass


@register_error(
    error_class=PyroItalyError,
    code="AUTH_001",
    description="Authentication failed",
    resolution="Check your API ID, API hash, and other credentials",
    docs_url="https://docs.pyroitaly.org/errors/AUTH_001"
)
class AuthenticationError(PyroItalyError):
    """Exception raised for authentication-related errors
    
    This exception is raised when there are issues with authentication
    or authorization.
    """
    pass


@register_error(
    error_class=PyroItalyError,
    code="AUTH_002",
    description="Session expired or invalid",
    resolution="Create a new session or re-authenticate",
    docs_url="https://docs.pyroitaly.org/errors/AUTH_002"
)
class SessionError(PyroItalyError):
    """Exception raised for session-related errors
    
    This exception is raised when there are issues with the session
    management.
    """
    pass


@register_error(
    error_class=PyroItalyError,
    code="API_001",
    description="Telegram API error",
    resolution="Check the error code and message for more details",
    docs_url="https://docs.pyroitaly.org/errors/API_001"
)
class APIError(PyroItalyError):
    """Exception raised for API-related errors
    
    This exception is raised when there are issues with the Telegram API
    responses or requests.
    """
    
    def __init__(self, message: Optional[str] = None, code: Optional[int] = None, **kwargs):
        """Initialize the API error
        
        Args:
            message: Custom error message
            code: API error code
            **kwargs: Additional error context
        """
        self.api_code = code
        message_with_code = f"API error {code}: {message}" if code else message
        super().__init__(message_with_code, api_code=code, **kwargs)


@register_error(
    error_class=PyroItalyError,
    code="PLUGIN_001",
    description="Plugin error",
    resolution="Check the plugin implementation and dependencies",
    docs_url="https://docs.pyroitaly.org/errors/PLUGIN_001"
)
class PluginError(PyroItalyError):
    """Exception raised for plugin-related errors
    
    This exception is raised when there are issues with plugins.
    """
    
    def __init__(self, message: Optional[str] = None, plugin_name: Optional[str] = None, **kwargs):
        """Initialize the plugin error
        
        Args:
            message: Custom error message
            plugin_name: Name of the plugin that caused the error
            **kwargs: Additional error context
        """
        message_with_plugin = f"Plugin '{plugin_name}': {message}" if plugin_name else message
        super().__init__(message_with_plugin, plugin_name=plugin_name, **kwargs)


@register_error(
    error_class=PyroItalyError,
    code="FLOOD_001",
    description="Too many requests (flood wait)",
    resolution="Wait for the specified time before making more requests",
    docs_url="https://docs.pyroitaly.org/errors/FLOOD_001"
)
class FloodWaitError(PyroItalyError):
    """Exception raised for flood wait errors
    
    This exception is raised when Telegram servers indicate that
    the client is making too many requests.
    """
    
    def __init__(self, message: Optional[str] = None, seconds: Optional[int] = None, **kwargs):
        """Initialize the flood wait error
        
        Args:
            message: Custom error message
            seconds: Number of seconds to wait
            **kwargs: Additional error context
        """
        self.seconds = seconds
        message_with_seconds = f"Flood wait for {seconds} seconds" if seconds else message
        super().__init__(message_with_seconds, wait_seconds=seconds, **kwargs)


@register_error(
    error_class=PyroItalyError,
    code="PARAM_001",
    description="Invalid parameter",
    resolution="Check the parameter type and value",
    docs_url="https://docs.pyroitaly.org/errors/PARAM_001"
)
class InvalidParameterError(PyroItalyError):
    """Exception raised for invalid parameter errors
    
    This exception is raised when a function or method receives
    an invalid parameter.
    """
    
    def __init__(self, message: Optional[str] = None, param_name: Optional[str] = None, **kwargs):
        """Initialize the invalid parameter error
        
        Args:
            message: Custom error message
            param_name: Name of the invalid parameter
            **kwargs: Additional error context
        """
        message_with_param = f"Invalid parameter '{param_name}': {message}" if param_name else message
        super().__init__(message_with_param, param_name=param_name, **kwargs)


def format_exception(exc: Exception) -> str:
    """Format an exception with traceback for logging
    
    Args:
        exc: Exception to format
        
    Returns:
        Formatted exception string with traceback
    """
    tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return "".join(tb)


def handle_error(func: Callable) -> Callable:
    """Decorator to handle errors in functions
    
    This decorator catches exceptions and converts them to PyroItalyError
    instances with appropriate context.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PyroItalyError:
            # Already a PyroItalyError, just re-raise
            raise
        except Exception as e:
            # Convert to PyroItalyError with context
            logger.error(f"Error in {func.__name__}: {e}")
            logger.debug(format_exception(e))
            
            # Get function context
            frame = inspect.currentframe()
            if frame:
                frame_info = inspect.getframeinfo(frame)
                file_name = os.path.basename(frame_info.filename)
                line_number = frame_info.lineno
                context = {
                    "function": func.__name__,
                    "file": file_name,
                    "line": line_number
                }
            else:
                context = {"function": func.__name__}
            
            raise UnknownError.from_exception(e, **context)
    
    return wrapper


def async_handle_error(func: Callable) -> Callable:
    """Decorator to handle errors in async functions
    
    This decorator catches exceptions in async functions and converts them
    to PyroItalyError instances with appropriate context.
    
    Args:
        func: Async function to decorate
        
    Returns:
        Decorated async function
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PyroItalyError:
            # Already a PyroItalyError, just re-raise
            raise
        except Exception as e:
            # Convert to PyroItalyError with context
            logger.error(f"Error in {func.__name__}: {e}")
            logger.debug(format_exception(e))
            
            # Get function context
            frame = inspect.currentframe()
            if frame:
                frame_info = inspect.getframeinfo(frame)
                file_name = os.path.basename(frame_info.filename)
                line_number = frame_info.lineno
                context = {
                    "function": func.__name__,
                    "file": file_name,
                    "line": line_number
                }
            else:
                context = {"function": func.__name__}
            
            raise UnknownError.from_exception(e, **context)
    
    return wrapper
