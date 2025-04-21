"""
Advanced features example for Gpgram.

This example demonstrates the advanced features of Gpgram, including:
- Media handling
- Conversation state management
- Rate limiting
- Inline query handling
"""

import os
import asyncio
from loguru import logger

import gpgram
from gpgram import (
    Bot, Dispatcher, Router, CommandFilter,
    ConversationManager, ConversationHandler,
    RateLimitMiddleware,
    download_file, upload_media_group, create_media_group,
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

# Create a conversation manager
conversation_manager = ConversationManager()

# Define conversation states
INITIAL = 0
NAME = 1
AGE = 2
PHOTO = 3

# Define conversation handlers
async def start_conversation(update, bot):
    """Start the conversation."""
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Hi! I'm a bot that demonstrates advanced features of Gpgram. Let's start a conversation. What's your name?"
    )
    return NAME

async def process_name(update, bot):
    """Process the user's name."""
    name = update.message.text
    
    # Store the name in conversation data
    conversation_manager.set_state(
        chat_id=update.message.chat.id,
        state=AGE,
        user_id=update.message.from_user.id,
        data={"name": name}
    )
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Nice to meet you, {name}! How old are you?"
    )
    return AGE

async def process_age(update, bot):
    """Process the user's age."""
    try:
        age = int(update.message.text)
        
        # Get the conversation data
        data = conversation_manager.get_data(
            chat_id=update.message.chat.id,
            user_id=update.message.from_user.id
        )
        
        # Update the data
        conversation_manager.update_data(
            chat_id=update.message.chat.id,
            user_id=update.message.from_user.id,
            age=age
        )
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"Thanks, {data.get('name')}! You are {age} years old. Now, please send me a photo."
        )
        return PHOTO
    except ValueError:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Please enter a valid age (a number)."
        )
        return AGE

async def process_photo(update, bot):
    """Process the user's photo."""
    if not update.message.photo:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Please send me a photo."
        )
        return PHOTO
    
    # Get the conversation data
    data = conversation_manager.get_data(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    
    # Get the largest photo
    photo = update.message.photo[-1]
    
    # Download the photo
    photo_path = f"user_{update.message.from_user.id}_photo.jpg"
    await download_file(photo.file_id, bot, photo_path)
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Thanks for the photo, {data.get('name')}! I've saved it as {photo_path}. Here's a summary of our conversation:\n\n"
             f"Name: {data.get('name')}\n"
             f"Age: {data.get('age')}\n"
             f"Photo: Saved as {photo_path}"
    )
    
    # End the conversation
    conversation_manager.clear_state(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    return None

async def cancel_conversation(update, bot):
    """Cancel the conversation."""
    conversation_manager.clear_state(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Conversation cancelled."
    )
    return None

# Create a conversation handler
conversation_handler = ConversationHandler(
    entry_points={
        "conversation": start_conversation
    },
    states={
        NAME: {
            "": process_name  # Default handler for the NAME state
        },
        AGE: {
            "": process_age  # Default handler for the AGE state
        },
        PHOTO: {
            "": process_photo  # Default handler for the PHOTO state
        }
    },
    fallbacks={
        "cancel": cancel_conversation
    }
)

# Register command handlers
@router.message(CommandFilter("start"))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm a bot that demonstrates advanced features of Gpgram. Here are the available commands:\n\n"
             "/conversation - Start a conversation\n"
             "/cancel - Cancel the conversation\n"
             "/media - Show media handling features\n"
             "/inline - Show inline query features"
    )

@router.message(CommandFilter("conversation"))
async def conversation_command(message, bot):
    """Handle the /conversation command."""
    await conversation_handler.handle_update(message, bot)

@router.message(CommandFilter("cancel"))
async def cancel_command(message, bot):
    """Handle the /cancel command."""
    await conversation_handler.handle_update(message, bot)

@router.message(CommandFilter("media"))
async def media_command(message, bot):
    """Handle the /media command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Here are some media handling features:\n\n"
             "1. Send me a photo, and I'll download it and send it back to you.\n"
             "2. Send me multiple photos, and I'll create a media group."
    )

@router.message()
async def message_handler(message, bot):
    """Handle all messages."""
    # Check if there's an active conversation
    state = conversation_manager.get_state(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    
    if state is not None:
        # Handle the message in the context of the conversation
        await conversation_handler.handle_update(message, bot)
        return
    
    # Handle photos
    if message.photo:
        # Download the photo
        photo = message.photo[-1]
        photo_path = f"user_{message.from_user.id}_photo.jpg"
        
        await download_file(photo.file_id, bot, photo_path)
        
        # Send the photo back
        with open(photo_path, "rb") as f:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=f,
                caption=f"I've downloaded your photo and saved it as {photo_path}."
            )
    
    # Handle text messages
    elif message.text:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You said: {message.text}"
        )

@router.inline_query()
async def inline_query_handler(inline_query, bot):
    """Handle inline queries."""
    query = inline_query.query.lower()
    results = []
    
    # Create some inline query results
    if not query:
        # Default results
        results = [
            create_inline_query_result_article(
                id="1",
                title="Example 1",
                input_message_content=create_input_text_message_content(
                    message_text="This is example 1"
                ),
                description="Click to send example 1"
            ),
            create_inline_query_result_article(
                id="2",
                title="Example 2",
                input_message_content=create_input_text_message_content(
                    message_text="This is example 2"
                ),
                description="Click to send example 2"
            )
        ]
    else:
        # Filter results based on query
        if "hello" in query:
            results.append(
                create_inline_query_result_article(
                    id="hello",
                    title="Hello World",
                    input_message_content=create_input_text_message_content(
                        message_text="Hello, World!"
                    ),
                    description="Send a hello world message"
                )
            )
        
        if "gpgram" in query:
            results.append(
                create_inline_query_result_article(
                    id="gpgram",
                    title="About Gpgram",
                    input_message_content=create_input_text_message_content(
                        message_text="Gpgram is a modern, asynchronous Telegram Bot API library with advanced handler capabilities."
                    ),
                    description="Information about Gpgram"
                )
            )
    
    # Answer the inline query
    await answer_inline_query(
        bot=bot,
        inline_query_id=inline_query.id,
        results=results,
        cache_time=300
    )

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
        
        # Register middleware
        dp.register_middleware(RateLimitMiddleware(
            limit=5,  # 5 requests per minute
            window=60,
            block_duration=60,
            exempt_user_ids={123456789},  # Replace with your user ID
            message_template="Rate limit exceeded. Please wait {time} seconds."
        ))
        
        # Start conversation manager cleanup
        conversation_manager.start_cleanup()
        
        # Print bot information
        me = await bot.get_me()
        logger.info(f"Starting bot @{me.get('username')}")
        
        # Start polling
        await dp.run_polling(
            allowed_updates=["message", "edited_message", "callback_query", "inline_query"]
        )
        
    except Exception as e:
        logger.exception(f"Error in main function: {e}")
    finally:
        # Close the bot session
        if 'bot' in locals():
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
