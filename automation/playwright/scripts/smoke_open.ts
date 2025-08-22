import { chromium } from 'playwright'
export async function smokeOpen(url = 'https://example.com') {
    const browser = await chromium.launch()
    const page = await browser.newPage()
    await page.goto(url)
    const title = await page.title()
    await browser.close()
    return title
}
