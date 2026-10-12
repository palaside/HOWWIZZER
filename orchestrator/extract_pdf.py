import fitz, os, pathlib, json

pdf_path = r"d:/Project/WEPAPP/เริ่มต้นตั้งค่าและเลือกโหมดทำงาน.pdf"
output_txt = r"d:/Project/WEPAPP/orchestrator/state/pdf_text.txt"

# Ensure output directory exists
pathlib.Path(os.path.dirname(output_txt)).mkdir(parents=True, exist_ok=True)

with fitz.open(pdf_path) as doc:
    text = "\n".join(page.get_text() for page in doc)

with open(output_txt, "w", encoding="utf-8") as f:
    f.write(text)

print(f"PDF text extracted to {output_txt}")
