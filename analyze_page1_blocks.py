import fitz
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")
page = doc[0]

print("Page 1 Rect:", page.rect)
width, height = page.rect.width, page.rect.height

# Let's inspect x coordinates to see columns
blocks = page.get_text("blocks")
cards = []
for b in blocks:
    text_clean = b[4].strip().replace('\n', ' ')
    cards.append({
        "bbox": [round(b[0], 1), round(b[1], 1), round(b[2], 1), round(b[3], 1)],
        "text": text_clean
    })

with open("d:/Project/WEPAPP/page1_blocks.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, ensure_ascii=False, indent=2)

print(f"Dumped {len(cards)} blocks to page1_blocks.json")

# Analyze horizontal divisions
x_centers = [(c["bbox"][0] + c["bbox"][2])/2 for c in cards]
print("X coordinates min/max:", min(c["bbox"][0] for c in cards), max(c["bbox"][2] for c in cards))
