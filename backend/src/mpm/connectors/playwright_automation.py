# backend/connectors/playwright_automation.py
from __future__ import annotations
import os
import time
from typing import Optional
from playwright.sync_api import sync_playwright, BrowserContext

class CookieCaptureResult(dict):
    """typed-ish container: { cookies, storage_state_path, user_agent }"""
    pass

class PlaywrightAutomation:
    def __init__(self, headless: bool = False, user_agent: Optional[str] = None):
        self.headless = headless
        self.user_agent = user_agent

    def _new_context(self, pw, proxy: Optional[str] = None) -> BrowserContext:
        launch_args = {"headless": self.headless}
        proxy_args = {}
        if proxy:
            # HTTP proxy: "http://user:pass@host:port"
            proxy_args["proxy"] = {"server": proxy}

        browser = pw.chromium.launch(**launch_args, **proxy_args)
        context_args = {}
        if self.user_agent:
            context_args["user_agent"] = self.user_agent
        return browser.new_context(**context_args)

    def capture_cookies(
        self,
        login_url: str,
        max_wait_ms: int = 120_000,
        proxy: Optional[str] = None,
        storage_state_dir: str = "./storage_states",
        storage_state_name: Optional[str] = None,
    ) -> CookieCaptureResult:
        """
        Opens a browser to login_url, waits up to max_wait_ms for manual login,
        then captures cookies + storage state for reuse.
        """
        os.makedirs(storage_state_dir, exist_ok=True)
        storage_state_name = storage_state_name or f"state_{int(time.time())}.json"
        storage_path = os.path.join(storage_state_dir, storage_state_name)

        with sync_playwright() as pw:
            ctx = self._new_context(pw, proxy=proxy)
            page = ctx.new_page()
            page.goto(login_url, wait_until="load")
            # Let the user complete MFA / QR / etc.
            page.wait_for_timeout(max_wait_ms)
            # Persist storage state (cookies + localStorage)
            ctx.storage_state(path=storage_path)
            cookies = ctx.cookies()
            ua = page.evaluate("() => navigator.userAgent")
            ctx.close()

        return CookieCaptureResult(
            cookies=cookies,
            storage_state_path=storage_path,
            user_agent=ua,
        )

    def load_storage_state(
        self,
        storage_state_path: str,
        proxy: Optional[str] = None,
    ) -> CookieCaptureResult:
        """Open a context using a saved storage_state to validate / refresh."""
        with sync_playwright() as pw:
            # Note: with 'storage_state', you pass it at context creation
            launch_args = {"headless": self.headless}
            proxy_args = {}
            if proxy:
                proxy_args["proxy"] = {"server": proxy}
            browser = pw.chromium.launch(**launch_args, **proxy_args)
            context = browser.new_context(storage_state=storage_state_path)
            page = context.new_page()
            ua = page.evaluate("() => navigator.userAgent")
            cookies = context.cookies()
            context.close()
        return CookieCaptureResult(
            cookies=cookies,
            storage_state_path=storage_state_path,
            user_agent=ua,
        )
