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
from typing import Optional, Dict, Any, List, Callable, Union

from .client import Client
from .types import Message, User, Chat

log = logging.getLogger(__name__)


class AutoReconnect:
    """Auto reconnection handler for PyroItaly clients
    
    This class provides automatic reconnection capabilities for PyroItaly clients
    when connection issues occur, with configurable retry policies.
    """
    
    def __init__(
        self, 
        client: Client,
        max_retries: int = 5,
        retry_delay: int = 5,
        exponential_backoff: bool = True,
        max_delay: int = 300
    ):
        """Initialize the auto reconnection handler
        
        Args:
            client: The PyroItaly client to handle
            max_retries: Maximum number of reconnection attempts
            retry_delay: Initial delay between retries in seconds
            exponential_backoff: Whether to use exponential backoff for retries
            max_delay: Maximum delay between retries in seconds
        """
        self.client = client
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.exponential_backoff = exponential_backoff
        self.max_delay = max_delay
        self._retry_count = 0
        self._is_connected = False
        self._monitor_task = None
        
        # Register connection handlers
        self.client.add_handler(self._on_disconnect, -100)
    
    async def start(self):
        """Start the auto reconnection monitor"""
        self._is_connected = True
        self._retry_count = 0
        
        if self._monitor_task is None:
            self._monitor_task = asyncio.create_task(self._connection_monitor())
    
    async def stop(self):
        """Stop the auto reconnection monitor"""
        self._is_connected = False
        
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            self._monitor_task = None
    
    async def _on_disconnect(self, client: Client):
        """Handle disconnection events
        
        Args:
            client: The client that disconnected
        """
        if self._is_connected:
            log.warning("Client disconnected, attempting to reconnect...")
            await self._attempt_reconnect()
    
    async def _attempt_reconnect(self):
        """Attempt to reconnect the client with retry policy"""
        self._retry_count = 0
        current_delay = self.retry_delay
        
        while self._retry_count < self.max_retries and self._is_connected:
            self._retry_count += 1
            
            log.info(f"Reconnection attempt {self._retry_count}/{self.max_retries} in {current_delay} seconds...")
            await asyncio.sleep(current_delay)
            
            try:
                if not self.client.is_connected:
                    await self.client.connect()
                    log.info("Successfully reconnected!")
                    self._retry_count = 0
                    break
            except Exception as e:
                log.error(f"Reconnection attempt failed: {e}")
                
                # Calculate next delay with exponential backoff if enabled
                if self.exponential_backoff:
                    current_delay = min(current_delay * 2, self.max_delay)
        
        if self._retry_count >= self.max_retries and self._is_connected:
            log.error(f"Failed to reconnect after {self.max_retries} attempts")
    
    async def _connection_monitor(self):
        """Monitor connection status periodically"""
        while self._is_connected:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            if not self.client.is_connected and self._is_connected:
                log.warning("Connection monitor detected disconnection")
                await self._attempt_reconnect()


