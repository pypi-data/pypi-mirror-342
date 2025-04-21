"""
Callback Query type for Telegram API.
"""

from typing import Optional, Dict, Any
from pydantic import Field

from .base import TelegramObject
from .user import User
from .message import Message

class CallbackQuery(TelegramObject):
    """
    This object represents an incoming callback query from a callback button in an inline keyboard.

    Attributes:
        id: Unique identifier for this query
        from_user: Sender
        message: Message with the callback button that originated the query
        inline_message_id: Identifier of the message sent via the bot in inline mode, that originated the query
        chat_instance: Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent
        data: Data associated with the callback button
        game_short_name: Short name of a Game to be returned, serves as the unique identifier for the game
    """

    id: str
    from_user: User = Field(alias='from')
    chat_instance: str
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
