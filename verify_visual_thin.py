import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Frontend Dashboard - Tab 1
        page = await browser.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        try:
            await page.goto('http://127.0.0.1:8888/frontend/templates/index.html', wait_until='networkidle')
        except:
            await page.goto('http://127.0.0.1:5500/frontend/templates/index.html', wait_until='networkidle')
            
        await page.screenshot(path='preview_dashboard_tab1.png', full_page=False)
        print("Captured preview_dashboard_tab1.png")
        
        # Switch to Tab 4 (17 Docs)
        tab4_btn = await page.query_selector('#tabBtn17Docs')
        if tab4_btn:
            await tab4_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path='preview_dashboard_tab4.png', full_page=False)
            print("Captured preview_dashboard_tab4.png")
            
        # 2. Check memo font weight
        page_memo = await browser.new_page(viewport={'width': 1200, 'height': 1600}, device_scale_factor=2)
        try:
            await page_memo.goto('http://127.0.0.1:8888/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html', wait_until='networkidle')
        except:
            await page_memo.goto('http://127.0.0.1:5500/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html', wait_until='networkidle')
            
        await page_memo.screenshot(path='preview_memo_thin.png', full_page=False)
        print("Captured preview_memo_thin.png")
        
        # Check computed font-weight of content paragraph vs title
        title_weight = await page_memo.evaluate("() => window.getComputedStyle(document.querySelector('.meta-label')).fontWeight")
        content_weight = await page_memo.evaluate("() => window.getComputedStyle(document.querySelector('.content-para')).fontWeight")
        meta_dots_weight = await page_memo.evaluate("() => window.getComputedStyle(document.querySelector('.meta-fill-dotted')).fontWeight")
        print(f"Computed weights -> Heading: {title_weight}, Content: {content_weight}, Dotted text: {meta_dots_weight}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
