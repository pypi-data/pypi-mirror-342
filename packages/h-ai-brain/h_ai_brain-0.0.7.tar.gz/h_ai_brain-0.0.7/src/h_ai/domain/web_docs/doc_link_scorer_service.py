import re
from urllib.parse import urlparse

from ...domain.web_docs.documentation_pattern_repository import DocumentationPatternRepository


class DocLinkScorerService:
    """Service for scoring potential documentation links"""

    def __init__(self, pattern_repo: DocumentationPatternRepository):
        self.pattern_repo = pattern_repo

    def score(self, full_url: str, link_text: str) -> float:
        """
        Score a link based on how likely it is to be documentation
        Returns a value between 0.0 and 1.0
        """
        score = 0.0
        max_score = 3.0  # Maximum possible score

        # Parse the URL
        parsed_url = urlparse(full_url)
        domain = parsed_url.netloc
        path = parsed_url.path

        # Check domain patterns
        for doc_domain in self.pattern_repo.doc_domains:
            if doc_domain in domain:
                score += 1.0
                break

        # Check path patterns
        for path_pattern in self.pattern_repo.doc_path_patterns:
            if re.search(path_pattern, path):
                score += 1.0
                break

        # Check link text patterns
        for text_pattern in self.pattern_repo.doc_text_patterns:
            if re.search(text_pattern, link_text):
                score += 1.0
                break

        # Normalize score to 0.0-1.0 range
        return min(score / max_score, 1.0)