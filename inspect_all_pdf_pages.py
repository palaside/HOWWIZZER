import pypdf
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('เริ่มต้นตั้งค่าและเลือกโหมดทำงาน.pdf')
print("Total pages:", len(reader.pages))

page_summaries = []
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    first_lines = " | ".join(lines[:5])
    has_text = len(text.strip()) > 0
    images = len(page.images)
    page_summaries.append({
        "page": i + 1,
        "has_text": has_text,
        "text_len": len(text),
        "num_images": images,
        "preview": first_lines[:200]
    })
    print(f"P.{i+1:02d} (imgs:{images}, txt:{len(text)}): {first_lines[:120]}")

with open("pdf_page_index.json", "w", encoding="utf-8") as f:
    json.dump(page_summaries, f, ensure_ascii=False, indent=2)
