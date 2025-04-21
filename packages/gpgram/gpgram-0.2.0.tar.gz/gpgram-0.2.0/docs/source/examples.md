# Examples

This section provides examples of using Gpgram for various tasks.

## Simple Bot

A simple bot with basic commands:

```python
import asyncio
import logging
import os

from gpgram import Bot, Dispatcher, Router, CommandFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a router for message handlers
router = Router()

@router.message(CommandFilter('start'))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello, {message.from_user.full_name}! I'm a simple bot created with Gpgram."
    )

@router.message(CommandFilter('help'))
async def help_command(message, bot):
    """Handle the /help command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="I'm a simple bot created with Gpgram. Try the /start command!"
    )

@router.message()
async def echo_message(message, bot):
    """Echo all messages."""
    if message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}"
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="I can only echo text messages!"
        )

async def main():
    """Run the bot."""
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logging.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return
    
    # Create a bot instance
    bot = Bot(token=token)
    
    # Create a dispatcher
    dp = Dispatcher(bot=bot)
    
    # Register the router
    dp.register_router(router)
    
    # Start polling
    await dp.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```

## Echo Bot

A basic echo bot:

```python
import asyncio
import logging
import os

from gpgram import Bot, Dispatcher, Router, CommandFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a router for message handlers
router = Router()

@router.message(CommandFilter('start'))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello, {message.from_user.full_name}! I'm an echo bot. Send me any message and I'll send it back to you."
    )

@router.message(CommandFilter('help'))
async def help_command(message, bot):
    """Handle the /help command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="I'm an echo bot. Send me any message and I'll send it back to you."
    )

@router.message()
async def echo_message(message, bot):
    """Echo all messages."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=message.text or "I can only echo text messages!"
    )

async def main():
    """Run the bot."""
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logging.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    # Create a bot instance
    bot = Bot(token=token)

    try:
        # Print bot information
        me = await bot.get_me()
        logging.info(f"Starting bot @{me.get('username')}")

        # Create a dispatcher
        dispatcher = Dispatcher(bot=bot)

        # Register the router
        dispatcher.register_router(router)

        # Start polling
        await dispatcher.run_polling(bot=bot)

    finally:
        # Close the bot session
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## Inline Keyboard Bot

A bot demonstrating inline keyboards:

```python
import asyncio
import logging
import os

from gpgram import Bot, Dispatcher, Router, CommandFilter, InlineKeyboardBuilder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a router for message handlers
router = Router()

@router.message(CommandFilter('start'))
async def start_command(message, bot):
    """Handle the /start command."""
    # Create an inline keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.add("Option 1", callback_data="option_1")
    keyboard.add("Option 2", callback_data="option_2")
    keyboard.row()
    keyboard.add("Option 3", callback_data="option_3")
    keyboard.add("Option 4", callback_data="option_4")

    await bot.send_message(
        chat_id=message.chat.id,
        text="Please select an option:",
        reply_markup=keyboard.as_markup()
    )

@router.callback_query()
async def handle_callback_query(callback_query, bot):
    """Handle callback queries from inline keyboards."""
    # Get the callback data
    data = callback_query.data

    # Send a response based on the callback data
    if data == "option_1":
        text = "You selected Option 1"
    elif data == "option_2":
        text = "You selected Option 2"
    elif data == "option_3":
        text = "You selected Option 3"
    elif data == "option_4":
        text = "You selected Option 4"
    else:
        text = f"Unknown option: {data}"

    # Answer the callback query
    await bot.answer_callback_query(
        callback_query_id=callback_query.id,
        text=f"You clicked: {data}"
    )

    # Edit the message text
    await bot.edit_message_text(
        text=text,
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=InlineKeyboardBuilder()
            .add("Back to menu", callback_data="back_to_menu")
            .as_markup()
    )

