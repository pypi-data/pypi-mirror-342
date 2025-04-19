from typing import Type, TypeVar, Dict, Any

from .topics import MessageTopic
from ..domain.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class VectorSaveRequestMessage(HaiMessage):
    """Message to data in vector store"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, collection_name: str, document_id: str, content: str, metadata: str) -> 'VectorSaveRequestMessage':
        """Create a message requesting Twitter user data"""
        return cls.create(
            topic=MessageTopic.AI_VECTORS_SAVE,
            payload={
                "collection_name": collection_name,
                "document_id": document_id,
                "content": content,
                "metadata": metadata
            },
        )

    @property
    def collection_name(self) -> str:
        """Get the collection name from payload"""
        return self.payload.get("collection_name")

    @property
    def document_id(self) -> str:
        """Get the document ID from payload"""
        return self.payload.get("document_id")

    @property
    def content(self) -> str:
        """Get the content from payload"""
        return self.payload.get("content")

    @property
    def metadata(self) -> str:
        """Get the metadata from payload"""
        return self.payload.get("metadata")
