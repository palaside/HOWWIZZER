import pdfplumber, json, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs/thai-docx.skill/ระบบเอกสาร/5.ประวัติการใช้อาวุธ ปืน.pdf'

pages_data = []

with pdfplumber.open(pdf_path) as pdf:
    for idx in range(5): # 5 pages for squads 2 to 6
        p = pdf.pages[idx]
        t = p.extract_tables()[0]
        
        # Header is row 0
        header = t[0]
        
        # Rows 1 to 13
        items = []
        for r in t[1:]:
            items.append({
                "part": r[0].strip() if r[0] else "",
                "model": r[1].strip() if r[1] else "",
                "serial": r[2].strip() if r[2] else "",
                "remark": r[3].strip() if r[3] else ""
            })
        
        # Squad number
        squad_num = idx + 2
        pages_data.append({
            "page_num": idx + 1,
            "squad_num": squad_num,
            "title": f"ประวัติการใช้อาวุธ ป.หมู่ {squad_num}",
            "items": items
        })

print(json.dumps(pages_data, ensure_ascii=False, indent=2))

with open(r'd:\Project\WEPAPP\gun_history_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)
print("Saved gun_history_extracted.json")
