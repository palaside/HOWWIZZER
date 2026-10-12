import pdfplumber, os, sys
from PIL import Image

pdf_path = r'docs\thai-docx.skill\ระบบเอกสาร\6.สมุดประวัติการใช้ปืนใหญ่.pdf'
with pdfplumber.open(pdf_path) as pdf:
    p1 = pdf.pages[0]
    img_obj = p1.images[0]
    # Extract cropped image
    cropped = p1.crop((img_obj['x0'], img_obj['top'], img_obj['x1'], img_obj['bottom'])).to_image(resolution=300)
    out_path = r'd:\Project\WEPAPP\artillery_emblem.png'
    cropped.save(out_path)
    print("Saved logo to:", out_path)
