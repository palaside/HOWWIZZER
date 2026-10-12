import pdfplumber, sys, json
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs\thai-docx.skill\ระบบเอกสาร\6.สมุดประวัติการใช้ปืนใหญ่.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for i, p in enumerate(pdf.pages):
        words = p.extract_words()
        print(f"=== Page {i+1}: {len(words)} words ===")
        text_lines = p.extract_text().split('\n')
        for l in text_lines:
            if l.strip():
                print("  ", l.strip())
