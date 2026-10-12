# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Read base table_layout_sd1.json
with open('table_layout_sd1.json', 'r', encoding='utf-8') as f:
    bp = json.load(f)

# Update for Weekly Inspection June 2569 (สัปดาห์ที่ ๓ ตั้งแต่วันที่ ๑๕ มิ.ย. – ๑๙ มิ.ย. ๖๙)
bp["doc_id"] = "REF-WEEKLY-INSPECTION-JUN-V1"
bp["title"] = "บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (ประจำสัปดาห์)"
bp["period"] = "สัปดาห์ที่ ๓ ตั้งแต่วันที่ ๑๕ มิ.ย. – ๑๙ มิ.ย. ๖๙"

# Page 1 Memo updates
p1 = bp["page_1_memo"]
p1["date_text"] = "มิ.ย. ๖๙"
p1["body"] = "ตามอ้างถึง ป.๔ พัน.๔ ร้อย.๒ ขอรายงานผลการตรวจอาวุธ และสิ่งอุปกรณ์ ประจำโรงเก็บปืนใหญ่ ประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) ประจำสัปดาห์ใน วันศุกร์ที่ ๑๙ มิ.ย. ๖๙ เวลา ๑๓๐๐ – ๑๕๐๐ น. รายละเอียดตามสิ่งที่ส่งมาด้วย"
p1["staff_initials"] = {
    "draft_inspect": "จ.ส.อ.                    ร่าง/ตรวจ                   มิ.ย. ๖๙",
    "type_verify": "ส.ท. วรากรฯ  พิมพ์/ทาน         ๑๙     มิ.ย. ๖๙"
}

# Page 2 & 3 Form SD.1 updates
sd1 = bp["inspection_form_sd1"]
sd1["week_text"] = "สัปดาห์ที่ ๓ ตั้งแต่วันที่ ๑๕ มิ.ย. – ๑๙ มิ.ย. ๖๙"
sd1["inspection_time"] = "(ตรวจในวันวันศุกร์ที่ ๑๙ มิ.ย. ๖๙  เวลา  ๑๓๐๐ – ๑๕๐๐ น.)"

# Signatures for Page 3
sd1["signatures"] = {
    "corrector": {
        "type": "signature_block",
        "role": "ผู้แก้ไข",
        "rank": "จ.ส.อ.",
        "name": "(ณัฐชัย  รักษาวงษ์)",
        "position": "ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒"
    },
    "inspector": {
        "type": "signature_block",
        "role": "ผู้ตรวจ",
        "rank": "ร.อ.",
        "name": "(กฤติน  นราพงษ์)",
        "position": "ผบ.ป.๔ พัน.๔ ร้อย.๒",
        "date_text": "มิ.ย. ๖๙"
    }
}

# Page 4 Photo Sheet updates
ps = bp["photo_sheet"]
ps["images"] = [
    "weekly_assets/weekly_p4_img1.jpeg",
    "weekly_assets/weekly_p4_img2.jpeg",
    "weekly_assets/weekly_p4_img3.jpeg",
    "weekly_assets/weekly_p4_img4.jpeg"
]
ps["signature"] = {
    "type": "signature_block",
    "label": "ตรวจถูกต้อง",
    "rank": "ร.อ.",
    "name": "(กฤติน  นราพงษ์)",
    "position": "ผบ.ป.๔ พัน.๔ ร้อย.๒",
    "date_text": "มิ.ย. ๖๙"
}

# Page 5 Gun Record updates
gr = bp["gun_inspection_record"]
gr["date_col"] = "วันศุกร์ที่ ๑๙ มิ.ย. ๖๙\nเวลา ๑๓๐๐ - ๑๕๐๐"
gr["signature"] = {
    "type": "signature_block",
    "role": "ตรวจถูกต้อง",
    "rank": "ร.อ.",
    "name": "(กฤติน  นราพงษ์)",
    "position": "ผบ.ป.๔ พัน.๔ ร้อย.๒",
    "date_text": "มิ.ย. ๖๙"
}

output_path = "table_layout_weekly_inspection.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(bp, f, ensure_ascii=False, indent=2)

print(f"Blueprint created: {output_path}")
