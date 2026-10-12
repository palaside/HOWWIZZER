import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/ทบ_468_204_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. Full page 1 screenshot
    sheet1 = page.locator(".sheet-container").first
    sheet1.screenshot(path=os.path.join(output_dir, "weapon_page_1_full.png"))
    print("Saved weapon_page_1_full.png")

    # 2. Table Header and Top section (checking 1 Enter gap & "หมายเลข" 20%)
    top_sec = page.locator(".sheet-container").first
    # Crop top part: title + thead + first few rows
    thead = page.locator(".military-weapon-table thead").first
    thead.screenshot(path=os.path.join(output_dir, "weapon_header_crop.png"))
    print("Saved weapon_header_crop.png")

    # 3. Cert and Sig block crop
    cert_sig = page.locator(".cert-cell").first
    cert_sig.screenshot(path=os.path.join(output_dir, "weapon_cert_sig_crop.png"))
    print("Saved weapon_cert_sig_crop.png")

    # 4. Page 2 full
    sheet2 = page.locator(".sheet-container").nth(1)
    sheet2.screenshot(path=os.path.join(output_dir, "weapon_page_2_full.png"))
    print("Saved weapon_page_2_full.png")

    # 5. Page 2 Table Rows Crop (Showing 9 rows of กล้องเล็งพาโนรามิค centered)
    table2 = page.locator(".sheet-container:nth-of-type(2) .military-weapon-table").first
    table2.screenshot(path=os.path.join(output_dir, "weapon_page_2_table_crop.png"))
    print("Saved weapon_page_2_table_crop.png")

    # 6. Page 1 Table Rows Crop
    table1 = page.locator(".sheet-container:nth-of-type(1) .military-weapon-table").first
    table1.screenshot(path=os.path.join(output_dir, "weapon_page_1_table_crop.png"))
    print("Saved weapon_page_1_table_crop.png")

    browser.close()
