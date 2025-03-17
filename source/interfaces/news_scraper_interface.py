import abc
from functools import partial
from typing import Any, Type

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

    async def _navigate_if_necessary(self, url: str):
        if url != self._wshandler.page.url:
            await self._wshandler.safe_goto(url)

    @abc.abstractmethod
    def get_article_url(self) -> str:
        pass

    @abc.abstractmethod
    async def get_title(self, url: str) -> str:
        pass

    @abc.abstractmethod
    async def get_date(self, url: str) -> str:
        pass

    @abc.abstractmethod
    def get_author(self) -> str:
        pass

    @abc.abstractmethod
    def get_image_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_body(self) -> str:
        pass

    @abc.abstractmethod
    def search(self) -> list[dict[str, str]]:
        pass

    async def destroy(self):
        if self._wshandler is not None:
            await self._wshandler.destroy()
            self._wshandler = None
