from collections.abc import Iterable
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


@pytest.mark.parametrize('input_content,expected_output', [
    pytest.param("""\
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
""", {'allow': [], 'disallow': ['/logout-user?redirect=*', '/349353471/', '/admin/', '/andytow/', '/apps/talk',
                                '/apps/zar']}),
    pytest.param("""
    User-agent: Googlebot *
    Disallow: /logout-user?redirect=* /349353471/ /admin/ /andytow/ /apps/talk /apps/zar
    """,
                 {'allow': [], 'disallow': ['/logout-user?redirect=*', '/349353471/', '/admin/', '/andytow/',
                                            '/apps/talk', '/apps/zar']}),
    pytest.param("""
    User-agent: *
    Disallow: /logout-user?redirect=*
    Allow: /349353471/
    """, {'allow': ['/349353471/'], 'disallow': ['/logout-user?redirect=*']}),
    pytest.param("""
    USER-AGENT: *
    Disallowed: /logout-user?redirect=*
    Allowed: /349353471/
    
    User-agent: Googlebot
    Disallowed: /admin/
    Allowed: /andytow/
    """, {'allow': ['/349353471/'], 'disallow': ['/logout-user?redirect=*']}),
    pytest.param("""
    User-agent: Googlebot
    Disallowed: /admin/
    Allowed: /andytow/
    user-agent: *
    disallowed: /logout-user?redirect=*
    allowed: /349353471/
    """, {'allow': ['/349353471/'], 'disallow': ['/logout-user?redirect=*']}),
])
async def test_parse_robots_file_success(new_instance, input_content: str, expected_output: dict[str, Iterable[str]]):
    parsed_content = new_instance.parse_robots_file(input_content)
    assert parsed_content == expected_output


@pytest.mark.parametrize('parsed_robots,input_url,expected_output', [
    pytest.param({'allow': [], 'disallow': []}, 'https://www.pagina12.com.ar/', True),
    pytest.param({'allow': ['/'], 'disallow': []}, 'https://www.pagina12.com.ar/', True),
    pytest.param({'allow': [], 'disallow': ['/']}, 'https://www.pagina12.com.ar/', False),
    pytest.param({'allow': ['/test/'], 'disallow': ['/']}, 'https://www.pagina12.com.ar/test/', True),
    pytest.param({'allow': ['/'], 'disallow': ['/test/']}, 'https://www.pagina12.com.ar/test/', False),
    pytest.param({'allow': ['/*/'], 'disallow': ['/']}, 'https://www.pagina12.com.ar/test/', True),
    pytest.param({'allow': ['/*/*/'], 'disallow': ['/*/']}, 'https://www.pagina12.com.ar/test/', False),
    pytest.param({'allow': ['/*/*/'], 'disallow': ['/*/']}, 'https://www.pagina12.com.ar/test/ing/', True),
])
async def test_ensure_compliant_url_success(new_instance,
                                            parsed_robots: dict[str, list[str]],
                                            input_url: str,
                                            expected_output: bool):
    is_compliant = new_instance.ensure_compliant_url(parsed_robots, input_url)
    assert is_compliant == expected_output
