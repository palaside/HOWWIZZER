import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Frontend Dashboard with Photo Upload Card
        page = await browser.new_page(viewport={'width': 1440, 'height': 1050}, device_scale_factor=2)
        await page.goto('http://127.0.0.1:8888/frontend/templates/index.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Scroll down to inspection photos card
        photo_card = await page.query_selector('#inspectionPhotosGrid')
        if photo_card:
            await photo_card.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)
            await page.screenshot(path='preview_dashboard_photos_card.png', full_page=False)
            print("Captured preview_dashboard_photos_card.png")
            
        # 2. Document Page 4 (Form SD.1 inspection photos)
        page_sd1 = await browser.new_page(viewport={'width': 1200, 'height': 1600}, device_scale_factor=2)
        await page_sd1.goto('http://127.0.0.1:8888/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html', wait_until='networkidle')
        await page_sd1.wait_for_timeout(500)
        
        # Find 4th page (.page-portrait with photo-grid)
        pages = await page_sd1.query_selector_all('.page-portrait')
        for i, pg in enumerate(pages):
            grid = await pg.query_selector('.photo-grid')
            if grid:
                await pg.screenshot(path='preview_sd1_page4_photos.png')
                print(f"Captured Page {i+1} preview_sd1_page4_photos.png")
                break
                
        await browser.close()
        print("Visual verification complete!")

if __name__ == '__main__':
    asyncio.run(verify())
