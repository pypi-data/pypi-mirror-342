"""
Update type for Telegram API.
"""

from typing import Optional, Dict, Any, List, TYPE_CHECKING
from pydantic import Field

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User

from .base import TelegramObject
from .message import Message
from .callback_query import CallbackQuery

class Update(TelegramObject):
    """
    This object represents an incoming update.

    Attributes:
        update_id: The update's unique identifier
        message: New incoming message of any kind - text, photo, sticker, etc.
        edited_message: New version of a message that is known to the bot and was edited
        channel_post: New incoming channel post of any kind - text, photo, sticker, etc.
        edited_channel_post: New version of a channel post that is known to the bot and was edited
        callback_query: New incoming callback query
        inline_query: New incoming inline query
        chosen_inline_result: The result of an inline query that was chosen by a user
        shipping_query: New incoming shipping query
        pre_checkout_query: New incoming pre-checkout query
        poll: New poll state
        poll_answer: A user changed their answer in a non-anonymous poll
        my_chat_member: The bot's chat member status was updated in a chat
        chat_member: A chat member's status was updated in a chat
        chat_join_request: A request to join the chat has been sent
    """

    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
    inline_query: Optional[Any] = None
    chosen_inline_result: Optional[Any] = None
    shipping_query: Optional[Any] = None
    pre_checkout_query: Optional[Any] = None
    poll: Optional[Any] = None
    poll_answer: Optional[Any] = None
    my_chat_member: Optional[Any] = None
    chat_member: Optional[Any] = None
    chat_join_request: Optional[Any] = None

    @property
    def effective_message(self) -> Optional[Message]:
        """
        Get the effective message from the update.

        Returns:
            The first non-None message from the update
        """
        return (
            self.message or self.edited_message or
            self.channel_post or self.edited_channel_post
        )

    @property
    def effective_chat(self) -> Optional['Chat']:
        """
        Get the effective chat from the update.

        Returns:
            The chat from the effective message or other update types
        """
        if self.effective_message:
            return self.effective_message.chat

        # Add support for other update types with chat attribute
        return None

    @property
    def effective_user(self) -> Optional['User']:
        """
        Get the effective user from the update.

        Returns:
            The user from the effective message or other update types
        """
        if self.effective_message:
            return self.effective_message.from_user

        # Add support for other update types with from_user attribute
        return None