class SessionManager:
    """Session management utilities for PyroItaly
    
    This class provides utilities for exporting and importing sessions,
    allowing users to backup and restore their session data.
    """
    
    @staticmethod
    async def export_session(client: Client, password: Optional[str] = None) -> str:
        """Export a session to a portable string format
        
        Args:
            client: The client whose session to export
            password: Optional password to encrypt the session data
            
        Returns:
            Exported session string
        """
        if not client.is_connected:
            raise ValueError("Client must be connected to export session")
        
        # Get session data
        session_data = {
            "dc_id": client.storage.dc_id(),
            "api_id": client.api_id,
            "test_mode": client.test_mode,
            "auth_key": client.storage.auth_key(),
            "user_id": client.storage.user_id(),
            "date": int(time.time())
        }
        
        # Convert to string
        import base64
        import json
        
        session_str = base64.b64encode(json.dumps(session_data).encode()).decode()
        
        # Encrypt if password provided
        if password:
            import hashlib
            from cryptography.fernet import Fernet
            
            key = hashlib.sha256(password.encode()).digest()
            f = Fernet(base64.urlsafe_b64encode(key))
            session_str = f.encrypt(session_str.encode()).decode()
        
        return f"pyroitaly:{session_str}"
    
    @staticmethod
    async def import_session(
        client: Client, 
        session_str: str, 
        password: Optional[str] = None
    ) -> bool:
        """Import a session from a string format
        
        Args:
            client: The client to import the session into
            session_str: The session string to import
            password: Optional password to decrypt the session data
            
        Returns:
            True if import was successful
        """
        if client.is_connected:
            raise ValueError("Client must be disconnected to import session")
        
        # Check format
        if not session_str.startswith("pyroitaly:"):
            raise ValueError("Invalid session string format")
        
        session_str = session_str[10:]  # Remove prefix
        
        # Decrypt if password provided
        if password:
            import base64
            import hashlib
            from cryptography.fernet import Fernet
            
            try:
                key = hashlib.sha256(password.encode()).digest()
                f = Fernet(base64.urlsafe_b64encode(key))
                session_str = f.decrypt(session_str.encode()).decode()
            except Exception:
                raise ValueError("Invalid password or corrupted session data")
        
        # Parse session data
        import base64
        import json
        
        try:
            session_data = json.loads(base64.b64decode(session_str).decode())
        except Exception:
            raise ValueError("Corrupted session data")
        
        # Validate required fields
        required_fields = ["dc_id", "api_id", "auth_key", "user_id"]
        for field in required_fields:
            if field not in session_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Import into client storage
        client.storage.dc_id(session_data["dc_id"])
        client.storage.auth_key(session_data["auth_key"])
        client.storage.user_id(session_data["user_id"])
        
        return True


class PluginSystem:
    """Plugin system for PyroItaly
    
    This class provides a plugin system that allows users to extend
    PyroItaly functionality with custom plugins.
    """
    
    def __init__(self, client: Client):
        """Initialize the plugin system
        
        Args:
            client: The PyroItaly client to attach plugins to
        """
        self.client = client
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(
        self, 
        name: str, 
        version: str, 
        description: str, 
        author: str
    ) -> Dict[str, Any]:
        """Register a new plugin
        
        Args:
            name: Plugin name
            version: Plugin version
            description: Plugin description
            author: Plugin author
            
        Returns:
            Plugin metadata dictionary
        """
        if name in self.plugins:
            raise ValueError(f"Plugin {name} is already registered")
        
        plugin_data = {
            "name": name,
            "version": version,
            "description": description,
            "author": author,
            "handlers": [],
            "commands": [],
            "enabled": True
        }
        
        self.plugins[name] = plugin_data
        log.info(f"Registered plugin: {name} v{version} by {author}")
        
        return plugin_data
    
    def unregister_plugin(self, name: str) -> bool:
        """Unregister a plugin
        
        Args:
            name: Plugin name to unregister
            
        Returns:
            True if plugin was unregistered
        """
        if name not in self.plugins:
            return False
        
        # Remove all handlers
        for handler_id in self.plugins[name]["handlers"]:
            self.client.remove_handler(handler_id)
        
        # Remove all commands
        for command in self.plugins[name]["commands"]:
            # TODO: Implement command removal
            pass
        
        # Remove plugin
        del self.plugins[name]
        log.info(f"Unregistered plugin: {name}")
        
        return True
    
    def register_handler(self, plugin_name: str, handler, group: int = 0) -> int:
        """Register a handler for a plugin
        
        Args:
            plugin_name: Plugin name
            handler: Handler function
            group: Handler group
            
        Returns:
            Handler ID
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        
        handler_id = self.client.add_handler(handler, group)
        self.plugins[plugin_name]["handlers"].append(handler_id)
        
        return handler_id
    
    def register_command(
        self, 
        plugin_name: str, 
        command: str, 
        handler: Callable[[Client, Message], Any], 
        description: str = ""
    ) -> None:
        """Register a command for a plugin
        
        Args:
            plugin_name: Plugin name
            command: Command name (without /)
            handler: Command handler function
            description: Command description
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} is not registered")
        
        from pyroitaly import filters
        
        # Register command handler
        handler_id = self.client.add_handler(
            handler=handler,
            filters=filters.command(command),
            group=0
        )
        
        self.plugins[plugin_name]["handlers"].append(handler_id)
        self.plugins[plugin_name]["commands"].append({
            "command": command,
            "description": description
        })
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a hook callback
        
        Args:
            hook_name: Hook name
            callback: Hook callback function
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append(callback)
    
    async def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger a hook with arguments
        
        Args:
            hook_name: Hook name to trigger
            *args: Positional arguments to pass to hooks
            **kwargs: Keyword arguments to pass to hooks
            
        Returns:
            List of results from hook callbacks
        """
        results = []
        
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    if asyncio.iscoroutine(result):
                        result = await result
                    results.append(result)
                except Exception as e:
                    log.error(f"Error in hook {hook_name}: {e}")
        
        return results
    
    def get_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered plugins
        
        Returns:
            Dictionary of plugins
        """
        return self.plugins
    
    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin was enabled
        """
        if name not in self.plugins:
            return False
        
        self.plugins[name]["enabled"] = True
        return True
    
    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin was disabled
        """
        if name not in self.plugins:
            return False
        
        self.plugins[name]["enabled"] = False
        return True


