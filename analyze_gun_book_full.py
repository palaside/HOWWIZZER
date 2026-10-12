import pdfplumber, json, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs\thai-docx.skill\ระบบเอกสาร\6.สมุดประวัติการใช้ปืนใหญ่.pdf'

analysis = {}

with pdfplumber.open(pdf_path) as pdf:
    for idx, p in enumerate(pdf.pages):
        p_num = idx + 1
        analysis[f"page_{p_num}"] = {
            "width": p.width,
            "height": p.height,
            "text": p.extract_text(),
            "tables": []
        }
        for t in p.find_tables():
            cells = t.cells
            x_cuts = sorted(list(set([round(c[0], 2) for c in cells] + [round(c[2], 2) for c in cells])))
            y_cuts = sorted(list(set([round(c[1], 2) for c in cells] + [round(c[3], 2) for c in cells])))
            widths = [round(x_cuts[i+1] - x_cuts[i], 2) for i in range(len(x_cuts)-1)]
            total_w = sum(widths)
            pcts = [round(w / total_w * 100, 2) for w in widths]
            
            extracted_data = t.extract()
            analysis[f"page_{p_num}"]["tables"].append({
                "bbox": [round(v, 2) for v in t.bbox],
                "x_cuts": x_cuts,
                "col_widths_pt": widths,
                "col_widths_pct": pcts,
                "rows_count": len(extracted_data),
                "header_sample": extracted_data[:2] if len(extracted_data) >= 2 else extracted_data
            })

with open(r'd:\Project\WEPAPP\gun_book_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print("Saved gun_book_analysis.json successfully!")
