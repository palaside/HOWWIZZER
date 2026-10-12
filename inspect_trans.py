import json

with open('tb400_005_extracted_raw.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

extracted_cards = []

# List of known 15 items in order:
# 1. ปบค. 95 ขนาด 105 มม. พร้อมรถรอง เอ็ม.2 เอ.2 (1015-00-722-9752)
# 2. เครื่องมือชุดช่างซ่อมปืนใหญ่ (5180-00-757-7727)
# 3. เครื่องวัดอุณหภูมิส่วนบรรจุ (66885-00-344-4613)
# 4. ลำกล้องปืนหลอดพร้อมเครื่องประกอบ (-)
# 5. กล้องพาโนรามิค (1230-35-165-0005)
# 6. กล้องข้อศอก (-)
# 7. เครื่องตั้งมุมยิงประณีต (-)
# 8. เครื่องวัดอุณหภูมิดินส่ง ( แบบดิจิตอล ) (6685-xx-165-1315)
# 9. ฐานกล้องเล็ง (-)
# 10. กล้องคอลลิเมเตอร์ (1240-006-6065)
# 11. เครื่องอะไหล่สำหรับซ่อมบำรุงขั้น 2 ปบค.95 ขนาด 105 มม. (1015-00-712-0207)
# 12. ชุดตรวจและเติมแก๊ส (-)
# 13. กระโจมประจำหมู่ (8340-35-229-0026)
# 14. กระโจมกระสุน (8340-35-229-0025)
# 15. กระโจมส่วนบรรจุ (8340-35-229-0058)

# Let's inspect each table cell across the pages
all_tables = []
for p in raw:
    for t_idx, t in enumerate(p['tables']):
        all_tables.append({
            'page': p['page'],
            'table_idx': t_idx,
            'rows': len(t),
            'cols': len(t[0]) if t else 0,
            'data': t
        })

with open('tb400_005_all_tables.json', 'w', encoding='utf-8') as f:
    json.dump(all_tables, f, ensure_ascii=False, indent=2)

print(f"Total tables dumped: {len(all_tables)}")
