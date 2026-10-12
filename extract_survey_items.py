import fitz
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

print(f"Total pages: {len(doc)}")

for page_idx in range(len(doc)):
    page = doc[page_idx]
    text = page.get_text()
    
    # Find items (ใบสำรวจ no, NSN, Item name)
    survey_nos = re.findall(r"ที่ใบส\s*ำรวจ\s*\n\s*([0-9/]+)", text)
    nsns = re.findall(r"([0-9]{4}\s*–\s*[0-9]{2}\s*–\s*[0-9]{3}\s*-\s*[0-9]{4})", text)
    
    print(f"\n--- Page {page_idx+1} ---")
    print(f"Survey Nos found: {set(survey_nos)}")
    print(f"NSNs found: {set(nsns)}")
    
    # Let's see some lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    # Print distinct interesting lines
    print("Sample lines:")
    for l in lines[:20]:
        print("  ", l)
