#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

output_dir = 'C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14'
html_path = os.path.abspath('ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.html')
file_url = f'file:///{html_path.replace("\\\\", "/")}'

with sync_playwright() as p:
    browser = p.chromium.launch()
    # A4 Landscape at 96 DPI: 297mm x 210mm -> 1123 x 794 px
    # Give enough viewport to render properly
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    page.goto(file_url)
    page.wait_for_timeout(1000)

    # Screenshot Page 1 (Cover)
    p1 = page.locator('#page-1')
    p1_file = os.path.join(output_dir, 'tb468_360_page_1_cover.png')
    p1.screenshot(path=p1_file)
    print(f"Captured: {p1_file}")

    # Screenshot Page 2 (Equipment Table)
    p2 = page.locator('#page-2')
    p2_file = os.path.join(output_dir, 'tb468_360_page_2_equip.png')
    p2.screenshot(path=p2_file)
    print(f"Captured: {p2_file}")

    # Screenshot Page 3 (Calendar Matrix)
    p3 = page.locator('#page-3')
    p3_file = os.path.join(output_dir, 'tb468_360_page_3_calendar.png')
    p3.screenshot(path=p3_file)
    print(f"Captured: {p3_file}")

    # Screenshot Page 4 (Instructions)
    p4 = page.locator('#page-4')
    p4_file = os.path.join(output_dir, 'tb468_360_page_4_instructions.png')
    p4.screenshot(path=p4_file)
    print(f"Captured: {p4_file}")

    browser.close()

print("All screenshots captured successfully.")
