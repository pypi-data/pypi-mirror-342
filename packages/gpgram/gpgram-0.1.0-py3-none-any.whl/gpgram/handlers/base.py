"""
Base handler class for Telegram Bot API.
"""

from typing import Callable, List, Optional, Union, Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot
    from ..types.update import Update

class BaseHandler:
    """
    Base class for all handlers.

    This class provides the basic functionality for handlers.
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
        self.callback = callback
        self.filters = filters if isinstance(filters, list) else [filters] if filters else []
        self.args = args
        self.kwargs = kwargs

    def check_update(self, update: 'Update') -> bool:
        """
        Check if the update should be handled by this handler.

        Args:
            update: Update to check

        Returns:
            True if the update should be handled, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")

    async def handle_update(self, update: 'Update', bot: 'Bot') -> Any:
        """
        Handle the update.

        Args:
            update: Update to handle
            bot: Bot instance

        Returns:
            Result of the handler callback
        """
        return await self.callback(update, bot, *self.args, **self.kwargs)
