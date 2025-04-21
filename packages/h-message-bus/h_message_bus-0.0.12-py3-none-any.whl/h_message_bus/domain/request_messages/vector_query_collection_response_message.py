from typing import Type, TypeVar, Dict, Any

from ..models.request_message_topic import RequestMessageTopic
from ...domain.models.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class VectorQueryCollectionResponseMessage(HaiMessage):
    """Response Message from reading vector data"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, results: [str], dimensions: [str]) -> 'VectorQueryCollectionResponseMessage':
        """Create a message requesting Twitter user data"""
        return cls.create(
            topic=RequestMessageTopic.AI_VECTORS_QUERY_RESPONSE,
            payload={
                "dimensions": dimensions,
                "results": results
            },
        )

    @property
    def dimensions(self) -> list[str]:
        """Returns the dimensions from the message payload"""
        return self.payload.get("dimensions", [])

    @property
    def results(self) -> list[str]:
        """Returns the results from the message payload"""
        return self.payload.get("results", [])

    @classmethod
    def from_hai_message(cls, message: HaiMessage) -> 'VectorQueryCollectionResponseMessage':
        # Extract necessary fields from the message payload
        payload = message.payload

        return cls.create_message(
            dimensions=payload.get('dimensions', []),
            results=payload.get('results', [])
        )
