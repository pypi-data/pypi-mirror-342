"""
Example bot using the simplified syntax of Gpgram.

This example demonstrates how to use the simplified syntax of Gpgram.
"""

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
