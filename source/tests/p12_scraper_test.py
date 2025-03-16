import pytest

from source.classes.p12_scraper import P12Scraper
from source.interfaces.news_scraper_interface import NewsScraperInterface


@pytest.fixture
async def new_instance() -> P12Scraper:
    p12scraper = P12Scraper()
    yield p12scraper
    await p12scraper.destroy()


def test_interface_success(new_instance: P12Scraper):
    assert isinstance(new_instance, NewsScraperInterface)
