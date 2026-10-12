import pypdf
import json

pdf_path = 'docs/thai-docx.skill/ระบบเอกสาร/11.ทบ468-360 ปรนนิบัติบำรุง.pdf'
reader = pypdf.PdfReader(pdf_path)

output = []
output.append(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    output.append(f"\n==================== PAGE {i+1} ====================")
    text = page.extract_text()
    output.append(text if text else "[NO TEXT / SCANNED]")

with open("inspect_tb468_360.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Inspection completed.")
