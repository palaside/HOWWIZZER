import json
import pdfplumber

pdf_path = r'd:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\12.บัญชีคุมสิ่งอุปกรณ์ ประเภท 2 และ 4.pdf'

with pdfplumber.open(pdf_path) as pdf:
    # Check page 7, 9, 11
    sample_pages = [7, 9, 11, 13, 25, 51, 101, 177]
    for p_no in sample_pages:
        page = pdf.pages[p_no - 1]
        tables = page.extract_tables()
        print(f"=== PAGE {p_no} TABLES (count={len(tables)}) ===")
        for t_idx, t in enumerate(tables):
            print(f"Table {t_idx+1}: {len(t)} rows")
            for r in t[:6]:
                print("  ", [c.replace('\n', ' ') if c else '' for c in r])
