import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600}, device_scale_factor=2.5)
        
        url = 'http://127.0.0.1:8888/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html'
        await page.goto(url, wait_until='networkidle')
        
        # Verify ZWS presence in body text
        has_zws = await page.evaluate("() => document.body.innerText.includes('\\u200b')")
        print(f"ZWS Detected in DOM: {has_zws}")
        
        # Extract paragraph text to inspect segmentation
        para_text = await page.evaluate("() => document.querySelector('.content-para').innerText")
        print(f"Paragraph length: {len(para_text)} characters")
        print(f"ZWS count in paragraph: {para_text.count('\\u200b')}")
        
        await page.screenshot(path='preview_zws_memo.png', full_page=False)
        print("Captured preview_zws_memo.png at 300 DPI")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
