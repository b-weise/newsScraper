import fnmatch
import json
import random
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, urlunparse

from playwright.async_api import async_playwright, APIResponse, Page


class NonCompliantURL(Exception):
    pass


class UninitializedPlaywright(Exception):
    pass


class WebsiteHandler:
    """
    Handles fundamental website interactions, including robots.txt compliance,
    user-agent handling and browser tab management.
    """
    def __init__(self, headless: bool = True, robots_useragent_key: str = 'user-agent',
                 robots_allow_key: str = 'allow', robots_disallow_key: str = 'disallow',
                 default_timeout_sec: int = 5, default_navigation_timeout_sec: int = 25):
        self.__headless = headless
        self.__robots_useragent_key = robots_useragent_key
        self.__robots_allow_key = robots_allow_key
        self.__robots_disallow_key = robots_disallow_key
        self.__default_timeout_sec = default_timeout_sec
        self.__default_navigation_timeout_sec = default_navigation_timeout_sec
        self.__common_useragents_url = 'https://www.useragents.me/'
        self.__page = None
        self.__browser_context = None
        self.__parsed_robots = None

    async def initialize_playwright(self, user_agent: Optional[str] = None):
        """
        Initializes Playwright and sets up browser context.
        Must be called externally as __init__() cannot invoke asynchronous methods.
        Destroys any existing context when invoked.
        """
        await self.destroy()
        playwright = await async_playwright().start()
        browser = playwright.chromium
        self.__browser_context = await browser.launch_persistent_context('', headless=self.__headless,
                                                                         user_agent=user_agent)
        self.__page = self.__browser_context.pages[0]
        self.__setup_page(self.__page)

    def __check_playwright_instance(self):
        """
        Ensures that Playwright has been initialized.
        """
        if self.__browser_context is None:
            raise UninitializedPlaywright(
                'Playwright is not initialized. Call the "initialize_playwright" method first.')

    def __setup_page(self, page: Page):
        """
        Sets page configurations such as default timeouts.
        """
        page.set_default_timeout(self.__default_timeout_sec * 1000)
        page.set_default_navigation_timeout(self.__default_navigation_timeout_sec * 1000)

    @property
    def page(self):
        """
        The main page launched during browser context initialization.
        """
        self.__check_playwright_instance()
        return self.__page

    async def get_request(self, url: str) -> APIResponse:
        """
        Performs an HTTP GET request and returns the response object.
        """
        self.__check_playwright_instance()
        response = await self.__browser_context.request.get(url)
        return response

    def parse_robots_file(self, robots_content: str) -> dict[str, list[str]]:
        """
        Parses robots.txt. Only loads generic user-agent ('User-agent *') directives.
        Parsing logic follows these references:
            https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt#create_rules
            https://en.wikipedia.org/wiki/Robots.txt#Examples
        """
        def split_line(line: str) -> list[str]:
            """
            Splits a text line by whitespace.
            """
            return re.split(r'\s+', line)

        def is_directive_present(directive: str, line: str) -> bool:
            """
            Performs a case-insensitive search for a robots.txt directive.
            Matches against the beginning of the line and partial words,
            e.g. the token 'allow' matches 'allowed'.
            """
            return re.match(f'^{directive}', line, flags=re.I) is not None

        useragent_key = self.__robots_useragent_key
        allow_key = self.__robots_allow_key
        disallow_key = self.__robots_disallow_key
        parsed_content = {
            f'{allow_key}': [],
            f'{disallow_key}': [],
        }
        is_relevant_useragent_space = False
        was_relevant_useragent_already_extracted = False
        for line in robots_content.split('\n'):
            line = line.strip()
            if is_directive_present(useragent_key, line):
                line_pieces = split_line(line)
                line_pieces = line_pieces[1:]  # Discard keyword item
                is_relevant_useragent_space = any(map(lambda token: token == '*', line_pieces))
            if is_relevant_useragent_space:
                was_relevant_useragent_already_extracted = True
                for directive in [allow_key, disallow_key]:
                    if is_directive_present(directive, line):
                        line_pieces = split_line(line)
                        line_pieces = line_pieces[1:]  # Discard keyword item
                        parsed_content[directive] += line_pieces
            if was_relevant_useragent_already_extracted and not is_relevant_useragent_space:
                break
        return parsed_content

    def is_compliant_url(self, url: str, parsed_robots: Optional[dict[str, list[str]]] = None) -> bool:
        """
        Evaluates whether the given URL follows loaded robots.txt rules.
        If no robots.txt is loaded, all URLs are allowed.
        """
        parsed_robots = parsed_robots or {}
        allowed_paths = parsed_robots.get(self.__robots_allow_key, [])
        disallowed_paths = parsed_robots.get(self.__robots_disallow_key, [])
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

    async def safe_goto(self, url: str, parsed_robots: Optional[dict[str, list[str]]] = None,
                        page: Optional[Page] = None):
        """
        Navigates to the given URL only if it complies with host's robots.txt rules,
        assuming there's a robots file loaded.
        """
        parsed_robots = parsed_robots or self.__parsed_robots
        self.__check_playwright_instance()
        if not self.is_compliant_url(url, parsed_robots):
            raise NonCompliantURL(f'The URL "{url}" is disallowed by robots.txt rules.')
        page = page or self.__page
        await page.goto(url)

    async def get_common_useragent(self) -> str:
        """
        Navigates to __common_useragents_url, scrapes commonly found user-agents published there,
        and returns one chosen randomly.
        """
        self.__check_playwright_instance()
        await self.__page.goto(self.__common_useragents_url)
        json_parent_div = self.__page.locator('#most-common-desktop-useragents-json-csv')
        json_div = json_parent_div.locator('div', has_text='JSON')
        json_textarea = json_div.locator('textarea')
        json_text = await json_textarea.input_value()
        parsed_json = json.loads(json_text)
        random_useragent = random.choice(parsed_json)['ua']
        return random_useragent

    async def get_current_useragent(self):
        """
        Returns the user-agent of the current browser context.
        """
        self.__check_playwright_instance()
        useragent = await self.__page.evaluate('() => navigator.userAgent')
        return useragent

    async def change_useragent(self):
        """
        Re-initializes the browser context with a different, random user-agent.
        """
        new_useragent = await self.get_common_useragent()
        print(f'New user-agent: {new_useragent}')
        await self.initialize_playwright(user_agent=new_useragent)

    async def initialize_random_useragent_context(self):
        """
        Launches the original Playwright browser context to scrape a commonly used user-agent,
        then re-initializes the browser context with the retrieved user-agent.
        """
        await self.initialize_playwright()
        await self.change_useragent()

    async def setup_robots_compliance(self, sample_url: str):
        """
        Downloads and parses the robots.txt file from the host of the given sample_url.
        """
        url_scheme, url_hostname, _, _, _, _ = list(urlparse(sample_url))
        robots_url = str(urlunparse([url_scheme, url_hostname, '/robots.txt', '', '', '']))
        robots_response = await self.get_request(robots_url)
        robots_contents = await robots_response.text()
        parsed_robots = self.parse_robots_file(robots_contents)
        self.__parsed_robots = parsed_robots

    async def get_new_page(self, url: Optional[str] = None, parsed_robots: Optional[dict[str, list[str]]] = None):
        """
        Opens, configures and returns a new page. If URL is provided, navigates to it.
        """
        self.__check_playwright_instance()
        new_page = await self.__browser_context.new_page()
        self.__setup_page(new_page)
        if url is not None:
            await self.safe_goto(url=url, parsed_robots=parsed_robots, page=new_page)
        return new_page

    async def destroy(self):
        """
        Releases allocated resources.
        """
        if self.__browser_context is not None:
            await self.__browser_context.close()
            self.__page = None
            self.__browser_context = None
