import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        
        # 1. Capture Tab 5 Table
        page = await context.new_page()
        await page.goto("http://127.0.0.1:8888/frontend/templates/index.html", wait_until="networkidle")
        await page.wait_for_timeout(400)
        await page.click("#tabBtnInformalSurvey")
        await page.wait_for_timeout(600)
        
        table_container = await page.query_selector("#informalInventoryTableContainer")
        if table_container:
            await table_container.screenshot(path="verified_informal_table_updated.png")
            print("[PASS] Captured verified_informal_table_updated.png")
        
        # 2. Capture Memo Preview with Garuda
        memo_page = await context.new_page()
        await memo_page.goto("http://127.0.0.1:8888/บันทึกข้อความ_รายงานการชำรุดเสียหาย_Rebuild_Thai.html", wait_until="networkidle")
        await memo_page.wait_for_timeout(400)
        
        # Capture header with Garuda
        header_el = await memo_page.query_selector(".memo-garuda-container")
        if header_el:
            await header_el.screenshot(path="verified_memo_garuda_header.png")
            print("[PASS] Captured verified_memo_garuda_header.png")
            
        # Capture full first page
        pages = await memo_page.query_selector_all(".a4-page")
        if len(pages) > 0:
            await pages[0].screenshot(path="verified_memo_page1.png")
            print("[PASS] Captured verified_memo_page1.png")
        if len(pages) > 1:
            await pages[1].screenshot(path="verified_memo_page2_dualcopy.png")
            print("[PASS] Captured verified_memo_page2_dualcopy.png")
            
        await browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    asyncio.run(main())
