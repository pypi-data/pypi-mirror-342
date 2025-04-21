import asyncio
from typing import Optional, Set, Dict, List
from urllib.parse import urlparse

import aiohttp

from ...domain.web_docs.gitbook.text_page import TextPage
from ...domain.webpages.web_text_fetcher_repository import WebTextFetcherRepository
from ...infrastructure.beautifulsoup.soup_processor import SoupProcessor


class GitbookWebFetcherService(WebTextFetcherRepository):

    def __init__(self, url: str):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.base_url = url.rstrip('/')
        self.base_domain = urlparse(self.base_url).netloc

        self.delay = 1.0  # Delay between requests in seconds
        self.max_retries = 3
        self.retry_delay = 2  # Initial retry delay in seconds
        self.concurrent_requests = 3  # Number of concurrent requests

        self.visited_urls: Set[str] = set()
        self.content_hashes: Dict[str, str] = {}  # Hash -> URL
        self.pages: Dict[str, TextPage] = {}

    async def fetch(self) -> Optional[List[TextPage]]:
        timeout = aiohttp.ClientTimeout(total=180)  # 3 minutes total timeout
        async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
            # Start with main page

            await self._process_url(session, self.base_url)

            # Wait for all tasks to complete
            await asyncio.sleep(0)

            # Sort pages by index
            sorted_pages = sorted(
                self.pages.values(),
                key=lambda p: p.index
            )
            return sorted_pages

    async def _process_url(self, session: aiohttp.ClientSession, url: str) -> None:
        if url in self.visited_urls:
            return
        print(f"Processing {url}")
        self.visited_urls.add(url)

        # Fetch page content
        html_content = await self._fetch_page(session, url)
        if not html_content:
            return

        # Extract page content
        page = await GitbookWebFetcherService.extract_page_content(url, html_content)
        if not page:
            return

        # Check for duplicate content
        if page.content_hash in self.content_hashes:
            return

        # Set page index
        page.index = len(self.pages)

        # Add page to collection
        self.pages[url] = page
        self.content_hashes[page.content_hash] = url

        # Extract navigation links from this page
        nav_links = await GitbookWebFetcherService.gitbook_extract_navigation(self.base_url, html_content)

        #Process the discovered links
        for link in nav_links:
            if link not in self.visited_urls:
                # Add delay between requests
                await asyncio.sleep(self.delay)
                # Process the URL
                await self._process_url(session, link)

    @staticmethod
    async def extract_page_content(url: str, html_content: str) -> Optional[TextPage]:
        try:
            soup_processor = SoupProcessor(html_content)

            title = soup_processor.extract_title()
            if not title:
                title = urlparse(url).path.split('/')[-1] or "Index"
                title = title.replace('-', ' ').replace('_', ' ').title()

            last_updated = soup_processor.extract_last_updated_refs_from_soup()

            body_tag = soup_processor.find_body_content()
            if body_tag is None:
                return None
            soup_processor.clean_template_usage(body_tag)
            chapters = soup_processor.extract_chapters(content=body_tag)

            return TextPage(
                url=url,
                title=title,
                content=html_content,
                last_updated=last_updated,
                chapters=chapters,
            )
        except Exception as e:
            return None

    @staticmethod
    async def gitbook_extract_navigation(base_url: str, html_content: str) -> List[str]:
        """Extract navigation links from a page"""
        try:

            soup_processor = SoupProcessor(html_content)

            nav_links = []
            processed_urls = set()

            # Extract links from modern layout
            nav_links.extend(soup_processor.gitbook_extract_modern_nav(base_url, processed_urls))

            # Extract links from traditional layout
            nav_links.extend(soup_processor.gitbook_extract_traditional_nav(base_url, processed_urls))

            # Extract links from pagination elements
            nav_links.extend(soup_processor.gitbook_extract_pagination_links(base_url, processed_urls))

            # Extract links from search for specific class patterns
            nav_links.extend(soup_processor.gitbook_extract_class_based_nav(base_url, processed_urls))

            # Remove duplicates while preserving order
            return list(dict.fromkeys(nav_links))

        except Exception as e:
            return []

    async def _fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a page with retry logic"""
        retry_count = 0
        current_delay = self.retry_delay

        while retry_count < self.max_retries:
            try:
                async with session.get(url) as response:
                    if response.status == 429:  # Rate limit
                        retry_after = response.headers.get('Retry-After', '60')
                        wait_time = int(retry_after)

                        await asyncio.sleep(wait_time)
                        retry_count += 1
                        continue

                    if response.status == 200:
                        return await response.text()
                    else:
                        return None

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if retry_count < self.max_retries - 1:
                    await asyncio.sleep(current_delay)
                    current_delay *= 2  # Exponential backoff
                    retry_count += 1
                else:
                    return None
        return None