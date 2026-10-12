import pdfplumber, sys, json
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs\thai-docx.skill\ระบบเอกสาร\6.สมุดประวัติการใช้ปืนใหญ่.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for i in range(2, 6):
        print(f"=== PAGE {i+1} WORDS ===")
        for w in pdf.pages[i].extract_words():
            print(f"  {w['text']} ({w['x0']:.1f}, {w['top']:.1f})")
