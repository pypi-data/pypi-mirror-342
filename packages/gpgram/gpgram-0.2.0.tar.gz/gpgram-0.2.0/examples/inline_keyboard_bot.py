"""
Example bot with inline keyboards using Gpgram.
"""

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
        reply_markup=keyboard.build()
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
            .build()
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
        reply_markup=keyboard.build()
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
