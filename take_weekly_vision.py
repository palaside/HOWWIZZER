import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # device_scale_factor=2.5 renders at 240-300 DPI print-crisp resolution
        context = await browser.new_context(
            viewport={"width": 1200, "height": 1700},
            device_scale_factor=2.5
        )
        page = await context.new_page()
        
        file_path = "file:///" + os.path.abspath("references/approved_weekly_inspection/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html").replace("\\", "/")
        await page.goto(file_path, wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Locate all page containers (.page-portrait and .page-landscape)
        pages = await page.query_selector_all(".page-portrait, .page-landscape")
        print(f"Found {len(pages)} pages")
        
        artifacts_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\54977ce8-2a4a-46cc-b64e-4df942170631"
        for i, p_elem in enumerate(pages):
            out_img = os.path.join(artifacts_dir, f"weekly_crisp_p{i+1}.png")
            await p_elem.screenshot(path=out_img)
            print(f"Captured crisp: {out_img}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

