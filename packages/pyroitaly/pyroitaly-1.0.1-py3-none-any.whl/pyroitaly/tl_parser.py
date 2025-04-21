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

import logging
import struct
from typing import Any, Dict, List, Optional, Tuple, Union

from .utils import zero_copy_view

log = logging.getLogger(__name__)


class TLParser:
    """Optimized TL-Schema parser with zero-copy operations
    
    This class provides optimized parsing of Telegram's Type Language (TL) schema
    using zero-copy operations with memoryview and struct for better performance.
    """
    
    def __init__(self):
        # Pre-compile common struct formats for better performance
        self._int_struct = struct.Struct("<i")
        self._long_struct = struct.Struct("<q")
        self._double_struct = struct.Struct("<d")
        self._int128_struct = struct.Struct("<16s")
        self._int256_struct = struct.Struct("<32s")
    
    def parse_int(self, data: Union[bytes, memoryview], offset: int = 0) -> int:
        """Parse a 32-bit integer from binary data
        
        Args:
            data: Binary data to parse
            offset: Offset in the data
            
        Returns:
            Parsed integer value
        """
        if isinstance(data, bytes):
            data = zero_copy_view(data)
        return self._int_struct.unpack_from(data, offset)[0]
    
    def parse_long(self, data: Union[bytes, memoryview], offset: int = 0) -> int:
        """Parse a 64-bit integer from binary data
        
        Args:
            data: Binary data to parse
            offset: Offset in the data
            
        Returns:
            Parsed long integer value
        """
        if isinstance(data, bytes):
            data = zero_copy_view(data)
        return self._long_struct.unpack_from(data, offset)[0]
    
    def parse_double(self, data: Union[bytes, memoryview], offset: int = 0) -> float:
        """Parse a double-precision float from binary data
        
        Args:
            data: Binary data to parse
            offset: Offset in the data
            
        Returns:
            Parsed float value
        """
        if isinstance(data, bytes):
            data = zero_copy_view(data)
        return self._double_struct.unpack_from(data, offset)[0]
    
    def parse_bytes(self, data: Union[bytes, memoryview], offset: int = 0) -> Tuple[bytes, int]:
        """Parse a bytes field from binary data
        
        Args:
            data: Binary data to parse
            offset: Offset in the data
            
        Returns:
            Tuple of (parsed bytes, new offset)
        """
        if isinstance(data, bytes):
            data = zero_copy_view(data)
        
        length = data[offset]
        
        if length < 254:
            # Short form: 1 byte length + data + padding
            padding = (length + 1) % 4
            if padding > 0:
                padding = 4 - padding
            
            result = bytes(data[offset+1:offset+1+length])
            new_offset = offset + 1 + length + padding
            return result, new_offset
        else:
            # Long form: 4 bytes length + data + padding
            length = self.parse_int(data, offset+1)
            padding = length % 4
            if padding > 0:
                padding = 4 - padding
            
            result = bytes(data[offset+5:offset+5+length])
            new_offset = offset + 5 + length + padding
            return result, new_offset
    
    def parse_string(self, data: Union[bytes, memoryview], offset: int = 0) -> Tuple[str, int]:
        """Parse a string field from binary data
        
        Args:
            data: Binary data to parse
            offset: Offset in the data
            
        Returns:
            Tuple of (parsed string, new offset)
        """
        bytes_value, new_offset = self.parse_bytes(data, offset)
        return bytes_value.decode('utf-8', errors='replace'), new_offset
    
    def serialize_int(self, value: int) -> bytes:
        """Serialize a 32-bit integer to binary data
        
        Args:
            value: Integer value to serialize
            
        Returns:
            Serialized binary data
        """
        return self._int_struct.pack(value)
    
    def serialize_long(self, value: int) -> bytes:
        """Serialize a 64-bit integer to binary data
        
        Args:
            value: Long integer value to serialize
            
        Returns:
            Serialized binary data
        """
        return self._long_struct.pack(value)
    
    def serialize_double(self, value: float) -> bytes:
        """Serialize a double-precision float to binary data
        
        Args:
            value: Float value to serialize
            
        Returns:
            Serialized binary data
        """
        return self._double_struct.pack(value)
    
    def serialize_bytes(self, value: bytes) -> bytes:
        """Serialize a bytes field to binary data
        
        Args:
            value: Bytes value to serialize
            
        Returns:
            Serialized binary data
        """
        length = len(value)
        
        if length < 254:
            # Short form
            padding = (length + 1) % 4
            if padding > 0:
                padding = 4 - padding
            
            return bytes([length]) + value + bytes(padding)
        else:
            # Long form
            padding = length % 4
            if padding > 0:
                padding = 4 - padding
            
            return bytes([254]) + self.serialize_int(length) + value + bytes(padding)
    
    def serialize_string(self, value: str) -> bytes:
        """Serialize a string field to binary data
        
        Args:
            value: String value to serialize
            
        Returns:
            Serialized binary data
        """
        return self.serialize_bytes(value.encode('utf-8'))


# Create a global instance for convenience
tl_parser = TLParser()
