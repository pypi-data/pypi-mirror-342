"""
Common simplified interfaces for Gpgram.

This module provides simplified interfaces for common Telegram Bot API functionality.
"""

from .button import Button, InlineButton, KeyboardButton
from .message import Message
from .bot import Bot
from .handler import Handler

__all__ = [
    "Button", "InlineButton", "KeyboardButton",
    "Message",
    "Bot",
    "Handler",
]
