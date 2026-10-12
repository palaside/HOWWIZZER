import asyncio
from playwright.async_api import async_playwright
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    html_path = os.path.abspath("บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 1600})
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        pages = await page.query_selector_all(".page-portrait")
        print(f"Found {len(pages)} portrait pages")
        
        for i, p_elem in enumerate(pages):
            out_name = f"gen_insp_rebuild_p{i+1}.png"
            await p_elem.screenshot(path=out_name)
            print(f"Captured: {out_name}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
