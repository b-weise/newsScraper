import pytest_asyncio
from playwright.async_api import Page

from source.classes.website_handler import WebsiteHandler


@pytest_asyncio.fixture(scope='module')
async def new_instance() -> WebsiteHandler:
    wshandler = WebsiteHandler()
    yield wshandler
    await wshandler.destroy()


@pytest_asyncio.fixture(scope='module')
async def initialized_playwright(new_instance) -> WebsiteHandler:
    await new_instance.initialize_playwright()
    return new_instance


def test_instantiation_success(new_instance: WebsiteHandler):
    assert isinstance(new_instance, WebsiteHandler)


async def test_initialized_playwright_success(initialized_playwright: WebsiteHandler):
    assert isinstance(initialized_playwright, WebsiteHandler)


async def test_page(initialized_playwright: WebsiteHandler):
    assert isinstance(initialized_playwright.page, Page)
