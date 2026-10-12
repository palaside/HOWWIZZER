import json

with open('items_master_seed.json', 'r', encoding='utf-8') as f:
    items_seed = json.load(f)

with open('extracted_transactions_by_page.json', 'r', encoding='utf-8') as f:
    trans_by_page = json.load(f)

# Build blueprint
blueprint = {
    "document_id": "REF-TB-400-005-V1",
    "form_code": "ทบ.๔๐๐ – ๐๐๕",
    "form_name": "บัญชีสิ่งอุปกรณ์ของหน่วย (ทบ.๔๐๐-๐๐๕)",
    "category": "บัตรบัญชีคุมสิ่งอุปกรณ์ กองทัพบก สาย สพ. (Unit Property Book Card)",
    "unit_info": {
        "unit_name": "ป.4 พัน.4 ร้อย.2",
        "station": "ค่ายจิรประวัติ   อ.เมือง     จว.นครสวรรค์",
        "toe": "อจย ๖-๒๗  ( ๒ พ.ค. ๒๙ )"
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
    "toc": [
        {"no": "๑", "name": "ปบค. ขนาด 105 มม. พร้อมรถรองปืน เอ็ม.2 เอ.2", "page": "๑"},
        {"no": "๒", "name": "เครื่องมือชุดช่างซ่อมปืนใหญ่", "page": "๒"},
        {"no": "๓", "name": "เครื่องวัดอุณหภูมิส่วนบรรจุ", "page": "๓"},
        {"no": "๔", "name": "ลำกล้องปืนหลอดพร้อมเครื่องประกอบ", "page": "๔"},
        {"no": "๕", "name": "กล้องพาโนรามิค", "page": "๕", "section": "ประเภท 4 ( นอกอัตรา )"},
        {"no": "๖", "name": "กล้องข้อศอก", "page": "๖"},
        {"no": "๗", "name": "เครื่องตั้งมุมยิงประณีต", "page": "๗"},
        {"no": "๘", "name": "เครื่องวัดอุณหภูมิดินส่ง ( แบบดิจิตอล )", "page": "๘"},
        {"no": "๙", "name": "ฐานกล้องเล็ง", "page": "๙"},
        {"no": "๑๐", "name": "กล้องคอลลิเมเตอร์", "page": "๑๐"},
        {"no": "๑๑", "name": "เครื่องอะไหล่ซ่อมบำรุง 2 ( ปบค.95 )", "page": "๑๑"},
        {"no": "๑๒", "name": "ชุดตรวจและเติมแก๊ส", "page": "๑๒"},
        {"no": "๑๓", "name": "กระโจมประจำหมู่", "page": "๑๓", "section": "สาย พธ."},
        {"no": "๑๔", "name": "กระโจมกระสุน", "page": "๑๔"},
        {"no": "๑๕", "name": "กระโจมส่วนบรรจุ", "page": "๑๕"}
    ],
    "commander_certification": {
        "title": "บันทึกผลการตรวจของผู้บังคับบัญชา",
        "inspection_date": "เม.ย. 69",
        "inspection_result": "ถูกต้องตามจำนวนและสามารถใช้การได้เป็นอย่างดี",
        "statement": "“ข้าพเจ้าขอรับรองว่าทรัพย์สินซึ่งแสดงไว้ในบัญชีคุมนี้ เป็นทรัพย์สินที่หน่วยได้รับไว้ในความรับผิดชอบจริง และได้เก็บรักษาไว้ในสภาพเรียบร้อย ถูกต้องตามระเบียบของทางราชการทุกประการ”",
        "commander_rank": "ร.ท.",
        "commander_name": "(กฤติน  นราพงษ์)",
        "commander_position": "ผบ.ป.๔ พัน.๔ ร้อย.๒"
    },
    "cards": []
}

# Add items to blueprint
for key, itm in items_seed.items():
    blueprint["cards"].append(itm)

with open('table_layout_400_005.json', 'w', encoding='utf-8') as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)

print("Created table_layout_400_005.json successfully!")
