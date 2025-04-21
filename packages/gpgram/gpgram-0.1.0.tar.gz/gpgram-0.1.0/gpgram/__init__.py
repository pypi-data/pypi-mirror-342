"""
Gpgram - A modern, asynchronous Telegram Bot API library with advanced handler capabilities.

This library provides a clean, async-first interface to the Telegram Bot API
with advanced routing and handler capabilities.
"""

__version__ = "0.1.0"

from .bot import Bot
from .dispatcher import Dispatcher
from .router import Router
from .types import Update, Message, User, Chat, CallbackQuery
from .filters import (
    CommandFilter, TextFilter, RegexFilter,
    ContentTypeFilter, ChatTypeFilter
)
from .utils import InlineKeyboardBuilder, ReplyKeyboardBuilder, escape_markdown, escape_html

__all__ = [
    # Core components
    "Bot", "Dispatcher", "Router",

    # Types
    "Update", "Message", "User", "Chat", "CallbackQuery",

    # Filters
    "CommandFilter", "TextFilter", "RegexFilter",
    "ContentTypeFilter", "ChatTypeFilter",

    # Utils
    "InlineKeyboardBuilder", "ReplyKeyboardBuilder",
    "escape_markdown", "escape_html",
]
