from source.classes.website_handler import WebsiteHandler
from source.interfaces.news_scraper_interface import BaseNewsScraper


class P12Scraper(BaseNewsScraper):
    def __init__(self):
        super().__init__()
        self._host = 'https://www.pagina12.com.ar/'

    def get_article_url(self) -> str:
        pass

    async def get_title(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        header_div = self._wshandler.page.locator('div.article-header')
        title_h1 = header_div.locator('h1')
        title_text = await title_h1.inner_text()
        return title_text

    async def get_date(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        desktop_only_div = self._wshandler.page.locator('div.hide-on-mobile')
        article_info_div = desktop_only_div.locator('div.article-info')
        date_time = article_info_div.locator('time')
        date_text = await date_time.inner_text()
        return date_text

    def get_author(self) -> str:
        pass

    def get_image_url(self) -> str:
        pass

    def get_body(self) -> str:
        pass

    def search(self) -> list[dict[str, str]]:
        pass
