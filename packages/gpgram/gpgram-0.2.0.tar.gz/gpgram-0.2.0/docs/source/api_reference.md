# API Reference

```{toctree}
:maxdepth: 2
:caption: API Reference

api/core
api/types
api/filters
api/utils
api/simplified
api/advanced
api/payments
```

This section provides detailed documentation for all the classes and methods in Gpgram.

## Core Components

The core components of Gpgram are:

- [Bot](api/bot.md) - The main interface to the Telegram Bot API
- [Dispatcher](api/dispatcher.md) - Manages the routing of updates to the appropriate handlers
- [Router](api/router.md) - Organizes handlers for different types of updates

## Types

Gpgram provides Pydantic models for Telegram API types:

- [Update](api/update.md) - Represents an incoming update from Telegram
- [Message](api/message.md) - Represents a message in Telegram
- [User](api/user.md) - Represents a Telegram user or bot
- [Chat](api/chat.md) - Represents a chat in Telegram
- [CallbackQuery](api/callback-query.md) - Represents a callback query from an inline keyboard

## Filters

Filters are used to determine whether a handler should process an update:

- [CommandFilter](api/command-filter.md) - Filters messages by command
- [TextFilter](api/text-filter.md) - Filters messages by text content
- [RegexFilter](api/regex-filter.md) - Filters messages by regular expression pattern
- [ContentTypeFilter](api/content-type-filter.md) - Filters messages by content type
- [ChatTypeFilter](api/chat-type-filter.md) - Filters messages by chat type

## Utilities

Gpgram provides utilities for common tasks:

- [InlineKeyboardBuilder](api/inline-keyboard-builder.md) - Builds inline keyboards for messages
- [ReplyKeyboardBuilder](api/reply-keyboard-builder.md) - Builds reply keyboards for messages

## Simplified Interfaces

Gpgram provides simplified interfaces for common tasks:

- [SimpleBot](api/simple-bot.md) - A simplified interface for the Bot class
- [SimpleMessage](api/simple-message.md) - A simplified interface for the Message class
- [Handler](api/handler.md) - A simplified interface for handling updates
- [Button](api/button.md) - Base class for all button types
- [InlineButton](api/inline-button.md) - Represents an inline keyboard button
- [KeyboardButton](api/keyboard-button.md) - Represents a keyboard button

## Advanced Features

Gpgram provides advanced features for more complex bots:

- [Middleware](api/middleware.md) - Middleware for pre and post-processing updates
- [Logging](api/logging.md) - Advanced logging with Loguru
- [Error Handling](api/error-handling.md) - Error handling in Gpgram

## Payments

Gpgram provides support for Telegram Payments:

- [Invoice](api/invoice.md) - Represents an invoice for payment
- [LabeledPrice](api/labeled-price.md) - Represents a portion of the price for goods or services
- [ShippingOption](api/shipping-option.md) - Represents a shipping option
- [SuccessfulPayment](api/successful-payment.md) - Represents a successful payment
