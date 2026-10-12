import fitz
import os

pdf_path = r"D:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\8.ขอส่งใบติดตามทวงถาม 90 วัน.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

out_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_img = os.path.join(out_dir, f"memo_inquiry_90_p{i+1}.png")
    pix.save(out_img)
    print(f"Saved page {i+1} to {out_img} ({pix.width}x{pix.height})")

# Extract text & spans
all_pages_data = []
for i, page in enumerate(doc):
    text_page = page.get_text("words")
    rect = page.rect
    all_pages_data.append({
        "page": i + 1,
        "width_pt": rect.width,
        "height_pt": rect.height,
        "text": page.get_text()
    })

import json
with open(r"d:\Project\WEPAPP\memo_inquiry_90_extracted.json", "w", encoding="utf-8") as f:
    json.dump(all_pages_data, f, ensure_ascii=False, indent=2)

print("Text extraction complete!")
