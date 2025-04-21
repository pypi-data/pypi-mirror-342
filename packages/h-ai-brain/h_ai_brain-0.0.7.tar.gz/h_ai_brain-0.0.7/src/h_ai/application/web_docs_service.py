from typing import List, Optional

from ..domain.web_docs.doc_link_scorer_service import DocLinkScorerService
from ..domain.web_docs.documentation_pattern_repository import DocumentationPatternRepository
from ..domain.web_docs.gitbook.text_page import TextPage
from ..domain.web_docs.gitbook_web_fetcher_service import GitbookWebFetcherService
from ..domain.web_docs.web_docs_link_detector import WebDocsLinkDetector
from ..domain.web_docs.web_link import WebLink
from ..infrastructure.playwright.playwright_web_content_fetcher import PlayWrightWebContentFetcher


class WebDocsService:

    def __init__(self):
        self.pattern_repo = DocumentationPatternRepository()
        self.scorer = DocLinkScorerService(self.pattern_repo)
        self.headless_browser = PlayWrightWebContentFetcher()
        self.web_link_detector = WebDocsLinkDetector(
            self.scorer,
            self.headless_browser)


    async def discover_documentation(self, website_url: str) -> Optional[List[TextPage]]:
        detected_links = await self.detect_documentation_links(website_url)
        for link in detected_links:
            print(f"Fetching {link.url}")
            gitbook_fetcher = GitbookWebFetcherService(link.url)
            gitbook_pages = await gitbook_fetcher.fetch()
            return gitbook_pages

    async def detect_documentation_links(self, website_url: str) -> List[WebLink]:
        """
        Function to detect documentation links from a website
        Returns a list of potential documentation root URLs
        """
        return await self.web_link_detector.find_docs_links(website_url)
