import fitz
import json

doc = fitz.open(r"D:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\8.ขอส่งใบติดตามทวงถาม 90 วัน.pdf")
pages_detail = []

for page_idx, page in enumerate(doc):
    blocks = page.get_text("dict")["blocks"]
    spans = []
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for span in line["spans"]:
                    spans.append({
                        "text": span["text"],
                        "bbox": span["bbox"],
                        "size": span["size"],
                        "font": span["font"],
                        "color": span["color"]
                    })
    pages_detail.append({
        "page": page_idx + 1,
        "rect": [page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1],
        "spans": spans
    })

with open(r"d:\Project\WEPAPP\memo_inquiry_90_spans_all.json", "w", encoding="utf-8") as f:
    json.dump(pages_detail, f, ensure_ascii=False, indent=2)

print("Saved detailed spans for all 3 pages!")
