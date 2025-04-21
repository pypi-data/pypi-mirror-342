# Getting Started

This guide will help you get started with Gpgram, a modern, asynchronous Telegram Bot API library.

## Prerequisites

Before you begin, make sure you have:

- Python 3.8 or higher
- A Telegram bot token (get one from [@BotFather](https://t.me/botfather))

## Installation

Install Gpgram using pip:

```bash
pip install gpgram
```

## Creating Your First Bot

Let's create a simple echo bot that responds to the `/start` command and echoes back any text messages it receives.

```python
import asyncio
import logging
import os

from gpgram import Bot, Dispatcher, Router, CommandFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a router for message handlers
router = Router()

@router.message(CommandFilter('start'))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Hello, {message.from_user.full_name}! I'm a simple echo bot."
    )

@router.message()
async def echo_message(message, bot):
    """Echo all messages."""
    if message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}"
        )

async def main():
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

Save this code to a file (e.g., `echo_bot.py`) and run it:

```bash
# Set your Telegram bot token
export TELEGRAM_BOT_TOKEN="your_bot_token_here"  # Linux/macOS
# or
set TELEGRAM_BOT_TOKEN=your_bot_token_here  # Windows Command Prompt
# or
$env:TELEGRAM_BOT_TOKEN = "your_bot_token_here"  # Windows PowerShell

# Run the bot
python echo_bot.py
```

Now you can talk to your bot on Telegram!

## Using the Simplified Syntax

Gpgram also provides a simplified syntax for common tasks:

```python
import asyncio
import os
from gpgram import SimpleBot, Handler

async def main():
    # Create a bot instance with the simplified interface
    bot = SimpleBot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    
    # Create a handler
    handler = Handler(bot=bot)
    
    # Register command handlers
    @handler.command("start")
    async def start_command(message, bot):
        await message.reply(
            bot=bot,
            text="Hello! I'm a bot created with Gpgram's simplified syntax."
        )
    
    # Register message handlers
    @handler.message()
    async def echo_handler(message, bot):
        if message.text:
            await message.reply(
                bot=bot,
                text=f"You said: {message.text}"
            )
    
    # Start polling
    await handler.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

## Adding Inline Keyboards

Let's add an inline keyboard to our bot:

```python
from gpgram import InlineKeyboardBuilder

@router.message(CommandFilter('menu'))
async def menu_command(message, bot):
    # Create an inline keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.add("Option 1", callback_data="option_1")
    keyboard.add("Option 2", callback_data="option_2")
    keyboard.row()
    keyboard.add("Option 3", callback_data="option_3")
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="Please select an option:",
        reply_markup=keyboard.as_markup()
    )

@router.callback_query()
async def handle_callback_query(callback_query, bot):
    # Answer the callback query
    await bot.answer_callback_query(
        callback_query_id=callback_query.id,
        text=f"You clicked: {callback_query.data}"
    )
    
    # Send a response based on the callback data
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=f"You selected: {callback_query.data}"
    )
```

## Using Filters

Gpgram provides various filters to handle specific types of messages:

```python
from gpgram import TextFilter, RegexFilter, ChatTypeFilter

# Text filter
@router.message(TextFilter("hello", ignore_case=True))
async def hello_message(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello to you too!"
    )

# Regex filter
@router.message(RegexFilter(r"^[0-9]+$"))
async def number_message(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="That's a number!"
    )

# Chat type filter
@router.message(ChatTypeFilter("private"))
async def private_message(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="This is a private chat"
    )
```

## Using Middleware

Middleware allows you to process updates before and after they are handled:

```python
from gpgram import BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging updates."""
    
    async def on_pre_process_update(self, update, data):
        """Log updates before processing."""
        print(f"Received update: {update.update_id}")
    
    async def on_post_process_update(self, update, data, handler_result):
        """Log updates after processing."""
        print(f"Processed update: {update.update_id}")

# Register the middleware
dp.register_middleware(LoggingMiddleware())
```

## Error Handling

You can register an error handler to handle exceptions:

```python
# Error handler
async def error_handler(exception, update):
    """Handle errors."""
    print(f"Error processing update {update.update_id}: {exception}")

# Register the error handler
dp.register_error_handler(error_handler)
```

## Next Steps

Now that you've created your first bot, you can explore more advanced features:

- [API Reference](api_reference.md) - Detailed documentation of all classes and methods
- [Examples](examples.md) - More examples of using Gpgram
- [A-Z Reference](api/index.md) - Comprehensive reference of all components
