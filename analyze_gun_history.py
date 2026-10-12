import pdfplumber, json, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs/thai-docx.skill/ระบบเอกสาร/5.ประวัติการใช้อาวุธ ปืน.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p = pdf.pages[0]
    tables = p.find_tables()
    for t in tables:
        print("Table bbox:", t.bbox)
        # column boundaries
        cells = t.cells
        x_cuts = sorted(list(set([c[0] for c in cells] + [c[2] for c in cells])))
        print("X cuts:", [round(x, 2) for x in x_cuts])
        widths = [round(x_cuts[i+1] - x_cuts[i], 2) for i in range(len(x_cuts)-1)]
        print("Col widths (pt):", widths)
        total_w = sum(widths)
        pcts = [round(w / total_w * 100, 2) for w in widths]
        print("Col widths (%):", pcts)

    print("\n--- All words in table header and row 1 ---")
    words = p.extract_words()
    for w in [w for w in words if 150 <= w['top'] <= 220]:
        print(f"y={w['top']:.1f}, x={w['x0']:.1f}-{w['x1']:.1f}: {w['text']}")
