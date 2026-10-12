import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    html_path = os.path.abspath("ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 1000})
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        pages = await page.query_selector_all(".page-landscape")
        print(f"Found {len(pages)} landscape pages")
        
        for i, p_elem in enumerate(pages):
            out_name = f"repair_track_a_playwright_p{i+1}.png"
            await p_elem.screenshot(path=out_name)
            print(f"Captured: {out_name}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
