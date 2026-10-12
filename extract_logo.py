import pdfplumber, os, sys
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'docs\thai-docx.skill\ระบบเอกสาร\6.สมุดประวัติการใช้ปืนใหญ่.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    print('Images on page 1:', len(p1.images))
    for idx, img in enumerate(p1.images):
        print(f"Image {idx+1}: x0={img['x0']:.1f}, top={img['top']:.1f}, w={img['width']:.1f}, h={img['height']:.1f}")
