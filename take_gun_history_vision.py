import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/ประวัติการใช้อาวุธ_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. Full Page 1 screenshot
    sheet1 = page.locator(".sheet-container").first
    sheet1.screenshot(path=os.path.join(output_dir, "gun_history_page_1_full.png"))
    print("Saved gun_history_page_1_full.png")

    # 2. Table crop on Page 1
    table1 = page.locator(".sheet-container:nth-of-type(1) .gun-history-table").first
    table1.screenshot(path=os.path.join(output_dir, "gun_history_table_crop.png"))
    print("Saved gun_history_table_crop.png")

    # 3. Signature & Firing record crop
    sig_area = page.locator(".sheet-container:nth-of-type(1) .sig-block").first
    sig_area.screenshot(path=os.path.join(output_dir, "gun_history_sig_crop.png"))
    print("Saved gun_history_sig_crop.png")

    # 4. Full Page 2 screenshot
    sheet2 = page.locator(".sheet-container").nth(1)
    sheet2.screenshot(path=os.path.join(output_dir, "gun_history_page_2_full.png"))
    print("Saved gun_history_page_2_full.png")

    browser.close()
