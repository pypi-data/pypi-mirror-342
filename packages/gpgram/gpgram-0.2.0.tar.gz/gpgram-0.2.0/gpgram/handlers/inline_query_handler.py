"""
Inline query handler for Gpgram.

This module provides handlers for inline queries in Telegram bots.
"""

from typing import Optional, Callable, Awaitable, Dict, Any, List, Union

from ..types.update import Update
from .base import BaseHandler
from ..logging import get_logger

logger = get_logger(__name__)


class InlineQueryHandler(BaseHandler):
    """
    Handler for inline queries.
    
    This handler processes inline queries from users.
    """
    
    def __init__(
        self,
        callback: Callable[[Dict[str, Any], 'Bot'], Awaitable[None]],
        pattern: Optional[str] = None,
        chat_types: Optional[List[str]] = None,
    ):
        """
        Initialize the InlineQueryHandler.
        
        Args:
            callback: Callback function to handle the inline query
            pattern: Regular expression pattern to match against the query
            chat_types: List of chat types to handle inline queries from
        """
        super().__init__()
        self.callback = callback
        self.pattern = self._compile_pattern(pattern) if pattern else None
        self.chat_types = chat_types
    
    async def check_update(self, update: Update) -> bool:
        """
        Check if the update should be handled by this handler.
        
        Args:
            update: Update to check
        
        Returns:
            True if the update should be handled, False otherwise
        """
        if not update.inline_query:
            return False
        
        # Check pattern if provided
        if self.pattern and not self.pattern.search(update.inline_query.query):
            return False
        
        # Check chat type if provided
        if self.chat_types:
            from_user = update.inline_query.from_user
            if not from_user:
                return False
            
            # For inline queries, we can only check if it's from a private chat
            # by checking if it's from a user
            if 'private' in self.chat_types:
                return True
            
            return False
        
        return True
    
    async def handle_update(self, update: Update, bot: 'Bot') -> None:
        """
        Handle the update.
        
        Args:
            update: Update to handle
            bot: Bot instance
        """
        await self.callback(update.inline_query, bot)


async def answer_inline_query(
    bot: 'Bot',
    inline_query_id: str,
    results: List[Dict[str, Any]],
    cache_time: Optional[int] = None,
    is_personal: Optional[bool] = None,
    next_offset: Optional[str] = None,
    switch_pm_text: Optional[str] = None,
    switch_pm_parameter: Optional[str] = None,
) -> bool:
    """
    Answer an inline query.
    
    Args:
        bot: Bot instance
        inline_query_id: Unique identifier for the answered query
        results: List of results for the inline query
        cache_time: Maximum amount of time in seconds the result can be cached
        is_personal: Whether the results are personal to the user
        next_offset: Offset that a client should send in the next query
        switch_pm_text: Text of the button that switches the user to a private chat with the bot
        switch_pm_parameter: Deep-linking parameter for the /start message
    
    Returns:
        True if the inline query was answered successfully, False otherwise
    """
    try:
        return await bot.answer_inline_query(
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )
    except Exception as e:
        logger.exception(f"Error answering inline query: {e}")
        return False


def create_inline_query_result_article(
    id: str,
    title: str,
    input_message_content: Dict[str, Any],
    reply_markup: Optional[Dict[str, Any]] = None,
    url: Optional[str] = None,
    hide_url: Optional[bool] = None,
    description: Optional[str] = None,
    thumb_url: Optional[str] = None,
    thumb_width: Optional[int] = None,
    thumb_height: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Create an inline query result article.
    
    Args:
        id: Unique identifier for this result
        title: Title of the result
        input_message_content: Content of the message to be sent
        reply_markup: Inline keyboard attached to the message
        url: URL of the result
        hide_url: Whether to hide the URL in the message
        description: Short description of the result
        thumb_url: URL of the thumbnail for the result
        thumb_width: Thumbnail width
        thumb_height: Thumbnail height
    
    Returns:
        Inline query result article
    """
    result = {
        'type': 'article',
        'id': id,
        'title': title,
        'input_message_content': input_message_content,
    }
    
    if reply_markup:
        result['reply_markup'] = reply_markup
    
    if url:
        result['url'] = url
    
    if hide_url is not None:
        result['hide_url'] = hide_url
    
    if description:
        result['description'] = description
    
    if thumb_url:
        result['thumb_url'] = thumb_url
    
    if thumb_width:
        result['thumb_width'] = thumb_width
    
    if thumb_height:
        result['thumb_height'] = thumb_height
    
    return result


def create_input_text_message_content(
    message_text: str,
    parse_mode: Optional[str] = None,
    entities: Optional[List[Dict[str, Any]]] = None,
    disable_web_page_preview: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Create an input text message content.
    
    Args:
        message_text: Text of the message to be sent
        parse_mode: Mode for parsing entities in the message text
        entities: List of special entities that appear in the message text
        disable_web_page_preview: Disables link previews for links in the message
    
    Returns:
        Input text message content
    """
    content = {
        'message_text': message_text,
    }
    
    if parse_mode:
        content['parse_mode'] = parse_mode
    
    if entities:
        content['entities'] = entities
    
    if disable_web_page_preview is not None:
        content['disable_web_page_preview'] = disable_web_page_preview
    
    return content