# Utility commands for bots
async def cmd_ping(client: Client, message: Message):
    """Ping command to check bot responsiveness
    
    Args:
        client: The PyroItaly client
        message: The command message
    """
    start = time.time()
    reply = await message.reply_text("Pinging...")
    end = time.time()
    
    ping_time = round((end - start) * 1000, 2)
    await reply.edit_text(f"Pong! `{ping_time}ms`")


async def cmd_status(client: Client, message: Message):
    """Status command to check bot status
    
    Args:
        client: The PyroItaly client
        message: The command message
    """
    start_time = getattr(client, "start_time", time.time())
    uptime = time.time() - start_time
    
    # Format uptime
    days, remainder = divmod(int(uptime), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    # Get memory usage
    import os
    import psutil
    
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    
    # Get client info
    me = await client.get_me()
    
    status_text = (
        f"**Bot Status**\n\n"
        f"**Name:** {me.first_name}\n"
        f"**ID:** `{me.id}`\n"
        f"**Uptime:** `{uptime_str}`\n"
        f"**Memory Usage:** `{memory_usage:.2f} MB`\n"
        f"**PyroItaly Version:** `{client.version}`\n"
    )
    
    await message.reply_text(status_text)


async def cmd_debug(client: Client, message: Message):
    """Debug command to get detailed debug information
    
    Args:
        client: The PyroItaly client
        message: The command message
    """
    import platform
    import sys
    
    # System info
    system_info = (
        f"**System Information**\n"
        f"**OS:** `{platform.system()} {platform.release()}`\n"
        f"**Python:** `{platform.python_version()}`\n"
        f"**PyroItaly:** `{client.version}`\n\n"
    )
    
    # Connection info
    dc_id = client.storage.dc_id()
    is_bot = getattr(client, "bot", False)
    
    connection_info = (
        f"**Connection Information**\n"
        f"**DC ID:** `{dc_id}`\n"
        f"**Bot Account:** `{is_bot}`\n"
        f"**IPv6:** `{getattr(client, 'ipv6', False)}`\n"
        f"**Connected:** `{client.is_connected}`\n\n"
    )
    
    # Message info
    chat_info = (
        f"**Message Information**\n"
        f"**Chat ID:** `{message.chat.id}`\n"
        f"**Message ID:** `{message.id}`\n"
        f"**User ID:** `{message.from_user.id if message.from_user else 'N/A'}`\n"
    )
    
    debug_text = system_info + connection_info + chat_info
    await message.reply_text(debug_text)
