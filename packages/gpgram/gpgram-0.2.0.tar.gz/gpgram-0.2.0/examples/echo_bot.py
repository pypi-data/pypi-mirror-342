"""
Example echo bot using Gpgram.
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
