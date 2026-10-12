import fitz
import json

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")
page = doc[0]

print("Page 1 Rect:", page.rect)

# Extract drawings (rectangles, lines)
drawings = page.get_drawings()
print(f"Total vector drawings on Page 1: {len(drawings)}")

# Extract text blocks with bbox
blocks = page.get_text("blocks")
print(f"Total text blocks on Page 1: {len(blocks)}")
for b in blocks[:25]:
    # b is (x0, y0, x1, y1, text, block_no, block_type)
    text_clean = b[4].strip().replace('\n', ' ')
    print(f"BBox: ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}) -> {text_clean[:60]}")
