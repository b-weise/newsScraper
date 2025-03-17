from typing import Callable

import pytest

from source.interfaces.news_scraper_interface import BaseNewsScraper


class FullSample(BaseNewsScraper):
    #  Methods
    get_article_url: Callable = lambda: ()
    get_title: Callable = lambda: ()
    get_date: Callable = lambda: ()
    get_author: Callable = lambda: ()
    get_image_url: Callable = lambda: ()
    get_body: Callable = lambda: ()
    search: Callable = lambda: ()


def test_instance_success():
    assert isinstance(FullSample(), BaseNewsScraper)


class EmptySample(BaseNewsScraper):
    pass


def test_instance_failure():
    with pytest.raises(TypeError):
        EmptySample()
