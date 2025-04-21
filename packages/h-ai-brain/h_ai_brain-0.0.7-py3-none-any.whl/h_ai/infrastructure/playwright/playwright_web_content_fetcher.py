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
            browser = await p.chromium.launch(headless=True, args=[
            '--disable-dev-shm-usage',  # Required for Docker
            '--no-sandbox',  # Required for Docker non-root user
            '--disable-setuid-sandbox',  # Required for Docker security
            '--disable-gpu',  # Reduces resource usage
            ])

            logger.debug(
                f"Launching headless browser with user agent: {self.headers.get('User-Agent')}"
            )
            try:
                context = await browser.new_context(
                    user_agent=self.headers.get('User-Agent')
                )
                page = await context.new_page()

                # Set timeout
                page.set_default_timeout(self.page_load_timeout * 1000)  # Convert to ms

                page.on("console", lambda msg: logger.debug(f"Browser console {url}: {msg.text}"))

                # Navigate to the URL
                await page.goto(url, timeout=self.page_load_timeout * 1000, wait_until='domcontentloaded')

                # Wait for network to be idle if requested
                if self.wait_for_idle:
                    logger.debug(f"Waiting for network idle on {url}")

                    await page.wait_for_load_state("networkidle", timeout=self.page_load_timeout * 1000)
                    logger.debug(
                        f"Network idle on {url} after {self.page_load_timeout} seconds"
                    )

                logger.debug(f"Successfully fetched {url} with headless browser")

                # Get the rendered HTML
                return await page.content()

            except Exception as e:
                logger.error(f"Error fetching {url} with headless browser: {str(e)}")
                return None
            finally:
                await browser.close()