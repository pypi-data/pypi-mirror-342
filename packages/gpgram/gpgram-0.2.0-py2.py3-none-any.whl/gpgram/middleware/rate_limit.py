"""
Rate limiting middleware for Gpgram.

This module provides middleware for rate limiting in Telegram bots.
"""

import time
import asyncio
from typing import Dict, Any, Optional, Tuple, List, Set, Union
from dataclasses import dataclass, field

from .base import BaseMiddleware
from ..logging import get_logger

logger = get_logger(__name__)


@dataclass
class RateLimitInfo:
    """
    Information about rate limiting for a user or chat.
    
    Attributes:
        count: Number of requests in the current window
        window_start: Start time of the current window
        last_reset: Last time the count was reset
        blocked_until: Time until which the user/chat is blocked
    """
    count: int = 0
    window_start: float = field(default_factory=time.time)
    last_reset: float = field(default_factory=time.time)
    blocked_until: float = 0


class RateLimitMiddleware(BaseMiddleware):
    """
    Middleware for rate limiting in Telegram bots.
    
    This middleware limits the number of requests a user or chat can make in a given time window.
    """
    
    def __init__(
        self,
        limit: int = 30,
        window: int = 60,
        key_func=None,
        block_duration: int = 300,
        exempt_user_ids: Optional[Set[int]] = None,
        exempt_chat_ids: Optional[Set[int]] = None,
        message_template: str = "Rate limit exceeded. Please try again in {time} seconds.",
    ):
        """
        Initialize the RateLimitMiddleware.
        
        Args:
            limit: Maximum number of requests allowed in the window
            window: Time window in seconds
            key_func: Function to extract a key from an update (defaults to user_id:chat_id)
            block_duration: Duration to block a user/chat after exceeding the limit (in seconds)
            exempt_user_ids: Set of user IDs exempt from rate limiting
            exempt_chat_ids: Set of chat IDs exempt from rate limiting
            message_template: Template for the rate limit exceeded message
        """
        self.limit = limit
        self.window = window
        self.key_func = key_func or self._default_key_func
        self.block_duration = block_duration
        self.exempt_user_ids = exempt_user_ids or set()
        self.exempt_chat_ids = exempt_chat_ids or set()
        self.message_template = message_template
        self.rate_limits: Dict[str, RateLimitInfo] = {}
    
    def _default_key_func(self, update, data: Dict[str, Any]) -> str:
        """
        Default function to extract a key from an update.
        
        Args:
            update: Update object
            data: Data dictionary
        
        Returns:
            Key for rate limiting
        """
        user_id = None
        chat_id = None
        
        if hasattr(update, 'message') and update.message:
            chat_id = update.message.chat.id
            if update.message.from_user:
                user_id = update.message.from_user.id
        
        elif hasattr(update, 'callback_query') and update.callback_query:
            if update.callback_query.from_user:
                user_id = update.callback_query.from_user.id
            
            if hasattr(update.callback_query, 'message') and update.callback_query.message:
                chat_id = update.callback_query.message.chat.id
        
        if user_id and chat_id:
            return f"{user_id}:{chat_id}"
        elif user_id:
            return f"{user_id}"
        elif chat_id:
            return f"chat:{chat_id}"
        
        return "unknown"
    
    def _is_exempt(self, update) -> bool:
        """
        Check if an update is exempt from rate limiting.
        
        Args:
            update: Update object
        
        Returns:
            True if the update is exempt, False otherwise
        """
        user_id = None
        chat_id = None
        
        if hasattr(update, 'message') and update.message:
            chat_id = update.message.chat.id
            if update.message.from_user:
                user_id = update.message.from_user.id
        
        elif hasattr(update, 'callback_query') and update.callback_query:
            if update.callback_query.from_user:
                user_id = update.callback_query.from_user.id
            
            if hasattr(update.callback_query, 'message') and update.callback_query.message:
                chat_id = update.callback_query.message.chat.id
        
        return (user_id in self.exempt_user_ids) or (chat_id in self.exempt_chat_ids)
    
    async def _send_rate_limit_message(self, update, data: Dict[str, Any], blocked_until: float) -> None:
        """
        Send a rate limit exceeded message.
        
        Args:
            update: Update object
            data: Data dictionary
            blocked_until: Time until which the user/chat is blocked
        """
        bot = data.get('bot')
        if not bot:
            return
        
        wait_time = int(blocked_until - time.time())
        if wait_time <= 0:
            return
        
        message = self.message_template.format(time=wait_time)
        
        try:
            if hasattr(update, 'message') and update.message:
                await bot.send_message(chat_id=update.message.chat.id, text=message)
            
            elif hasattr(update, 'callback_query') and update.callback_query:
                if hasattr(update.callback_query, 'message') and update.callback_query.message:
                    await bot.send_message(chat_id=update.callback_query.message.chat.id, text=message)
                else:
                    await bot.answer_callback_query(
                        callback_query_id=update.callback_query.id,
                        text=message,
                        show_alert=True
                    )
        except Exception as e:
            logger.exception(f"Error sending rate limit message: {e}")
    
    async def on_pre_process_update(self, update, data: Dict[str, Any]) -> None:
        """
        Process an update before it's handled.
        
        Args:
            update: Update object
            data: Data dictionary
        """
        # Skip rate limiting for exempt users/chats
        if self._is_exempt(update):
            return
        
        key = self.key_func(update, data)
        now = time.time()
        
        # Get or create rate limit info
        if key not in self.rate_limits:
            self.rate_limits[key] = RateLimitInfo(count=0, window_start=now, last_reset=now)
        
        rate_limit = self.rate_limits[key]
        
        # Check if the user/chat is blocked
        if rate_limit.blocked_until > now:
            # Send rate limit message and raise exception to stop processing
            await self._send_rate_limit_message(update, data, rate_limit.blocked_until)
            raise RateLimitExceeded(f"Rate limit exceeded for {key}")
        
        # Reset count if window has passed
        if now - rate_limit.window_start > self.window:
            rate_limit.count = 0
            rate_limit.window_start = now
            rate_limit.last_reset = now
        
        # Increment count
        rate_limit.count += 1
        
        # Check if limit is exceeded
        if rate_limit.count > self.limit:
            # Block the user/chat
            rate_limit.blocked_until = now + self.block_duration
            
            # Send rate limit message and raise exception to stop processing
            await self._send_rate_limit_message(update, data, rate_limit.blocked_until)
            raise RateLimitExceeded(f"Rate limit exceeded for {key}")
    
    async def on_post_process_update(self, update, data: Dict[str, Any], handler_result) -> None:
        """
        Process an update after it's handled.
        
        Args:
            update: Update object
            data: Data dictionary
            handler_result: Result of the handler
        """
        # No post-processing needed
        pass


class RateLimitExceeded(Exception):
    """Exception raised when a rate limit is exceeded."""
    pass
