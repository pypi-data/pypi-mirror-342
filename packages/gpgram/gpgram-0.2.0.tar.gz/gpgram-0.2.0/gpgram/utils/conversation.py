"""
Conversation state management for Gpgram.

This module provides utilities for managing conversation states in Telegram bots.
"""

import asyncio
import time
from typing import Dict, Any, Optional, Callable, Awaitable, Union, Set
from dataclasses import dataclass, field

from ..logging import get_logger

logger = get_logger(__name__)


@dataclass
class ConversationState:
    """
    Represents the state of a conversation.
    
    Attributes:
        state: Current state of the conversation
        data: Additional data associated with the conversation
        created_at: Timestamp when the conversation was created
        updated_at: Timestamp when the conversation was last updated
        ttl: Time-to-live in seconds (0 means no expiration)
    """
    state: Any
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    ttl: int = 0  # Time-to-live in seconds (0 means no expiration)


class ConversationManager:
    """
    Manages conversation states for users.
    
    This class provides methods for storing, retrieving, and updating conversation states.
    """
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize the ConversationManager.
        
        Args:
            default_ttl: Default time-to-live in seconds for conversation states
        """
        self._states: Dict[str, ConversationState] = {}
        self._default_ttl = default_ttl
        self._cleanup_task = None
    
    def start_cleanup(self, interval: int = 300):
        """
        Start the cleanup task to remove expired states.
        
        Args:
            interval: Cleanup interval in seconds
        """
        if self._cleanup_task is not None:
            self._cleanup_task.cancel()
        
        self._cleanup_task = asyncio.create_task(self._cleanup_loop(interval))
    
    async def _cleanup_loop(self, interval: int):
        """
        Periodically clean up expired states.
        
        Args:
            interval: Cleanup interval in seconds
        """
        while True:
            try:
                self._cleanup_expired()
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Error in cleanup loop: {e}")
                await asyncio.sleep(interval)
    
    def _cleanup_expired(self):
        """Remove expired states."""
        now = time.time()
        expired_keys = []
        
        for key, state in self._states.items():
            if state.ttl > 0 and now - state.updated_at > state.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._states[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired conversation states")
    
    def _get_key(self, chat_id: int, user_id: Optional[int] = None) -> str:
        """
        Get the key for storing a conversation state.
        
        Args:
            chat_id: Chat ID
            user_id: User ID (if None, only chat_id is used)
        
        Returns:
            Key for storing the conversation state
        """
        if user_id is not None:
            return f"{chat_id}:{user_id}"
        return str(chat_id)
    
    def get_state(self, chat_id: int, user_id: Optional[int] = None) -> Optional[Any]:
        """
        Get the current state of a conversation.
        
        Args:
            chat_id: Chat ID
            user_id: User ID (if None, only chat_id is used)
        
        Returns:
            Current state of the conversation, or None if no state exists
        """
        key = self._get_key(chat_id, user_id)
        state_obj = self._states.get(key)
        
        if state_obj is None:
            return None
        
        # Check if the state has expired
        if state_obj.ttl > 0 and time.time() - state_obj.updated_at > state_obj.ttl:
            del self._states[key]
            return None
        
        return state_obj.state
    
    def set_state(
        self,
        chat_id: int,
        state: Any,
        user_id: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
    ) -> None:
        """
        Set the state of a conversation.
        
        Args:
            chat_id: Chat ID
            state: New state
            user_id: User ID (if None, only chat_id is used)
            data: Additional data to store with the state
            ttl: Time-to-live in seconds (if None, default_ttl is used)
        """
        key = self._get_key(chat_id, user_id)
        now = time.time()
        
        # Get existing state or create a new one
        state_obj = self._states.get(key)
        if state_obj is None:
            state_obj = ConversationState(
                state=state,
                data=data or {},
                created_at=now,
                updated_at=now,
                ttl=ttl if ttl is not None else self._default_ttl,
            )
        else:
            state_obj.state = state
            state_obj.updated_at = now
            if data is not None:
                state_obj.data = data
            if ttl is not None:
                state_obj.ttl = ttl
        
        self._states[key] = state_obj
    
    def update_data(
        self,
        chat_id: int,
        user_id: Optional[int] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> bool:
        """
        Update the data associated with a conversation state.
        
        Args:
            chat_id: Chat ID
            user_id: User ID (if None, only chat_id is used)
            data: Dictionary of data to update
            **kwargs: Additional key-value pairs to update
        
        Returns:
            True if the state was updated, False if no state exists
        """
        key = self._get_key(chat_id, user_id)
        state_obj = self._states.get(key)
        
        if state_obj is None:
            return False
        
        # Check if the state has expired
        if state_obj.ttl > 0 and time.time() - state_obj.updated_at > state_obj.ttl:
            del self._states[key]
            return False
        
        # Update the data
        if data:
            state_obj.data.update(data)
        
        if kwargs:
            state_obj.data.update(kwargs)
        
        state_obj.updated_at = time.time()
        return True
    
    def get_data(
        self,
        chat_id: int,
        user_id: Optional[int] = None,
        key: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """
        Get the data associated with a conversation state.
        
        Args:
            chat_id: Chat ID
            user_id: User ID (if None, only chat_id is used)
            key: Key to get from the data (if None, all data is returned)
            default: Default value to return if the key doesn't exist
        
        Returns:
            Data associated with the conversation state
        """
        state_key = self._get_key(chat_id, user_id)
        state_obj = self._states.get(state_key)
        
        if state_obj is None:
            return {} if key is None else default
        
        # Check if the state has expired
        if state_obj.ttl > 0 and time.time() - state_obj.updated_at > state_obj.ttl:
            del self._states[state_key]
            return {} if key is None else default
        
        if key is None:
            return state_obj.data
        
        return state_obj.data.get(key, default)
    
    def clear_state(self, chat_id: int, user_id: Optional[int] = None) -> bool:
        """
        Clear the state of a conversation.
        
        Args:
            chat_id: Chat ID
            user_id: User ID (if None, only chat_id is used)
        
        Returns:
            True if the state was cleared, False if no state exists
        """
        key = self._get_key(chat_id, user_id)
        if key in self._states:
            del self._states[key]
            return True
        return False
    
    def get_all_states(self) -> Dict[str, Any]:
        """
        Get all conversation states.
        
        Returns:
            Dictionary mapping keys to states
        """
        return {key: state.state for key, state in self._states.items()}
    
    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all conversation data.
        
        Returns:
            Dictionary mapping keys to data
        """
        return {key: state.data for key, state in self._states.items()}
    
    def clear_all(self) -> None:
        """Clear all conversation states."""
        self._states.clear()


