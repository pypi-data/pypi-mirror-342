# Gpgram

A modern, asynchronous Telegram Bot API library with advanced handler capabilities, inspired by python-telegram-bot and aiogram.

## Features

- 🚀 **Fully asynchronous** using Python's `asyncio`
- 🧩 **Clean, intuitive API design** for easy bot development
- 🔄 **Advanced routing system** for handling updates
- 🔍 **Flexible filter system** for message handling
- 🔌 **Middleware support** for pre and post-processing updates
- 🛠️ **Utility functions** for common tasks
- 📝 **Type hints** for better IDE support
- 🧪 **Pydantic integration** for data validation
- 🔒 **Error handling** with custom exceptions
- 🌟 **Simplified syntax** for common tasks

## Installation

```bash
pip install gpgram
```

## Quick Start

Here's a simple echo bot example:

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
        text=f"Hello, {message.from_user.full_name}! I'm a simple bot."
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
    # Create a bot instance
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    # Create a dispatcher
    dp = Dispatcher(bot=bot)

    # Register the router
    dp.register_router(router)

    # Start polling
    await dp.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
```

## Advanced Usage

### Using Filters

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

### Using Inline Keyboards

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
        reply_markup=keyboard.build()
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

### Using Middleware

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

### Error Handling

```python
# Error handler
async def error_handler(exception, update):
    """Handle errors."""
    print(f"Error processing update {update.update_id}: {exception}")

# Register the error handler
dp.register_error_handler(error_handler)
```

## Simplified Syntax

Gpgram also provides a simplified syntax for common tasks:

```python
import os
import asyncio
from gpgram import SimpleBot, Handler, Button, InlineButton

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
    @handler.message(contains="hello")
    async def hello_handler(message, bot):
        await message.reply(
            bot=bot,
            text=f"Hello, {message.from_user_first_name}!"
        )

    # Create inline buttons
    button1 = InlineButton(text="Option 1", callback_data="option1")
    button2 = InlineButton(text="Option 2", callback_data="option2")

    # Create a keyboard with the buttons
    keyboard = Button.row(button1, button2)

    # Start polling
    await handler.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

Check out the examples directory for more detailed examples:

- `simple_bot.py` - A simple bot with basic commands
- `advanced_bot.py` - An advanced bot with inline keyboards, middleware, and error handling
- `echo_bot.py` - A basic echo bot
- `inline_keyboard_bot.py` - A bot demonstrating inline keyboards
- `simple_syntax_bot.py` - A bot using the simplified syntax

## Documentation

For more detailed documentation, see the docstrings in the code or visit our [documentation website](https://gpgram.readthedocs.io/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
