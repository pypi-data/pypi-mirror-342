"""
Keyboard builders for Telegram Bot API.
"""

from typing import Dict, List, Optional, Union, Any

class InlineKeyboardBuilder:
    """
    Builder for inline keyboards.
    
    This class provides a convenient way to build inline keyboards.
    """
    
    def __init__(self):
        """Initialize the builder."""
        self.keyboard: List[List[Dict[str, Any]]] = []
    
    def add(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        pay: Optional[bool] = None,
        login_url: Optional[Dict[str, Any]] = None,
        web_app: Optional[Dict[str, Any]] = None,
        row: Optional[int] = None,
    ) -> 'InlineKeyboardBuilder':
        """
        Add a button to the keyboard.
        
        Args:
            text: Text of the button
            callback_data: Data to be sent in a callback query to the bot when button is pressed
            url: HTTP or tg:// url to be opened when button is pressed
            switch_inline_query: If set, pressing the button will prompt the user to select one of their chats
            switch_inline_query_current_chat: If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field
            pay: Specify True, to send a Pay button
            login_url: An HTTP URL used to automatically authorize the user
            web_app: Description of the Web App that will be launched when the user presses the button
            row: Row to add the button to (0-indexed)
        
        Returns:
            The builder instance for chaining
        """
        button = {'text': text}
        
        if callback_data is not None:
            button['callback_data'] = callback_data
        elif url is not None:
            button['url'] = url
        elif switch_inline_query is not None:
            button['switch_inline_query'] = switch_inline_query
        elif switch_inline_query_current_chat is not None:
            button['switch_inline_query_current_chat'] = switch_inline_query_current_chat
        elif pay is not None:
            button['pay'] = pay
        elif login_url is not None:
            button['login_url'] = login_url
        elif web_app is not None:
            button['web_app'] = web_app
        
        # Add the button to the specified row or create a new row
        if row is not None:
            # Ensure the row exists
            while len(self.keyboard) <= row:
                self.keyboard.append([])
            
            self.keyboard[row].append(button)
        else:
            # Add to the last row or create a new row
            if not self.keyboard:
                self.keyboard.append([])
            
            self.keyboard[-1].append(button)
        
        return self
    
    def row(self) -> 'InlineKeyboardBuilder':
        """
        Add a new row to the keyboard.
        
        Returns:
            The builder instance for chaining
        """
        self.keyboard.append([])
        return self
    
    def build(self) -> Dict[str, List[List[Dict[str, Any]]]]:
        """
        Build the keyboard.
        
        Returns:
            The keyboard as a dictionary
        """
        # Remove empty rows
        keyboard = [row for row in self.keyboard if row]
        
        return {'inline_keyboard': keyboard}


class ReplyKeyboardBuilder:
    """
    Builder for reply keyboards.
    
    This class provides a convenient way to build reply keyboards.
    """
    
    def __init__(
        self,
        resize_keyboard: bool = False,
        one_time_keyboard: bool = False,
        input_field_placeholder: Optional[str] = None,
        selective: bool = False,
        is_persistent: bool = False,
    ):
        """
        Initialize the builder.
        
        Args:
            resize_keyboard: Requests clients to resize the keyboard vertically for optimal fit
            one_time_keyboard: Requests clients to hide the keyboard as soon as it's been used
            input_field_placeholder: The placeholder to be shown in the input field when the keyboard is active
            selective: Use this parameter if you want to show the keyboard to specific users only
            is_persistent: Requests clients to always show the keyboard when the regular keyboard is hidden
        """
        self.keyboard: List[List[Dict[str, Any]]] = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective
        self.is_persistent = is_persistent
    
    def add(
        self,
        text: str,
        request_contact: bool = False,
        request_location: bool = False,
        request_poll: Optional[Dict[str, Any]] = None,
        request_user: Optional[Dict[str, Any]] = None,
        request_chat: Optional[Dict[str, Any]] = None,
        web_app: Optional[Dict[str, Any]] = None,
        row: Optional[int] = None,
    ) -> 'ReplyKeyboardBuilder':
        """
        Add a button to the keyboard.
        
        Args:
            text: Text of the button
            request_contact: If True, the user's phone number will be sent as a contact when the button is pressed
            request_location: If True, the user's current location will be sent when the button is pressed
            request_poll: If specified, the user will be asked to create a poll and send it when the button is pressed
            request_user: If specified, the user will be asked to select a user from their contacts and that user will be sent when the button is pressed
            request_chat: If specified, the user will be asked to select a chat from their chats and that chat will be sent when the button is pressed
            web_app: If specified, the described Web App will be launched when the button is pressed
            row: Row to add the button to (0-indexed)
        
        Returns:
            The builder instance for chaining
        """
        button = {'text': text}
        
        if request_contact:
            button['request_contact'] = True
        elif request_location:
            button['request_location'] = True
        elif request_poll is not None:
            button['request_poll'] = request_poll
        elif request_user is not None:
            button['request_user'] = request_user
        elif request_chat is not None:
            button['request_chat'] = request_chat
        elif web_app is not None:
            button['web_app'] = web_app
        
        # Add the button to the specified row or create a new row
        if row is not None:
            # Ensure the row exists
            while len(self.keyboard) <= row:
                self.keyboard.append([])
            
            self.keyboard[row].append(button)
        else:
            # Add to the last row or create a new row
            if not self.keyboard:
                self.keyboard.append([])
            
            self.keyboard[-1].append(button)
        
        return self
    
    def row(self) -> 'ReplyKeyboardBuilder':
        """
        Add a new row to the keyboard.
        
        Returns:
            The builder instance for chaining
        """
        self.keyboard.append([])
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Build the keyboard.
        
        Returns:
            The keyboard as a dictionary
        """
        # Remove empty rows
        keyboard = [row for row in self.keyboard if row]
        
        result = {'keyboard': keyboard}
        
        if self.resize_keyboard:
            result['resize_keyboard'] = True
        
        if self.one_time_keyboard:
            result['one_time_keyboard'] = True
        
        if self.input_field_placeholder:
            result['input_field_placeholder'] = self.input_field_placeholder
        
        if self.selective:
            result['selective'] = True
        
        if self.is_persistent:
            result['is_persistent'] = True
        
        return result
