"""
Conversation example for Gpgram.

This example demonstrates how to use conversation state management with Gpgram.
"""

import os
import asyncio
from loguru import logger

from gpgram import (
    Bot, Dispatcher, Router, CommandFilter,
    ConversationManager, ConversationHandler, get_conversation_manager
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

# Get the global conversation manager
conversation_manager = get_conversation_manager()

# Define conversation states
INITIAL = 0
NAME = 1
AGE = 2
LOCATION = 3
CONFIRMATION = 4

# Define conversation handlers
async def start_survey(update, bot):
    """Start the survey conversation."""
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Welcome to the survey! I'll ask you a few questions.\n\n"
             "What's your name?"
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
            text=f"Thanks, {data.get('name')}! Where are you from?"
        )
        return LOCATION
    except ValueError:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Please enter a valid age (a number)."
        )
        return AGE

async def process_location(update, bot):
    """Process the user's location."""
    location = update.message.text
    
    # Get the conversation data
    data = conversation_manager.get_data(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    
    # Update the data
    conversation_manager.update_data(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id,
        location=location
    )
    
    # Show the summary and ask for confirmation
    await bot.send_message(
        chat_id=update.message.chat.id,
        text=f"Here's a summary of your information:\n\n"
             f"Name: {data.get('name')}\n"
             f"Age: {data.get('age')}\n"
             f"Location: {location}\n\n"
             f"Is this information correct? (yes/no)"
    )
    return CONFIRMATION

async def process_confirmation(update, bot):
    """Process the user's confirmation."""
    confirmation = update.message.text.lower()
    
    # Get the conversation data
    data = conversation_manager.get_data(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    
    if confirmation in ["yes", "y", "correct", "true"]:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"Thank you, {data.get('name')}! Your survey has been submitted.\n\n"
                 f"You can start a new survey with /survey."
        )
        
        # End the conversation
        conversation_manager.clear_state(
            chat_id=update.message.chat.id,
            user_id=update.message.from_user.id
        )
        return None
    elif confirmation in ["no", "n", "incorrect", "false"]:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Let's start over. What's your name?"
        )
        
        # Reset the conversation data
        conversation_manager.set_state(
            chat_id=update.message.chat.id,
            state=NAME,
            user_id=update.message.from_user.id,
            data={}
        )
        return NAME
    else:
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="Please answer with 'yes' or 'no'."
        )
        return CONFIRMATION

async def cancel_survey(update, bot):
    """Cancel the survey."""
    conversation_manager.clear_state(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id
    )
    
    await bot.send_message(
        chat_id=update.message.chat.id,
        text="Survey cancelled. You can start a new survey with /survey."
    )
    return None

# Create a conversation handler
survey_handler = ConversationHandler(
    entry_points={
        "survey": start_survey
    },
    states={
        NAME: {
            "": process_name  # Default handler for the NAME state
        },
        AGE: {
            "": process_age  # Default handler for the AGE state
        },
        LOCATION: {
            "": process_location  # Default handler for the LOCATION state
        },
        CONFIRMATION: {
            "": process_confirmation  # Default handler for the CONFIRMATION state
        }
    },
    fallbacks={
        "cancel": cancel_survey
    }
)

# Register command handlers
@router.message(CommandFilter("start"))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm a conversation bot created with Gpgram.\n\n"
             "I can help you fill out a survey. Use /survey to start the survey.\n"
             "You can cancel the survey at any time with /cancel."
    )

@router.message(CommandFilter("help"))
async def help_command(message, bot):
    """Handle the /help command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="This bot demonstrates how to use conversation state management with Gpgram.\n\n"
             "Available commands:\n"
             "/start - Start the bot\n"
             "/help - Show this help message\n"
             "/survey - Start the survey\n"
             "/cancel - Cancel the survey\n"
             "/status - Check your current survey status"
    )

@router.message(CommandFilter("survey"))
async def survey_command(message, bot):
    """Handle the /survey command."""
    await survey_handler.handle_update(message, bot)

@router.message(CommandFilter("cancel"))
async def cancel_command(message, bot):
    """Handle the /cancel command."""
    await survey_handler.handle_update(message, bot)

@router.message(CommandFilter("status"))
async def status_command(message, bot):
    """Handle the /status command."""
    # Get the conversation state
    state = conversation_manager.get_state(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    
    # Get the conversation data
    data = conversation_manager.get_data(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    
    if state is None:
        await bot.send_message(
            chat_id=message.chat.id,
            text="You don't have an active survey. Use /survey to start one."
        )
    else:
        # Map state to a human-readable name
        state_names = {
            NAME: "Waiting for name",
            AGE: "Waiting for age",
            LOCATION: "Waiting for location",
            CONFIRMATION: "Waiting for confirmation"
        }
        
        state_name = state_names.get(state, f"Unknown state ({state})")
        
        # Build the status message
        status = f"Your survey is in progress.\n\nCurrent state: {state_name}\n\n"
        
        if data:
            status += "Information collected so far:\n"
            
            if "name" in data:
                status += f"Name: {data['name']}\n"
            
            if "age" in data:
                status += f"Age: {data['age']}\n"
            
            if "location" in data:
                status += f"Location: {data['location']}\n"
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=status
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
        await survey_handler.handle_update(message, bot)
    else:
        # Handle regular messages
        if message.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"You said: {message.text}\n\n"
                     f"Use /survey to start a survey."
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="I can only process text messages."
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
        
        # Start conversation manager cleanup
        conversation_manager.start_cleanup(interval=300)  # Clean up every 5 minutes
        
        # Print bot information
        me = await bot.get_me()
        logger.info(f"Starting bot @{me.get('username')}")
        
        # Start polling
        await dp.run_polling()
        
    except Exception as e:
        logger.exception(f"Error in main function: {e}")
    finally:
        # Close the bot session
        if 'bot' in locals():
            await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
