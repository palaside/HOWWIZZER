import fitz
import json
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r"D:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\17.บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ 2).pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

full_text = []

for i, page in enumerate(doc):
    rect = page.rect
    w_mm = rect.width * 25.4 / 72.0
    h_mm = rect.height * 25.4 / 72.0
    orient = "Landscape" if rect.width > rect.height else "Portrait"
    print(f"--- Page {i+1} ---")
    print(f"Size: {w_mm:.1f} x {h_mm:.1f} mm ({orient})")
    
    text = page.get_text()
    print(f"Text length: {len(text)}")
    full_text.append(f"=== Page {i+1} ({orient}) ===\n" + text)
    
    # Render PNG
    pix = page.get_pixmap(dpi=150)
    out_img = f"gen_insp_orig_p{i+1}.png"
    pix.save(out_img)
    print(f"Rendered: {out_img}")

with open("gen_insp_full_text.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(full_text))

print("Dumped text to gen_insp_full_text.txt")
