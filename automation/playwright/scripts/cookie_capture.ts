import { chromium, type BrowserContext } from 'playwright'

export async function cookieCapture(opts: {
    loginUrl: string
    headless?: boolean
    maxWaitMs?: number
    userAgent?: string
    proxy?: string
    outPath: string
}) {
    const { loginUrl, headless = false, maxWaitMs = 120_000, userAgent, proxy, outPath } = opts
    const browser = await chromium.launch({
        headless,
        proxy: proxy ? { server: proxy } : undefined,
    })
    const context = await browser.newContext({
        userAgent: userAgent || undefined,
    })
    const page = await context.newPage()
    await page.goto(loginUrl, { waitUntil: 'load' })

    // Give operator time to complete login (QR/MFA/etc.)
    await page.waitForTimeout(maxWaitMs)

    await context.storageState({ path: outPath })
    const cookies = await context.cookies()
    const ua = await page.evaluate(() => navigator.userAgent)

    await browser.close()
    return { cookies, storage_state_path: outPath, user_agent: ua }
}
