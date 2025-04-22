from typing import Type, TypeVar, Dict, Any, Optional

from ..models.request_message_topic import RequestMessageTopic
from ...domain.models.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')


class TelegramUserMessageRequestMessage(HaiMessage):
    """Message containing user message data"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, message: str, user_id: str, username: str,
                       source: str = "", replied_to_text: Optional[str] = None,
                       chat_id: Optional[int] = None,
                       message_id: Optional[int] = None) -> 'TelegramUserMessageRequestMessage':
        """Create a message with user message data

        Args:
            message: The cleaned message content
            user_id: The ID of the user
            username: The username of the user
            source: The source of the message
            replied_to_text: The text being replied to, if any
            chat_id: The Telegram chat ID
            message_id: The Telegram message ID

        Returns:
            A new TelegramUserMessageRequestMessage instance
        """
        payload = {
            "message": message,
            "user_id": user_id,
            "username": username,
            "source": source
        }

        if replied_to_text:
            payload["replied_to_text"] = replied_to_text

        if chat_id is not None:
            payload["chat_id"] = chat_id

        if message_id is not None:
            payload["message_id"] = message_id

        return cls.create(
            topic=RequestMessageTopic.TG_USER_SEND_AI_CHAT_SEND,
            payload=payload
        )

    @property
    def message(self) -> str:
        """Get the message content from the payload"""
        return self.payload.get("message", "")

    @property
    def user_id(self) -> str:
        """Get the user ID from the payload"""
        return self.payload.get("user_id", "")

    @property
    def username(self) -> str:
        """Get the username from the payload"""
        return self.payload.get("username", "")

    @property
    def source(self) -> str:
        """Get the message source from the payload"""
        return self.payload.get("source", "")

    @property
    def replied_to_text(self) -> str:
        """Get the replied to text from the payload"""
        return self.payload.get("replied_to_text", "")

    @property
    def chat_id(self) -> int:
        """Get the Telegram chat ID from the payload"""
        return self.payload.get("chat_id", 0)

    @property
    def message_id(self) -> int:
        """Get the Telegram message ID from the payload"""
        return self.payload.get("message_id", 0)

    @classmethod
    def from_hai_message(cls, message: HaiMessage) -> 'TelegramUserMessageRequestMessage':
        """Create a TelegramUserMessageRequestMessage from a generic HaiMessage"""
        payload = message.payload

        return cls.create_message(
            message=payload.get("message", ""),
            user_id=payload.get("user_id", ""),
            username=payload.get("username", ""),
            source=payload.get("source", ""),
            replied_to_text=payload.get("replied_to_text", ""),
            chat_id=payload.get("chat_id"),
            message_id=payload.get("message_id")
        )

