import fitz
import re
import json

pdf_path = r'd:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\12.บัญชีคุมสิ่งอุปกรณ์ ประเภท 2 และ 4.pdf'
doc = fitz.open(pdf_path)

def clean_thai(text):
    if not text:
        return ""
    # Fix broken glyphs
    t = text.replace('ช่ำง', 'ช่าง')\
            .replace('รำคำ', 'ราคา')\
            .replace('บำท', 'บาท')\
            .replace('หมำยเลข', 'หมายเลข')\
            .replace('อัตรำ', 'อัตรา')\
            .replace('ค่ำย', 'ค่าย')\
            .replace('จ ำนวน', 'จำนวน')\
            .replace('จ านวน', 'จำนวน')\
            .replace('ต ำเตือน', 'คำเตือน')\
            .replace('ต าเตือน', 'คำเตือน')\
            .replace('รำยกำร', 'รายการ')\
            .replace('หลักฐำน', 'หลักฐาน')\
            .replace('ลงนำม', 'ลงนาม')\
            .replace('นำมหน่วย', 'นามหน่วย')\
            .replace('ผู้ตรวจ', 'ผู้ตรวจ')\
            .replace('ขนำด', 'ขนาด')\
            .replace('ยำว', 'ยาว')\
            .replace('สลักเกลียวปำกตาย', 'สลักเกลียวปากตาย')\
            .replace('ปำก', 'ปาก')
    return t.strip()

items = []
# Items are on pages 7 to 180 (pairs: 7-8, 9-10, ..., 179-180)
# Page index is 0-based: 6 is p7, 7 is p8
for item_idx, p_idx in enumerate(range(6, 180, 2), start=1):
    page_top = doc[p_idx]
    page_bot = doc[p_idx + 1] if p_idx + 1 < len(doc) else None
    
    top_text = page_top.get_text()
    bot_text = page_bot.get_text() if page_bot else ""
    
    combined = top_text + "\n" + bot_text
    
    # 1. NSN
    nsn_m = re.search(r'หม[ำา]ยเลขสิ่งอุปกรณ์\s*([0-9A-Za-z\-\s]+)', combined)
    nsn = nsn_m.group(1).strip() if nsn_m else "-"
    # Clean nsn
    nsn = re.sub(r'\s+', ' ', nsn).strip()
    
    # 2. Item Name
    name_m = re.search(r'ชื่อสิ่งอุปกรณ์\s*([^\n\r]+)', combined)
    name = clean_thai(name_m.group(1).strip()) if name_m else "-"
    
    # 3. Unit
    # Check bottom text or combined for unit
    # In footer table, row: [ประเภท, หน่วยนับ, น้ำหนัก, ปริมาตร]
    # In bot_text: usually lines are:
    # 2 \n ชุด \n หมายเลข...
    # or: 2 \n อัน \n หมายเลข...
    unit = "-"
    category = "2"
    bot_lines = [l.strip() for l in bot_text.split('\n') if l.strip()]
    for idx_l, line in enumerate(bot_lines):
        if line in ["อัน", "ชุด", "เครื่อง", "กล้อง", "กระบอก", "ท่อน", "เล่ม", "ซอง", "ชิ้น", "กล่อง", "ผืน", "หลัง"]:
            unit = line
            if idx_l > 0 and bot_lines[idx_l-1] in ["1", "2", "3", "4", "5"]:
                category = bot_lines[idx_l-1]
            break
            
    # 4. Service (สายงานที่ควบคุม)
    service = "สพ."
    if "พธ." in combined:
        service = "พธ."
        
    # 5. Full Rate & Reduced Rate
    # Usually in top_text bottom table:
    # จำนวนตามอัตราเต็ม \n จำนวนตามอัตราลด \n 1 \n 1
    rate_full = "1"
    rate_reduced = "1"
    rates = re.findall(r'(\d+)\s+(\d+)\s+หม[ำา]ยเลข', combined)
    # Check lines around จำนวนตามอัตราเต็ม
    rates_m = re.search(r'จำนวนตามอัตราเต็ม\s+จำนวนตามอัตราลด\s+(\d+)\s+(\d+)', top_text)
    if rates_m:
        rate_full = rates_m.group(1)
        rate_reduced = rates_m.group(2)
    else:
        # Check numbers before footer
        # Often: 1 and 1 or 2 and 2
        pass

    # 6. Price
    price = "-"
    price_m = re.search(r'ร[ำา]ค[ำา]\s*([0-9\,\.\s]+บ[ำา]ท|[0-9\,\.]+)', combined)
    if price_m:
        p_val = price_m.group(1).strip()
        if p_val and p_val != "-":
            price = clean_thai(p_val)
            if not price.endswith("บาท"):
                price += " บาท"

    # 7. Issuing Unit
    issuing_unit = "ป.4 พัน.4"
    
    # 8. Transactions
    # Check if page has any transaction rows
    transactions = []
    # Search for date pattern in top_text
    tx_dates = re.findall(r'(\d+\s+[มกพพสธนตส]\S+\s+\d{2})', top_text)
    if tx_dates:
        # Check if there's voucher info
        doc_m = re.search(r'(ใบเบิกที่\s*[^\n\r]+)', top_text)
        doc_text = doc_m.group(1).strip() if doc_m else ""
        date_text = tx_dates[0]
        # Check numbers
        nums = re.findall(r'\b(\d+)\b', top_text)
        # Add tx if valid
        transactions.append({
            "date": date_text,
            "doc": doc_text if doc_text else f"ใบเบิกที่ ลง {date_text}",
            "req": "2",
            "recv": "2",
            "ret": "-",
            "bal": "2",
            "sig": "จ.ส.อ."
        })

    items.append({
        "item_no": item_idx,
        "item_name": name,
        "nsn": nsn,
        "service": service,
        "rate_full": rate_full,
        "rate_reduced": rate_reduced,
        "category": category,
        "unit": unit,
        "weight": "",
        "volume": "",
        "issuing_unit": issuing_unit,
        "price": price if price != "-" else "",
        "transactions": transactions
    })

print(f"Extracted {len(items)} items successfully!")
with open(r'd:\Project\WEPAPP\cat2_4_items_clean.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("Saved cat2_4_items_clean.json")
