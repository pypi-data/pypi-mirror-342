
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from h_message_bus import HaiMessage


@dataclass(frozen=True)
class QueueItem:
    """Value object representing an item in the priority queue"""
    id: str
    content: HaiMessage
    priority: int
    created_at: datetime
    metadata: Optional[dict] = None

    @classmethod
    def create(cls, content: HaiMessage, priority: int, metadata: Optional[dict] = None) -> "QueueItem":
        """Factory method to create a new QueueItem"""
        return cls(
            id=str(uuid.uuid4()),
            content=content,
            priority=priority,
            created_at=datetime.utcnow(),
            metadata=metadata
        )

    def __lt__(self, other):
        """Comparison method for priority queue ordering
        - Primary sort by priority: Higher number = higher priority
        - Secondary sort by timestamp: Earlier timestamp = higher priority (FIFO)
        """
        if not isinstance(other, QueueItem):
            return NotImplemented

        # First, compare by priority (higher priority value comes first)
        if self.priority != other.priority:
            return self.priority > other.priority

        # If priorities are equal, compare by timestamp (older timestamp comes first)
        return self.created_at < other.created_at
