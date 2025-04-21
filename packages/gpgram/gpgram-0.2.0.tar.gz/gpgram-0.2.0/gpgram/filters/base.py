"""
Base filter class for Telegram Bot API.
"""

from typing import Any, Callable, ClassVar, Dict, List, Optional, Set, Type, Union

class BaseFilter:
    """
    Base class for all filters.
    
    This class provides the basic functionality for filters.
    """
    
    def __init__(self):
        """Initialize the filter."""
        pass
    
    def __call__(self, update_obj: Any) -> bool:
        """
        Check if the update object passes the filter.
        
        Args:
            update_obj: Update object to check
        
        Returns:
            True if the update object passes the filter, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def __and__(self, other: Union['BaseFilter', Callable]) -> 'AndFilter':
        """
        Combine this filter with another filter using logical AND.
        
        Args:
            other: Other filter to combine with
        
        Returns:
            Combined filter
        """
        return AndFilter(self, other)
    
    def __or__(self, other: Union['BaseFilter', Callable]) -> 'OrFilter':
        """
        Combine this filter with another filter using logical OR.
        
        Args:
            other: Other filter to combine with
        
        Returns:
            Combined filter
        """
        return OrFilter(self, other)
    
    def __invert__(self) -> 'NotFilter':
        """
        Invert this filter.
        
        Returns:
            Inverted filter
        """
        return NotFilter(self)


class AndFilter(BaseFilter):
    """
    Filter that combines two filters using logical AND.
    
    This filter passes if both of the combined filters pass.
    """
    
    def __init__(self, filter1: Union[BaseFilter, Callable], filter2: Union[BaseFilter, Callable]):
        """
        Initialize the filter.
        
        Args:
            filter1: First filter to combine
            filter2: Second filter to combine
        """
        super().__init__()
        self.filter1 = filter1
        self.filter2 = filter2
    
    def __call__(self, update_obj: Any) -> bool:
        """
        Check if the update object passes the filter.
        
        Args:
            update_obj: Update object to check
        
        Returns:
            True if the update object passes both filters, False otherwise
        """
        return self.filter1(update_obj) and self.filter2(update_obj)


class OrFilter(BaseFilter):
    """
    Filter that combines two filters using logical OR.
    
    This filter passes if either of the combined filters pass.
    """
    
    def __init__(self, filter1: Union[BaseFilter, Callable], filter2: Union[BaseFilter, Callable]):
        """
        Initialize the filter.
        
        Args:
            filter1: First filter to combine
            filter2: Second filter to combine
        """
        super().__init__()
        self.filter1 = filter1
        self.filter2 = filter2
    
    def __call__(self, update_obj: Any) -> bool:
        """
        Check if the update object passes the filter.
        
        Args:
            update_obj: Update object to check
        
        Returns:
            True if the update object passes either filter, False otherwise
        """
        return self.filter1(update_obj) or self.filter2(update_obj)


class NotFilter(BaseFilter):
    """
    Filter that inverts another filter.
    
    This filter passes if the inverted filter does not pass.
    """
    
    def __init__(self, filter_to_invert: Union[BaseFilter, Callable]):
        """
        Initialize the filter.
        
        Args:
            filter_to_invert: Filter to invert
        """
        super().__init__()
        self.filter_to_invert = filter_to_invert
    
    def __call__(self, update_obj: Any) -> bool:
        """
        Check if the update object passes the filter.
        
        Args:
            update_obj: Update object to check
        
        Returns:
            True if the update object does not pass the inverted filter, False otherwise
        """
        return not self.filter_to_invert(update_obj)
