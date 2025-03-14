from playwright.async_api import async_playwright, APIResponse
import re


class WebsiteHandler:
    def __init__(self, headless: bool = True):
        self.headless = headless
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

    @staticmethod
    def parse_robots_file(robots_content: str) -> dict[str, list[str]]:
        allow_key = 'allow'
        disallow_key = 'disallow'
        parsed_content = {
            f'{allow_key}': [],
            f'{disallow_key}': [],
        }
        for line in robots_content.split('\n'):
            line = line.strip()
            for keyword in [allow_key, disallow_key]:
                if re.match(f'^{keyword}', line, flags=re.I) is not None:
                    line_pieces = re.split(r'\s+', line)
                    parsed_content[keyword] += line_pieces[1:]
        return parsed_content

    async def destroy(self):
        if self.page is not None:
            await self.page.close()
            self.page = None
