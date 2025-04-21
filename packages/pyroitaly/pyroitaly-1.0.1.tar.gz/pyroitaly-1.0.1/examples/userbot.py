#!/usr/bin/env python3
#  PyroItaly - Telegram MTProto API Client Library for Python
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
Example userbot script for PyroItaly

This example demonstrates how to create a Telegram userbot using PyroItaly.
It includes message handling, command filtering, and demonstrates
the use of the plugin system, auto reconnection, session management and other features.
"""

import asyncio
import logging
import os
import time
from datetime import datetime

from pyroitaly import Client, filters
from pyroitaly.types import Message
from pyroitaly.plugins import AutoReconnect, PluginSystem, SessionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Userbot configuration
API_ID = os.environ.get("API_ID", "12345")  # Replace with your API ID
API_HASH = os.environ.get("API_HASH", "abcdef1234567890abcdef1234567890")  # Replace with your API Hash
SESSION_NAME = "userbot_session"  # Session name for storage

# Initialize the client
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH
)

# Initialize auto reconnection
auto_reconnect = AutoReconnect(app)

# Initialize plugin system
plugin_system = PluginSystem(app)

# Command prefix for userbot commands
CMD_PREFIX = "."


# Register a sample plugin
def register_sample_plugin():
    plugin = plugin_system.register_plugin(
        name="userbot_tools",
        version="1.0.1",
        description="Useful tools for userbot",
        author="PyroItaly"
    )
    
    # Register plugin hooks
    plugin_system.register_hook("userbot_start", on_userbot_start)
    plugin_system.register_hook("userbot_stop", on_userbot_stop)


# Plugin hook handlers
async def on_userbot_start():
    logger.info("Userbot started hook triggered")


async def on_userbot_stop():
    logger.info("Userbot stopped hook triggered")


@app.on_message(filters.command("ping", prefixes=CMD_PREFIX) & filters.me)
async def ping_command(client: Client, message: Message):
    """Handler for .ping command"""
    start = time.time()
    reply = await message.edit_text("Pinging...")
    end = time.time()
    
    ping_time = round((end - start) * 1000, 2)
    await reply.edit_text(f"Pong! `{ping_time}ms`")


@app.on_message(filters.command("alive", prefixes=CMD_PREFIX) & filters.me)
async def alive_command(client: Client, message: Message):
    """Handler for .alive command"""
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
    
    alive_text = (
        f"**PyroItaly Userbot**\n\n"
        f"**User:** {me.first_name}\n"
        f"**ID:** `{me.id}`\n"
        f"**Uptime:** `{uptime_str}`\n"
        f"**Memory Usage:** `{memory_usage:.2f} MB`\n"
        f"**PyroItaly Version:** `{client.version}`\n"
    )
    
    await message.edit_text(alive_text)


@app.on_message(filters.command("id", prefixes=CMD_PREFIX) & filters.me)
async def id_command(client: Client, message: Message):
    """Handler for .id command"""
    if message.reply_to_message:
        # Get ID of the replied user
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        
        text = f"**User ID:** `{user_id}`\n**Chat ID:** `{chat_id}`"
        
        if message.reply_to_message.forward_from:
            forward_id = message.reply_to_message.forward_from.id
            text += f"\n**Forwarded From:** `{forward_id}`"
    else:
        # Get chat ID
        chat_id = message.chat.id
        text = f"**Chat ID:** `{chat_id}`"
        
        if message.from_user:
            text = f"**User ID:** `{message.from_user.id}`\n{text}"
    
    await message.edit_text(text)


@app.on_message(filters.command("info", prefixes=CMD_PREFIX) & filters.me)
async def info_command(client: Client, message: Message):
    """Handler for .info command"""
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            await message.edit_text("User not found.")
            return
    elif message.from_user:
        user = message.from_user
    else:
        await message.edit_text("Specify a user or reply to a message.")
        return
    
    text = f"**User Info**\n\n"
    text += f"**ID:** `{user.id}`\n"
    text += f"**First Name:** {user.first_name}\n"
    
    if user.last_name:
        text += f"**Last Name:** {user.last_name}\n"
    
    if user.username:
        text += f"**Username:** @{user.username}\n"
    
    text += f"**Permanent Link:** [link](tg://user?id={user.id})\n"
    text += f"**Is Bot:** {user.is_bot}\n"
    
    if user.status:
        text += f"**Status:** {user.status}\n"
    
    if user.language_code:
        text += f"**Language Code:** {user.language_code}\n"
    
    await message.edit_text(text, disable_web_page_preview=True)


@app.on_message(filters.command("purge", prefixes=CMD_PREFIX) & filters.me)
async def purge_command(client: Client, message: Message):
    """Handler for .purge command - delete messages"""
    if not message.reply_to_message:
        await message.edit_text("Reply to a message to start purging from.")
        return
    
    message_ids = []
    start_message_id = message.reply_to_message.id
    current_message_id = message.id
    
    # Collect message IDs to delete
    for message_id in range(start_message_id, current_message_id + 1):
        message_ids.append(message_id)
    
    # Delete in chunks of 100 (Telegram limit)
    n_deleted = 0
    for i in range(0, len(message_ids), 100):
        chunk = message_ids[i:i + 100]
        try:
            await client.delete_messages(message.chat.id, chunk)
            n_deleted += len(chunk)
        except Exception as e:
            logger.error(f"Error deleting messages: {e}")
    
    # Send confirmation and delete it after 5 seconds
    confirm = await client.send_message(message.chat.id, f"Purged {n_deleted} messages.")
    await asyncio.sleep(5)
    await confirm.delete()


@app.on_message(filters.command("export_session", prefixes=CMD_PREFIX) & filters.me & filters.private)
async def export_session_command(client: Client, message: Message):
    """Handler for .export_session command - export session for backup"""
    # Only allow in private chats for security
    if not message.chat.type == "private":
        await message.edit_text("⚠️ This command can only be used in private chats for security reasons.")
        return
    
    await message.edit_text("Exporting session... Please wait.")
    
    try:
        # Get optional password if provided
        password = None
        if len(message.command) > 1:
            password = message.command[1]
        
        # Export session
        session_str = await SessionManager.export_session(client, password)
        
        # Send as a text file for better security
        import io
        file = io.BytesIO(session_str.encode())
        file.name = f"pyroitaly_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        await message.delete()  # Delete the command message for security
        
        await client.send_document(
            message.chat.id,
            file,
            caption="🔐 **Exported Session**\n\nKeep this file secure and private. "
                    "It can be used to access your account."
        )
    except Exception as e:
        await message.edit_text(f"Error exporting session: {str(e)}")


@app.on_message(filters.command("echo", prefixes=CMD_PREFIX) & filters.me)
async def echo_command(client: Client, message: Message):
    """Handler for .echo command"""
    # Get the text after the command
    if len(message.command) > 1:
        text = message.text.split(None, 1)[1]
        await message.edit_text(text)
    else:
        await message.edit_text("Please provide some text to echo.")


@app.on_message(filters.command("help", prefixes=CMD_PREFIX) & filters.me)
async def help_command(client: Client, message: Message):
    """Handler for .help command"""
    help_text = (
        "**PyroItaly Userbot Commands**\n\n"
        f"{CMD_PREFIX}ping - Check response time\n"
        f"{CMD_PREFIX}alive - Show userbot status\n"
        f"{CMD_PREFIX}id - Get user/chat ID\n"
        f"{CMD_PREFIX}info - Get detailed user info\n"
        f"{CMD_PREFIX}purge - Delete messages\n"
        f"{CMD_PREFIX}echo [text] - Echo back text\n"
        f"{CMD_PREFIX}export_session [password] - Export session (private chat only)\n"
        f"{CMD_PREFIX}help - Show this help message\n"
    )
    
    await message.edit_text(help_text)


async def main():
    """Main function to start the userbot"""
    # Register plugins
    register_sample_plugin()
    
    # Start the client
    await app.start()
    app.start_time = time.time()  # Track start time
    
    # Start auto reconnection
    await auto_reconnect.start()
    
    # Trigger the userbot_start hook
    await plugin_system.trigger_hook("userbot_start")
    
    logger.info("Userbot started successfully!")
    
    # Keep the userbot running
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Userbot stopped by user")
    finally:
        # Trigger the userbot_stop hook
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(plugin_system.trigger_hook("userbot_stop"))
            else:
                asyncio.run(plugin_system.trigger_hook("userbot_stop"))
        except Exception as e:
            logger.error(f"Error triggering userbot_stop hook: {e}")
