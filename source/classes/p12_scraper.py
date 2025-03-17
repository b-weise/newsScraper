import asyncio
import re
from typing import Optional
from urllib.parse import urlparse, urlunparse, quote

from playwright.async_api import Page

from source.classes.base_news_scraper import BaseNewsScraper


class P12Scraper(BaseNewsScraper):
    def __init__(self):
        super().__init__()
        self._host = 'https://www.pagina12.com.ar/'
        self.__author_text_prefix = 'Por'

    async def get_title(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        header_div = page.locator('div.article-header')
        title_h1 = header_div.locator('h1')
        title_text = await title_h1.inner_text()
        return self._sanitize_text(title_text)

    async def get_date(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        desktop_only_div = page.locator('div.hide-on-mobile')
        article_info_div = desktop_only_div.locator('div.article-info')
        date_time = article_info_div.locator('time')
        date_text = await date_time.inner_text()
        return self._sanitize_text(date_text)

    async def get_author(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        header_div = page.locator('div.article-header')
        author_div = header_div.locator('div.author')
        author_a = author_div.locator('a')
        author_text = await author_a.inner_text()
        author_text = re.sub(f'^\\s*{self.__author_text_prefix}\\s+', '', author_text)
        return self._sanitize_text(author_text)

    async def get_image_url(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        main_image_div = page.locator('div.article-main-image')
        image_img = main_image_div.locator('img')
        image_src = await image_img.get_attribute('src')
        url_scheme, url_hostname, url_path, _, _, _ = list(urlparse(image_src))
        image_url = str(urlunparse([url_scheme, url_hostname, url_path, '', '', '']))
        return image_url

    async def get_body(self, url: Optional[str] = None, page: Optional[Page] = None) -> str:
        self._check_website_handler_instance()
        page = page or self._wshandler.page
        await self._navigate_if_necessary(url=url, page=page)
        main_content_div = page.locator('div.article-main-content')
        article_text_div = main_content_div.locator('div.article-text')
        article_text = await article_text_div.inner_text()
        return self._sanitize_text(article_text)

    async def search(self, keyword: str) -> list[dict[str, str]]:
        self._check_website_handler_instance()
        url_scheme, url_hostname, _, _, _, _ = list(urlparse(self._host))

        def build_search_url():
            sanitized_keyword = quote(keyword)
            url_path = '/buscar'
            url_query = f'q={sanitized_keyword}'
            full_url = str(urlunparse([url_scheme, url_hostname, url_path, '', url_query, '']))
            return full_url

        search_url = build_search_url()
        await self._navigate_if_necessary(search_url)

        async def get_paths():
            articles_paths = []
            article_item_header_divs = self._wshandler.page.locator('div.article-item__header')
            for item in await article_item_header_divs.all():
                url_a = item.locator('a')
                url_href = await url_a.get_attribute('href')
                articles_paths.append(url_href)
            return articles_paths

        results = []
        articles_paths = await get_paths()
        pages = []

        async def build_result(article_path):
            article_url = str(urlunparse([url_scheme, url_hostname, article_path, '', '', '']))
            result = {'article_url': article_url}
            new_page = await self._wshandler.get_new_page(article_url)

            async def store_result(key, getter_coro):
                result[key] = await getter_coro

            await asyncio.gather(store_result('title', self.get_title(page=new_page)),
                                 store_result('date', self.get_date(page=new_page)),
                                 store_result('author', self.get_author(page=new_page)),
                                 store_result('image_url', self.get_image_url(page=new_page)),
                                 store_result('body', self.get_body(page=new_page)))
            results.append(result)
            pages.append(new_page)

        await asyncio.gather(*[build_result(path) for path in articles_paths])

        for page in pages:
            page.close()

        return results
