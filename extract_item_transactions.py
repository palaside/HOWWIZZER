import json

with open('tb400_005_all_tables.json', 'r', encoding='utf-8') as f:
    tables = json.load(f)

with open('items_master_seed.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Let's inspect the transaction tables for each page:
# Pages with front tables:
# P1: เครื่องวัดอุณหภูมิส่วนบรรจุ (2 transactions: 29 ก.ค. 07, 14 ธ.ค. 32)
# P3: เครื่องอะไหล่สำหรับซ่อมบำรุงขั้น 2 (1 transaction: 3 พ.ย. 04)
# P5: เครื่องมือชุดช่างซ่อมปืนใหญ่ (2 transactions: 29 เม.ย. 16, 4 เม.ย. 28)
# P6: ปบค. 95 ขนาด 105 มม. (transactions...)
# P15: ปบค. 95 (continuation transactions...)
# P18: กล้องคอลลิเมเตอร์ (transactions...)
# P20: เครื่องวัดอุณหภูมิดินส่ง (transactions...)
# P22: กล้องพาโนรามิค (transactions...)
# P24: กล้องข้อศอก (transactions...)
# P25: เครื่องตั้งมุมยิงประณีต (transactions...)
# P26: ฐานกล้องเล็ง (transactions...)
# P30: กระโจมประจำหมู่ (transactions...)
# P32: กระโจมกระสุน (transactions...)
# P34: กระโจมส่วนบรรจุ (transactions...)

# Let's write an extractor to dump all transaction rows into clean dictionaries
page_trans_map = {}

for tbl in tables:
    p_num = tbl['page']
    data = tbl['data']
    # Check if table has transaction structure
    if len(data) >= 15 and len(data[0]) >= 6:
        # Find rows with actual dates
        rows_with_data = []
        for r_idx in range(2, len(data) - 2):
            row = data[r_idx]
            # Check if row has date or doc
            cell_txt = " ".join([str(c) for c in row if c and str(c).strip()])
            if any(month in cell_txt for month in ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']):
                rows_with_data.append({
                    'raw_row': row,
                    'text': cell_txt
                })
        if rows_with_data:
            page_trans_map[p_num] = rows_with_data

with open('extracted_transactions_by_page.json', 'w', encoding='utf-8') as f:
    json.dump(page_trans_map, f, ensure_ascii=False, indent=2)

print(f"Extracted transactions from {len(page_trans_map)} pages")
