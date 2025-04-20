import logging
from typing import Optional

from playwright.async_api import async_playwright

from ...domain.webpages.web_fetcher_repository import WebFetcherRepository

logger = logging.getLogger(__name__)

class PlayWrightWebContentFetcher(WebFetcherRepository):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.page_load_timeout = 60
        self.wait_for_idle = True

    async def fetch(self, url: str) -> Optional[str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                context = await browser.new_context(
                    user_agent=self.headers.get('User-Agent')
                )
                page = await context.new_page()

                # Set timeout
                page.set_default_timeout(self.page_load_timeout * 1000)  # Convert to ms

                # Navigate to the URL
                await page.goto(url)

                # Wait for network to be idle if requested
                if self.wait_for_idle:
                    await page.wait_for_load_state("networkidle")

                logger.debug(f"Successfully fetched {url} with headless browser")

                # Get the rendered HTML
                return await page.content()

            except Exception as e:
                logger.error(f"Error fetching {url} with headless browser: {str(e)}")
                return None
            finally:
                await browser.close()