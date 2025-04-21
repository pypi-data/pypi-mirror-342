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

import asyncio
import base64
import functools
import hashlib
import os
import struct
import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from getpass import getpass
from typing import Union, List, Dict, Optional, Any, Callable

# Use orjson for better performance if available
try:
    import orjson
    
    def json_loads(data: Union[str, bytes]) -> Any:
        """Fast JSON deserialization using orjson"""
        return orjson.loads(data)
    
    def json_dumps(data: Any) -> str:
        """Fast JSON serialization using orjson"""
        return orjson.dumps(data).decode('utf-8')
    
except ImportError:
    import json
    
    def json_loads(data: Union[str, bytes]) -> Any:
        """JSON deserialization using standard json module"""
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return json.loads(data)
    
    def json_dumps(data: Any) -> str:
        """JSON serialization using standard json module"""
        return json.dumps(data)


def zero_copy_view(data: bytes) -> memoryview:
    """Create a zero-copy view of the data using memoryview
    
    This avoids unnecessary memory allocations when working with binary data.
    
    Args:
        data: The binary data to create a view of
        
    Returns:
        A memoryview object that provides a zero-copy view of the data
    """
    return memoryview(data)


def async_cached(func: Callable) -> Callable:
    """Decorator to cache async function results
    
    This decorator caches the results of async functions to avoid
    redundant computations and improve performance.
    
    Args:
        func: The async function to cache
        
    Returns:
        Wrapped function with caching capability
    """
    cache = {}
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = await func(*args, **kwargs)
        return cache[key]
    
    return wrapper


def run_in_threadpool(func: Callable) -> Callable:
    """Run CPU-bound functions in a thread pool to avoid blocking the event loop
    
    Args:
        func: The function to run in a thread pool
        
    Returns:
        Wrapped function that runs in a thread pool
    """
    executor = ThreadPoolExecutor(max_workers=os.cpu_count())
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            executor, 
            functools.partial(func, *args, **kwargs)
        )
    
    return wrapper
