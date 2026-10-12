import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    sheets = page.locator(".sheet-container")
    count = sheets.count()
    print(f"Found {count} sheets.")
    
    for i in range(count):
        sheet = sheets.nth(i)
        out_name = f"gun_book_page_{i+1}_full.png"
        sheet.screenshot(path=os.path.join(output_dir, out_name))
        print(f"Saved {out_name}")

    browser.close()
