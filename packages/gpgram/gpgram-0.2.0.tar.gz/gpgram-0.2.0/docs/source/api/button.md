# Button

The `Button` class is a base class for all button types in Gpgram. It provides static methods for creating inline and keyboard buttons, as well as organizing buttons into rows.

## Overview

The `Button` class is part of the simplified interface in Gpgram. It provides a convenient way to create and organize buttons for Telegram bot keyboards.

```python
from gpgram import Button, InlineButton, KeyboardButton

# Create inline buttons
button1 = Button.create_inline(text="Option 1", callback_data="option1")
button2 = Button.create_inline(text="Option 2", callback_data="option2")

# Create a row of buttons
row = Button.row(button1, button2)
```

```{note}
The `Button` class is an abstract base class that shouldn't be instantiated directly. Use `InlineButton` or `KeyboardButton` instead, or the static methods provided by the `Button` class.
```

## Static Methods

### create_inline

```python
@staticmethod
def create_inline(
    text: str,
    callback_data: Optional[str] = None,
    url: Optional[str] = None,
    switch_inline_query: Optional[str] = None,
    switch_inline_query_current_chat: Optional[str] = None,
    pay: Optional[bool] = None,
) -> 'InlineButton':
    """
    Create an inline button.
    
    Args:
        text: Button text
        callback_data: Data to be sent in a callback query when button is pressed
        url: HTTP or tg:// URL to be opened when button is pressed
        switch_inline_query: Parameter for inline query to switch to
        switch_inline_query_current_chat: Parameter for inline query in current chat
        pay: Specify True if this is a Pay button
        
    Returns:
        An InlineButton instance
    """
```

Creates an inline button for use in inline keyboards.

**Parameters:**
- **text** (`str`): Button text
- **callback_data** (`Optional[str]`): Data to be sent in a callback query when button is pressed
- **url** (`Optional[str]`): HTTP or tg:// URL to be opened when button is pressed
- **switch_inline_query** (`Optional[str]`): Parameter for inline query to switch to
- **switch_inline_query_current_chat** (`Optional[str]`): Parameter for inline query in current chat
- **pay** (`Optional[bool]`): Specify True if this is a Pay button

**Returns:**
- `InlineButton`: An InlineButton instance

### create_keyboard

```python
@staticmethod
def create_keyboard(
    text: str,
    request_contact: Optional[bool] = None,
    request_location: Optional[bool] = None,
    request_poll: Optional[Dict[str, Any]] = None,
) -> 'KeyboardButton':
    """
    Create a keyboard button.
    
    Args:
        text: Button text
        request_contact: Specify True to request user's phone number
        request_location: Specify True to request user's location
        request_poll: Specify poll type to create a poll
        
    Returns:
        A KeyboardButton instance
    """
```

Creates a keyboard button for use in reply keyboards.

**Parameters:**
- **text** (`str`): Button text
- **request_contact** (`Optional[bool]`): Specify True to request user's phone number
- **request_location** (`Optional[bool]`): Specify True to request user's location
- **request_poll** (`Optional[Dict[str, Any]]`): Specify poll type to create a poll

**Returns:**
- `KeyboardButton`: A KeyboardButton instance

### row

```python
@staticmethod
def row(*buttons: Union['InlineButton', 'KeyboardButton']) -> List[Union['InlineButton', 'KeyboardButton']]:
    """
    Create a row of buttons.
    
    Args:
        *buttons: Buttons to include in the row
        
    Returns:
        A list of buttons representing a row
    """
```

Creates a row of buttons for use in keyboards.

**Parameters:**
- ***buttons** (`Union['InlineButton', 'KeyboardButton']`): Buttons to include in the row

**Returns:**
- `List[Union['InlineButton', 'KeyboardButton']]`: A list of buttons representing a row

## Examples

### Creating Inline Buttons

```python
from gpgram import Button, SimpleBot, Handler

async def main():
    # Create a bot instance
    bot = SimpleBot(token="YOUR_BOT_TOKEN")
    
    # Create a handler
    handler = Handler(bot=bot)
    
    @handler.command("buttons")
    async def buttons_command(message, bot):
        # Create inline buttons
        button1 = Button.create_inline(text="Option 1", callback_data="option1")
        button2 = Button.create_inline(text="Option 2", callback_data="option2")
        button3 = Button.create_inline(text="Visit Website", url="https://example.com")
        
        # Create rows of buttons
        row1 = Button.row(button1, button2)
        row2 = Button.row(button3)
        
        # Create a keyboard with the buttons
        from gpgram.common.button import InlineKeyboard
        keyboard = InlineKeyboard()
        keyboard.add_row(row1)
        keyboard.add_row(row2)
        
        # Send a message with the keyboard
        await message.reply(
            bot=bot,
            text="Here are some buttons:",
            reply_markup=keyboard
        )
    
    # Start polling
    await handler.start_polling()
```

### Creating Keyboard Buttons

```python
from gpgram import Button, SimpleBot, Handler

async def main():
    # Create a bot instance
    bot = SimpleBot(token="YOUR_BOT_TOKEN")
    
    # Create a handler
    handler = Handler(bot=bot)
    
    @handler.command("keyboard")
    async def keyboard_command(message, bot):
        # Create keyboard buttons
        button1 = Button.create_keyboard(text="Send my contact", request_contact=True)
        button2 = Button.create_keyboard(text="Send my location", request_location=True)
        button3 = Button.create_keyboard(text="Regular button")
        
        # Create rows of buttons
        row1 = Button.row(button1, button2)
        row2 = Button.row(button3)
        
        # Create a keyboard with the buttons
        from gpgram.common.button import ReplyKeyboard
        keyboard = ReplyKeyboard(resize_keyboard=True)
        keyboard.add_row(row1)
        keyboard.add_row(row2)
        
        # Send a message with the keyboard
        await message.reply(
            bot=bot,
            text="Here's a keyboard:",
            reply_markup=keyboard
        )
    
    # Start polling
    await handler.start_polling()
```

## See Also

- [InlineButton](inline-button.md) - Represents an inline keyboard button
- [KeyboardButton](keyboard-button.md) - Represents a keyboard button
- [InlineKeyboardBuilder](inline-keyboard-builder.md) - Builds inline keyboards
- [ReplyKeyboardBuilder](reply-keyboard-builder.md) - Builds reply keyboards
