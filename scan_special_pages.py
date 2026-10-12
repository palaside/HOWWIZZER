import json
import re

with open('tb400_005_all_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Let's inspect each page's tables and text
# Let's write out a full map of the document
cards_summary = []

for p in pages:
    p_num = p['page']
    txt = p['full_text']
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    
    # Check for TOC
    if "สารบัญ" in txt:
        print(f"Page {p_num} is TOC")
    elif "รายการสถานที่อยู่ของสิ่งอุปกรณ์" in txt:
        print(f"Page {p_num} is Location Record (Card Back)")
    elif "บันทึกผลการตรวจของผู้บังคับบัญชา" in txt:
        print(f"Page {p_num} is Commander Inspection Record")
    elif "ข้าพเจ้าขอรับรองว่าทรัพย์สิน" in txt:
        print(f"Page {p_num} is Unit Certification")
    elif "คำเตือน" in txt or "ต าเตือน" in txt:
        print(f"Page {p_num} is Warning")

print("Done scanning special pages")
