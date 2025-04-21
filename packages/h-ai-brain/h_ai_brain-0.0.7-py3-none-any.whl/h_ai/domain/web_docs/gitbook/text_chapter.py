from dataclasses import dataclass, field
from typing import List


@dataclass
class TextChapter:
    """Represents a chapter/section in a page defined by a heading."""
    heading: str
    level: int  # h1=1, h2=2, etc.
    paragraphs: List[str] = field(default_factory=list)

    def to_dict(self):
        """Convert this TextChapter instance to a serializable dictionary"""
        return {
            'heading': self.heading,
            'level': self.level,
            'paragraphs': self.paragraphs
        }
