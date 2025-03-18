import re
from collections.abc import Callable, Iterable
from typing import Optional
from urllib.parse import urlparse, urlunparse, quote

from playwright.async_api import Page, TimeoutError as PWTimeoutError, expect

from source.classes.base_news_scraper import BaseNewsScraper


class P12Scraper(BaseNewsScraper):
    """
    Implements all abstract methods from BaseNewsScraper with logic specific to pagina12.com.ar.
    """
    def __init__(self, throttling_chunk_size: int = 5):
        super().__init__(throttling_chunk_size=throttling_chunk_size)
        self._host = 'https://www.pagina12.com.ar/'

    async def get_title(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        header_div = page.locator('div.article-header')
        title_h1 = header_div.locator('h1')
        title_text = await title_h1.inner_text()
        return self._sanitize_text(title_text)

    async def get_date(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        desktop_only_div = page.locator('div.hide-on-mobile')
        article_info_div = desktop_only_div.locator('div.article-info')
        date_time = article_info_div.locator('time')
        date_text = await date_time.get_attribute('datetime')
        return self._sanitize_text(date_text)

    async def get_author(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        author_text = ''
        try:
            self._check_website_handler_instance()
            page = page or self._wshandler.page
            await self._navigate_if_necessary(url=url, page=page)
            header_div = page.locator('div.article-header')
            author_div = header_div.locator('div.author')
            author_a = author_div.locator('a')
            author_text = await author_a.inner_text()
            author_text = re.sub(f'^\\s*Por\\s+', '', author_text)
            author_text = self._sanitize_text(author_text)
        except PWTimeoutError:
            pass  # Author absence is acceptable
        return author_text

    async def get_image_url(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        image_url = ''
        try:
            main_image_div = None
            image_img = None
            image_src = None
            try:
                main_image_div = page.locator('div.article-main-image')
                image_img = main_image_div.locator('img')
                image_src = await image_img.get_attribute('src')
            except PWTimeoutError:
                # Some articles lack a main image
                main_image_div = page.locator('div.no-main-image')
                image_img = main_image_div.locator('img').first
                image_src = await image_img.get_attribute('src')
            url_scheme, url_hostname, url_path, _, _, _ = list(urlparse(image_src))
            image_url = str(urlunparse([url_scheme, url_hostname, url_path, '', '', '']))
        except PWTimeoutError:
            pass  # Others have no images at all; therefore, their absence is acceptable
        return image_url

    async def get_body(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        main_content_div = page.locator('div.article-main-content')
        article_text_div = main_content_div.locator('div.article-text')
        article_text = await article_text_div.inner_text()
        return self._sanitize_text(article_text)

    async def search(self, keyword: str, case_sensitive: bool = False,
                     do_throttle: bool = True) -> list[dict[str, str]]:
        """
        Uses the site's internal search engine to find candidate articles, gathers their paths, scrapes them
        and performs another, case-sensible search in each candidate's title and body. Returns matching articles.
        """
        def build_search_url():
            """
            Sanitizes the given keyword before building a search URL that includes it.
            """
            sanitized_keyword = quote(keyword)
            url_path = '/buscar'
            url_query = f'q={sanitized_keyword}'
            full_url = str(urlunparse([url_scheme, url_hostname, url_path, '', url_query, '']))
            return full_url

        async def get_paths():
            """
            Scrapes all articles paths from the search results page.
            """
            articles_paths = []
            article_item_header_divs = self._wshandler.page.locator('div.article-item__header')
            for item in await article_item_header_divs.all():
                url_a = item.locator('a')
                url_href = await url_a.get_attribute('href')
                articles_paths.append(url_href)
            return articles_paths

        async def check_environment_hook(page: Page, article_scraper: Callable) -> Iterable[str] | None:
            """
            A hook that determines if the page environment is suitable for scraping.
            """
            try:
                await expect(page.locator('article.live-blog-post').first).to_be_attached(attached=False)
            except AssertionError:
                # Live article: ignore it
                return None
            else:
                # Non-live article: scrape it
                return await article_scraper(page)

        def search_for_keyword() -> list[dict[str, str]]:
            """
            Searches for the given search_token in the scraped_candidates' title and body,
            considering letter case sensitivity.
            """
            search_token = keyword
            matches = []
            for candidate in scraped_candidates:
                if candidate is None:
                    continue
                search_space = candidate['title'] + candidate['body']
                if not case_sensitive:
                    search_token = search_token.casefold()
                    search_space = search_space.casefold()
                if search_token in search_space:
                    matches.append(candidate)
            return matches

        self._check_website_handler_instance()
        url_scheme, url_hostname, _, _, _, _ = list(urlparse(self._host))

        search_url = build_search_url()
        await self._navigate_if_necessary(search_url)

        articles_urls = list(map(lambda path: str(urlunparse([url_scheme, url_hostname, path, '', '', ''])),
                                 await get_paths()))

        scraped_candidates = await self._gather_articles(articles_urls=articles_urls, do_throttle=do_throttle,
                                                         check_environment_hook=check_environment_hook)

        matching_articles = search_for_keyword()

        return matching_articles
