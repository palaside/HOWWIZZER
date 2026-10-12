import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # US Legal Landscape viewport (355.6mm x 215.9mm = ~1344 x 816 px at 96 DPI)
    page = browser.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. Page 1 Full
    page_1 = page.locator("#page-1")
    page_1.screenshot(path=os.path.join(output_dir, "survey_sp_page_1_full.png"))
    print("Saved survey_sp_page_1_full.png")
    
    # 2. Page 2 Full
    page_2 = page.locator("#page-2")
    page_2.screenshot(path=os.path.join(output_dir, "survey_sp_page_2_full.png"))
    print("Saved survey_sp_page_2_full.png")
    
    # 3. Page 12 Full (Last page)
    page_12 = page.locator("#page-12")
    page_12.screenshot(path=os.path.join(output_dir, "survey_sp_page_12_full.png"))
    print("Saved survey_sp_page_12_full.png")
    
    # 4. Crop of Top Card on Page 1
    top_card_p1 = page.locator("#page-1 .top-card")
    top_card_p1.screenshot(path=os.path.join(output_dir, "survey_sp_top_card_crop.png"))
    print("Saved survey_sp_top_card_crop.png")
    
    # 5. Crop of Slip 1 on Page 1
    slip_1_p1 = page.locator("#page-1 .top-card .slip-1")
    slip_1_p1.screenshot(path=os.path.join(output_dir, "survey_sp_slip_1_crop.png"))
    print("Saved survey_sp_slip_1_crop.png")

    # 6. Crop of Meta Box on Page 1
    meta_p1 = page.locator("#page-1 .top-card .slip-1 .meta-box-table")
    meta_p1.screenshot(path=os.path.join(output_dir, "survey_sp_meta_crop.png"))
    print("Saved survey_sp_meta_crop.png")

    browser.close()

print("All screenshots taken successfully!")
