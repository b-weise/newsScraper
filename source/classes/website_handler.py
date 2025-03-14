from playwright.async_api import async_playwright


class WebsiteHandler:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.page = None

    async def initialize_playwright(self):
        playwright = await async_playwright().start()
        browser = playwright.chromium
        browser_context = await browser.launch_persistent_context('', headless=self.headless)
        self.page = browser_context.pages[0]

    async def destroy(self):
        if self.page is not None:
            await self.page.close()
            self.page = None
