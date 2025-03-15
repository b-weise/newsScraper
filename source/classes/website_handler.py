from playwright.async_api import async_playwright, APIResponse
import re


class WebsiteHandler:
    def __init__(self,
                 headless: bool = True,
                 robots_useragent_key: str = 'user-agent',
                 robots_allow_key: str = 'allow',
                 robots_disallow_key: str = 'disallow',
                 ):
        self.headless = headless
        self.robots_useragent_key = robots_useragent_key
        self.robots_allow_key = robots_allow_key
        self.robots_disallow_key = robots_disallow_key
        self.page = None
        self.api_request_context = None

    async def initialize_playwright(self):
        playwright = await async_playwright().start()
        browser = playwright.chromium
        browser_context = await browser.launch_persistent_context('', headless=self.headless)
        self.api_request_context = browser_context.request
        self.page = browser_context.pages[0]

    async def request_get(self, url: str) -> APIResponse:
        response = await self.api_request_context.get(url)
        return response

    def parse_robots_file(self, robots_content: str) -> dict[str, list[str]]:
        def split_line(line: str) -> list[str]:
            return re.split(r'\s+', line)

        def is_keyword_present(line: str, keyword: str) -> bool:
            return re.match(f'^{keyword}', line, flags=re.I) is not None

        useragent_key = self.robots_useragent_key
        allow_key = self.robots_allow_key
        disallow_key = self.robots_disallow_key
        parsed_content = {
            f'{allow_key}': [],
            f'{disallow_key}': [],
        }
        is_relevant_useragent_space = False
        was_relevant_useragent_already_extracted = False
        for line in robots_content.split('\n'):
            line = line.strip()
            if is_keyword_present(line, useragent_key):
                line_pieces = split_line(line)
                line_pieces = line_pieces[1:]  # Discard keyword item
                is_relevant_useragent_space = any(map(lambda token: token == '*', line_pieces))
            if is_relevant_useragent_space:
                was_relevant_useragent_already_extracted = True
                for keyword in [allow_key, disallow_key]:
                    if is_keyword_present(line, keyword):
                        line_pieces = split_line(line)
                        line_pieces = line_pieces[1:]  # Discard keyword item
                        parsed_content[keyword] += line_pieces
            if was_relevant_useragent_already_extracted and not is_relevant_useragent_space:
                break
        return parsed_content

    async def destroy(self):
        if self.page is not None:
            await self.page.close()
            self.page = None
