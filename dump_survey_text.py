import fitz
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

with open(r"d:\Project\WEPAPP\survey_pages_text.txt", "w", encoding="utf-8") as out:
    for i in range(len(doc)):
        out.write(f"\n==================== PAGE {i+1} ====================\n")
        out.write(doc[i].get_text())

print("Written all pages text to survey_pages_text.txt")
