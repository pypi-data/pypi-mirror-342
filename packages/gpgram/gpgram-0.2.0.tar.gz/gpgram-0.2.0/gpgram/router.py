"""
Router class for routing updates to handlers.
"""

import asyncio
import inspect
from typing import List, Optional, Dict, Any, Callable, Awaitable, Set, Union, Type, TypeVar

from .logging import get_logger

from .types.update import Update

T = TypeVar('T')

class Router:
    """
    Router class for routing updates to handlers.

    This class is responsible for routing updates to the appropriate handlers
    based on filters and other criteria.
    """

    def __init__(self, name: Optional[str] = None):
        """
        Initialize the Router.

        Args:
            name: Name of the router
        """
        self.name = name or self.__class__.__name__
        self.logger = get_logger(__name__)
        self._handlers: List[Dict[str, Any]] = []
        self._routers: List[Router] = []
        self._parent: Optional[Router] = None

    def include_router(self, router: 'Router') -> None:
        """
        Include another router as a sub-router.

        Args:
            router: Router to include
        """
        router._parent = self
        self._routers.append(router)

    def message(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a message handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_message_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def callback_query(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a callback query handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_callback_query_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def inline_query(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register an inline query handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_inline_query_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def chosen_inline_result(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a chosen inline result handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_chosen_inline_result_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def shipping_query(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a shipping query handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_shipping_query_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def pre_checkout_query(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a pre-checkout query handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_pre_checkout_query_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def poll(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a poll handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_poll_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def poll_answer(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a poll answer handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_poll_answer_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def chat_member(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a chat member handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_chat_member_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def my_chat_member(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a my chat member handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_my_chat_member_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def chat_join_request(
        self,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> Callable:
        """
        Register a chat join request handler.

        Args:
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler

        Returns:
            Decorator function
        """
        def decorator(callback: Callable) -> Callable:
            self.register_chat_join_request_handler(callback, filters, *args, **kwargs)
            return callback

        return decorator

    def register_message_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a message handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'message',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_callback_query_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a callback query handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'callback_query',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_inline_query_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register an inline query handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'inline_query',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_chosen_inline_result_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a chosen inline result handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'chosen_inline_result',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_shipping_query_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a shipping query handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'shipping_query',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_pre_checkout_query_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a pre-checkout query handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'pre_checkout_query',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_poll_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a poll handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'poll',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_poll_answer_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a poll answer handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'poll_answer',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_chat_member_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a chat member handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'chat_member',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_my_chat_member_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a my chat member handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'my_chat_member',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    def register_chat_join_request_handler(
        self,
        callback: Callable,
        filters: Optional[Union[Callable, List[Callable]]] = None,
        *args,
        **kwargs
    ) -> None:
        """
        Register a chat join request handler.

        Args:
            callback: Handler callback function
            filters: Filters to apply to the handler
            *args: Additional arguments to pass to the handler
            **kwargs: Additional keyword arguments to pass to the handler
        """
        self._handlers.append({
            'type': 'chat_join_request',
            'callback': callback,
            'filters': filters,
            'args': args,
            'kwargs': kwargs,
        })

    async def dispatch(self, update: Update, bot: 'Bot') -> bool:
        """
        Dispatch an update to the appropriate handlers.

        Args:
            update: Update to dispatch
            bot: Bot instance

        Returns:
            True if the update was handled, False otherwise
        """
        # Try to handle the update with this router's handlers
        if await self._process_update(update, bot):
            return True

        # Try to handle the update with sub-routers
        for router in self._routers:
            if await router.dispatch(update, bot):
                return True

        return False

    async def _process_update(self, update: Update, bot: 'Bot') -> bool:
        """
        Process an update with this router's handlers.

        Args:
            update: Update to process
            bot: Bot instance

        Returns:
            True if the update was handled, False otherwise
        """
        # Determine the update type
        update_type = self._get_update_type(update)

        if not update_type:
            return False

        # Find matching handlers
        matching_handlers = [
            handler for handler in self._handlers
            if handler['type'] == update_type and await self._check_filters(handler, update)
        ]

        # Process matching handlers
        for handler in matching_handlers:
            try:
                # Get the handler callback
                callback = handler['callback']

                # Prepare arguments for the callback
                args = list(handler['args'])
                kwargs = dict(handler['kwargs'])

                # Add update and bot to kwargs if they are expected by the callback
                signature = inspect.signature(callback)
                parameters = signature.parameters

                if 'update' in parameters:
                    kwargs['update'] = update

                if 'bot' in parameters:
                    kwargs['bot'] = bot

                # Add the specific update object (message, callback_query, etc.) if expected
                update_obj = self._get_update_object(update, update_type)
                if update_obj:
                    for param_name, param in parameters.items():
                        if param_name not in kwargs and isinstance(update_obj, param.annotation):
                            kwargs[param_name] = update_obj
                        elif param_name not in kwargs and param_name == update_type:
                            kwargs[param_name] = update_obj

                # Call the handler
                result = callback(*args, **kwargs)

                # Handle coroutines
                if inspect.iscoroutine(result):
                    await result

                return True

            except Exception as e:
                self.logger.exception(f"Error in handler {handler['callback'].__name__}: {e}")

        return bool(matching_handlers)

    async def _check_filters(self, handler: Dict[str, Any], update: Update) -> bool:
        """
        Check if an update passes the handler's filters.

        Args:
            handler: Handler to check
            update: Update to check

        Returns:
            True if the update passes the filters, False otherwise
        """
        filters = handler.get('filters')

        if not filters:
            return True

        if not isinstance(filters, list):
            filters = [filters]

        for filter_func in filters:
            try:
                # Get the update object for the handler type
                update_obj = self._get_update_object(update, handler['type'])

                if not update_obj:
                    return False

                # Check if the filter is a coroutine function
                if asyncio.iscoroutinefunction(filter_func):
                    result = await filter_func(update_obj)
                else:
                    result = filter_func(update_obj)

                if not result:
                    return False

            except Exception as e:
                self.logger.exception(f"Error in filter {filter_func.__name__}: {e}")
                return False

        return True

    def _get_update_type(self, update: Update) -> Optional[str]:
        """
        Get the type of an update.

        Args:
            update: Update to get the type of

        Returns:
            Type of the update, or None if the update has no recognizable type
        """
        if update.message:
            return 'message'
        elif update.edited_message:
            return 'edited_message'
        elif update.channel_post:
            return 'channel_post'
        elif update.edited_channel_post:
            return 'edited_channel_post'
        elif update.callback_query:
            return 'callback_query'
        elif update.inline_query:
            return 'inline_query'
        elif update.chosen_inline_result:
            return 'chosen_inline_result'
        elif update.shipping_query:
            return 'shipping_query'
        elif update.pre_checkout_query:
            return 'pre_checkout_query'
        elif update.poll:
            return 'poll'
        elif update.poll_answer:
            return 'poll_answer'
        elif update.my_chat_member:
            return 'my_chat_member'
        elif update.chat_member:
            return 'chat_member'
        elif update.chat_join_request:
            return 'chat_join_request'

        return None

    def _get_update_object(self, update: Update, update_type: str) -> Optional[Any]:
        """
        Get the object from an update based on its type.

        Args:
            update: Update to get the object from
            update_type: Type of the update

        Returns:
            The object from the update, or None if the update has no object of the specified type
        """
        if update_type == 'message':
            return update.message
        elif update_type == 'edited_message':
            return update.edited_message
        elif update_type == 'channel_post':
            return update.channel_post
        elif update_type == 'edited_channel_post':
            return update.edited_channel_post
        elif update_type == 'callback_query':
            return update.callback_query
        elif update_type == 'inline_query':
            return update.inline_query
        elif update_type == 'chosen_inline_result':
            return update.chosen_inline_result
        elif update_type == 'shipping_query':
            return update.shipping_query
        elif update_type == 'pre_checkout_query':
            return update.pre_checkout_query
        elif update_type == 'poll':
            return update.poll
        elif update_type == 'poll_answer':
            return update.poll_answer
        elif update_type == 'my_chat_member':
            return update.my_chat_member
        elif update_type == 'chat_member':
            return update.chat_member
        elif update_type == 'chat_join_request':
            return update.chat_join_request

        return None
