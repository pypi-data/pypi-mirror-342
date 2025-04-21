"""
Chat type for Telegram API.
"""

from typing import Optional, List, Dict, Any
from pydantic import Field

from .base import TelegramObject

class Chat(TelegramObject):
    """
    This object represents a chat.
    
    Attributes:
        id: Unique identifier for this chat
        type: Type of chat, can be either "private", "group", "supergroup" or "channel"
        title: Title, for supergroups, channels and group chats
        username: Username, for private chats, supergroups and channels if available
        first_name: First name of the other party in a private chat
        last_name: Last name of the other party in a private chat
        photo: Chat photo
        bio: Bio of the other party in a private chat
        description: Description, for groups, supergroups and channel chats
        invite_link: Primary invite link, for groups, supergroups and channel chats
        pinned_message: The most recent pinned message
        permissions: Default chat member permissions, for groups and supergroups
        slow_mode_delay: For supergroups, the minimum allowed delay between consecutive messages
        message_auto_delete_time: The time after which all messages will be automatically deleted
        has_protected_content: True, if messages from the chat can't be forwarded to other chats
        sticker_set_name: For supergroups, name of group sticker set
        can_set_sticker_set: True, if the bot can change the group sticker set
        linked_chat_id: Unique identifier for the linked chat
        location: For supergroups, the location to which the supergroup is connected
    """
    
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[Dict[str, Any]] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    permissions: Optional[Dict[str, Any]] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[Dict[str, Any]] = None
    
    @property
    def full_name(self) -> str:
        """
        Get the chat's full name.
        
        Returns:
            The chat's full name (title for groups, first name + last name for private chats)
        """
        if self.type == 'private':
            if self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.first_name or ""
        return self.title or ""
    
    @property
    def is_private(self) -> bool:
        """Check if the chat is a private chat."""
        return self.type == 'private'
    
    @property
    def is_group(self) -> bool:
        """Check if the chat is a group chat."""
        return self.type == 'group'
    
    @property
    def is_supergroup(self) -> bool:
        """Check if the chat is a supergroup."""
        return self.type == 'supergroup'
    
    @property
    def is_channel(self) -> bool:
        """Check if the chat is a channel."""
        return self.type == 'channel'
