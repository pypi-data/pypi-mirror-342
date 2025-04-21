"""
Message class for Telegram Bot API.

This module provides a simplified interface for working with messages in Telegram bots.
"""

from typing import Optional, Union, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot
    from ..types.message import Message as TelegramMessage
    from .button import InlineKeyboard, ReplyKeyboard


class Message:
    """
    Simplified interface for Telegram messages.
    
    This class provides a simplified interface for working with Telegram messages.
    """
    
    def __init__(self, message: 'TelegramMessage'):
        """
        Initialize a message.
        
        Args:
            message: Original Telegram message object
        """
        self._message = message
    
    @property
    def id(self) -> int:
        """Get the message ID."""
        return self._message.message_id
    
    @property
    def text(self) -> Optional[str]:
        """Get the message text."""
        return self._message.text
    
    @property
    def chat_id(self) -> int:
        """Get the chat ID."""
        return self._message.chat.id
    
    @property
    def from_user_id(self) -> Optional[int]:
        """Get the user ID of the sender."""
        return self._message.from_user.id if self._message.from_user else None
    
    @property
    def from_user_name(self) -> Optional[str]:
        """Get the username of the sender."""
        return self._message.from_user.username if self._message.from_user else None
    
    @property
    def from_user_first_name(self) -> Optional[str]:
        """Get the first name of the sender."""
        return self._message.from_user.first_name if self._message.from_user else None
    
    @property
    def is_command(self) -> bool:
        """Check if the message is a command."""
        return bool(self.text and self.text.startswith('/'))
    
    @property
    def command(self) -> Optional[str]:
        """Get the command without the slash."""
        if not self.is_command:
            return None
        
        command_parts = self.text.split()
        if not command_parts:
            return None
        
        # Remove the slash and extract command name
        command = command_parts[0][1:].split('@')[0]
        return command
    
    @property
    def args(self) -> List[str]:
        """Get the command arguments."""
        if not self.is_command or not self.text:
            return []
        
        command_parts = self.text.split()
        if len(command_parts) <= 1:
            return []
        
        return command_parts[1:]
    
    @property
    def original(self) -> 'TelegramMessage':
        """Get the original Telegram message object."""
        return self._message
    
    async def reply(
        self,
        bot: 'Bot',
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_markup: Optional[Union['InlineKeyboard', 'ReplyKeyboard', Dict[str, Any]]] = None,
    ) -> 'Message':
        """
        Reply to this message.
        
        Args:
            bot: Bot instance
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
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
        
        result = await bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=self.id,
            reply_markup=markup,
        )
        
        from ..types.message import Message as TelegramMessage
        return Message(TelegramMessage.from_dict(result))
    
    async def edit(
        self,
        bot: 'Bot',
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Union['InlineKeyboard', Dict[str, Any]]] = None,
    ) -> 'Message':
        """
        Edit this message.
        
        Args:
            bot: Bot instance
            text: New text of the message
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            reply_markup: Additional interface options
            
        Returns:
            The edited message
        """
        markup = None
        if reply_markup is not None:
            if hasattr(reply_markup, 'as_markup'):
                markup = reply_markup.as_markup()
            else:
                markup = reply_markup
        
        result = await bot.edit_message_text(
            text=text,
            chat_id=self.chat_id,
            message_id=self.id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=markup,
        )
        
        from ..types.message import Message as TelegramMessage
        return Message(TelegramMessage.from_dict(result))
    
    async def delete(self, bot: 'Bot') -> bool:
        """
        Delete this message.
        
        Args:
            bot: Bot instance
            
        Returns:
            True on success
        """
        return await bot._make_request(
            "deleteMessage",
            {
                'chat_id': self.chat_id,
                'message_id': self.id,
            }
        )
    
    @classmethod
    def from_telegram_message(cls, message: 'TelegramMessage') -> 'Message':
        """
        Create a Message from a Telegram message.
        
        Args:
            message: Telegram message object
            
        Returns:
            A Message instance
        """
        return cls(message)
