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
Example bot script for PyroItaly

This example demonstrates how to create a Telegram bot using PyroItaly.
It includes basic command handling, message filtering, and demonstrates
the use of the plugin system, auto reconnection, and other features.
"""

import asyncio
import logging
import os
from datetime import datetime

from pyroitaly import Client, filters
from pyroitaly.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyroitaly.plugins import AutoReconnect, PluginSystem, cmd_ping, cmd_status, cmd_debug

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot configuration
API_ID = os.environ.get("API_ID", "12345")  # Replace with your API ID
API_HASH = os.environ.get("API_HASH", "abcdef1234567890abcdef1234567890")  # Replace with your API Hash
BOT_TOKEN = os.environ.get("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")  # Replace with your bot token

# Initialize the client
app = Client(
    "example_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize auto reconnection
auto_reconnect = AutoReconnect(app)

# Initialize plugin system
plugin_system = PluginSystem(app)


# Register a sample plugin
def register_sample_plugin():
    plugin = plugin_system.register_plugin(
        name="sample_plugin",
        version="1.0.1",
        description="A sample plugin for demonstration",
        author="PyroItaly"
    )
    
    # Register plugin hooks
    plugin_system.register_hook("bot_start", on_bot_start)
    plugin_system.register_hook("bot_stop", on_bot_stop)
    
    # Register plugin commands
    plugin_system.register_command(
        plugin_name="sample_plugin",
        command="hello",
        handler=cmd_hello,
        description="Say hello to the user"
    )


# Plugin hook handlers
async def on_bot_start():
    logger.info("Bot started hook triggered")


async def on_bot_stop():
    logger.info("Bot stopped hook triggered")


# Command handlers
async def cmd_hello(client: Client, message: Message):
    """Handler for /hello command"""
    user = message.from_user
    await message.reply_text(f"Hello, {user.first_name}! This is a sample plugin command.")


@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handler for /start command"""
    user = message.from_user
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create inline keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("🌐 GitHub", url="https://github.com/ItalyMusic/pyroitaly")
        ]
    ])
    
    await message.reply_text(
        f"Hello {user.mention}!\n\n"
        f"Welcome to the PyroItaly example bot. This bot demonstrates "
        f"the capabilities of the PyroItaly library.\n\n"
        f"Use /help to see available commands.\n"
        f"Started at: {start_time}",
        reply_markup=keyboard
    )


@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Handler for /help command"""
    help_text = (
        "**Available Commands:**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check bot response time\n"
        "/status - Show bot status\n"
        "/debug - Show debug information\n"
        "/hello - Sample plugin command\n"
        "/echo [text] - Echo back your text\n"
    )
    
    await message.reply_text(help_text)


@app.on_message(filters.command("echo"))
async def echo_command(client: Client, message: Message):
    """Handler for /echo command"""
    # Get the text after the command
    command_parts = message.text.split(" ", 1)
    
    if len(command_parts) > 1:
        text = command_parts[1]
        await message.reply_text(f"Echo: {text}")
    else:
        await message.reply_text("Please provide some text to echo.")


@app.on_callback_query()
async def handle_callback_queries(client, callback_query):
    """Handler for callback queries from inline keyboards"""
    data = callback_query.data
    
    if data == "help":
        help_text = (
            "**Available Commands:**\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/ping - Check bot response time\n"
            "/status - Show bot status\n"
            "/debug - Show debug information\n"
            "/hello - Sample plugin command\n"
            "/echo [text] - Echo back your text\n"
        )
        await callback_query.message.edit_text(help_text)
    
    elif data == "about":
        about_text = (
            "**PyroItaly Example Bot**\n\n"
            "This is an example bot showcasing the PyroItaly library features.\n\n"
            "PyroItaly is a faster, lighter, and cleaner alternative to Pyrogram / Pyroitaly, "
            "while maintaining the same features and functionality.\n\n"
            "GitHub: https://github.com/ItalyMusic/pyroitaly"
        )
        await callback_query.message.edit_text(about_text)
    
    # Answer the callback query to remove the loading indicator
    await callback_query.answer()


# Register the built-in utility commands
app.add_handler(cmd_ping, filters.command("ping"))
app.add_handler(cmd_status, filters.command("status"))
app.add_handler(cmd_debug, filters.command("debug"))


async def main():
    """Main function to start the bot"""
    # Register plugins
    register_sample_plugin()
    
    # Start the client
    await app.start()
    
    # Start auto reconnection
    await auto_reconnect.start()
    
    # Trigger the bot_start hook
    await plugin_system.trigger_hook("bot_start")
    
    # Set bot commands
    await app.set_bot_commands([
        {"command": "start", "description": "Start the bot"},
        {"command": "help", "description": "Show help message"},
        {"command": "ping", "description": "Check bot response time"},
        {"command": "status", "description": "Show bot status"},
        {"command": "debug", "description": "Show debug information"},
        {"command": "hello", "description": "Sample plugin command"},
        {"command": "echo", "description": "Echo back your text"}
    ])
    
    logger.info("Bot started successfully!")
    
    # Keep the bot running
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        # Trigger the bot_stop hook
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(plugin_system.trigger_hook("bot_stop"))
            else:
                asyncio.run(plugin_system.trigger_hook("bot_stop"))
        except Exception as e:
            logger.error(f"Error triggering bot_stop hook: {e}")
