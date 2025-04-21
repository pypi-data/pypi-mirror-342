import queue
import threading
from queue import PriorityQueue
from typing import Dict, List, Optional

from ...domain.priorityqueue.priority_queue_repository import PriorityQueueRepository
from ...domain.priorityqueue.queue_item import QueueItem


class InMemoryPriorityQueueRepository(PriorityQueueRepository):
    """In-memory implementation of the PriorityQueueRepository using Python's PriorityQueue"""

    def __init__(self):
        # Dictionary mapping queue names to their PriorityQueue instances
        self.queues: Dict[str, PriorityQueue] = {}
        # Locks to ensure thread safety
        self.locks: Dict[str, threading.Lock] = {}

    def _get_or_create_queue(self, queue_name: str, maxsize: int = 10000) -> PriorityQueue:
        """Get or create a queue with the given name"""
        if queue_name not in self.queues:
            self.queues[queue_name] = PriorityQueue(maxsize=maxsize)
            self.locks[queue_name] = threading.Lock()
        return self.queues[queue_name]

    def _get_lock(self, queue_name: str) -> threading.Lock:
        """Get the lock for the specified queue"""
        if queue_name not in self.locks:
            self.locks[queue_name] = threading.Lock()
        return self.locks[queue_name]

    def add_item(self, queue_name: str, item: QueueItem) -> None:
        """Add an item to the specified queue"""
        q = self._get_or_create_queue(queue_name)
        with self._get_lock(queue_name):
            # The queue automatically orders by priority
            q.put(item)

    def get_highest_priority_item(self, queue_name: str, block: bool = False, timeout: Optional[float] = None) -> Optional[QueueItem]:
        """Get and remove the highest priority item from the queue"""
        if queue_name not in self.queues:
            return None

        q = self.queues[queue_name]
        try:
            # We need to acquire the lock to check initially, but then we need to release it
            # so that other threads can add items while we're blocking
            with self._get_lock(queue_name):
                # If not blocking and queue is empty, return immediately
                if not block and q.empty():
                    return None

            # Note: queue.get() with block=True will internally manage locking
            # We don't hold our custom lock during the blocking wait
            return q.get(block=block, timeout=timeout)
        except queue.Empty:
            # This will be raised if timeout occurs with no items
            return None


    def get_items(self, queue_name: str, limit: int = 10) -> List[QueueItem]:
         """Get multiple items from the queue in priority order without removing them"""
         if queue_name not in self.queues:
             return []

         q = self.queues[queue_name]
         result = []

         with self._get_lock(queue_name):
             # Create a temporary list to hold items that we'll put back
             temp_items = []

             # Get up to 'limit' items
             count = 0
             while not q.empty() and count < limit:
                 item = q.get()
                 temp_items.append(item)
                 result.append(item)
                 count += 1

             # Put all the items back in the same order
             for item in temp_items:
                 q.put(item)

         return result

    def queue_length(self, queue_name: str) -> int:
        """Get the number of items in the queue"""
        if queue_name not in self.queues:
            return 0

        q = self.queues[queue_name]
        with self._get_lock(queue_name):
            return q.qsize()

    def get_queue_names(self) -> List[str]:
        """Get a list of all available queue names"""
        return list(self.queues.keys())
