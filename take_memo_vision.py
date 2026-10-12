import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # A4 portrait viewport
    page = browser.new_page(viewport={"width": 1000, "height": 1350}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)

    # 1. Full page
    sheet = page.locator("#memo-page-1")
    sheet.screenshot(path=os.path.join(output_dir, "memo_latest_rebuild_full.png"))
    print("Saved memo_latest_rebuild_full.png")

    # 2. Crop of Header & Metadata
    header = page.locator(".header-container")
    header.screenshot(path=os.path.join(output_dir, "memo_latest_header_crop.png"))
    print("Saved memo_latest_header_crop.png")

    # 3. Crop of Metadata section
    meta = page.locator(".meta-section")
    meta.screenshot(path=os.path.join(output_dir, "memo_latest_meta_crop.png"))
    print("Saved memo_latest_meta_crop.png")

    # 4. Crop of Signature block
    sig = page.locator(".signature-container")
    sig.screenshot(path=os.path.join(output_dir, "memo_latest_sig_crop.png"))
    print("Saved memo_latest_sig_crop.png")

    browser.close()

print("All memo screenshots taken successfully!")
