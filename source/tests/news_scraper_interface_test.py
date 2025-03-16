from typing import Callable

import pytest

from source.interfaces.news_scraper_interface import NewsScraperInterface


class EmptySample(NewsScraperInterface):
    pass


def test_interface_failure():
    assert not issubclass(EmptySample, NewsScraperInterface)


def test_instance_failure():
    with pytest.raises(TypeError):
        EmptySample()


class FullSample(NewsScraperInterface):
    #  Properties
    host: str = ''
    #  Methods
    get_article_url: Callable = lambda: ()
    get_title: Callable = lambda: ()
    get_date: Callable = lambda: ()
    get_author: Callable = lambda: ()
    get_image_url: Callable = lambda: ()
    get_body: Callable = lambda: ()
    search: Callable = lambda: ()


def test_interface_success():
    assert issubclass(FullSample, NewsScraperInterface)


def test_instance_success():
    assert isinstance(FullSample(), NewsScraperInterface)
