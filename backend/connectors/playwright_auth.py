from playwright.sync_api import sync_playwright
import json

class PlaywrightAuth:
    def __init__(self, headless: bool = False):
        self.headless = headless

    def login(self, login_url: str) -> str:
        """
        Opens a browser window, navigates to `login_url`,
        waits for the user to complete login, then captures cookies.
        Returns JSON-encoded cookies string.
        """
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=self.headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(login_url)

        # Wait up to 2 minutes for manual login
        page.wait_for_timeout(120_000)

        cookies = context.cookies()
        browser.close()
        playwright.stop()
        return json.dumps(cookies)
