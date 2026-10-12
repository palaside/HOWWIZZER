import fitz
import json

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

print("=== PAGE 1 TEXT ===")
print(doc[0].get_text()[:1500])

print("=== PAGE 13 TEXT (LAST PAGE) ===")
print(doc[12].get_text()[:1500])
