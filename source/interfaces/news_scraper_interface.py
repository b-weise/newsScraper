import abc
from functools import partial
from typing import Any, Type


class NewsScraperInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls: Type, __subclass: Any) -> bool:
        def has_attribute(is_method: bool, name: str) -> bool:
            is_present = hasattr(__subclass, name)
            if is_present and is_method:
                is_present = callable(getattr(__subclass, name))
            return is_present

        mandatory_properties = ['host']
        has_property = partial(has_attribute, False)
        mandatory_methods = ['get_article_url', 'get_title', 'get_date', 'get_author', 'get_image_url', 'get_body',
                             'search']
        has_method = partial(has_attribute, True)
        is_subclass = all(map(has_property, mandatory_properties)) and all(map(has_method, mandatory_methods))
        return is_subclass

    @abc.abstractmethod
    def get_article_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
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
