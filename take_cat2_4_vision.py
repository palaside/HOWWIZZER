import os
from playwright.sync_api import sync_playwright

output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"
html_path = r"d:/Project/WEPAPP/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # A5 Portrait viewport at 2x scale
    page = browser.new_page(viewport={"width": 1000, "height": 1400}, device_scale_factor=2)
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(1000)
    
    # 1. Cover Page
    p_cov = page.locator("#page-cover")
    if p_cov.count() > 0:
        p_cov.screenshot(path=os.path.join(output_dir, "cat2_4_page_cover.png"))
        print("Saved cat2_4_page_cover.png")
        
    # 2. Certification Page
    p_cert = page.locator("#page-cert")
    if p_cert.count() > 0:
        p_cert.screenshot(path=os.path.join(output_dir, "cat2_4_page_cert.png"))
        print("Saved cat2_4_page_cert.png")
        
        # Crop of Signature
        sig = page.locator("#page-cert .sig-container")
        if sig.count() > 0:
            sig.screenshot(path=os.path.join(output_dir, "cat2_4_sig_crop.png"))
            print("Saved cat2_4_sig_crop.png")
            
    # 3. Inspection & Warning Page
    p_insp = page.locator("#page-inspection")
    if p_insp.count() > 0:
        p_insp.screenshot(path=os.path.join(output_dir, "cat2_4_page_inspection.png"))
        print("Saved cat2_4_page_inspection.png")

    # 4. Card 1 Front
    card_1_f = page.locator("#card-1-front")
    if card_1_f.count() > 0:
        card_1_f.screenshot(path=os.path.join(output_dir, "cat2_4_card_1_front.png"))
        print("Saved cat2_4_card_1_front.png")
        
        # Crop of Footer Spec Table
        f_spec = page.locator("#card-1-front .footer-spec-table")
        if f_spec.count() > 0:
            f_spec.screenshot(path=os.path.join(output_dir, "cat2_4_card_1_footer_crop.png"))
            print("Saved cat2_4_card_1_footer_crop.png")
            
    # 5. Card 1 Back
    card_1_b = page.locator("#card-1-back")
    if card_1_b.count() > 0:
        card_1_b.screenshot(path=os.path.join(output_dir, "cat2_4_card_1_back.png"))
        print("Saved cat2_4_card_1_back.png")
        
        # Crop of Back Table Header
        b_hdr = page.locator("#card-1-back .back-table thead")
        if b_hdr.count() > 0:
            b_hdr.screenshot(path=os.path.join(output_dir, "cat2_4_back_hdr_crop.png"))
            print("Saved cat2_4_back_hdr_crop.png")
        
    # 6. Card 2 Front (ฆ้อนเล็ก)
    card_2_f = page.locator("#card-2-front")
    if card_2_f.count() > 0:
        card_2_f.screenshot(path=os.path.join(output_dir, "cat2_4_card_2_front.png"))
        print("Saved cat2_4_card_2_front.png")

    browser.close()

print("All visual QA screenshots taken successfully!")
