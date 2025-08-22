import { cookieCapture } from '../scripts/cookie_capture.js'
import fs from 'node:fs'
import path from 'node:path'

function arg(name: string, fallback?: string) {
    const i = process.argv.indexOf(`--${name}`)
    return i > -1 ? process.argv[i + 1] : fallback
}

async function main() {
    const login = arg('login')
    const out = arg('out', path.resolve('automation/playwright/storage_states/state.json'))
    const maxWaitMs = Number(arg('wait', '120000'))
    const headless = arg('headless', 'false') === 'true'
    const proxy = arg('proxy')
    const userAgent = arg('ua')

    if (!login) {
        console.error('Usage: npm run pw:capture -- --login <URL> [--out path] [--wait ms] [--headless true|false] [--proxy http://...] [--ua UA]')
        process.exit(1)
    }
    fs.mkdirSync(path.dirname(out), { recursive: true })
    const res = await cookieCapture({ loginUrl: login, outPath: out, maxWaitMs, headless, proxy, userAgent })
    console.log(JSON.stringify(res, null, 2))
}
main().catch(e => { console.error(e); process.exit(1) })
