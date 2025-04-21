"""
Advanced example bot using Gpgram.
"""

import asyncio
import logging
import os
from typing import Dict, Any

from gpgram import (
    Bot, Dispatcher, Router, 
    CommandFilter, TextFilter, RegexFilter, ChatTypeFilter,
    InlineKeyboardBuilder
)
from gpgram.middleware.base import BaseMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a router for message handlers
router = Router()

# Create a custom middleware
class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging updates."""
    
    async def on_pre_process_update(self, update, data):
        """Log updates before processing."""
        logging.info(f"Received update: {update.update_id}")
    
    async def on_post_process_update(self, update, data, handler_result):
        """Log updates after processing."""
        logging.info(f"Processed update: {update.update_id}")
    
    async def on_pre_process_message(self, message, data):
        """Log messages before processing."""
        if message.from_user:
            logging.info(f"Received message from {message.from_user.full_name} (ID: {message.from_user.id})")

# Command handlers
@router.message(CommandFilter('start'))
async def start_command(message, bot):
    """Handle the /start command."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add("Help", callback_data="help")
    keyboard.add("About", callback_data="about")
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello, {message.from_user.full_name}! I'm an advanced bot created with Gpgram.",
        reply_markup=keyboard.build()
    )

@router.message(CommandFilter('help'))
async def help_command(message, bot):
    """Handle the /help command."""
    help_text = (
        "I'm an advanced bot created with Gpgram. Here are my commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About this bot\n"
        "/keyboard - Show a keyboard\n"
        "/photo - Send a photo\n"
    )
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=help_text
    )

@router.message(CommandFilter('about'))
async def about_command(message, bot):
    """Handle the /about command."""
    about_text = (
        "This is an advanced example bot created with Gpgram.\n\n"
        "Gpgram is a modern, asynchronous Telegram Bot API library with "
        "advanced handler capabilities, inspired by python-telegram-bot and aiogram."
    )
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=about_text
    )

@router.message(CommandFilter('keyboard'))
async def keyboard_command(message, bot):
    """Handle the /keyboard command."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add("Button 1", callback_data="button1")
    keyboard.add("Button 2", callback_data="button2")
    keyboard.row()
    keyboard.add("Button 3", callback_data="button3")
    keyboard.add("Button 4", callback_data="button4")
    keyboard.row()
    keyboard.add("URL Button", url="https://github.com")
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Here's a keyboard:",
        reply_markup=keyboard.build()
    )

@router.message(CommandFilter('photo'))
async def photo_command(message, bot):
    """Handle the /photo command."""
    # Send a photo from URL
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://picsum.photos/500/300",
        caption="Here's a random photo!"
    )

# Text handlers
@router.message(TextFilter("hello", ignore_case=True))
async def hello_message(message, bot):
    """Handle messages containing 'hello'."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello to you too, {message.from_user.full_name}!"
    )

@router.message(RegexFilter(r"^\d+$"))
async def number_message(message, bot):
    """Handle messages containing only numbers."""
    number = int(message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"You sent the number {number}. Here's {number} doubled: {number * 2}"
    )

# Callback query handlers
@router.callback_query()
async def handle_callback_query(callback_query, bot):
    """Handle callback queries from inline keyboards."""
    # Get the callback data
    data = callback_query.data
    
    # Answer the callback query
    await bot.answer_callback_query(
        callback_query_id=callback_query.id,
        text=f"You clicked: {data}"
    )
    
    # Send a response based on the callback data
    if data == "help":
        help_text = (
            "I'm an advanced bot created with Gpgram. Here are my commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/about - About this bot\n"
            "/keyboard - Show a keyboard\n"
            "/photo - Send a photo\n"
        )
        
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=help_text
        )
    
    elif data == "about":
        about_text = (
            "This is an advanced example bot created with Gpgram.\n\n"
            "Gpgram is a modern, asynchronous Telegram Bot API library with "
            "advanced handler capabilities, inspired by python-telegram-bot and aiogram."
        )
        
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=about_text
        )
    
    elif data.startswith("button"):
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"You clicked button: {data}"
        )

# Default message handler
@router.message()
async def default_message(message, bot):
    """Handle all other messages."""
    if message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}\n\nTry /help to see available commands."
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="I received your message, but I can only process text messages."
        )

# Error handler
async def error_handler(exception, update):
    """Handle errors."""
    logging.error(f"Error processing update {update.update_id}: {exception}")

async def main():
    """Run the bot."""
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logging.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    # Create a bot instance
    bot = Bot(token=token, parse_mode="HTML")
    
    # Create a dispatcher
    dp = Dispatcher(bot=bot)
    
    # Register the router
    dp.register_router(router)
    
    # Register the middleware
    dp.register_middleware(LoggingMiddleware())
    
    # Register the error handler
    dp.register_error_handler(error_handler)
    
    # Print bot information
    me = await bot.get_me()
    logging.info(f"Starting bot @{me.get('username')}")
    
    # Start polling
    await dp.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
