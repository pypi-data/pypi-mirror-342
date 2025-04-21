"""
Webhook support for Gpgram.

This module provides utilities for setting up and handling webhooks in Telegram bots.
"""

import json
import asyncio
import ssl
from typing import Optional, Dict, Any, List, Union, Callable, Awaitable
from aiohttp import web

from .bot import Bot
from .dispatcher import Dispatcher
from .types.update import Update
from .logging import get_logger

logger = get_logger(__name__)


class WebhookServer:
    """
    Server for handling Telegram webhooks.
    
    This class provides a web server for receiving webhook updates from Telegram.
    """
    
    def __init__(
        self,
        dispatcher: Dispatcher,
        host: str = "0.0.0.0",
        port: int = 8443,
        webhook_path: str = "/webhook",
        ssl_context: Optional[ssl.SSLContext] = None,
        secret_token: Optional[str] = None,
        drop_pending_updates: bool = False,
        allowed_updates: Optional[List[str]] = None,
        custom_routes: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initialize the WebhookServer.
        
        Args:
            dispatcher: Dispatcher instance
            host: Host to bind the server to
            port: Port to bind the server to
            webhook_path: Path for the webhook endpoint
            ssl_context: SSL context for HTTPS
            secret_token: Secret token to validate webhook requests
            drop_pending_updates: Whether to drop pending updates when setting the webhook
            allowed_updates: List of update types to receive
            custom_routes: List of custom routes to add to the server
        """
        self.dispatcher = dispatcher
        self.host = host
        self.port = port
        self.webhook_path = webhook_path
        self.ssl_context = ssl_context
        self.secret_token = secret_token
        self.drop_pending_updates = drop_pending_updates
        self.allowed_updates = allowed_updates
        self.custom_routes = custom_routes or []
        
        self.app = web.Application()
        self.runner = None
        self.site = None
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up routes for the web server."""
        # Add webhook route
        self.app.router.add_post(self.webhook_path, self._handle_webhook)
        
        # Add health check route
        self.app.router.add_get("/health", self._handle_health_check)
        
        # Add custom routes
        for route in self.custom_routes:
            method = route.get("method", "get").lower()
            path = route.get("path", "/")
            handler = route.get("handler")
            
            if handler is None:
                logger.warning(f"No handler provided for route {path}")
                continue
            
            if method == "get":
                self.app.router.add_get(path, handler)
            elif method == "post":
                self.app.router.add_post(path, handler)
            elif method == "put":
                self.app.router.add_put(path, handler)
            elif method == "delete":
                self.app.router.add_delete(path, handler)
            else:
                logger.warning(f"Unsupported method {method} for route {path}")
    
    async def _handle_webhook(self, request: web.Request) -> web.Response:
        """
        Handle webhook requests from Telegram.
        
        Args:
            request: Web request
        
        Returns:
            Web response
        """
        # Verify secret token if provided
        if self.secret_token:
            token_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            if token_header != self.secret_token:
                logger.warning("Invalid secret token in webhook request")
                return web.Response(status=403, text="Forbidden")
        
        try:
            # Parse update
            update_data = await request.json()
            update = Update.from_dict(update_data)
            
            # Process update
            asyncio.create_task(self.dispatcher.process_update(update))
            
            return web.Response(status=200)
        except Exception as e:
            logger.exception(f"Error handling webhook request: {e}")
            return web.Response(status=500, text="Internal Server Error")
    
    async def _handle_health_check(self, request: web.Request) -> web.Response:
        """
        Handle health check requests.
        
        Args:
            request: Web request
        
        Returns:
            Web response
        """
        return web.Response(
            status=200,
            content_type="application/json",
            text=json.dumps({"status": "ok"})
        )
    
    async def start(self) -> None:
        """Start the webhook server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        self.site = web.TCPSite(
            self.runner,
            host=self.host,
            port=self.port,
            ssl_context=self.ssl_context
        )
        
        await self.site.start()
        logger.info(f"Webhook server started at {self.host}:{self.port}")
    
    async def stop(self) -> None:
        """Stop the webhook server."""
        if self.site:
            await self.site.stop()
        
        if self.runner:
            await self.runner.cleanup()
        
        logger.info("Webhook server stopped")


async def setup_webhook(
    bot: Bot,
    url: str,
    certificate: Optional[Union[str, bytes]] = None,
    ip_address: Optional[str] = None,
    max_connections: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
    drop_pending_updates: bool = False,
    secret_token: Optional[str] = None,
) -> bool:
    """
    Set up a webhook for a bot.
    
    Args:
        bot: Bot instance
        url: HTTPS URL to send updates to
        certificate: Public key certificate (self-signed) for webhook
        ip_address: Fixed IP address for webhook
        max_connections: Maximum number of simultaneous HTTPS connections for webhook
        allowed_updates: List of update types to receive
        drop_pending_updates: Whether to drop pending updates
        secret_token: Secret token to validate webhook requests
    
    Returns:
        True if the webhook was set up successfully, False otherwise
    """
    try:
        result = await bot.set_webhook(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
        )
        
        if result:
            logger.info(f"Webhook set up successfully at {url}")
            return True
        
        logger.error("Failed to set up webhook")
        return False
    except Exception as e:
        logger.exception(f"Error setting up webhook: {e}")
        return False


async def remove_webhook(bot: Bot, drop_pending_updates: bool = False) -> bool:
    """
    Remove a webhook for a bot.
    
    Args:
        bot: Bot instance
        drop_pending_updates: Whether to drop pending updates
    
    Returns:
        True if the webhook was removed successfully, False otherwise
    """
    try:
        result = await bot.delete_webhook(drop_pending_updates=drop_pending_updates)
        
        if result:
            logger.info("Webhook removed successfully")
            return True
        
        logger.error("Failed to remove webhook")
        return False
    except Exception as e:
        logger.exception(f"Error removing webhook: {e}")
        return False


async def get_webhook_info(bot: Bot) -> Optional[Dict[str, Any]]:
    """
    Get information about a webhook.
    
    Args:
        bot: Bot instance
    
    Returns:
        Webhook information, or None if an error occurred
    """
    try:
        return await bot.get_webhook_info()
    except Exception as e:
        logger.exception(f"Error getting webhook info: {e}")
        return None


async def run_webhook(
    dispatcher: Dispatcher,
    webhook_url: str,
    webhook_path: str = "/webhook",
    host: str = "0.0.0.0",
    port: int = 8443,
    ssl_cert_path: Optional[str] = None,
    ssl_key_path: Optional[str] = None,
    secret_token: Optional[str] = None,
    drop_pending_updates: bool = False,
    allowed_updates: Optional[List[str]] = None,
    custom_routes: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """
    Run a bot with webhook updates.
    
    Args:
        dispatcher: Dispatcher instance
        webhook_url: HTTPS URL for the webhook
        webhook_path: Path for the webhook endpoint
        host: Host to bind the server to
        port: Port to bind the server to
        ssl_cert_path: Path to SSL certificate
        ssl_key_path: Path to SSL private key
        secret_token: Secret token to validate webhook requests
        drop_pending_updates: Whether to drop pending updates
        allowed_updates: List of update types to receive
        custom_routes: List of custom routes to add to the server
    """
    bot = dispatcher.bot
    
    # Set up SSL context if certificate and key are provided
    ssl_context = None
    if ssl_cert_path and ssl_key_path:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(ssl_cert_path, ssl_key_path)
    
    # Set up webhook
    webhook_set = await setup_webhook(
        bot=bot,
        url=webhook_url,
        certificate=open(ssl_cert_path, 'rb').read() if ssl_cert_path else None,
        allowed_updates=allowed_updates,
        drop_pending_updates=drop_pending_updates,
        secret_token=secret_token,
    )
    
    if not webhook_set:
        logger.error("Failed to set up webhook, exiting")
        return
    
    # Create and start webhook server
    server = WebhookServer(
        dispatcher=dispatcher,
        host=host,
        port=port,
        webhook_path=webhook_path,
        ssl_context=ssl_context,
        secret_token=secret_token,
        allowed_updates=allowed_updates,
        custom_routes=custom_routes,
    )
    
    try:
        await server.start()
        
        # Keep the event loop running
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.info("Webhook server cancelled")
    except Exception as e:
        logger.exception(f"Error in webhook server: {e}")
    finally:
        # Remove webhook and stop server
        await remove_webhook(bot)
        await server.stop()
