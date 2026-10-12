import fitz
import re
import json

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

# Let's inspect the original PDF page by page to find every item header
# Header pattern on each slip:
# - "ใบสำรวจสิ่งอุปกรณ์"
# - "หมายเลขสิ่งอุปกรณ์และ" / "รายการ" -> NSN
# - Item name
# - "ที่เก็บ" -> e.g. "โรงเก็บปืนใหญ่", "ป.4 พัน.4 ร้อย.2"
# - "ที่ใบสำรวจ" -> e.g. "1/66"
# - "วันสำรวจ" -> e.g. "พ.ย. 66"

# Let's write an accurate parser using bounding boxes
all_detected_slips = []

for pno in range(len(doc)):
    page = doc[pno]
    text = page.get_text()
    
    # We look for all occurrences of "X/66"
    matches = list(re.finditer(r"([0-9]+)\s*/\s*66", text))
    for m in matches:
        all_detected_slips.append({
            "page": pno + 1,
            "survey_no": f"{m.group(1)}/66",
            "pos": m.start()
        })

print(f"Detected slips: {len(all_detected_slips)}")
# Sort and print unique by survey_no
seen = set()
unique_slips = []
for s in all_detected_slips:
    if s["survey_no"] not in seen:
        seen.add(s["survey_no"])
        unique_slips.append(s)

print("Unique survey nos found:", [s["survey_no"] for s in unique_slips])
