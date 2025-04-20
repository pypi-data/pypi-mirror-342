from abc import ABC, abstractmethod
from typing import Optional


class WebFetcherRepository(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> Optional[str]:
        """Fetch the content of the given URL."""
        pass