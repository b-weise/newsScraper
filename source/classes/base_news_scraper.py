import abc
import asyncio
import re
from typing import Optional

from playwright.async_api import Page

from source.classes.website_handler import WebsiteHandler


class UninitializedWebsiteHandler(Exception):
    pass


class BaseNewsScraper(metaclass=abc.ABCMeta):
    def __init__(self):
        self._host = None
        self._wshandler = None

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
        sanitized_text_block = solid_text_block.replace(u"\u00A0", ' ')  # Replace non-breaking spaces
        trimmed_text_block = sanitized_text_block.strip()
        return trimmed_text_block

    async def _gather_results(self, results_urls: list[str]) -> list[dict[str, str]]:
        results = []
        pages = []

        async def build_result(article_url):
            result = {'article_url': article_url}
            new_page = await self._wshandler.get_new_page(article_url)

            async def store_result(key, getter_coro):
                result[key] = await getter_coro

            await asyncio.gather(store_result('title', self.get_title(page=new_page)),
                                 store_result('date', self.get_date(page=new_page)),
                                 store_result('author', self.get_author(page=new_page)),
                                 store_result('image_url', self.get_image_url(page=new_page)),
                                 store_result('body', self.get_body(page=new_page)))
            results.append(result)
            pages.append(new_page)

        await asyncio.gather(*[build_result(url) for url in results_urls])

        for page in pages:
            page.close()

        return results

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
    async def search(self, keyword: str) -> list[dict[str, str]]:
        pass

    async def destroy(self):
        if self._wshandler is not None:
            await self._wshandler.destroy()
            self._wshandler = None
