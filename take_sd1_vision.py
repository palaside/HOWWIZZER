import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 1900})
        
        file_path = "file:///" + os.path.abspath("แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html").replace("\\", "/")
        await page.goto(file_path, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Locate all page containers (.page-portrait and .page-landscape)
        pages = await page.query_selector_all(".page-portrait, .page-landscape")
        print(f"Found {len(pages)} pages")
        
        artifacts_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
        for i, p_elem in enumerate(pages):
            out_img = os.path.join(artifacts_dir, f"sd1_playwright_p{i+1}.png")
            await p_elem.screenshot(path=out_img)
            print(f"Captured: {out_img}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
