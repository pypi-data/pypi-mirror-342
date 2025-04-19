from typing import Type, TypeVar, Dict, Any

from .topics import MessageTopic
from ..domain.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class VectorReadRequestMessage(HaiMessage):
    """Message to read data from vector store"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, collection_name: str, query: str, top_n: str) -> 'VectorReadRequestMessage':
        """Create a message requesting Twitter user data"""
        return cls.create(
            topic=MessageTopic.AI_VECTORS_QUERY,
            payload={
                "collection_name": collection_name,
                "query": query,
                "top_n": top_n
            },
        )

    @property
    def collection_name(self) -> str:
        """Get the collection name from the message payload"""
        return self.payload.get("collection_name", "")

    @property
    def query(self) -> str:
        """Get the query from the message payload"""
        return self.payload.get("query", "")

    @property
    def top_n(self) -> str:
        """Get the top_n value from the message payload"""
        return self.payload.get("top_n", "")
