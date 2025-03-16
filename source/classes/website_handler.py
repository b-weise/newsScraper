import fnmatch
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright, APIResponse


class NonCompliantURL(Exception):
    pass


class UninitializedPlaywright(Exception):
    pass


class WebsiteHandler:
    def __init__(self, headless: bool = True, robots_useragent_key: str = 'user-agent',
                 robots_allow_key: str = 'allow', robots_disallow_key: str = 'disallow',
                 common_useragents_url: str = 'https://www.useragents.me/'):
        self.headless = headless
        self.robots_useragent_key = robots_useragent_key
        self.robots_allow_key = robots_allow_key
        self.robots_disallow_key = robots_disallow_key
        self.common_useragents_url = common_useragents_url
        self.__page = None
        self.api_request_context = None

    async def initialize_playwright(self):
        playwright = await async_playwright().start()
        browser = playwright.chromium
        browser_context = await browser.launch_persistent_context('', headless=self.headless)
        self.api_request_context = browser_context.request
        self.__page = browser_context.pages[0]

    def __check_playwright_instance(self):
        if self.__page is None:
            raise UninitializedPlaywright('Playwright is not initialized. Call the "initialize_playwright" method first.')

    @property
    def page(self):
        self.__check_playwright_instance()
        return self.__page

    async def get_request(self, url: str) -> APIResponse:
        self.__check_playwright_instance()
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

    def is_compliant_url(self, url: str, parsed_robots: dict[str, list[str]]) -> bool:
        # criteria based on: https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt
        allowed_paths = parsed_robots[self.robots_allow_key]
        disallowed_paths = parsed_robots[self.robots_disallow_key]
        url_path = urlparse(url).path
        all_paths = allowed_paths + disallowed_paths
        all_paths_sorted = sorted(all_paths,
                                  key=lambda path: len(Path(path).resolve().parents))  # Sorted by specificity
        is_compliant = True
        for path in all_paths_sorted:
            path_pattern = path
            if path[-1] != '*':
                path_pattern += '*'
            if fnmatch.fnmatch(url_path, path_pattern):
                is_compliant = path in allowed_paths
        return is_compliant

    async def safe_goto(self, url: str, parsed_robots: dict[str, list[str]]):
        self.__check_playwright_instance()
        if not self.is_compliant_url(url, parsed_robots):
            raise NonCompliantURL(f'The URL "{url}" is disallowed by robots.txt rules.')
        await self.__page.goto(url)

    async def get_common_useragent(self) -> str:
        await self.__page.goto(self.common_useragents_url)
        json_parent_div = self.__page.locator('#most-common-desktop-useragents-json-csv')
        json_div = json_parent_div.locator('div', has_text='JSON')
        json_textarea = json_div.locator('textarea')
        json_text = await json_textarea.input_value()
        parsed_json = json.loads(json_text)
        return parsed_json[0]['ua']

    async def destroy(self):
        if self.__page is not None:
            await self.__page.close()
            self.__page = None
