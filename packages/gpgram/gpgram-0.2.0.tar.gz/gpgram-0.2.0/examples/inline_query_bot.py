"""
Inline query example for Gpgram.

This example demonstrates how to handle inline queries with Gpgram.
"""

import os
import asyncio
import json
from loguru import logger

from gpgram import (
    Bot, Dispatcher, Router, CommandFilter,
    answer_inline_query, create_inline_query_result_article, create_input_text_message_content
)

# Configure logging
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Create a router for message handlers
router = Router()

# Sample data for inline queries
ARTICLES = [
    {
        "id": "1",
        "title": "Gpgram",
        "description": "A modern, asynchronous Telegram Bot API library",
        "content": "Gpgram is a modern, asynchronous Telegram Bot API library with advanced handler capabilities."
    },
    {
        "id": "2",
        "title": "Python",
        "description": "A programming language",
        "content": "Python is a high-level, interpreted programming language known for its readability and versatility."
    },
    {
        "id": "3",
        "title": "Telegram",
        "description": "A messaging platform",
        "content": "Telegram is a cloud-based messaging app with a focus on security and speed."
    },
    {
        "id": "4",
        "title": "Inline Queries",
        "description": "A Telegram Bot API feature",
        "content": "Inline queries allow users to interact with your bot directly from any chat by typing @your_bot_username followed by a query."
    },
    {
        "id": "5",
        "title": "Async/Await",
        "description": "Python concurrency features",
        "content": "Async/await is a syntax for asynchronous programming in Python, allowing for non-blocking I/O operations."
    }
]

# Register command handlers
@router.message(CommandFilter("start"))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm an inline query bot created with Gpgram.\n\n"
             "Try using me in inline mode by typing @your_bot_username in any chat, "
             "followed by a search term. For example:\n\n"
             "@your_bot_username python"
    )

@router.message(CommandFilter("help"))
async def help_command(message, bot):
    """Handle the /help command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="This bot demonstrates how to handle inline queries with Gpgram.\n\n"
             "Available inline query terms:\n"
             "- gpgram\n"
             "- python\n"
             "- telegram\n"
             "- inline\n"
             "- async\n\n"
             "You can also try searching for these terms."
    )

@router.message()
async def echo_message(message, bot):
    """Echo all messages."""
    if message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}\n\n"
                 f"Try using me in inline mode by typing @your_bot_username in any chat."
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="I can only echo text messages!"
        )

@router.inline_query()
async def inline_query_handler(inline_query, bot):
    """Handle inline queries."""
    query = inline_query.query.lower()
    results = []
    
    # Filter articles based on query
    filtered_articles = ARTICLES
    if query:
        filtered_articles = [
            article for article in ARTICLES
            if query in article["title"].lower() or query in article["description"].lower()
        ]
    
    # Create inline query results
    for article in filtered_articles:
        results.append(
            create_inline_query_result_article(
                id=article["id"],
                title=article["title"],
                input_message_content=create_input_text_message_content(
                    message_text=article["content"]
                ),
                description=article["description"],
                # You can add more properties here, such as:
                # thumb_url="https://example.com/thumb.jpg",
                # reply_markup={"inline_keyboard": [[{"text": "Visit Website", "url": "https://example.com"}]]}
            )
        )
    
    # Answer the inline query
    await answer_inline_query(
        bot=bot,
        inline_query_id=inline_query.id,
        results=results,
        cache_time=300,  # Cache for 5 minutes
        is_personal=True  # Results are personalized for the user
    )

@router.chosen_inline_result()
async def chosen_inline_result_handler(chosen_inline_result, bot):
    """Handle chosen inline results."""
    result_id = chosen_inline_result.result_id
    query = chosen_inline_result.query
    
    # Log the chosen result
    logger.info(f"User chose result {result_id} for query '{query}'")
    
    # You can perform additional actions here, such as updating statistics

async def main():
    """Run the bot."""
    try:
        # Get the bot token from environment variable
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not token:
            logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
            return
        
        # Create a bot instance
        bot = Bot(token=token)
        
        # Create a dispatcher
        dp = Dispatcher(bot=bot)
        
        # Register the router
        dp.register_router(router)
        
        # Print bot information
        me = await bot.get_me()
        logger.info(f"Starting bot @{me.get('username')}")
        
        # Start polling
        await dp.run_polling(
            allowed_updates=["message", "inline_query", "chosen_inline_result"]
        )
        
    except Exception as e:
        logger.exception(f"Error in main function: {e}")
    finally:
        # Close the bot session
        if 'bot' in locals():
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