@router.callback_query(lambda query: query.data == "back_to_menu")
async def back_to_menu(callback_query, bot):
    """Handle the back to menu button."""
    # Create an inline keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.add("Option 1", callback_data="option_1")
    keyboard.add("Option 2", callback_data="option_2")
    keyboard.row()
    keyboard.add("Option 3", callback_data="option_3")
    keyboard.add("Option 4", callback_data="option_4")

    # Answer the callback query
    await bot.answer_callback_query(
        callback_query_id=callback_query.id,
        text="Back to main menu"
    )

    # Edit the message text
    await bot.edit_message_text(
        text="Please select an option:",
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard.as_markup()
    )

async def main():
    """Run the bot."""
    # Get the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        logging.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    # Create a bot instance
    bot = Bot(token=token)

    try:
        # Print bot information
        me = await bot.get_me()
        logging.info(f"Starting bot @{me.get('username')}")

        # Create a dispatcher
        dispatcher = Dispatcher(bot=bot)

        # Register the router
        dispatcher.register_router(router)

        # Start polling
        await dispatcher.run_polling(bot=bot)

    finally:
        # Close the bot session
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## Simplified Syntax Bot

A bot using the simplified syntax:

```python
import os
import asyncio
from loguru import logger

# Import the simplified interfaces
from gpgram import SimpleBot, Handler, Button, InlineButton

# Configure logging
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

async def main():
    try:
        # Get the bot token from environment variable
        token = os.getenv('TELEGRAM_BOT_TOKEN')

        if not token:
            logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
            return

        # Create a bot instance with the simplified interface
        bot = SimpleBot(token=token)
        
        # Create a handler
        handler = Handler(bot=bot)
        
        # Register command handlers
        @handler.command("start")
        async def start_command(message, bot):
            await message.reply(
                bot=bot,
                text="Hello! I'm a bot created with Gpgram's simplified syntax."
            )
        
        @handler.command("help")
        async def help_command(message, bot):
            await message.reply(
                bot=bot,
                text="This is a help message. Try the following commands:\n"
                     "/start - Start the bot\n"
                     "/help - Show this help message\n"
                     "/buttons - Show buttons example"
            )
        
        @handler.command("buttons")
        async def buttons_command(message, bot):
            # Create inline buttons
            button1 = InlineButton(text="Option 1", callback_data="option1")
            button2 = InlineButton(text="Option 2", callback_data="option2")
            button3 = InlineButton(text="Visit Website", url="https://example.com")
            
            # Create a keyboard with the buttons
            keyboard = Button.row(button1, button2)
            keyboard2 = Button.row(button3)
            
            from gpgram.common.button import InlineKeyboard
            inline_keyboard = InlineKeyboard()
            inline_keyboard.add_row(keyboard)
            inline_keyboard.add_row(keyboard2)
            
            await message.reply(
                bot=bot,
                text="Here are some buttons:",
                reply_markup=inline_keyboard
            )
        
        # Register message handlers
        @handler.message(contains="hello")
        async def hello_handler(message, bot):
            await message.reply(
                bot=bot,
                text=f"Hello, {message.from_user_first_name}!"
            )
        
        # Register callback query handlers
        @handler.callback_query(data="option1")
        async def option1_handler(callback_query, bot):
            await bot.answer_callback_query(
                callback_query_id=callback_query["id"],
                text="You selected Option 1"
            )
            
            await bot.send_message(
                chat_id=callback_query["message"]["chat"]["id"],
                text="You selected Option 1"
            )
        
        @handler.callback_query(data="option2")
        async def option2_handler(callback_query, bot):
            await bot.answer_callback_query(
                callback_query_id=callback_query["id"],
                text="You selected Option 2"
            )
            
            await bot.send_message(
                chat_id=callback_query["message"]["chat"]["id"],
                text="You selected Option 2"
            )
        
        # Get bot information
        me = await bot.get_me()
        logger.info(f"Starting bot @{me.get('username')}")
        
        # Start polling
        await handler.start_polling()
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Bot

An advanced bot with inline keyboards, middleware, and error handling:

```python
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
        reply_markup=keyboard.as_markup()
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
```
