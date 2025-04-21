"""
Gpgram - A modern, asynchronous Telegram Bot API library with advanced handler capabilities.

This library provides a clean, async-first interface to the Telegram Bot API
with advanced routing and handler capabilities.
"""

__version__ = "0.1.0"

# Core classes
from .bot import Bot
from .dispatcher import Dispatcher
from .router import Router
from .types import Update, Message, User, Chat, CallbackQuery
from .filters import (
    CommandFilter, TextFilter, RegexFilter,
    ContentTypeFilter, ChatTypeFilter
)
from .utils import InlineKeyboardBuilder, ReplyKeyboardBuilder, escape_markdown, escape_html
from .utils.media import download_file, upload_media_group, create_media_group, download_profile_photos
from .utils.conversation import ConversationManager, ConversationHandler, get_conversation_manager
from .middleware.rate_limit import RateLimitMiddleware
from .webhook import WebhookServer, setup_webhook, remove_webhook, get_webhook_info, run_webhook
from .handlers.inline_query_handler import InlineQueryHandler, answer_inline_query, create_inline_query_result_article, create_input_text_message_content

# Common simplified interfaces
from .common import Button, InlineButton, KeyboardButton
from .common import Message as SimpleMessage
from .common import Bot as SimpleBot
from .common import Handler

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

    # Media utilities
    "download_file", "upload_media_group", "create_media_group", "download_profile_photos",

    # Conversation management
    "ConversationManager", "ConversationHandler", "get_conversation_manager",

    # Middleware
    "RateLimitMiddleware",

    # Webhook support
    "WebhookServer", "setup_webhook", "remove_webhook", "get_webhook_info", "run_webhook",

    # Inline query handling
    "InlineQueryHandler", "answer_inline_query", "create_inline_query_result_article", "create_input_text_message_content",

    # Common simplified interfaces
    "Button", "InlineButton", "KeyboardButton",
    "SimpleMessage", "SimpleBot", "Handler",
]
