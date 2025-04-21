"""
Simple example bot using Gpgram.
"""

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
