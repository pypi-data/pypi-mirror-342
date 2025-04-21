"""
Message type for Telegram API.
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime
from pydantic import Field

if TYPE_CHECKING:
    from ..bot import Bot

from .base import TelegramObject
from .user import User
from .chat import Chat

class Message(TelegramObject):
    """
    This object represents a message.

    Attributes:
        message_id: Unique message identifier inside this chat
        from_user: Sender of the message; empty for messages sent to channels
        date: Date the message was sent
        chat: Conversation the message belongs to
        text: For text messages, the actual UTF-8 text of the message
        # ... many more attributes as per Telegram API
    """

    message_id: int
    date: datetime
    chat: 'Chat'
    from_user: Optional['User'] = Field(None, alias='from')
    text: Optional[str] = None
    entities: Optional[List[Dict[str, Any]]] = None
    animation: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    photo: Optional[List[Dict[str, Any]]] = None
    sticker: Optional[Dict[str, Any]] = None
    video: Optional[Dict[str, Any]] = None
    video_note: Optional[Dict[str, Any]] = None
    voice: Optional[Dict[str, Any]] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[Dict[str, Any]]] = None
    contact: Optional[Dict[str, Any]] = None
    dice: Optional[Dict[str, Any]] = None
    game: Optional[Dict[str, Any]] = None
    poll: Optional[Dict[str, Any]] = None
    venue: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    new_chat_members: Optional[List[Dict[str, Any]]] = None
    left_chat_member: Optional[Dict[str, Any]] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[List[Dict[str, Any]]] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[Dict[str, Any]] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional['Message'] = None
    invoice: Optional[Dict[str, Any]] = None
    successful_payment: Optional[Dict[str, Any]] = None
    connected_website: Optional[str] = None
    passport_data: Optional[Dict[str, Any]] = None
    proximity_alert_triggered: Optional[Dict[str, Any]] = None
    voice_chat_scheduled: Optional[Dict[str, Any]] = None
    voice_chat_started: Optional[Dict[str, Any]] = None
    voice_chat_ended: Optional[Dict[str, Any]] = None
    voice_chat_participants_invited: Optional[Dict[str, Any]] = None
    reply_to_message: Optional['Message'] = None
    via_bot: Optional[User] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_signature: Optional[str] = None
    forward_sender_name: Optional[str] = None
    forward_date: Optional[datetime] = None
    is_automatic_forward: Optional[bool] = None
    reply_markup: Optional[Dict[str, Any]] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

    async def reply_text(
        self,
        bot: 'Bot',
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> 'Message':
        """
        Reply to this message with text.

        Args:
            bot: Bot instance to use for sending the message
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options

        Returns:
            The sent Message
        """
        return await bot.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id or self.message_id,
            reply_markup=reply_markup,
        )
