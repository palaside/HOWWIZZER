import fitz
import re
import json

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

# Let's extract all text across all pages into one continuous stream, but tag pages
all_text = ""
for i, page in enumerate(doc):
    all_text += f"\n<<<PAGE_{i+1}>>>\n" + page.get_text()

with open("d:/Project/WEPAPP/all_survey_stream.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Saved all_survey_stream.txt")
