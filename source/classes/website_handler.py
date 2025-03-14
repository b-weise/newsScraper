import sys
import traceback

from playwright.async_api import async_playwright


class WebsiteHandler:
    def __init__(self,
                 ):
        self.page = None

    async def initialize_playwright(self):
        try:
            playwright = await async_playwright().start()
            browser = playwright.chromium
            browser_context = await browser.launch_persistent_context('', headless=False)
            self.page = browser_context.pages[0]
        except:
            print(''.join(traceback.format_exception(*sys.exc_info())))

    async def destroy(self):
        if self.page is not None:
            await self.page.close()
            self.page = None
