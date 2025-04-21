"""
Base class for Telegram API types.
"""

from typing import Any, Dict, List, Optional, TypeVar, Type, ClassVar, get_type_hints
from pydantic import BaseModel

T = TypeVar('T', bound='TelegramObject')

class TelegramObject(BaseModel):
    """
    Base class for all Telegram API types.

    This class provides methods for converting between Python objects and
    JSON-serializable dictionaries.
    """

    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "allow"
    }

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create an instance of the class from a dictionary.

        Args:
            data: Dictionary containing the object's data

        Returns:
            An instance of the class
        """
        if data is None:
            return None

        return cls.model_validate(data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary.

        Returns:
            Dictionary representation of the object
        """
        return self.model_dump(exclude_none=True)
