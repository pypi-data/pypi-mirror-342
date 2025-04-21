"""
Webhook example for Gpgram.

This example demonstrates how to use webhooks with Gpgram.
"""

import os
import asyncio
import ssl
from loguru import logger

from gpgram import (
    Bot, Dispatcher, Router, CommandFilter,
    WebhookServer, setup_webhook, remove_webhook, get_webhook_info, run_webhook
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

# Register command handlers
@router.message(CommandFilter("start"))
async def start_command(message, bot):
    """Handle the /start command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! I'm a webhook bot created with Gpgram."
    )

@router.message(CommandFilter("help"))
async def help_command(message, bot):
    """Handle the /help command."""
    await bot.send_message(
        chat_id=message.chat.id,
        text="This bot demonstrates how to use webhooks with Gpgram."
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

# Custom route handler for health check
async def health_check(request):
    """Handle health check requests."""
    from aiohttp import web
    return web.Response(text="OK", status=200)

async def main():
    """Run the bot with webhook."""
    try:
        # Get the bot token and webhook URL from environment variables
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        webhook_url = os.getenv("WEBHOOK_URL")  # e.g., https://example.com/webhook
        
        if not token:
            logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
            return
        
        if not webhook_url:
            logger.error("No webhook URL provided. Set the WEBHOOK_URL environment variable.")
            return
        
        # Create a bot instance
        bot = Bot(token=token)
        
        # Create a dispatcher
        dp = Dispatcher(bot=bot)
        
        # Register the router
        dp.register_router(router)
        
        # Get SSL certificate paths (if available)
        ssl_cert_path = os.getenv("SSL_CERT_PATH")
        ssl_key_path = os.getenv("SSL_KEY_PATH")
        
        # Create SSL context if certificate and key are provided
        ssl_context = None
        if ssl_cert_path and ssl_key_path:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(ssl_cert_path, ssl_key_path)
        
        # Custom routes for the webhook server
        custom_routes = [
            {
                "method": "get",
                "path": "/health",
                "handler": health_check
            }
        ]
        
        # Create webhook server
        server = WebhookServer(
            dispatcher=dp,
            host="0.0.0.0",
            port=8443,  # Default port for Telegram webhooks
            webhook_path="/webhook",
            ssl_context=ssl_context,
            secret_token="your_secret_token",  # Replace with a secure token
            custom_routes=custom_routes
        )
        
        # Remove any existing webhook
        await remove_webhook(bot, drop_pending_updates=True)
        
        # Set up webhook
        webhook_set = await setup_webhook(
            bot=bot,
            url=webhook_url,
            certificate=open(ssl_cert_path, "rb").read() if ssl_cert_path else None,
            drop_pending_updates=True,
            secret_token="your_secret_token"  # Same as above
        )
        
        if not webhook_set:
            logger.error("Failed to set up webhook, exiting")
            return
        
        # Get webhook info
        webhook_info = await get_webhook_info(bot)
        logger.info(f"Webhook info: {webhook_info}")
        
        # Start webhook server
        await server.start()
        
        logger.info(f"Webhook server started at 0.0.0.0:8443")
        logger.info(f"Webhook URL: {webhook_url}")
        
        # Keep the event loop running
        while True:
            await asyncio.sleep(1)
            
    except asyncio.CancelledError:
        logger.info("Webhook server cancelled")
    except Exception as e:
        logger.exception(f"Error in main function: {e}")
    finally:
        # Remove webhook and close bot session
        if 'bot' in locals():
            await remove_webhook(bot)
            await bot.close()
        
        # Stop webhook server
        if 'server' in locals():
            await server.stop()

# Alternative simplified approach using run_webhook
async def main_simplified():
    """Run the bot with webhook using the simplified approach."""
    try:
        # Get the bot token and webhook URL from environment variables
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        webhook_url = os.getenv("WEBHOOK_URL")  # e.g., https://example.com/webhook
        
        if not token:
            logger.error("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
            return
        
        if not webhook_url:
            logger.error("No webhook URL provided. Set the WEBHOOK_URL environment variable.")
            return
        
        # Create a bot instance
        bot = Bot(token=token)
        
        # Create a dispatcher
        dp = Dispatcher(bot=bot)
        
        # Register the router
        dp.register_router(router)
        
        # Get SSL certificate paths (if available)
        ssl_cert_path = os.getenv("SSL_CERT_PATH")
        ssl_key_path = os.getenv("SSL_KEY_PATH")
        
        # Custom routes for the webhook server
        custom_routes = [
            {
                "method": "get",
                "path": "/health",
                "handler": health_check
            }
        ]
        
        # Run webhook
        await run_webhook(
            dispatcher=dp,
            webhook_url=webhook_url,
            webhook_path="/webhook",
            host="0.0.0.0",
            port=8443,
            ssl_cert_path=ssl_cert_path,
            ssl_key_path=ssl_key_path,
            secret_token="your_secret_token",  # Replace with a secure token
            drop_pending_updates=True,
            allowed_updates=["message", "edited_message", "callback_query"],
            custom_routes=custom_routes
        )
        
    except Exception as e:
        logger.exception(f"Error in main function: {e}")

if __name__ == "__main__":
    # Choose which approach to use
    use_simplified = os.getenv("USE_SIMPLIFIED", "false").lower() == "true"
    
    if use_simplified:
        asyncio.run(main_simplified())
    else:
        asyncio.run(main())
