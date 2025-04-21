from typing import List

from ...domain.webpages.web_fetcher_repository import WebFetcherRepository
from ...domain.web_docs.doc_link_scorer_service import DocLinkScorerService
from ...domain.web_docs.web_link import WebLink
from ...infrastructure.beautifulsoup.soup_processor import SoupProcessor


class WebDocsLinkDetector:
    def __init__(self, doc_link_scorer: DocLinkScorerService, web_fetcher: WebFetcherRepository, confidence_threshold: float = 0.5):
        self.doc_link_scorer = doc_link_scorer
        self.web_fetcher = web_fetcher
        self.confidence_threshold = confidence_threshold

    async def find_docs_links(self, website_url: str) -> List[WebLink]:
        doc_links = []

        web_content = await self.web_fetcher.fetch(website_url)
        if not web_content:
            return doc_links

        soup_processor = SoupProcessor(web_content)
        web_links = soup_processor.extract_links(website_url)
        for web_link in web_links:
            score = self.doc_link_scorer.score(web_link.url, web_link.title)
            if score >= self.confidence_threshold:
                doc_links.append(web_link)
        return doc_links