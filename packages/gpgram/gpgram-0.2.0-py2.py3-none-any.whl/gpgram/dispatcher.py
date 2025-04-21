"""
Dispatcher class for handling updates from Telegram.
"""

import asyncio
import signal
import sys
from typing import List, Optional, Dict, Any, Callable, Awaitable, Set, Union, Coroutine

from .bot import Bot
from .router import Router
from .types.update import Update
from .middleware import MiddlewareManager, BaseMiddleware
from .logging import get_logger

class Dispatcher:
    """
    Dispatcher class for handling updates from Telegram.

    This class is responsible for receiving updates from Telegram and
    dispatching them to the appropriate handlers.
    """

    def __init__(
        self,
        bot: Optional[Bot] = None,
        update_queue: Optional[asyncio.Queue] = None,
    ):
        """
        Initialize the Dispatcher.

        Args:
            bot: Bot instance
            update_queue: Queue for updates
        """
        self.bot = bot
        self.update_queue = update_queue or asyncio.Queue()
        self.logger = get_logger(__name__)
        self.router = Router()
        self._running = False
        self._polling_task = None
        self._processing_task = None
        self._error_handlers: List[Callable[[Exception, Update], Awaitable[None]]] = []
        self.middleware = MiddlewareManager()
        self._shutdown_signals = (signal.SIGINT, signal.SIGTERM, signal.SIGABRT)

    def register_router(self, router: Router) -> None:
        """
        Register a router with the dispatcher.

        Args:
            router: Router to register
        """
        self.router.include_router(router)

    def register_middleware(self, middleware: BaseMiddleware) -> None:
        """
        Register a middleware with the dispatcher.

        Args:
            middleware: Middleware to register
        """
        self.middleware.register(middleware)

    def register_error_handler(
        self,
        callback: Callable[[Exception, Update], Awaitable[None]]
    ) -> None:
        """
        Register an error handler.

        Args:
            callback: Callback function to handle errors
        """
        self._error_handlers.append(callback)

    async def process_update(self, update: Update) -> None:
        """
        Process a single update.

        Args:
            update: Update to process
        """
        # Create data dictionary for middleware
        data = {'bot': self.bot}

        try:
            # Trigger pre-process middleware
            await self.middleware.trigger_pre_process_update(update, data)

            # Dispatch update to router
            result = await self.router.dispatch(update, self.bot)

            # Trigger post-process middleware
            await self.middleware.trigger_post_process_update(update, data, result)

        except Exception as e:
            self.logger.exception(f"Error processing update {update.update_id}: {e}")
            for handler in self._error_handlers:
                try:
                    await handler(e, update)
                except Exception as handler_error:
                    self.logger.exception(
                        f"Error in error handler while processing update {update.update_id}: {handler_error}"
                    )

    async def start_polling(
        self,
        bot: Optional[Bot] = None,
        poll_interval: float = 0.5,
        timeout: int = 30,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: bool = False,
        close_bot_session: bool = True,
    ) -> None:
        """
        Start polling updates from Telegram.

        Args:
            bot: Bot instance to use for polling
            poll_interval: Interval between polling requests in seconds
            timeout: Timeout for long polling in seconds
            allowed_updates: List of update types to receive
            drop_pending_updates: Whether to drop pending updates
            close_bot_session: Whether to close the bot session when stopping
        """
        if self._running:
            self.logger.warning("Polling is already running")
            return

        self._running = True
        self.bot = bot or self.bot

        if not self.bot:
            raise ValueError("Bot instance is required for polling")

        # Drop pending updates if requested
        if drop_pending_updates:
            await self.bot._make_request(
                "getUpdates",
                {
                    'offset': -1,
                    'limit': 1,
                    'timeout': 0,
                }
            )

        # Start polling task
        self._polling_task = asyncio.create_task(
            self._polling(poll_interval, timeout, allowed_updates)
        )

        # Start processing task
        self._processing_task = asyncio.create_task(
            self._process_updates()
        )

    async def stop_polling(self, close_bot_session: bool = True) -> None:
        """
        Stop polling updates.

        Args:
            close_bot_session: Whether to close the bot session
        """
        if not self._running:
            self.logger.warning("Polling is not running")
            return

        self._running = False

        # Cancel polling task
        if self._polling_task:
            self._polling_task.cancel()
            try:
                await self._polling_task
            except asyncio.CancelledError:
                pass
            self._polling_task = None

        # Cancel processing task
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
            self._processing_task = None

        # Close bot session if requested
        if close_bot_session and self.bot:
            await self.bot.close()

    async def _polling(
        self,
        poll_interval: float,
        timeout: int,
        allowed_updates: Optional[List[str]],
    ) -> None:
        """
        Poll for updates from Telegram.

        Args:
            poll_interval: Interval between polling requests in seconds
            timeout: Timeout for long polling in seconds
            allowed_updates: List of update types to receive
        """
        offset = None

        while self._running:
            try:
                updates = await self.bot.get_updates(
                    offset=offset,
                    timeout=timeout,
                    allowed_updates=allowed_updates,
                )

                if updates:
                    offset = updates[-1].update_id + 1
                    for update in updates:
                        await self.update_queue.put(update)

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.exception(f"Error while polling for updates: {e}")
                await asyncio.sleep(poll_interval)

    async def _process_updates(self) -> None:
        """Process updates from the update queue."""
        while self._running:
            try:
                update = await self.update_queue.get()
                await self.process_update(update)
                self.update_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.exception(f"Error while processing updates: {e}")

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        if sys.platform == 'win32':
            # Windows doesn't support SIGTERM or SIGABRT
            signals = (signal.SIGINT,)
        else:
            signals = self._shutdown_signals

        for sig in signals:
            try:
                signal.signal(sig, self._handle_signal)
            except (ValueError, OSError) as e:
                self.logger.warning(f"Failed to set signal handler for {sig}: {e}")

    def _handle_signal(self, signum, frame) -> None:
        """
        Handle shutdown signals.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop_polling())

    async def run_polling(
        self,
        bot: Optional[Bot] = None,
        poll_interval: float = 0.5,
        timeout: int = 30,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: bool = False,
        close_bot_session: bool = True,
        handle_signals: bool = True,
    ) -> None:
        """
        Start polling and block until stopped.

        Args:
            bot: Bot instance to use for polling
            poll_interval: Interval between polling requests in seconds
            timeout: Timeout for long polling in seconds
            allowed_updates: List of update types to receive
            drop_pending_updates: Whether to drop pending updates
            close_bot_session: Whether to close the bot session when stopping
            handle_signals: Whether to handle shutdown signals
        """
        try:
            # Set up signal handlers if requested
            if handle_signals:
                self._setup_signal_handlers()

            # Start polling
            await self.start_polling(
                bot=bot,
                poll_interval=poll_interval,
                timeout=timeout,
                allowed_updates=allowed_updates,
                drop_pending_updates=drop_pending_updates,
            )

            # Keep the event loop running
            while self._running:
                await asyncio.sleep(1)

        finally:
            # Stop polling
            await self.stop_polling(close_bot_session=close_bot_session)

    async def process_webhook_update(self, update_dict: Dict[str, Any]) -> None:
        """
        Process an update received via webhook.

        Args:
            update_dict: Update dictionary from webhook
        """
        update = Update.from_dict(update_dict)
        await self.process_update(update)
