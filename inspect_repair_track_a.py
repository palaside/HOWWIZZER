import pypdf
import pdfplumber
import fitz # PyMuPDF
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

pdf_path = "ใบติดตามใบส่งซ่อมแบบ_ก_ต้นฉบับ.pdf"

# 1. Basic PyPDF inspection
reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)
print(f"=== Total Pages: {page_count} ===")

doc_info = {
    "page_count": page_count,
    "pages": []
}

doc_fitz = fitz.open(pdf_path)

for idx, page in enumerate(reader.pages):
    mb = page.mediabox
    w_pt, h_pt = float(mb.width), float(mb.height)
    w_mm, h_mm = w_pt * 25.4 / 72, h_pt * 25.4 / 72
    orientation = "landscape" if w_pt > h_pt else "portrait"
    
    print(f"\n--- Page {idx + 1} ---")
    print(f"Dimensions: {w_pt:.1f} x {h_pt:.1f} pt ({w_mm:.1f} x {h_mm:.1f} mm) -> {orientation}")
    
    # Render page as PNG image for Visual QA
    fitz_page = doc_fitz[idx]
    pix = fitz_page.get_pixmap(dpi=150)
    img_name = f"repair_track_a_orig_p{idx+1}.png"
    pix.save(img_name)
    print(f"Saved render: {img_name} ({pix.width}x{pix.height})")
    
    # Extract text with layout
    txt = page.extract_text() or ""
    print("Extracted text preview:")
    for line in txt.splitlines()[:15]:
        if line.strip():
            print("  ", line.strip())

# 2. Extract tables and words with pdfplumber
with pdfplumber.open(pdf_path) as plum:
    all_pages_data = []
    for idx, p in enumerate(plum.pages):
        tables = p.extract_tables()
        words = p.extract_words()
        print(f"\nPage {idx+1} pdfplumber: found {len(tables)} tables, {len(words)} words")
        for t_idx, t in enumerate(tables):
            print(f" Table {t_idx+1} ({len(t)} rows):")
            for r in t[:5]:
                print("   ", r)
        all_pages_data.append({
            "page": idx + 1,
            "width": p.width,
            "height": p.height,
            "tables": tables,
            "words": words
        })

with open("repair_track_a_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_pages_data, f, ensure_ascii=False, indent=2)

print("\nDone inspect_repair_track_a.py")
