import fitz
import json
import re

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

# Let's inspect each item's text details
extracted_items = []

for item_no in range(1, 24):
    target_str = f"{item_no}/66"
    # find page where this appears
    pno = None
    y_pos = None
    for p in range(len(doc)):
        rects = doc[p].search_for(target_str)
        if rects:
            pno = p
            y_pos = rects[0].y0
            break
            
    if pno is None:
        continue
        
    page = doc[pno]
    # In this page, let's take words within y_pos - 80 to y_pos + 150
    # Wait, some tables spilled over to the next page!
    # Let's see: on page `pno`, words from y_pos - 100 to y_pos + 250
    words = page.get_text("words")
    item_words = [w for w in words if abs(w[1] - y_pos) < 180]
    
    # Let's also check if it spilled to next page
    next_page_words = []
    if pno + 1 < len(doc):
        # if target is near bottom of page (y_pos > 250), check top of next page (y < 120)
        if y_pos > 250:
            np = doc[pno + 1]
            next_page_words = [w for w in np.get_text("words") if w[1] < 120]
            
    # Combine text
    combined_text = " ".join([w[4] for w in item_words]) + " " + " ".join([w[4] for w in next_page_words])
    
    extracted_items.append({
        "item_no": item_no,
        "target": target_str,
        "page": pno + 1,
        "y_pos": round(y_pos, 1),
        "text": combined_text
    })

with open("d:/Project/WEPAPP/all_items_extracted.json", "w", encoding="utf-8") as f:
    json.dump(extracted_items, f, ensure_ascii=False, indent=2)

print("Saved all_items_extracted.json")
