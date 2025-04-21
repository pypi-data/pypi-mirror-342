# Invoice

The `Invoice` class represents an invoice for payment in Telegram. It contains information about the payment, such as title, description, currency, and total amount.

## Overview

The `Invoice` class is a Pydantic model that represents an invoice for payment in Telegram. It contains information about the payment, such as title, description, currency, and total amount.

```python
from gpgram.types.payments import Invoice

# Access an invoice from a message
invoice = message.invoice

# Access invoice properties
title = invoice.title
description = invoice.description
currency = invoice.currency
total_amount = invoice.total_amount
```

```{note}
The `Invoice` class is a Pydantic model that validates and converts the raw JSON data from Telegram into a Python object with proper types.
```

```{warning}
To use payments in your bot, you need to enable payments with BotFather and set up a payment provider. See the [Telegram Payments API](https://core.telegram.org/bots/payments) for more information.
```

## Properties

The `Invoice` class has the following properties:

- **title** (`str`): Product name
- **description** (`str`): Product description
- **start_parameter** (`str`): Unique bot deep-linking parameter that can be used to generate this invoice
- **currency** (`str`): Three-letter ISO 4217 currency code
- **total_amount** (`int`): Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

## Methods

### from_dict

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Invoice':
    """
    Create an Invoice from a dictionary.
    
    Args:
        data: Dictionary representation of the invoice
        
    Returns:
        An Invoice instance
    """
```

Creates an `Invoice` instance from a dictionary representation of an invoice.

**Parameters:**
- **data** (`Dict[str, Any]`): Dictionary representation of the invoice

**Returns:**
- `Invoice`: An Invoice instance

### to_dict

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Convert the invoice to a dictionary.
    
    Returns:
        Dictionary representation of the invoice
    """
```

Converts the `Invoice` instance to a dictionary representation.

**Returns:**
- `Dict[str, Any]`: Dictionary representation of the invoice

## Creating and Sending Invoices

To create and send an invoice, you need to use the `send_invoice` method of the `Bot` class. Here's an example:

```python
@router.message(CommandFilter('buy'))
async def buy_command(message, bot):
    # Create labeled prices
    prices = [
        {
            "label": "Product",
            "amount": 1000  # $10.00
        },
        {
            "label": "Tax",
            "amount": 200   # $2.00
        }
    ]
    
    # Send an invoice
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Product Title",
        description="Product Description",
        payload="unique_payment_payload",
        provider_token="YOUR_PAYMENT_PROVIDER_TOKEN",
        currency="USD",
        prices=prices,
        # Optional parameters
        photo_url="https://example.com/product.jpg",
        photo_width=600,
        photo_height=400,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,  # If you want to offer different shipping options
        disable_notification=False,
        reply_to_message_id=None,
        reply_markup=None
    )
```

## Handling Payment Callbacks

When a user makes a payment, Telegram sends several updates to your bot. You need to handle these updates to complete the payment process:

```python
# Handle pre-checkout queries
@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query, bot):
    # Here you can check if the order is still valid
    # If everything is okay, answer the pre-checkout query
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True
    )
    
    # If there's a problem, you can reject the payment
    # await bot.answer_pre_checkout_query(
    #     pre_checkout_query_id=pre_checkout_query.id,
    #     ok=False,
    #     error_message="Payment cannot be completed at this time."
    # )

# Handle successful payments
@router.message(lambda message: message.successful_payment is not None)
async def successful_payment_handler(message, bot):
    # Payment was successful, you can now fulfill the order
    payment = message.successful_payment
    
    # Log the payment
    logging.info(f"Payment for {payment.total_amount / 100} {payment.currency} received from {message.from_user.id}")
    
    # Thank the user
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Thank you for your payment of {payment.total_amount / 100} {payment.currency}!\n"
             f"We've received your order and will process it shortly."
    )
```

## Shipping Options

If you set `is_flexible=True` when sending an invoice, you need to handle shipping queries to provide shipping options:

```python
# Handle shipping queries
@router.shipping_query()
async def shipping_query_handler(shipping_query, bot):
    # Provide shipping options based on the shipping address
    shipping_options = [
        {
            "id": "standard",
            "title": "Standard Shipping",
            "prices": [
                {
                    "label": "Standard Shipping",
                    "amount": 500  # $5.00
                }
            ]
        },
        {
            "id": "express",
            "title": "Express Shipping",
            "prices": [
                {
                    "label": "Express Shipping",
                    "amount": 1000  # $10.00
                }
            ]
        }
    ]
    
    # Answer the shipping query
    await bot.answer_shipping_query(
        shipping_query_id=shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )
    
    # If shipping to the specified address is not possible
    # await bot.answer_shipping_query(
    #     shipping_query_id=shipping_query.id,
    #     ok=False,
    #     error_message="Sorry, we can't ship to your address."
    # )
```

## See Also

- [LabeledPrice](labeled-price.md) - Represents a portion of the price for goods or services
- [ShippingOption](shipping-option.md) - Represents a shipping option
- [SuccessfulPayment](successful-payment.md) - Represents a successful payment
- [Telegram Payments API](https://core.telegram.org/bots/payments) - Official documentation for Telegram Payments
