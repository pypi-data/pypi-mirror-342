"""
Bot class for interacting with the Telegram Bot API.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union, TypeVar, Type, BinaryIO, Callable, Awaitable

import httpx
from pydantic import BaseModel

from .types.update import Update
from .types.message import Message
from .logging import get_logger

T = TypeVar('T')

class BotException(Exception):
    """Base exception for Bot errors."""
    pass

class APIError(BotException):
    """Exception raised when the Telegram API returns an error."""

    def __init__(self, error_code: int, description: str):
        self.error_code = error_code
        self.description = description
        super().__init__(f"Telegram API error {error_code}: {description}")

class Bot:
    """
    Main class for interacting with the Telegram Bot API.

    This class provides methods for sending requests to the Telegram Bot API
    and handles the authentication with the bot token.
    """

    API_URL = "https://api.telegram.org/bot{token}/{method}"
    FILE_URL = "https://api.telegram.org/file/bot{token}/{file_path}"

    def __init__(
        self,
        token: str,
        parse_mode: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        connection_pool_size: int = 100,
    ):
        """
        Initialize the Bot instance.

        Args:
            token: Telegram Bot API token
            parse_mode: Default parse mode for sending messages
            base_url: Custom base URL for Telegram API
            timeout: Timeout for API requests in seconds
            connection_pool_size: Size of the connection pool
        """
        self.token = token
        self.parse_mode = parse_mode
        self.base_url = base_url or self.API_URL
        self.file_url = self.FILE_URL
        self.timeout = timeout
        self.logger = get_logger(__name__)

        # Create HTTP client with connection pooling
        self._client = httpx.AsyncClient(
            timeout=timeout,
            limits=httpx.Limits(max_connections=connection_pool_size)
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the bot's HTTP client session."""
        await self._client.aclose()

    async def _make_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a request to the Telegram Bot API.

        Args:
            method: API method name
            params: Parameters for the API method
            files: Files to upload
            **kwargs: Additional parameters to pass to the API method

        Returns:
            Response from the API as a dictionary

        Raises:
            APIError: If the API returns an error
            httpx.HTTPError: If there's an HTTP error
        """
        url = self.base_url.format(token=self.token, method=method)

        if params is None:
            params = {}

        # Add default parse_mode if not explicitly set
        if self.parse_mode and 'parse_mode' not in params and method in {
            'sendMessage', 'editMessageText', 'sendPhoto', 'sendVideo',
            'sendAudio', 'sendDocument', 'sendAnimation'
        }:
            params['parse_mode'] = self.parse_mode

        # Add additional kwargs to params
        params.update(kwargs)

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        try:
            if files:
                response = await self._client.post(url, data=params, files=files)
            else:
                response = await self._client.post(url, json=params)

            response.raise_for_status()
            result = response.json()

            if not result.get('ok'):
                error_code = result.get('error_code', 0)
                description = result.get('description', 'No description')
                self.logger.error(f"API error {error_code}: {description}")
                raise APIError(error_code, description)

            return result['result']

        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            raise

    async def get_me(self) -> Dict[str, Any]:
        """
        Get information about the bot.

        Returns:
            A User object representing the bot.
        """
        return await self._make_request("getMe")

    async def get_updates(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
    ) -> List[Update]:
        """
        Get updates from Telegram.

        Args:
            offset: Identifier of the first update to be returned
            limit: Limit the number of updates to be retrieved
            timeout: Timeout in seconds for long polling
            allowed_updates: List of update types to receive

        Returns:
            List of Update objects
        """
        params = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
            'allowed_updates': allowed_updates,
        }

        result = await self._make_request("getUpdates", params)
        return [Update.from_dict(update) for update in result]

    async def set_webhook(
        self,
        url: str,
        certificate: Optional[BinaryIO] = None,
        ip_address: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None,
        drop_pending_updates: Optional[bool] = None,
        secret_token: Optional[str] = None,
    ) -> bool:
        """
        Set webhook for getting updates.

        Args:
            url: HTTPS URL to send updates to
            certificate: Upload your public key certificate
            ip_address: The fixed IP address which will be used to send webhook requests
            max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook
            allowed_updates: List of the update types you want your bot to receive
            drop_pending_updates: Pass True to drop all pending updates
            secret_token: A secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token"

        Returns:
            True on success
        """
        params = {
            'url': url,
            'ip_address': ip_address,
            'max_connections': max_connections,
            'allowed_updates': allowed_updates,
            'drop_pending_updates': drop_pending_updates,
            'secret_token': secret_token,
        }

        files = None
        if certificate:
            files = {'certificate': certificate}

        result = await self._make_request("setWebhook", params, files)
        return result

    async def delete_webhook(
        self,
        drop_pending_updates: Optional[bool] = None,
    ) -> bool:
        """
        Remove webhook integration.

        Args:
            drop_pending_updates: Pass True to drop all pending updates

        Returns:
            True on success
        """
        params = {
            'drop_pending_updates': drop_pending_updates,
        }

        result = await self._make_request("deleteWebhook", params)
        return result

    async def get_webhook_info(self) -> Dict[str, Any]:
        """
        Get current webhook status.

        Returns:
            WebhookInfo object
        """
        return await self._make_request("getWebhookInfo")

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[Dict[str, Any]]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a message.

        Args:
            chat_id: Unique identifier for the target chat
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            entities: List of special entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            protect_content: Protects the content of the sent message from forwarding and saving
            reply_to_message_id: If the message is a reply, ID of the original message
            allow_sending_without_reply: Pass True if the message should be sent even if the specified replied-to message is not found
            reply_markup: Additional interface options

        Returns:
            The sent Message
        """
        params = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'entities': entities,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': reply_markup,
        }

        return await self._make_request("sendMessage", params)

    async def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Forward a message.

        Args:
            chat_id: Unique identifier for the target chat
            from_chat_id: Unique identifier for the chat where the original message was sent
            message_id: Message identifier in the chat specified in from_chat_id
            disable_notification: Sends the message silently
            protect_content: Protects the content of the forwarded message from forwarding and saving

        Returns:
            The forwarded Message
        """
        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
        }

        return await self._make_request("forwardMessage", params)

    async def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[Dict[str, Any]]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a photo.

        Args:
            chat_id: Unique identifier for the target chat
            photo: Photo to send
            caption: Photo caption
            parse_mode: Mode for parsing entities in the photo caption
            caption_entities: List of special entities in the caption
            disable_notification: Sends the message silently
            protect_content: Protects the content of the sent message from forwarding and saving
            reply_to_message_id: If the message is a reply, ID of the original message
            allow_sending_without_reply: Pass True if the message should be sent even if the specified replied-to message is not found
            reply_markup: Additional interface options

        Returns:
            The sent Message
        """
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'caption_entities': caption_entities,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': reply_markup,
        }

        files = None
        if isinstance(photo, str) and (photo.startswith('http') or photo.startswith('file://')):
            params['photo'] = photo
        else:
            files = {'photo': photo}

        return await self._make_request("sendPhoto", params, files)

    async def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[str, BinaryIO],
        thumb: Optional[Union[str, BinaryIO]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[Dict[str, Any]]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Send a document.

        Args:
            chat_id: Unique identifier for the target chat
            document: Document to send
            thumb: Thumbnail of the file
            caption: Document caption
            parse_mode: Mode for parsing entities in the document caption
            caption_entities: List of special entities in the caption
            disable_content_type_detection: Disables automatic content type detection for files
            disable_notification: Sends the message silently
            protect_content: Protects the content of the sent message from forwarding and saving
            reply_to_message_id: If the message is a reply, ID of the original message
            allow_sending_without_reply: Pass True if the message should be sent even if the specified replied-to message is not found
            reply_markup: Additional interface options

        Returns:
            The sent Message
        """
        params = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': parse_mode,
            'caption_entities': caption_entities,
            'disable_content_type_detection': disable_content_type_detection,
            'disable_notification': disable_notification,
            'protect_content': protect_content,
            'reply_to_message_id': reply_to_message_id,
            'allow_sending_without_reply': allow_sending_without_reply,
            'reply_markup': reply_markup,
        }

        files = {}

        if isinstance(document, str) and (document.startswith('http') or document.startswith('file://')):
            params['document'] = document
        else:
            files['document'] = document

        if thumb:
            if isinstance(thumb, str) and (thumb.startswith('http') or thumb.startswith('file://')):
                params['thumb'] = thumb
            else:
                files['thumb'] = thumb

        if not files:
            files = None

        return await self._make_request("sendDocument", params, files)

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
            show_alert: If True, an alert will be shown by the client instead of a notification
            url: URL that will be opened by the user's client
            cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side

        Returns:
            True on success
        """
        params = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time,
        }

        return await self._make_request("answerCallbackQuery", params)

    async def edit_message_text(
        self,
        text: str,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[Dict[str, Any]]] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], bool]:
        """
        Edit text and game messages.

        Args:
            text: New text of the message
            chat_id: Required if inline_message_id is not specified
            message_id: Required if inline_message_id is not specified
            inline_message_id: Required if chat_id and message_id are not specified
            parse_mode: Mode for parsing entities in the message text
            entities: List of special entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            reply_markup: A JSON-serialized object for an inline keyboard

        Returns:
            The edited Message or True if inline_message_id was specified
        """
        params = {
            'text': text,
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'parse_mode': parse_mode,
            'entities': entities,
            'disable_web_page_preview': disable_web_page_preview,
            'reply_markup': reply_markup,
        }

        return await self._make_request("editMessageText", params)

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
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
        }

        return await self._make_request("deleteMessage", params)

    # Add more methods for other Telegram API endpoints as needed
