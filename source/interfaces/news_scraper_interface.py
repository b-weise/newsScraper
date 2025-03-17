import abc
from functools import partial
from typing import Any, Type


class NewsScraperInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_article_url(self) -> str:
        pass

    @abc.abstractmethod
    async def get_title(self, url: str) -> str:
        pass

    @abc.abstractmethod
    def get_date(self) -> str:
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
