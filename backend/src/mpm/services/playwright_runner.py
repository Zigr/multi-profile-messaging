from playwright.async_api import async_playwright
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models

async def run_cookie_capture_and_store(url: str, profile_id: int, db: AsyncSession):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        cookies = await context.cookies()
        await browser.close()

        # Fetch profile and update cookies
        result = await db.execute(select(models.Profile).where(models.Profile.id == profile_id))
        profile = result.scalar_one_or_none()
        if not profile:
            raise ValueError(f"Profile with id={profile_id} not found")

        profile.cookies = cookies
        await db.commit()
        await db.refresh(profile)

        return profile
