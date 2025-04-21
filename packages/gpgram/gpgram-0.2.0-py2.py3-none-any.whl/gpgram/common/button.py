"""
Button classes for Telegram Bot API.

This module provides simplified interfaces for creating buttons in Telegram bots.
"""

from typing import Optional, Union, Dict, Any, List

from ..utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Button:
    """
    Base class for all button types.
    
    This is an abstract base class that shouldn't be instantiated directly.
    Use InlineButton or KeyboardButton instead.
    """
    
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
        return InlineButton(
            text=text,
            callback_data=callback_data,
            url=url,
            switch_inline_query=switch_inline_query,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
            pay=pay,
        )
    
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
        return KeyboardButton(
            text=text,
            request_contact=request_contact,
            request_location=request_location,
            request_poll=request_poll,
        )
    
    @staticmethod
    def row(*buttons: Union['InlineButton', 'KeyboardButton']) -> List[Union['InlineButton', 'KeyboardButton']]:
        """
        Create a row of buttons.
        
        Args:
            *buttons: Buttons to include in the row
            
        Returns:
            A list of buttons representing a row
        """
        return list(buttons)


class InlineButton:
    """
    Inline button for Telegram Bot API.
    
    This class represents an inline keyboard button.
    """
    
    def __init__(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        pay: Optional[bool] = None,
    ):
        """
        Initialize an inline button.
        
        Args:
            text: Button text
            callback_data: Data to be sent in a callback query when button is pressed
            url: HTTP or tg:// URL to be opened when button is pressed
            switch_inline_query: Parameter for inline query to switch to
            switch_inline_query_current_chat: Parameter for inline query in current chat
            pay: Specify True if this is a Pay button
        """
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.pay = pay
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the button to a dictionary.
        
        Returns:
            Dictionary representation of the button
        """
        button_dict = {"text": self.text}
        
        if self.callback_data is not None:
            button_dict["callback_data"] = self.callback_data
        if self.url is not None:
            button_dict["url"] = self.url
        if self.switch_inline_query is not None:
            button_dict["switch_inline_query"] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            button_dict["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        if self.pay is not None:
            button_dict["pay"] = self.pay
        
        return button_dict


class KeyboardButton:
    """
    Keyboard button for Telegram Bot API.
    
    This class represents a keyboard button.
    """
    
    def __init__(
        self,
        text: str,
        request_contact: Optional[bool] = None,
        request_location: Optional[bool] = None,
        request_poll: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a keyboard button.
        
        Args:
            text: Button text
            request_contact: Specify True to request user's phone number
            request_location: Specify True to request user's location
            request_poll: Specify poll type to create a poll
        """
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the button to a dictionary.
        
        Returns:
            Dictionary representation of the button
        """
        button_dict = {"text": self.text}
        
        if self.request_contact is not None:
            button_dict["request_contact"] = self.request_contact
        if self.request_location is not None:
            button_dict["request_location"] = self.request_location
        if self.request_poll is not None:
            button_dict["request_poll"] = self.request_poll
        
        return button_dict


class InlineKeyboard:
    """
    Inline keyboard for Telegram Bot API.
    
    This class provides a simplified interface for creating inline keyboards.
    """
    
    def __init__(self, buttons: Optional[List[List[InlineButton]]] = None):
        """
        Initialize an inline keyboard.
        
        Args:
            buttons: List of button rows
        """
        self.buttons = buttons or []
        self._builder = InlineKeyboardBuilder()
    
    def add_button(self, button: InlineButton) -> 'InlineKeyboard':
        """
        Add a button to the current row.
        
        Args:
            button: Button to add
            
        Returns:
            Self for method chaining
        """
        self._builder.add_button(**button.to_dict())
        return self
    
    def row(self) -> 'InlineKeyboard':
        """
        Start a new row.
        
        Returns:
            Self for method chaining
        """
        self._builder.row()
        return self
    
    def add_row(self, buttons: List[InlineButton]) -> 'InlineKeyboard':
        """
        Add a row of buttons.
        
        Args:
            buttons: List of buttons to add as a row
            
        Returns:
            Self for method chaining
        """
        for button in buttons:
            self._builder.add_button(**button.to_dict())
        self._builder.row()
        return self
    
    def as_markup(self) -> Dict[str, Any]:
        """
        Get the keyboard as a markup dictionary.
        
        Returns:
            Markup dictionary for the keyboard
        """
        return self._builder.as_markup()


class ReplyKeyboard:
    """
    Reply keyboard for Telegram Bot API.
    
    This class provides a simplified interface for creating reply keyboards.
    """
    
    def __init__(
        self,
        buttons: Optional[List[List[KeyboardButton]]] = None,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
    ):
        """
        Initialize a reply keyboard.
        
        Args:
            buttons: List of button rows
            resize_keyboard: Requests clients to resize the keyboard
            one_time_keyboard: Requests clients to hide the keyboard after use
            selective: Use this parameter if you want to show the keyboard to specific users only
        """
        self.buttons = buttons or []
        self._builder = ReplyKeyboardBuilder(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
        )
    
    def add_button(self, button: KeyboardButton) -> 'ReplyKeyboard':
        """
        Add a button to the current row.
        
        Args:
            button: Button to add
            
        Returns:
            Self for method chaining
        """
        self._builder.add_button(**button.to_dict())
        return self
    
    def row(self) -> 'ReplyKeyboard':
        """
        Start a new row.
        
        Returns:
            Self for method chaining
        """
        self._builder.row()
        return self
    
    def add_row(self, buttons: List[KeyboardButton]) -> 'ReplyKeyboard':
        """
        Add a row of buttons.
        
        Args:
            buttons: List of buttons to add as a row
            
        Returns:
            Self for method chaining
        """
        for button in buttons:
            self._builder.add_button(**button.to_dict())
        self._builder.row()
        return self
    
    def as_markup(self) -> Dict[str, Any]:
        """
        Get the keyboard as a markup dictionary.
        
        Returns:
            Markup dictionary for the keyboard
        """
        return self._builder.as_markup()
