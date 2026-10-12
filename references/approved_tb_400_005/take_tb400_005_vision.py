import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # A5 Portrait viewport at 2x scale
    page = browser.new_page(viewport={"width": 1000, "height": 1400}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. TOC Page
    p_toc = page.locator("#page-toc")
    if p_toc.count() > 0:
        p_toc.screenshot(path=os.path.join(output_dir, "tb400_005_page_toc.png"))
        print("Saved tb400_005_page_toc.png")
        
        # Crop of Cert & Signature
        cert = page.locator("#page-toc .cert-box")
        if cert.count() > 0:
            cert.screenshot(path=os.path.join(output_dir, "tb400_005_cert_sig_crop.png"))
            print("Saved tb400_005_cert_sig_crop.png")
            
        sig_block = page.locator("#page-toc .sig-container")
        if sig_block.count() > 0:
            sig_block.screenshot(path=os.path.join(output_dir, "tb400_005_sig_only_crop.png"))
            print("Saved tb400_005_sig_only_crop.png")
    
    # 2. Card 1 Front
    card_1_f = page.locator("#card-1-front")
    if card_1_f.count() > 0:
        card_1_f.screenshot(path=os.path.join(output_dir, "tb400_005_card_1_front.png"))
        print("Saved tb400_005_card_1_front.png")
        
        # Crop of Card 1 footer spec
        footer_spec = page.locator("#card-1-front .footer-spec-table")
        if footer_spec.count() > 0:
            footer_spec.screenshot(path=os.path.join(output_dir, "tb400_005_card_1_footer_crop.png"))
            print("Saved tb400_005_card_1_footer_crop.png")
        
    # 3. Card 1 Back
    card_1_b = page.locator("#card-1-back")
    if card_1_b.count() > 0:
        card_1_b.screenshot(path=os.path.join(output_dir, "tb400_005_card_1_back.png"))
        print("Saved tb400_005_card_1_back.png")
        
    # 4. Card 4 Front (ปบค. 95)
    card_4_f = page.locator("#card-4-front")
    if card_4_f.count() > 0:
        card_4_f.screenshot(path=os.path.join(output_dir, "tb400_005_card_4_front.png"))
        print("Saved tb400_005_card_4_front.png")

    browser.close()

print("All visual QA screenshots taken successfully!")
