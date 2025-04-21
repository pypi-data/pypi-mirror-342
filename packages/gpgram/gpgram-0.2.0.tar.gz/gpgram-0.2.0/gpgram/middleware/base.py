"""
Base middleware classes for Telegram Bot API.
"""

from typing import Any, Callable, Dict, List, Optional, Union, TYPE_CHECKING

from ..logging import get_logger

if TYPE_CHECKING:
    from ..types.update import Update
    from ..types.message import Message
    from ..types.callback_query import CallbackQuery

class BaseMiddleware:
    """
    Base class for all middlewares.

    This class provides the basic functionality for middlewares.
    """

    def __init__(self):
        """Initialize the middleware."""
        self.logger = get_logger(__name__)

    async def on_pre_process_update(self, update: 'Update', data: Dict[str, Any]) -> None:
        """
        Process update before it is handled by handlers.

        Args:
            update: Update to process
            data: Data to pass to handlers
        """
        pass

    async def on_post_process_update(self, update: 'Update', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Process update after it is handled by handlers.

        Args:
            update: Update to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        pass

    async def on_pre_process_message(self, message: 'Message', data: Dict[str, Any]) -> None:
        """
        Process message before it is handled by handlers.

        Args:
            message: Message to process
            data: Data to pass to handlers
        """
        pass

    async def on_post_process_message(self, message: 'Message', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Process message after it is handled by handlers.

        Args:
            message: Message to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        pass

    async def on_pre_process_callback_query(self, callback_query: 'CallbackQuery', data: Dict[str, Any]) -> None:
        """
        Process callback query before it is handled by handlers.

        Args:
            callback_query: Callback query to process
            data: Data to pass to handlers
        """
        pass

    async def on_post_process_callback_query(self, callback_query: 'CallbackQuery', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Process callback query after it is handled by handlers.

        Args:
            callback_query: Callback query to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        pass

    # Add more methods for other update types as needed


class MiddlewareManager:
    """
    Manager for middlewares.

    This class manages the middlewares and their execution.
    """

    def __init__(self):
        """Initialize the middleware manager."""
        self.middlewares: List[BaseMiddleware] = []
        self.logger = get_logger(__name__)

    def register(self, middleware: BaseMiddleware) -> None:
        """
        Register a middleware.

        Args:
            middleware: Middleware to register
        """
        self.middlewares.append(middleware)

    async def trigger_pre_process_update(self, update: 'Update', data: Dict[str, Any]) -> None:
        """
        Trigger pre-process update for all middlewares.

        Args:
            update: Update to process
            data: Data to pass to handlers
        """
        for middleware in self.middlewares:
            try:
                await middleware.on_pre_process_update(update, data)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    async def trigger_post_process_update(self, update: 'Update', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Trigger post-process update for all middlewares.

        Args:
            update: Update to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        for middleware in reversed(self.middlewares):
            try:
                await middleware.on_post_process_update(update, data, handler_result)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    async def trigger_pre_process_message(self, message: 'Message', data: Dict[str, Any]) -> None:
        """
        Trigger pre-process message for all middlewares.

        Args:
            message: Message to process
            data: Data to pass to handlers
        """
        for middleware in self.middlewares:
            try:
                await middleware.on_pre_process_message(message, data)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    async def trigger_post_process_message(self, message: 'Message', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Trigger post-process message for all middlewares.

        Args:
            message: Message to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        for middleware in reversed(self.middlewares):
            try:
                await middleware.on_post_process_message(message, data, handler_result)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    async def trigger_pre_process_callback_query(self, callback_query: 'CallbackQuery', data: Dict[str, Any]) -> None:
        """
        Trigger pre-process callback query for all middlewares.

        Args:
            callback_query: Callback query to process
            data: Data to pass to handlers
        """
        for middleware in self.middlewares:
            try:
                await middleware.on_pre_process_callback_query(callback_query, data)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    async def trigger_post_process_callback_query(self, callback_query: 'CallbackQuery', data: Dict[str, Any], handler_result: Any) -> None:
        """
        Trigger post-process callback query for all middlewares.

        Args:
            callback_query: Callback query to process
            data: Data passed to handlers
            handler_result: Result of the handler
        """
        for middleware in reversed(self.middlewares):
            try:
                await middleware.on_post_process_callback_query(callback_query, data, handler_result)
            except Exception as e:
                self.logger.exception(f"Error in middleware {middleware.__class__.__name__}: {e}")

    # Add more methods for other update types as needed
