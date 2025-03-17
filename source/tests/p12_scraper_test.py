import pytest

from source.classes.p12_scraper import P12Scraper
from source.classes.website_handler import NonCompliantURL
from source.interfaces.news_scraper_interface import BaseNewsScraper, UninitializedWebsiteHandler


@pytest.fixture
async def new_instance() -> P12Scraper:
    p12scraper = P12Scraper()
    yield p12scraper
    await p12scraper.destroy()


@pytest.fixture
async def new_initialized_instance(new_instance: P12Scraper) -> P12Scraper:
    await new_instance.initialize_website_handler()
    return new_instance


def test_interface_success(new_instance: P12Scraper):
    assert isinstance(new_instance, BaseNewsScraper)


@pytest.mark.parametrize('input_url,output_title', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', 'De genealogistas y analizantes'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 'El futuro de la IA y su impacto en el conocimiento: ¿cambiará la forma en que pensamos?'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 'Especialistas argentinos crean un robot capaz de descubrir fallas en las tuberías de cualquier ciudad'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 'Cambió el mundo'),
])
async def test_get_title_success(new_initialized_instance: P12Scraper, input_url: str, output_title: str):
    title = await new_initialized_instance.get_title(input_url)
    assert title == output_title


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_title_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_title(input_url)


async def test_get_title_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_title('https://www.pagina12.com.ar/800250-genealogistas')


@pytest.mark.parametrize('input_url,output_date', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', '30 de enero de 2025 - 00:34'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 '19 de octubre de 2024 - 00:01'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 '25 de septiembre de 2023 - 23:30'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 '14 de marzo de 2025 - 00:01'),
])
async def test_get_date_success(new_initialized_instance: P12Scraper, input_url: str, output_date: str):
    date = await new_initialized_instance.get_date(input_url)
    assert date == output_date


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_date_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_date(input_url)


async def test_get_date_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_date('https://www.pagina12.com.ar/800250-genealogistas')
