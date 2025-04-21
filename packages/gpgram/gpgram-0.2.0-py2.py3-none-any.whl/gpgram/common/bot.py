"""
Bot class for Telegram Bot API.

This module provides a simplified interface for working with Telegram bots.
"""

from typing import Optional, Union, Dict, Any, List, BinaryIO, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot as TelegramBot
    from .message import Message
    from .button import InlineKeyboard, ReplyKeyboard


class Bot:
    """
    Simplified interface for Telegram Bot API.
    
    This class provides a simplified interface for working with Telegram bots.
    """
    
    def __init__(self, token: str):
        """
        Initialize a bot.
        
        Args:
            token: Telegram bot token
        """
        from ..bot import Bot as TelegramBot
        self._bot = TelegramBot(token=token)
    
    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union['InlineKeyboard', 'ReplyKeyboard', Dict[str, Any]]] = None,
    ) -> 'Message':
        """
        Send a message.
        
        Args:
            chat_id: Unique identifier for the target chat
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options
            
        Returns:
            The sent message
        """
        markup = None
        if reply_markup is not None:
            if hasattr(reply_markup, 'as_markup'):
                markup = reply_markup.as_markup()
            else:
                markup = reply_markup
        
        result = await self._bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=markup,
        )
        
        from ..types.message import Message as TelegramMessage
        from .message import Message
        return Message(TelegramMessage.from_dict(result))
    
    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union['InlineKeyboard', 'ReplyKeyboard', Dict[str, Any]]] = None,
    ) -> 'Message':
        """
        Send a photo.
        
        Args:
            chat_id: Unique identifier for the target chat
            photo: Photo to send
            caption: Photo caption
            parse_mode: Mode for parsing entities in the caption
            disable_notification: Sends the message silently
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options
            
        Returns:
            The sent message
        """
        markup = None
        if reply_markup is not None:
            if hasattr(reply_markup, 'as_markup'):
                markup = reply_markup.as_markup()
            else:
                markup = reply_markup
        
        result = await self._bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=markup,
        )
        
        from ..types.message import Message as TelegramMessage
        from .message import Message
        return Message(TelegramMessage.from_dict(result))
    
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
    ) -> bool:
        """
        Answer a callback query.
        
        Args:
            callback_query_id: Unique identifier for the query to be answered
            text: Text of the notification
            show_alert: If True, an alert will be shown by the client
            url: URL that will be opened by the user's client
            cache_time: Time in seconds for which the result will be cached
            
        Returns:
            True on success
        """
        return await self._bot.answer_callback_query(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )
    
    async def edit_message_text(
        self,
        text: str,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Union['InlineKeyboard', Dict[str, Any]]] = None,
    ) -> Union[Dict[str, Any], bool]:
        """
        Edit a message's text.
        
        Args:
            text: New text of the message
            chat_id: Unique identifier for the target chat
            message_id: Identifier of the message to edit
            inline_message_id: Identifier of the inline message
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            reply_markup: Additional interface options
            
        Returns:
            The edited message or True on success
        """
        markup = None
        if reply_markup is not None:
            if hasattr(reply_markup, 'as_markup'):
                markup = reply_markup.as_markup()
            else:
                markup = reply_markup
        
        return await self._bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=markup,
        )
    
    async def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
    ) -> bool:
        """
        Delete a message.
        
        Args:
            chat_id: Unique identifier for the target chat
            message_id: Identifier of the message to delete
            
        Returns:
            True on success
        """
        return await self._bot._make_request(
            "deleteMessage",
            {
                'chat_id': chat_id,
                'message_id': message_id,
            }
        )
    
    async def get_me(self) -> Dict[str, Any]:
        """
        Get information about the bot.
        
        Returns:
            A dictionary containing information about the bot
        """
        return await self._bot.get_me()
    
    @property
    def original(self) -> 'TelegramBot':
        """Get the original Telegram bot object."""
        return self._bot
