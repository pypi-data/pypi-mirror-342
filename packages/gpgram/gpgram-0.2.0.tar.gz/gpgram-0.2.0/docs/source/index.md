# Gpgram Documentation

```{toctree}
:maxdepth: 2
:caption: Contents

getting_started
api_reference
examples
```

## Welcome to Gpgram

Gpgram is a modern, asynchronous Telegram Bot API library with advanced handler capabilities, inspired by python-telegram-bot and aiogram.

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

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
