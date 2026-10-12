import fitz

doc = fitz.open('docs/thai-docx.skill/ระบบเอกสาร/11.ทบ468-360 ปรนนิบัติบำรุง.pdf')

for page_idx in [2, 3]:
    page = doc[page_idx]
    with open(f"page_{page_idx+1}_dump.txt", "w", encoding="utf-8") as f:
        f.write(f"--- PAGE {page_idx+1} TEXT ---\n")
        for b in page.get_text('dict')['blocks']:
            if b.get('type') == 0:
                for l in b['lines']:
                    for s in l['spans']:
                        f.write(f"[{s['bbox'][0]:.1f}, {s['bbox'][1]:.1f}, {s['bbox'][2]:.1f}, {s['bbox'][3]:.1f}] ({s['font']} {s['size']:.1f}pt): {s['text']}\n")
        f.write(f"\n--- PAGE {page_idx+1} DRAWINGS ---\n")
        for d in page.get_drawings():
            f.write(f"rect: {d.get('rect')}, fill: {d.get('fill')}, color: {d.get('color')}, items: {len(d.get('items', []))}\n")

print("Dumps written.")
