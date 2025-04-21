import hashlib
from dataclasses import dataclass, field
from typing import Dict, List

from ....domain.web_docs.gitbook.text_chapter import TextChapter


@dataclass
class TextPage:
    """Represents text on a page from a web document"""
    url: str = ""
    title: str = ""
    content: str = ""
    last_updated: str = ""

    index: int = 0
    toc_level: int = 0
    parent_id: str = ""

    chapters: List[TextChapter] = field(default_factory=list)
    links: Dict[str, str] = field(default_factory=dict)  # Text -> URL

    id: str = field(init=False, default="")
    content_hash: str = field(init=False, default="")

    def __post_init__(self):
        self.id = hashlib.md5(self.url.encode()).hexdigest()
        # Generate a content hash for deduplication
        self.content_hash = hashlib.md5(self.content.encode()).hexdigest() if self.content else ""

    def to_dict(self):
        """Convert this TextPage instance to a serializable dictionary"""
        result = {
            'url': self.url,
            'title': self.title,
            #'content': self.content,
            'last_updated': self.last_updated,
            'index': self.index,
            'toc_level': self.toc_level,
            'parent_id': self.parent_id,
            'id': self.id,
            'content_hash': self.content_hash,
            'links': self.links,
            'chapters': [chapter.to_dict() for chapter in self.chapters]
        }
        return result
