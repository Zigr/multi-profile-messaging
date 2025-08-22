import { smokeOpen } from '../scripts/smoke_open.js'

async function main() {
    const script = process.argv[2]
    if (script === 'smoke_open') {
        const url = process.argv[3] || 'https://example.com'
        const title = await smokeOpen(url)
        console.log('Title:', title)
        return
    }
    console.error('Unknown script. Try: smoke_open <url>')
    process.exit(1)
}
main().catch(e => { console.error(e); process.exit(1) })
