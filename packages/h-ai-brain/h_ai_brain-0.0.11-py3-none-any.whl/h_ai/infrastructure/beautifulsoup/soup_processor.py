import logging
import re
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from ...domain.web_docs.gitbook.text_chapter import TextChapter
from ...domain.web_docs.web_link import WebLink

logger = logging.getLogger(__name__)

class SoupProcessor:
    def __init__(self, html_content:str):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_links(self, base_url: str) -> List[WebLink]:
        """Extract links from a page"""
        web_links = []
        links = self.soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '').strip()
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            full_url = urljoin(base_url, href)
            link_text = link.get_text().strip()
            web_link = WebLink(url=full_url, title=link_text)
            web_links.append(web_link)
        return web_links

    def normalize_url(self, href, base_url) -> Optional[str]:
        """Normalize URL to absolute form and filter out non-content URLs"""
        # Skip fragment-only URLs
        if href.startswith('#'):
            return None

        # Skip external links
        if href.startswith(('http://', 'https://')) and not href.startswith(base_url):
            return None

        # Skip resource URLs
        if href.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.pdf', '.zip', '.js', '.css')):
            return None

        # Convert to absolute URL if needed
        full_url = href
        if not href.startswith(('http://', 'https://')):
            full_url = urljoin(base_url, href)

        # Make sure URL belongs to the same domain
        if not full_url.startswith(base_url):
            return None

        return full_url

    def extract_last_updated_refs_from_soup(self) -> str:
        datetime_value = ""

        # Find and remove elements containing "Last updated" text
        for element in self.soup.find_all(string=lambda text: text and "Last updated" in text):
            # Get the parent element and remove it
            parent = element.parent
            if parent:
                parent.decompose()

        return datetime_value

    def extract_title(self) -> Optional[str]:
        """Extract the title of the page using multiple strategies"""
        # Strategy 1: Look for h1
        h1 = self.soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        # Strategy 2: Look for title tag
        title_tag = self.soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            title_parts = re.split(r'[|\-–]', title_text)
            return title_parts[0].strip()

        # Strategy 3: Try to find GitBook-specific title elements
        gitbook_title = self.soup.find('span', {'data-testid': 'page.title'})
        if gitbook_title:
            return gitbook_title.get_text(strip=True)

        return None

    def find_body_content(self) -> Optional[Tag]:
        body_content = self.soup.find('body')
        if body_content:
            return body_content
        return None

    def gitbook_extract_modern_nav(self, base_url, processed_urls):
        """Extract navigation from modern GitBook layout"""
        nav_links = []

        # Look for navigation sidebar
        sidebar = self.soup.select_one('div[data-testid="page.desktopTableOfContents"]')
        if sidebar:
            for link in sidebar.find_all('a', href=True):
                full_url = self.normalize_url(link['href'], base_url)
                if full_url and full_url not in processed_urls:
                    nav_links.append(full_url)
                    processed_urls.add(full_url)

        return nav_links

    def gitbook_extract_traditional_nav(self, base_url, processed_urls):
        """Extract navigation from traditional GitBook layout"""
        nav_links = []

        # Find GitBook navigation elements
        nav_elements = self.soup.find_all(['nav', 'aside'])
        for nav in nav_elements:
            # Look for lists that typically contain the navigation
            nav_lists = nav.find_all(['ol', 'ul'])
            for nav_list in nav_lists:
                for li in nav_list.find_all('li'):
                    link = li.find('a', href=True)
                    if link:
                        full_url = self.normalize_url(link['href'], base_url)
                        if full_url and full_url not in processed_urls:
                            nav_links.append(full_url)
                            processed_urls.add(full_url)

        # Try summary element which is common in GitBook
        summary = self.soup.find('ul', {'class': 'summary'})
        if summary:
            for link in summary.find_all('a', href=True):
                full_url = self.normalize_url(link['href'], base_url)
                if full_url and full_url not in processed_urls:
                    nav_links.append(full_url)
                    processed_urls.add(full_url)

        return nav_links

    def gitbook_extract_pagination_links(self, base_url, processed_urls):
        """Extract navigation from pagination elements"""
        nav_links = []

        # Find pagination links (next/prev)
        selectors = [
            'a[aria-label="Next"]',
            'a[aria-label="Previous"]',
            'a.navigation-next',
            'a.navigation-prev',
            'a:has(svg[data-icon="arrow-right"])',
            'a:has(svg[data-icon="arrow-left"])'
        ]

        for selector in selectors:
            try:
                for link in self.soup.select(selector):
                    if link.has_attr('href'):
                        full_url = self.normalize_url(link['href'], base_url)
                        if full_url and full_url not in processed_urls:
                            nav_links.append(full_url)
                            processed_urls.add(full_url)
            except Exception:
                continue

        return nav_links

    def gitbook_extract_class_based_nav(self, base_url, processed_urls):
        """Extract navigation based on common GitBook class patterns"""
        nav_links = []

        # Common class patterns for navigation in GitBook
        class_patterns = [
            'nav-', 'menu-', 'sidebar-', 'toc-', '-nav', '-menu', '-sidebar', '-toc'
        ]

        # Look for elements with these class patterns
        for pattern in class_patterns:
            elements = self.soup.find_all(class_=lambda c: c and pattern in c)
            for element in elements:
                for link in element.find_all('a', href=True):
                    full_url = self.normalize_url(link['href'], base_url)
                    if full_url and full_url not in processed_urls:
                        nav_links.append(full_url)
                        processed_urls.add(full_url)

        return nav_links

    @staticmethod
    def clean_template_usage(content: Tag):
        if not content or not isinstance(content, Tag):
            return None
        # Step 1: Build a mapping of template IDs to hidden div content
        template_map = {}
        # Find all hidden divs with IDs like S:*
        for hidden_div in content.find_all('div', {'hidden': True}, id=re.compile(r'S:\d+')):
            div_id = hidden_div.get('id')
            # Store the first child (e.g., <a> tag) or the entire content
            if hidden_div.contents:
                template_map[div_id] = hidden_div.contents[0] if len(hidden_div.contents) == 1 else hidden_div

        # Step 2: Replace <template> tags with content from hidden divs based on $RS logic
        for template in content.find_all('template', id=re.compile(r'P:\d+')):
            template_id = template.get('id')  # e.g., P:2
            # Convert P:* to S:* to match the hidden div (assuming $RS("S:2", "P:2") pattern)
            source_id = f"S:{template_id.split(':')[1]}"  # e.g., S:2
            if source_id in template_map:
                # Replace the template with the content from the hidden div
                replacement = template_map[source_id]
                # If it's a Tag, use it directly; if it's a div, extract its contents
                if isinstance(replacement, Tag):
                    template.replace_with(replacement)
                else:
                    template.replace_with(replacement.contents[0])

    @staticmethod
    def extract_chapters(content: Tag) -> List[TextChapter]:
        chapters = []

        # Create a default chapter for content before any heading
        default_chapter = TextChapter(heading="Introduction", level=0)
        current_chapter = default_chapter
        chapters.append(default_chapter)

        for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
            if element.name.startswith('h'):
                # Extract heading level (h1=1, h2=2, etc.)
                level = int(element.name[1])
                heading_text = element.get_text(strip=True)

                # Create a new chapter
                current_chapter = TextChapter(heading=heading_text, level=level)
                chapters.append(current_chapter)

            elif element.name == 'p' and current_chapter is not None:
                paragraph_text = element.get_text(strip=True)
                if paragraph_text:
                    current_chapter.paragraphs.append(paragraph_text)

        # Remove any chapters without content if they're not top-level
        return [ch for ch in chapters if ch.paragraphs or ch.level <= 2]