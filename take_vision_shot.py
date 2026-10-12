import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/ทบ_400_012_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. First data table with unit column (showing กระบอก, ชุด)
    table_p1 = page.locator(".military-data-table tbody").first
    table_p1.screenshot(path=os.path.join(output_dir, "vision_table_body_p1.png"))
    print("Saved table_p1 screenshot")
    
    # 2. Second page data table (showing กระโจม)
    table_p2 = page.locator(".military-data-table tbody").nth(1)
    table_p2.screenshot(path=os.path.join(output_dir, "vision_table_body_p2.png"))
    print("Saved table_p2 screenshot")
    
    # 3. Admin box with 1 enter distance
    admin_box = page.locator(".hdr-col-admin").first
    admin_box.screenshot(path=os.path.join(output_dir, "vision_admin_box_enter.png"))
    print("Saved admin_box screenshot")

    # 4. Table header
    thead = page.locator(".military-data-table thead").first
    thead.screenshot(path=os.path.join(output_dir, "vision_table_header_check.png"))
    print("Saved thead screenshot")

    browser.close()
