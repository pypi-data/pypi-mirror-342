# Old syntax
import asyncio
import os
from gpgram import Bot, Dispatcher, Router, CommandFilter

# Create a router for message handlers
router = Router()

@router.message(CommandFilter('start'))
async def start_command(message, bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello!"
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