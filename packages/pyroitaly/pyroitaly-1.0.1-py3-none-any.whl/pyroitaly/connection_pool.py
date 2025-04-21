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
import logging
import time
from typing import Dict, List, Optional, Tuple, Union

from .connection.transport import TCP, TCPAbridged
from .session.internals import DataCenter

log = logging.getLogger(__name__)


class ConnectionPool:
    """TCP Connection Pool for more efficient connection management
    
    This class manages a pool of TCP connections to Telegram servers,
    allowing for connection reuse and more efficient network operations.
    """
    
    def __init__(self, max_connections: int = 8):
        """Initialize the connection pool
        
        Args:
            max_connections: Maximum number of connections to keep in the pool
        """
        self.max_connections = max_connections
        self.connections: Dict[str, List[Tuple[TCP, float]]] = {}
        self.lock = asyncio.Lock()
        self.cleanup_task = None
    
    async def start(self):
        """Start the connection pool and its maintenance tasks"""
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def stop(self):
        """Stop the connection pool and close all connections"""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.cleanup_task = None
        
        async with self.lock:
            for key in list(self.connections.keys()):
                for conn, _ in self.connections[key]:
                    await conn.close()
                self.connections[key] = []
    
    async def _cleanup_loop(self):
        """Periodically clean up idle connections"""
        while True:
            await asyncio.sleep(60)  # Run cleanup every minute
            await self._cleanup_idle_connections()
    
    async def _cleanup_idle_connections(self, max_idle_time: int = 300):
        """Remove connections that have been idle for too long
        
        Args:
            max_idle_time: Maximum time in seconds a connection can be idle
        """
        now = time.time()
        async with self.lock:
            for key in list(self.connections.keys()):
                # Keep connections that are not too old
                active_connections = []
                for conn, last_used in self.connections[key]:
                    if now - last_used < max_idle_time:
                        active_connections.append((conn, last_used))
                    else:
                        await conn.close()
                        log.debug(f"Closed idle connection to {key}")
                
                self.connections[key] = active_connections
    
    async def get_connection(self, dc: DataCenter, transport_mode: str = "tcp_abridged") -> TCP:
        """Get a connection from the pool or create a new one
        
        Args:
            dc: DataCenter information
            transport_mode: Transport mode to use
            
        Returns:
            A TCP connection object
        """
        key = f"{dc.ip}:{dc.port}:{transport_mode}"
        
        async with self.lock:
            if key not in self.connections:
                self.connections[key] = []
            
            # Try to get an existing connection
            if self.connections[key]:
                conn, _ = self.connections[key].pop(0)
                return conn
        
        # Create a new connection if none available
        if transport_mode == "tcp_abridged":
            conn = TCPAbridged(dc.ip, dc.port)
        else:
            conn = TCP(dc.ip, dc.port)
        
        await conn.connect()
        return conn
    
    async def release_connection(self, conn: TCP, dc: DataCenter, transport_mode: str = "tcp_abridged"):
        """Return a connection to the pool
        
        Args:
            conn: The connection to release
            dc: DataCenter information
            transport_mode: Transport mode used
        """
        if not conn.is_connected:
            return
        
        key = f"{dc.ip}:{dc.port}:{transport_mode}"
        
        async with self.lock:
            if key not in self.connections:
                self.connections[key] = []
            
            # Only keep the connection if we're under the limit
            if len(self.connections[key]) < self.max_connections:
                self.connections[key].append((conn, time.time()))
            else:
                await conn.close()
