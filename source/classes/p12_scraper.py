import re
from urllib.parse import urlparse, urlunparse

from source.classes.base_news_scraper import BaseNewsScraper


class P12Scraper(BaseNewsScraper):
    def __init__(self):
        super().__init__()
        self._host = 'https://www.pagina12.com.ar/'
        self.__author_text_prefix = 'Por'

    def get_article_url(self) -> str:
        pass

    async def get_title(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        header_div = self._wshandler.page.locator('div.article-header')
        title_h1 = header_div.locator('h1')
        title_text = await title_h1.inner_text()
        return title_text.strip()

    async def get_date(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        desktop_only_div = self._wshandler.page.locator('div.hide-on-mobile')
        article_info_div = desktop_only_div.locator('div.article-info')
        date_time = article_info_div.locator('time')
        date_text = await date_time.inner_text()
        return date_text.strip()

    async def get_author(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        header_div = self._wshandler.page.locator('div.article-header')
        author_div = header_div.locator('div.author')
        author_a = author_div.locator('a')
        author_text = await author_a.inner_text()
        author_text = re.sub(f'^\\s*{self.__author_text_prefix}\\s+', '', author_text)
        return author_text.strip()

    async def get_image_url(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        main_image_div = self._wshandler.page.locator('div.article-main-image')
        image_img = main_image_div.locator('img')
        image_src = await image_img.get_attribute('src')
        url_scheme, url_hostname, url_path, _, _, _ = list(urlparse(image_src))
        image_url = urlunparse([url_scheme, url_hostname, url_path, '', '', ''])
        return str(image_url)

    async def get_body(self, url: str) -> str:
        self._check_website_handler_instance()
        await self._navigate_if_necessary(url)
        main_content_div = self._wshandler.page.locator('div.article-main-content')
        article_text_div = main_content_div.locator('div.article-text')
        article_text = await article_text_div.inner_text()
        text_lines = article_text.split('\n')
        solid_text_lines = list(filter(lambda line: re.match(r'^\s*$', line) is None,
                                       text_lines))  # remove empty lines
        solid_text_block = '\n'.join(solid_text_lines)
        sanitized_text_block = solid_text_block.replace(u"\u00A0", ' ')  # Replace non-breaking spaces
        return sanitized_text_block.strip()

    def search(self) -> list[dict[str, str]]:
        pass
