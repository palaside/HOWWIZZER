import os
import fitz  # PyMuPDF
import json

pdf_path = r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf"
output_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"

doc = fitz.open(pdf_path)
print(f"Total pages: {len(doc)}")

summary = []

for idx, page in enumerate(doc):
    rect = page.rect
    width_pt = rect.width
    height_pt = rect.height
    width_mm = width_pt * 25.4 / 72
    height_mm = height_pt * 25.4 / 72
    orientation = "Landscape" if width_pt > height_pt else "Portrait"
    
    text = page.get_text()
    
    # Render high-res image
    pix = page.get_pixmap(dpi=200)
    img_name = f"survey_orig_page_{idx+1}.png"
    img_path = os.path.join(output_dir, img_name)
    pix.save(img_path)
    
    page_info = {
        "page_number": idx + 1,
        "width_pt": width_pt,
        "height_pt": height_pt,
        "width_mm": round(width_mm, 2),
        "height_mm": round(height_mm, 2),
        "orientation": orientation,
        "image": img_path,
        "text_preview": text[:500],
        "full_text": text
    }
    summary.append(page_info)
    print(f"Page {idx+1}: {orientation} ({round(width_mm, 1)} x {round(height_mm, 1)} mm), chars={len(text)}, saved to {img_name}")

with open(r"d:\Project\WEPAPP\survey_doc_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("Inspection complete!")
