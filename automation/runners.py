from playwright.async_api import async_playwright


async def run_cookie_capture(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create a new incognito-like context
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        cookies = await context.cookies()
        await browser.close()
        return {"cookies": cookies}


async def run_screenshot(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        path = "screenshot.png"
        await page.screenshot(path=path)
        await browser.close()
        return {"screenshot_path": path}
