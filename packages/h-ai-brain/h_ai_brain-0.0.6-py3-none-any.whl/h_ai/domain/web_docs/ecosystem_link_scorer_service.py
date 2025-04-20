import re
from urllib.parse import urlparse

from ...domain.web_docs.ecosystem_pattern_repository import EcosystemPatternRepository


class EcosystemLinkScorerService:
    """Service for scoring potential ecosystem-related links and content"""

    def __init__(self, pattern_repo: EcosystemPatternRepository):
        self.pattern_repo = pattern_repo

    def score(self, full_url: str, link_text: str) -> float:
        """
        Score a link based on how likely it is to be ecosystem-related
        Returns a value between 0.0 and 1.0
        """
        score = 0.0
        max_score = 3.0  # Maximum possible score

        # Parse the URL
        parsed_url = urlparse(full_url)
        domain = parsed_url.netloc
        path = parsed_url.path

        # Check domain patterns
        for eco_domain in self.pattern_repo.ecosystem_domains:
            if eco_domain in domain:
                score += 1.0
                break

        # Check path patterns
        for path_pattern in self.pattern_repo.ecosystem_path_patterns:
            if re.search(path_pattern, path):
                score += 1.0
                break

        # Check link text patterns
        for text_pattern in self.pattern_repo.ecosystem_text_patterns:
            if re.search(text_pattern, link_text):
                score += 1.0
                break

        # Normalize score to 0.0-1.0 range
        return min(score / max_score, 1.0)

    def score_page(self, page_url: str, page_title: str, page_content: str) -> float:
        """
        Score an entire page based on how likely it is to contain ecosystem information
        Returns a value between 0.0 and 1.0

        Args:
            page_url: The URL of the page
            page_title: The title of the page
            page_content: The full text content of the page
        """
        # Start with the URL and title scoring
        url_score = self.score(page_url, page_title)

        # Content-based scoring
        content_score = 0.0
        max_content_score = 2.0

        # Check content patterns
        content_matches = 0
        for content_pattern in self.pattern_repo.ecosystem_content_patterns:
            if re.search(content_pattern, page_content):
                content_matches += 1

        # Score based on number of content matches
        if content_matches >= 3:
            content_score += 1.0
        elif content_matches > 0:
            content_score += 0.5

        # Check for header patterns
        for header_pattern in self.pattern_repo.ecosystem_header_patterns:
            if re.search(header_pattern, page_content):
                content_score += 1.0
                break

        # Combined score with higher weight on content
        return min((url_score + (content_score / max_content_score) * 2) / 3, 1.0)
