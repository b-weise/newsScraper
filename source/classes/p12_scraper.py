from source.classes.website_handler import WebsiteHandler
from source.interfaces.news_scraper_interface import NewsScraperInterface


class UninitializedWebsiteHandler(Exception):
    pass


class P12Scraper(NewsScraperInterface):
    def __init__(self):
        self.__host = 'https://www.pagina12.com.ar/'
        self.__wshandler = None

    @property
    def host(self):
        return self.__host

    async def initialize_website_handler(self):
        await self.destroy()
        self.__wshandler = WebsiteHandler()
        await self.__wshandler.initialize_random_useragent_context()
        await self.__wshandler.setup_robots_compliance(self.__host)

    def __check_website_handler_instance(self):
        if self.__wshandler is None:
            raise UninitializedWebsiteHandler(
                'WebsiteHandler is not initialized. Call the "initialize_website_handler" method first.')

    def get_article_url(self) -> str:
        pass

    async def get_title(self, url: str) -> str:
        self.__check_website_handler_instance()
        if url != self.__wshandler.page.url:
            await self.__wshandler.safe_goto(url)
        header_div = self.__wshandler.page.locator('div.article-header')
        title_h1 = header_div.locator('h1')
        title_text = await title_h1.inner_text()
        return title_text

    def get_date(self) -> str:
        pass

    def get_author(self) -> str:
        pass

    def get_image_url(self) -> str:
        pass

    def get_body(self) -> str:
        pass

    def search(self) -> list[dict[str, str]]:
        pass

    async def destroy(self):
        if self.__wshandler is not None:
            await self.__wshandler.destroy()
            self.__wshandler = None
