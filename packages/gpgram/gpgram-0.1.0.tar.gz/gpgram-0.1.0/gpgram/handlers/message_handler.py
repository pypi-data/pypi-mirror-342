"""
Message handler class for Telegram Bot API.
"""

from typing import Callable, List, Optional, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot

from .base import BaseHandler
from ..types.update import Update

class MessageHandler(BaseHandler):
    """
    Handler class for message updates.

    This class handles message updates from Telegram.
    """

    def __init__(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ):
        """
        Initialize the handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        super().__init__(callback, filters, *args, **kwargs)

    def check_update(self, update: Update) -> bool:
        """
        Check if the update should be handled by this handler.

        Args:
            update: Update to check

        Returns:
            True if the update should be handled, False otherwise
        """
        if not update.message:
            return False

        # Check filters
        for filter_func in self.filters:
            if not filter_func(update.message):
                return False

        return True

    async def handle_update(self, update: Update, bot: 'Bot') -> Any:
        """
        Handle the update.

        Args:
            update: Update to handle
            bot: Bot instance

        Returns:
            Result of the handler callback
        """
        return await self.callback(update.message, bot, *self.args, **self.kwargs)
