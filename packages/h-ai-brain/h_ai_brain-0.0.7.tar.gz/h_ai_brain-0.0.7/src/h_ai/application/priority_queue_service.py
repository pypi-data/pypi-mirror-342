
from typing import Any, List, Optional

from ..domain.priorityqueue.priority_queue_repository import PriorityQueueRepository
from ..domain.priorityqueue.queue_item import QueueItem


class PriorityQueueService:
    """Application service to manage priority queue operations"""

    def __init__(self, repository: PriorityQueueRepository):
        self.repository = repository

    def add_item(self, queue_name: str, content: Any, priority: int, metadata: Optional[dict] = None) -> QueueItem:
        """Add an item to the specified queue"""
        item = QueueItem.create(content, priority, metadata)
        self.repository.add_item(queue_name, item)
        return item

    def get_next_item(self, queue_name: str) -> Optional[QueueItem]:
        """Get and remove the highest priority item from the queue"""
        return self.repository.get_highest_priority_item(queue_name)

    def get_items(self, queue_name: str, limit: int = 10) -> List[QueueItem]:
        """Get multiple items from the queue in priority order without removing them"""
        return self.repository.get_items(queue_name, limit)

    def get_queue_length(self, queue_name: str) -> int:
        """Get the number of items in the queue"""
        return self.repository.queue_length(queue_name)

    def get_available_queues(self) -> List[str]:
        """Get a list of all available queue names"""
        return self.repository.get_queue_names()
