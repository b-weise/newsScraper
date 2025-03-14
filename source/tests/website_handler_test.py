import pytest_asyncio
from playwright.async_api import Page

from source.classes.website_handler import WebsiteHandler


@pytest.fixture(scope='module')
async def new_instance() -> WebsiteHandler:
    wshandler = WebsiteHandler()
    await wshandler.initialize_playwright()
    yield wshandler
    await wshandler.destroy()


async def test_initialized_playwright_success(new_instance: WebsiteHandler):
    assert isinstance(new_instance, WebsiteHandler)


async def test_page_success(new_instance: WebsiteHandler):
    assert isinstance(new_instance.page, Page)

