import asyncio
import os
import gpgram
from loguru import logger

# Configure Loguru
logger.remove()  # Remove default handler
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Create a router
router = gpgram.Router()

# Register handlers
@router.message(gpgram.CommandFilter('start'))
async def start_command(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm a bot created with Gpgram."
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
    try:
        # Get the bot token from environment variable
        token = "7651778724:AAGytxXl9wfDL5wsbQsktCygoXti7l_I434"

        if not token:
            logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
            return

        # Create a bot instance
        bot = gpgram.Bot(token=token)

        # Create a dispatcher
        dp = gpgram.Dispatcher(bot=bot)

        # Register the router with the dispatcher
        dp.register_router(router)

        try:
            # Print bot information
            me = await bot.get_me()
            logging.info(f"Starting bot @{me.get('username')}")
        except Exception as e:
            logging.error(f"Error getting bot info: {e}")
            logging.error("Please check your bot token and internet connection.")
            return

        # Start polling
        await dp.run_polling()
    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    asyncio.run(main())