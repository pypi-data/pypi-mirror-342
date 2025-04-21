
from abc import ABC, abstractmethod
from typing import List, Optional

from .queue_item import QueueItem


class PriorityQueueRepository(ABC):
    """Repository interface for priority queue operations"""

    @abstractmethod
    def add_item(self, queue_name: str, item: QueueItem) -> None:
        """Add an item to the specified queue"""
        pass

    @abstractmethod
    def get_highest_priority_item(self, queue_name: str, block: bool = False, timeout: Optional[float] = None) -> Optional[QueueItem]:
        """Get and remove the highest priority item from the queue"""
        pass

    # @abstractmethod
    # def get_items(self, queue_name: str, limit: int = 10) -> List[QueueItem]:
    #     """Get multiple items from the queue in priority order without removing them"""
    #     pass

    @abstractmethod
    def queue_length(self, queue_name: str) -> int:
        """Get the number of items in the queue"""
        pass

    @abstractmethod
    def get_queue_names(self) -> List[str]:
        """Get a list of all available queue names"""
        pass
