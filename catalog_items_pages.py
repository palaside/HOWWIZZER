import fitz
import json
import re

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

# We want to extract each of the 23 items cleanly.
# Let's inspect the layout of blocks where each survey_no occurs.

items_catalog = []

for item_idx in range(1, 24):
    target_no = f"{item_idx}/66"
    
    # Search which page has this target_no
    found_page = None
    target_rect = None
    for pno in range(len(doc)):
        page = doc[pno]
        rects = page.search_for(target_no)
        if rects:
            found_page = page
            target_rect = rects[0]
            page_num = pno + 1
            break
            
    if not found_page:
        continue
        
    # Get all text on this page
    text = found_page.get_text()
    
    # Also get words on found_page around target_rect
    # Let's inspect blocks on found_page
    blocks = found_page.get_text("blocks")
    
    # We want NSN, Item Name, Location, Unit, Date, Numbers, Signatures
    items_catalog.append({
        "item_no": item_idx,
        "survey_no": target_no,
        "page_in_pdf": page_num,
        "target_bbox": [target_rect.x0, target_rect.y0, target_rect.x1, target_rect.y1]
    })

print(f"Cataloged {len(items_catalog)} items.")
