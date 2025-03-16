from source.interfaces.news_scraper_interface import NewsScraperInterface


class P12Scraper(NewsScraperInterface):
    def __init__(self):
        self.__host = ''

    @property
    def host(self):
        return self.__host

    def get_article_url(self) -> str:
        pass

    def get_title(self) -> str:
        pass

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
        pass
