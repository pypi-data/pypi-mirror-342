"""
Handler class for Telegram Bot API.

This module provides a simplified interface for handling Telegram bot updates.
"""

from typing import Optional, Callable, Awaitable, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot as TelegramBot
    from .bot import Bot
    from .message import Message


class Handler:
    """
    Simplified interface for handling Telegram bot updates.
    
    This class provides a simplified interface for handling Telegram bot updates.
    """
    
    def __init__(self, bot: 'Bot'):
        """
        Initialize a handler.
        
        Args:
            bot: Bot instance
        """
        from ..dispatcher import Dispatcher
        from ..router import Router
        
        self._bot = bot
        self._dispatcher = Dispatcher(bot=bot.original)
        self._router = Router()
        self._dispatcher.register_router(self._router)
    
    def command(
        self,
        command: str,
        callback: Callable[['Message', 'Bot'], Awaitable[Any]],
    ) -> None:
        """
        Register a command handler.
        
        Args:
            command: Command to handle (without the slash)
            callback: Callback function to handle the command
        """
        from ..filters import CommandFilter
        
        async def wrapper(message, bot):
            from .message import Message
            wrapped_message = Message.from_telegram_message(message)
            await callback(wrapped_message, self._bot)
        
        self._router.message(CommandFilter(command))(wrapper)
    
    def message(
        self,
        callback: Callable[['Message', 'Bot'], Awaitable[Any]],
        text: Optional[str] = None,
        contains: Optional[str] = None,
        starts_with: Optional[str] = None,
        regex: Optional[str] = None,
    ) -> None:
        """
        Register a message handler.
        
        Args:
            callback: Callback function to handle the message
            text: Exact text to match
            contains: Text that the message should contain
            starts_with: Text that the message should start with
            regex: Regular expression to match
        """
        from ..filters import TextFilter, RegexFilter
        
        filter_obj = None
        if text is not None:
            filter_obj = TextFilter(text)
        elif contains is not None:
            filter_obj = TextFilter(contains, mode="contains")
        elif starts_with is not None:
            filter_obj = TextFilter(starts_with, mode="startswith")
        elif regex is not None:
            filter_obj = RegexFilter(regex)
        
        async def wrapper(message, bot):
            from .message import Message
            wrapped_message = Message.from_telegram_message(message)
            await callback(wrapped_message, self._bot)
        
        if filter_obj is not None:
            self._router.message(filter_obj)(wrapper)
        else:
            self._router.message()(wrapper)
    
    def callback_query(
        self,
        callback: Callable[[Dict[str, Any], 'Bot'], Awaitable[Any]],
        data: Optional[str] = None,
    ) -> None:
        """
        Register a callback query handler.
        
        Args:
            callback: Callback function to handle the callback query
            data: Callback data to match
        """
        from ..filters import CallbackDataFilter
        
        filter_obj = None
        if data is not None:
            filter_obj = CallbackDataFilter(data)
        
        async def wrapper(callback_query, bot):
            await callback(callback_query, self._bot)
        
        if filter_obj is not None:
            self._router.callback_query(filter_obj)(wrapper)
        else:
            self._router.callback_query()(wrapper)
    
    async def start_polling(self) -> None:
        """
        Start polling for updates.
        """
        await self._dispatcher.run_polling()
    
    def run(self) -> None:
        """
        Run the bot (blocking).
        """
        import asyncio
        
        async def main():
            await self.start_polling()
        
        asyncio.run(main())
