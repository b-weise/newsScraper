from typing import Optional

import pytest
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


@pytest.mark.parametrize('request_url,response_status', [
    pytest.param('https://www.pagina12.com.ar/robots.txt', 200),
])
async def test_request_get_status_success(request_url: str, response_status: int):
    wshandler = WebsiteHandler()
    await wshandler.initialize_playwright()
    response = await wshandler.request_get(url=request_url)
    status = response.status
    assert status == response_status


@pytest.mark.parametrize('request_url,response_body', [
    pytest.param('https://www.pagina12.com.ar/robots.txt', """\
# robots.txt for https://www.pagina12.com.ar/

Sitemap: https://www.pagina12.com.ar/sitemap.xml.gz
Sitemap: https://www.pagina12.com.ar/breakingnews.xml
Sitemap: https://www.pagina12.com.ar/breakingnews-short.xml

User-agent: *
Disallow: /logout-user?redirect=*
Disallow: /349353471/
Disallow: /admin/
Disallow: /andytow/
Disallow: /apps/talk
Disallow: /apps/zar
"""),
])
async def test_request_get_body_success(request_url: str, response_body: Optional[str]):
    wshandler = WebsiteHandler()
    await wshandler.initialize_playwright()
    response = await wshandler.request_get(url=request_url)
    text = await response.text()
    assert text == response_body
