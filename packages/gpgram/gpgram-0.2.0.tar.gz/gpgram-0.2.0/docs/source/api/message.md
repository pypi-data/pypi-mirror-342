# Message

The `Message` class represents a message in Telegram. It contains all the information about a message, including the sender, chat, text, media, and more.

## Overview

The `Message` class is a Pydantic model that represents a message in Telegram. It contains all the information about a message, including the sender, chat, text, media, and more.

```python
from gpgram.types import Message

# Access a message from an update
message = update.message

# Access message properties
text = message.text
chat_id = message.chat.id
user = message.from_user
```

```{note}
The `Message` class is a Pydantic model that validates and converts the raw JSON data from Telegram into a Python object with proper types.
```

## Properties

The `Message` class has the following properties:

- **message_id** (`int`): Unique message identifier inside this chat
- **from_user** (`User`): Sender of the message; empty for messages sent to channels. For backward compatibility, the field is called `from_user` but is aliased to `from` in the Telegram API.
- **chat** (`Chat`): Chat to which the message belongs
- **date** (`datetime`): Date the message was sent
- **text** (`Optional[str]`): For text messages, the actual UTF-8 text of the message, 0-4096 characters
- **reply_to_message** (`Optional[Message]`): For replies, the original message. Note that the Message object in this field will not contain further `reply_to_message` fields even if it itself is a reply.
- **forward_from** (`Optional[User]`): For forwarded messages, sender of the original message
- **forward_date** (`Optional[datetime]`): For forwarded messages, date the original message was sent
- **photo** (`Optional[List[PhotoSize]]`): Available sizes of the photo
- **caption** (`Optional[str]`): Caption for the photo, audio, document, video, etc.
- **sticker** (`Optional[Sticker]`): Message is a sticker, information about the sticker
- **video** (`Optional[Video]`): Message is a video, information about the video
- **audio** (`Optional[Audio]`): Message is an audio file, information about the file
- **document** (`Optional[Document]`): Message is a general file, information about the file
- **location** (`Optional[Location]`): Message is a shared location, information about the location
- **venue** (`Optional[Venue]`): Message is a venue, information about the venue
- **contact** (`Optional[Contact]`): Message is a shared contact, information about the contact
- **poll** (`Optional[Poll]`): Message is a native poll, information about the poll
- **reply_markup** (`Optional[InlineKeyboardMarkup]`): Inline keyboard attached to the message

```{note}
This is not an exhaustive list of all properties. The `Message` class has many more properties that correspond to the Telegram Bot API's [Message](https://core.telegram.org/bots/api#message) object.
```

## Methods

### from_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Message':
    """
    Create a Message from a dictionary.
    
    Args:
        data: Dictionary representation of the message
        
    Returns:
        A Message instance
    """
```

Creates a `Message` instance from a dictionary representation of a message.

**Parameters:**
- **data** (`Dict[str, Any]`): Dictionary representation of the message

**Returns:**
- `Message`: A Message instance

### to_dict

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Convert the message to a dictionary.
    
    Returns:
        Dictionary representation of the message
    """
```

Converts the `Message` instance to a dictionary representation.

**Returns:**
- `Dict[str, Any]`: Dictionary representation of the message

## Examples

### Accessing Message Properties

```python
@router.message()
async def handle_message(message, bot):
    # Access message properties
    message_id = message.message_id
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else None
    text = message.text or "No text"
    
    # Check if the message is a reply
    if message.reply_to_message:
        original_text = message.reply_to_message.text or "No text"
        await bot.send_message(
            chat_id=chat_id,
            text=f"You replied to: {original_text}"
        )
    
    # Check if the message contains media
    if message.photo:
        # Get the largest photo (last in the list)
        photo = message.photo[-1]
        await bot.send_message(
            chat_id=chat_id,
            text=f"You sent a photo with file_id: {photo.file_id}"
        )
    
    # Send a response
    await bot.send_message(
        chat_id=chat_id,
        text=f"Received your message: {text}"
    )
```

### Creating a Message from Dictionary

```python
from gpgram.types import Message

# Dictionary representation of a message
message_dict = {
    "message_id": 123,
    "from": {
        "id": 456,
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe"
    },
    "chat": {
        "id": 789,
        "type": "private",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe"
    },
    "date": 1625097600,
    "text": "Hello, world!"
}

# Create a Message instance
message = Message.from_dict(message_dict)

# Access properties
print(message.message_id)  # 123
print(message.from_user.username)  # johndoe
print(message.chat.id)  # 789
print(message.text)  # Hello, world!
```

## See Also

- [Update](update.md) - Contains a Message in its properties
- [Chat](chat.md) - Represents the chat where the message was sent
- [User](user.md) - Represents the sender of the message
- [SimpleMessage](simple-message.md) - A simplified interface for the Message class
