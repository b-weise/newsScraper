import abc
import re
from typing import Optional

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

    async def _navigate_if_necessary(self, url: Optional[str] = None) -> str:
        if url is None:
            url = self._wshandler.page.url
        elif url != self._wshandler.page.url:
            await self._wshandler.safe_goto(url)
        return url

    def _sanitize_text(self, raw_text_block: str) -> str:
        raw_text_lines = raw_text_block.split('\n')
        solid_text_lines = list(filter(lambda line: re.match(r'^\s*$', line) is None,
                                       raw_text_lines))  # Remove empty lines
        solid_text_block = '\n'.join(solid_text_lines)
        sanitized_text_block = solid_text_block.replace(u"\u00A0", ' ')  # Replace non-breaking spaces
        trimmed_text_block = sanitized_text_block.strip()
        return trimmed_text_block

    @abc.abstractmethod
    async def get_title(self, url: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_date(self, url: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_author(self, url: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_image_url(self, url: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    async def get_body(self, url: Optional[str] = None) -> str:
        pass

    @abc.abstractmethod
    async def search(self, keyword: str) -> list[dict[str, str]]:
        pass

    async def destroy(self):
        if self._wshandler is not None:
            await self._wshandler.destroy()
            self._wshandler = None
