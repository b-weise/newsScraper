from collections.abc import Iterable
from typing import Optional

import pytest
from playwright.async_api import Page

from source.classes.website_handler import WebsiteHandler, NonCompliantURL, UninitializedPlaywright


@pytest.fixture
async def new_instance() -> WebsiteHandler:
    wshandler = WebsiteHandler()
    yield wshandler
    await wshandler.destroy()


@pytest.fixture
async def new_initialized_instance(new_instance: WebsiteHandler) -> WebsiteHandler:
    await new_instance.initialize_playwright()
    return new_instance


async def test_initialized_playwright_success(new_instance: WebsiteHandler):
    assert isinstance(new_instance, WebsiteHandler)


async def test_page_success(new_initialized_instance: WebsiteHandler):
    assert isinstance(new_initialized_instance.page, Page)


async def test_page_failure(new_instance: WebsiteHandler):
    with pytest.raises(UninitializedPlaywright):
        new_instance.page


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
async def test_get_request_success(new_initialized_instance: WebsiteHandler, request_url: str,
                                   response_body: Optional[str]):
    response = await new_initialized_instance.get_request(request_url)
    assert response.status == 200
    text = await response.text()
    assert text == response_body


@pytest.mark.parametrize('request_url', [
    pytest.param('https://www.pagina12.com.ar/robots.txt'),
])
async def test_get_request_failure(new_instance: WebsiteHandler, request_url: str):
    with pytest.raises(UninitializedPlaywright):
        await new_instance.get_request(request_url)


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


@pytest.mark.parametrize('input_url,parsed_robots,expected_output', [
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': []}, True),
    pytest.param('https://www.pagina12.com.ar/', {'allow': ['/'], 'disallow': []}, True),
    pytest.param('https://www.pagina12.com.ar/test', {'allow': [], 'disallow': ['/*/']}, True),
    pytest.param('https://www.pagina12.com.ar/test', {'allow': ['/'], 'disallow': ['/*/']}, True),
    pytest.param('https://www.pagina12.com.ar/test', {'allow': ['/test'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test', {'allow': ['/test'], 'disallow': ['/test/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': ['/test/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': ['/*/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing', {'allow': ['/test/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing', {'allow': ['/*/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/test/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/'], 'disallow': ['/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/*/'], 'disallow': ['/*/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/ing/'], 'disallow': ['/*/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/*/'], 'disallow': ['/test/']}, True),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/ing/'], 'disallow': ['/test/']}, True),
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': ['/']}, False),
    pytest.param('https://www.pagina12.com.ar/test', {'allow': ['/'], 'disallow': ['/test']}, False),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': [], 'disallow': ['/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': ['/*/'], 'disallow': ['/test/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/', {'disallow': ['/test/'], 'allow': ['/*/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': ['/'], 'disallow': ['/test/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/', {'allow': ['/*/*/'], 'disallow': ['/*/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/ing', {'allow': ['/'], 'disallow': ['/*/']}, False),
    pytest.param('https://www.pagina12.com.ar/test/ing/', {'allow': ['/*/'], 'disallow': ['/*/*/']}, False),
])
async def test_is_compliant_url_success(new_instance, input_url: str, parsed_robots: dict[str, list[str]],
                                        expected_output: bool):
    is_compliant = new_instance.is_compliant_url(input_url, parsed_robots)
    assert is_compliant == expected_output


@pytest.mark.parametrize('input_url,parsed_robots', [
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': []}),
    pytest.param('https://www.pagina12.com.ar/', {'allow': ['/'], 'disallow': []}),
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': ['/*/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', {'allow': [], 'disallow': ['/*/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', {'allow': ['/'], 'disallow': ['/*/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas',
                 {'allow': ['/800250-genealogistas'], 'disallow': ['/']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/*/'], 'disallow': ['/']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/secciones/'], 'disallow': ['/']}),
])
async def test_safe_goto_success(new_initialized_instance: WebsiteHandler, input_url: str,
                                 parsed_robots: dict[str, list[str]]):
    await new_initialized_instance.safe_goto(input_url, parsed_robots)
    assert new_initialized_instance.page.url == input_url


@pytest.mark.parametrize('input_url,parsed_robots', [
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': ['/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', {'allow': [], 'disallow': ['/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas',
                 {'allow': ['/'], 'disallow': ['/800250-genealogistas']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', {'allow': ['/*/'], 'disallow': ['/']}),
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas',
                 {'allow': ['/800250-genealogistas/'], 'disallow': ['/800250-genealogistas']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/'], 'disallow': ['/*/']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/'], 'disallow': ['/secciones/']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/'], 'disallow': ['/*/*']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais', {'allow': ['/'], 'disallow': ['/*/el-pais']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais',
                 {'allow': ['/'], 'disallow': ['/secciones/el-pais']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais',
                 {'allow': ['/*/'], 'disallow': ['/secciones/']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais',
                 {'allow': ['/*/'], 'disallow': ['/*/el-pais']}),
    pytest.param('https://www.pagina12.com.ar/secciones/el-pais',
                 {'allow': ['/*/'], 'disallow': ['/secciones/el-pais']}),
])
async def test_safe_goto_failure(new_initialized_instance: WebsiteHandler, input_url: str,
                                 parsed_robots: dict[str, list[str]]):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.safe_goto(input_url, parsed_robots)


@pytest.mark.parametrize('input_url,parsed_robots', [
    pytest.param('https://www.pagina12.com.ar/', {'allow': [], 'disallow': ['/']}),
])
async def test_safe_goto_call_failure(new_instance: WebsiteHandler, input_url: str,
                                      parsed_robots: dict[str, list[str]]):
    with pytest.raises(UninitializedPlaywright):
        await new_instance.safe_goto(input_url, parsed_robots)


pytest.common_useragent_tests_storage = {
    'cycles': 6,
    'test_useragents': [],
    'current_common_useragents': [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/115.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3"],
}


@pytest.mark.parametrize('tests_counter', range(pytest.common_useragent_tests_storage['cycles']))
async def test_get_common_useragent_success(new_initialized_instance: WebsiteHandler, tests_counter: int):
    useragent = await new_initialized_instance.get_common_useragent()
    assert useragent in pytest.common_useragent_tests_storage['current_common_useragents']
    pytest.common_useragent_tests_storage['test_useragents'].append(useragent)
    if (len(pytest.common_useragent_tests_storage['test_useragents'])
            == pytest.common_useragent_tests_storage['cycles']):
        sorted_stored_useragents = sorted(pytest.common_useragent_tests_storage['test_useragents'])
        assert sorted_stored_useragents[0] != sorted_stored_useragents[-1]


async def test_get_common_useragent_failure(new_instance: WebsiteHandler):
    with pytest.raises(UninitializedPlaywright):
        await new_instance.get_common_useragent()
