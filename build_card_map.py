import json

with open('tb400_005_all_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Let's inspect page 1 and page 2
# Page 1 table has:
# Row 0: ['ว.ด.ป.', 'หลักฐาน', 'จำนวน', '', '', '', 'ลงนาม']
# Row 1: ['', '', 'ขอ\nเบิก', 'ได้รับ', 'ส่งคืน', 'คงมี', '']
# Row 2+: Transactions!
# And footer metadata in text or table
# Let's write a script to inspect and extract each card cleanly

cards_extracted = []

# Map of pages to items:
# Card 1: เครื่องวัดอุณหภูมิส่วนบรรจุ (P1, P2)
# Card 2: เครื่องอะไหล่สำหรับซ่อมบำรุงขั้น 2 (P3, P4)
# Card 3: เครื่องมือชุดช่างซ่อมปืนใหญ่ (P5, P6)
# Card 4: ปบค. 95 ขนาด 105 มม. (P7, P8, P15, P16, P17)
# Card 5: กล้องคอลลิเมเตอร์ (P18, P19)
# Card 6: เครื่องวัดอุณหภูมิดินส่ง (P20, P21)
# Card 7: กล้องพาโนรามิค (P22, P23)
# Card 8: กล้องข้อศอก (P24)
# Card 9: เครื่องตั้งมุมยิงประณีต (P25)
# Card 10: ฐานกล้องเล็ง (P26)
# Card 11: กระโจมประจำหมู่ (P30, P31)
# Card 12: กระโจมกระสุน (P32, P33)
# Card 13: กระโจมส่วนบรรจุ (P34, P35)

print("Mapping items...")
