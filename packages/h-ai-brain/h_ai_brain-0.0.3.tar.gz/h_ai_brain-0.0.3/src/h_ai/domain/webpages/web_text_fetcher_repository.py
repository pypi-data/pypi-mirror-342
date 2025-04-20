from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.web_docs.gitbook.text_page import TextPage


class WebTextFetcherRepository(ABC):

    @abstractmethod
    async def fetch(self) -> Optional[List[TextPage]]:
        """Fetch all content"""
        pass