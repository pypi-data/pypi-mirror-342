from typing import Type, TypeVar, Dict, Any

from .topics import MessageTopic
from ..domain.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class TwitterGetUserRequestMessage(HaiMessage):
    """Message to request Twitter user information"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, username: str) -> 'TwitterGetUserRequestMessage':
        """Create a message requesting Twitter user data"""
        return cls.create(
            topic=MessageTopic.AI_TWITTER_GET_USER,
            payload={"username": username},
        )

    @property
    def username(self) -> str:
        """Get the username from the payload"""
        return self.payload.get("username", "")
