import abc
import asyncio
import re
from collections.abc import Callable, Iterable
from typing import Optional

from playwright.async_api import Page

from source.classes.website_handler import WebsiteHandler


class UninitializedWebsiteHandler(Exception):
    pass


class BaseNewsScraper(metaclass=abc.ABCMeta):
    def __init__(self, throttling_chunk_size: int = 5, non_breaking_space_char: str = u"\u00A0"):
        self._host = None
        self._wshandler = None
        self.__non_breaking_space_char = non_breaking_space_char
        self.__throttling_chunk_size = throttling_chunk_size

    @property
    def host(self):
        return self._host

    async def initialize_website_handler(self):
        await self.destroy()
        self._wshandler = WebsiteHandler()
        await self._wshandler.initialize_random_useragent_context()
        await self._wshandler.setup_robots_compliance(self._host)

    def _check_website_handler_instance(self):
        if self._wshandler is None:
            raise UninitializedWebsiteHandler(
                'WebsiteHandler is not initialized. Call the "initialize_website_handler" method first.')

    async def _navigate_if_necessary(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        if url is None:
            url = self._wshandler.page.url
        elif url != self._wshandler.page.url:
            await self._wshandler.safe_goto(url=url, page=page)
        return url

    def _sanitize_text(self, raw_text_block: str) -> str:
        raw_text_lines = raw_text_block.split('\n')
        solid_text_lines = list(filter(lambda line: re.match(r'^\s*$', line) is None,
                                       raw_text_lines))  # Remove empty lines
        solid_text_block = '\n'.join(solid_text_lines)
        sanitized_text_block = solid_text_block.replace(self.__non_breaking_space_char, ' ')
        trimmed_text_block = sanitized_text_block.strip()
        return trimmed_text_block

    async def _gather_articles(self, articles_urls: list[str], check_environment_hook: Optional[Callable] = None,
                               do_throttle: bool = True) -> list[dict[str, str] | None]:
        def split_in_chunks() -> list[list[str]]:
            chunk_size = self.__throttling_chunk_size
            chunks_container = []
            for index in range(0, len(articles_urls), chunk_size):
                chunks_container.append(articles_urls[index:index + chunk_size])
            return chunks_container

        async def scrap_article(article_url) -> dict[str, str] | None:
            async def article_scraper(page: Page) -> Iterable[str]:
                return await asyncio.gather(self.get_title(page=page),
                                            self.get_date(page=page),
                                            self.get_author(page=page),
                                            self.get_image_url(page=page),
                                            self.get_body(page=page))

            new_page = await self._wshandler.get_new_page(article_url)
            pages.append(new_page)

            if check_environment_hook is None:
                scraping_results = await article_scraper(new_page)
            else:
                scraping_results = await check_environment_hook(new_page, article_scraper)

            scraped_article = None
            if scraping_results is not None:
                scraped_article = {'article_url': article_url,
                                   'title': scraping_results[0],
                                   'date': scraping_results[1],
                                   'author': scraping_results[2],
                                   'image_url': scraping_results[3],
                                   'body': scraping_results[4]}

            return scraped_article

        urls_chunks_container = []
        if do_throttle:
            urls_chunks_container = split_in_chunks()
        else:
            urls_chunks_container.append(articles_urls)

        scraped_articles = []
        for chunk in urls_chunks_container:
            pages = []
            scraped_articles += await asyncio.gather(*[scrap_article(url) for url in chunk])
            for page in pages:
                await page.close()

        return scraped_articles

    @abc.abstractmethod
    async def get_title(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_date(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_author(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_image_url(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_body(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        pass

    @abc.abstractmethod
    async def search(self, keyword: str, case_sensitive: bool = False,
                     do_throttle: bool = True) -> list[dict[str, str]]:
        pass

    async def destroy(self):
        if self._wshandler is not None:
            await self._wshandler.destroy()
            self._wshandler = None
