import json
import base64
import os

with open(r'd:\Project\WEPAPP\cat2_4_items_clean.json', encoding='utf-8') as f:
    items = json.load(f)

# Read emblem base64
emblem_path = r'd:\Project\WEPAPP\tiger_artillery_emblem.jpg'
with open(emblem_path, 'rb') as f:
    emblem_b64 = base64.b64encode(f.read()).decode('utf-8')

blueprint = {
    "document_id": "REF-TB-CAT2-4-V1",
    "form_code": "ทบ.๔๐๐ – ๐๐๕",
    "form_name": "บัญชีสิ่งอุปกรณ์ประเภท 2 และ 4 สาย สพ. (คลังโรงปืน)",
    "category": "สมุดบัญชีสิ่งอุปกรณ์ กองทัพบก สาย สพ. คลังโรงปืน (Unit Property Book Series 2 & 4)",
    "unit_info": {
        "unit_name": "ป.4 พัน.4 ร้อย.2",
        "station": "ค่ายจิรประวัติ  อ.เมือง  จว.นครสวรรค์",
        "toe": "อจย ๖-๒๗ ( ๒ พ.ค. ๒๙ )",
        "battalion_full": "กองพันทหารปืนใหญ่ที่ ๔ กรมทหารปืนใหญ่ที่ ๔"
    },
    "paper_setup": {
        "size": "A5",
        "orientation": "portrait",
        "width_mm": 148.0,
        "height_mm": 210.0,
        "margins_mm": {
            "top": 5.0,
            "bottom": 5.0,
            "left": 7.0,
            "right": 7.0
        }
    },
    "commander_certification": {
        "toe_ref": "อจย. 6-27 คำสั่ง ทบ. (เฉพาะ)",
        "unit": "หน่วย ป.4 พัน.4 ร้อย.2",
        "statement": "“ข้าพเจ้าขอรับรองว่าทรัพย์สิน ซึ่งแสดงไว้ในสมุดบัญชีสิ่งอุปกรณ์ เล่มนี้บันทึกไว้ถูกต้อง”",
        "commander_rank": "ร.อ.",
        "commander_name": "(ปวิณ    แก้วปิงเมือง)",
        "commander_position": "ผบ.ป.๔ พัน.๔ ร้อย.๒"
    },
    "warning_text": "คำเตือน: หน่วยเหนือจะต้องเก็บหลักฐานการรับ สป.รายการนี้ของหน่วยรอง หรือเจ้าหน้าที่ผู้รับไว้ให้มั่นคงครบทุกรายการ",
    "cards_count": len(items),
    "cards": items
}

with open(r'd:\Project\WEPAPP\table_layout_cat2_4.json', 'w', encoding='utf-8') as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)

print(f"Generated table_layout_cat2_4.json with {len(items)} cards successfully!")