# Global conversation manager instance
conversation_manager = ConversationManager()


def get_conversation_manager() -> ConversationManager:
    """
    Get the global conversation manager instance.
    
    Returns:
        Global conversation manager instance
    """
    return conversation_manager


class ConversationHandler:
    """
    Handler for managing conversations with users.
    
    This class provides a way to define conversation flows with states and transitions.
    """
    
    def __init__(
        self,
        entry_points: Dict[str, Callable],
        states: Dict[Any, Dict[str, Callable]],
        fallbacks: Dict[str, Callable] = None,
        conversation_timeout: int = 3600,
        name: Optional[str] = None,
    ):
        """
        Initialize the ConversationHandler.
        
        Args:
            entry_points: Dictionary mapping command names to handler functions
            states: Dictionary mapping states to dictionaries of command/handler pairs
            fallbacks: Dictionary mapping command names to fallback handler functions
            conversation_timeout: Timeout for conversations in seconds
            name: Name of the handler
        """
        self.entry_points = entry_points
        self.states = states
        self.fallbacks = fallbacks or {}
        self.conversation_timeout = conversation_timeout
        self.name = name or self.__class__.__name__
        self.manager = get_conversation_manager()
    
    async def handle_update(self, update, bot):
        """
        Handle an update in the context of a conversation.
        
        Args:
            update: Update to handle
            bot: Bot instance
        
        Returns:
            True if the update was handled, False otherwise
        """
        # Extract chat_id and user_id from the update
        chat_id = None
        user_id = None
        command = None
        
        if hasattr(update, 'message') and update.message:
            chat_id = update.message.chat.id
            user_id = update.message.from_user.id if update.message.from_user else None
            
            # Extract command if present
            if update.message.text and update.message.text.startswith('/'):
                command = update.message.text.split()[0][1:].split('@')[0]
        
        elif hasattr(update, 'callback_query') and update.callback_query:
            if update.callback_query.message:
                chat_id = update.callback_query.message.chat.id
            user_id = update.callback_query.from_user.id if update.callback_query.from_user else None
        
        if chat_id is None:
            return False
        
        # Get current state
        current_state = self.manager.get_state(chat_id, user_id)
        
        # Handle entry points if no state
        if current_state is None:
            if command and command in self.entry_points:
                handler = self.entry_points[command]
                next_state = await handler(update, bot)
                
                if next_state is not None:
                    self.manager.set_state(
                        chat_id, next_state, user_id, ttl=self.conversation_timeout
                    )
                
                return True
            
            return False
        
        # Handle state transitions
        if current_state in self.states:
            state_handlers = self.states[current_state]
            
            # Try to find a matching handler
            handler = None
            
            if command and command in state_handlers:
                handler = state_handlers[command]
            elif '' in state_handlers:  # Default handler for the state
                handler = state_handlers['']
            
            if handler:
                next_state = await handler(update, bot)
                
                if next_state is None:
                    # End the conversation
                    self.manager.clear_state(chat_id, user_id)
                else:
                    # Update the state
                    self.manager.set_state(
                        chat_id, next_state, user_id, ttl=self.conversation_timeout
                    )
                
                return True
        
        # Try fallbacks
        if command and command in self.fallbacks:
            handler = self.fallbacks[command]
            next_state = await handler(update, bot)
            
            if next_state is None:
                # End the conversation
                self.manager.clear_state(chat_id, user_id)
            else:
                # Update the state
                self.manager.set_state(
                    chat_id, next_state, user_id, ttl=self.conversation_timeout
                )
            
            return True
        
        return False
