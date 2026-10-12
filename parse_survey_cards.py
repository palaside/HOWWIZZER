import fitz
import json
import re

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

all_items = []

for page_idx in range(len(doc)):
    page = doc[page_idx]
    # In each page, let's split into top half (y < 306) and bottom half (y >= 306)
    # Page height is 612.12 pt
    mid_y = 306.0
    
    blocks = page.get_text("blocks")
    top_blocks = [b for b in blocks if (b[1] + b[3])/2 < mid_y]
    bottom_blocks = [b for b in blocks if (b[1] + b[3])/2 >= mid_y]
    
    def parse_half(half_blocks, page_num, section):
        if not half_blocks:
            return None
        text = "\n".join([b[4].strip() for b in half_blocks if b[4].strip()])
        # Check if this half has a survey card
        if "ใบส" not in text and "ที่ใบส" not in text and "รำยกำร" not in text and "รายการ" not in text:
            return None
        return {
            "page": page_num,
            "section": section,
            "raw_text": text
        }
        
    t = parse_half(top_blocks, page_idx + 1, "top")
    if t: all_items.append(t)
    b = parse_half(bottom_blocks, page_idx + 1, "bottom")
    if b: all_items.append(b)

print(f"Extracted {len(all_items)} cards across {len(doc)} pages.")

with open("d:/Project/WEPAPP/survey_cards_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

print("Saved survey_cards_raw.json")
