import fitz
import json

doc = fitz.open('docs/thai-docx.skill/ระบบเอกสาร/11.ทบ468-360 ปรนนิบัติบำรุง.pdf')

summary = []

for p_no, page in enumerate(doc):
    summary.append(f"==================== PAGE {p_no+1} ====================")
    summary.append(f"Page rect: {page.rect}")
    drawings = page.get_drawings()
    rects = [d['rect'] for d in drawings if 'rect' in d]
    lines = [d['items'] for d in drawings if 'items' in d]
    summary.append(f"Drawings count: {len(drawings)}, Rects count: {len(rects)}")
    
    # Text spans
    spans = []
    text_page = page.get_text('dict')
    for b in text_page['blocks']:
        if b.get('type') == 0:
            for l in b['lines']:
                for s in l['spans']:
                    if s['text'].strip():
                        spans.append(f"  [{s['bbox'][0]:.1f}, {s['bbox'][1]:.1f}, {s['bbox'][2]:.1f}, {s['bbox'][3]:.1f}] ({s['font']}, {s['size']:.1f}pt): '{s['text']}'")
    summary.append("Text spans (first 25):")
    summary.extend(spans[:25])
    if len(spans) > 25:
        summary.append(f"  ... and {len(spans)-25} more spans")

with open('summary_layout_468_360.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(summary))

print("Layout summary written.")
