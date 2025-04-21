"""
Message filters for Telegram Bot API.
"""

import re
from typing import List, Optional, Pattern, Set, Union

from .base import BaseFilter

class TextFilter(BaseFilter):
    """
    Filter for message text.
    
    This filter passes if the message text matches the specified text.
    """
    
    def __init__(
        self, 
        text: Union[str, List[str]], 
        ignore_case: bool = False
    ):
        """
        Initialize the filter.
        
        Args:
            text: Text or list of texts to match
            ignore_case: Whether to ignore case when matching
        """
        super().__init__()
        self.text = [text] if isinstance(text, str) else text
        self.ignore_case = ignore_case
    
    def __call__(self, message) -> bool:
        """
        Check if the message passes the filter.
        
        Args:
            message: Message to check
        
        Returns:
            True if the message text matches the specified text, False otherwise
        """
        if not message.text:
            return False
        
        if self.ignore_case:
            return message.text.lower() in [t.lower() for t in self.text]
        
        return message.text in self.text


class CommandFilter(BaseFilter):
    """
    Filter for commands.
    
    This filter passes if the message text starts with a command.
    """
    
    def __init__(
        self, 
        commands: Union[str, List[str]], 
        prefixes: Union[str, List[str]] = '/',
        ignore_case: bool = False
    ):
        """
        Initialize the filter.
        
        Args:
            commands: Command or list of commands to match
            prefixes: Prefix or list of prefixes for commands
            ignore_case: Whether to ignore case when matching
        """
        super().__init__()
        self.commands = [commands] if isinstance(commands, str) else commands
        self.prefixes = [prefixes] if isinstance(prefixes, str) else prefixes
        self.ignore_case = ignore_case
    
    def __call__(self, message) -> bool:
        """
        Check if the message passes the filter.
        
        Args:
            message: Message to check
        
        Returns:
            True if the message text starts with a command, False otherwise
        """
        if not message.text:
            return False
        
        text = message.text
        
        if self.ignore_case:
            text = text.lower()
            self.commands = [cmd.lower() for cmd in self.commands]
        
        for prefix in self.prefixes:
            for command in self.commands:
                # Check if the message starts with the command
                command_with_prefix = f"{prefix}{command}"
                
                if text.startswith(command_with_prefix):
                    # Check if the command is followed by a space, @ or end of string
                    if len(text) == len(command_with_prefix) or text[len(command_with_prefix)] in (' ', '@'):
                        return True
        
        return False


class RegexFilter(BaseFilter):
    """
    Filter for regex patterns.
    
    This filter passes if the message text matches the specified regex pattern.
    """
    
    def __init__(
        self, 
        pattern: Union[str, Pattern], 
        flags: int = 0
    ):
        """
        Initialize the filter.
        
        Args:
            pattern: Regex pattern to match
            flags: Regex flags
        """
        super().__init__()
        self.pattern = re.compile(pattern, flags) if isinstance(pattern, str) else pattern
    
    def __call__(self, message) -> bool:
        """
        Check if the message passes the filter.
        
        Args:
            message: Message to check
        
        Returns:
            True if the message text matches the regex pattern, False otherwise
        """
        if not message.text:
            return False
        
        return bool(self.pattern.search(message.text))


class ContentTypeFilter(BaseFilter):
    """
    Filter for message content type.
    
    This filter passes if the message has the specified content type.
    """
    
    def __init__(
        self, 
        content_types: Union[str, List[str]]
    ):
        """
        Initialize the filter.
        
        Args:
            content_types: Content type or list of content types to match
        """
        super().__init__()
        self.content_types = [content_types] if isinstance(content_types, str) else content_types
    
    def __call__(self, message) -> bool:
        """
        Check if the message passes the filter.
        
        Args:
            message: Message to check
        
        Returns:
            True if the message has the specified content type, False otherwise
        """
        for content_type in self.content_types:
            if content_type == 'text' and message.text:
                return True
            elif content_type == 'photo' and message.photo:
                return True
            elif content_type == 'audio' and message.audio:
                return True
            elif content_type == 'document' and message.document:
                return True
            elif content_type == 'video' and message.video:
                return True
            elif content_type == 'voice' and message.voice:
                return True
            elif content_type == 'video_note' and message.video_note:
                return True
            elif content_type == 'contact' and message.contact:
                return True
            elif content_type == 'location' and message.location:
                return True
            elif content_type == 'venue' and message.venue:
                return True
            elif content_type == 'animation' and message.animation:
                return True
            elif content_type == 'sticker' and message.sticker:
                return True
            elif content_type == 'poll' and message.poll:
                return True
            elif content_type == 'dice' and message.dice:
                return True
            elif content_type == 'game' and message.game:
                return True
            elif content_type == 'invoice' and message.invoice:
                return True
            elif content_type == 'successful_payment' and message.successful_payment:
                return True
        
        return False


class ChatTypeFilter(BaseFilter):
    """
    Filter for chat type.
    
    This filter passes if the chat has the specified type.
    """
    
    def __init__(
        self, 
        chat_types: Union[str, List[str]]
    ):
        """
        Initialize the filter.
        
        Args:
            chat_types: Chat type or list of chat types to match
        """
        super().__init__()
        self.chat_types = [chat_types] if isinstance(chat_types, str) else chat_types
    
    def __call__(self, message) -> bool:
        """
        Check if the message passes the filter.
        
        Args:
            message: Message to check
        
        Returns:
            True if the chat has the specified type, False otherwise
        """
        return message.chat.type in self.chat_types
