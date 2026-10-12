import fitz, sys, pathlib

pdf_path = pathlib.Path(r"D:/Project/WEPAPP/เริ่มต้นตั้งค่าและเลือกโหมดทำงาน.pdf")
output_path = pathlib.Path(r"D:/Project/WEPAPP/pdf_text.txt")

doc = fitz.open(pdf_path)
text = "\n".join([page.get_text() for page in doc])
output_path.write_text(text, encoding="utf-8")
print(f"Extracted text written to {output_path}")
