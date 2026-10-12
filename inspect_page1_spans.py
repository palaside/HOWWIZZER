import fitz

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")
page = doc[0]

# Inspect fonts used
fonts = page.get_fonts()
print("Fonts on page 1:", fonts)

# Inspect spans for font sizes
blocks = page.get_text("dict")["blocks"]
for b in blocks[:15]:
    if "lines" in b:
        for line in b["lines"]:
            for span in line["spans"]:
                txt = span["text"].strip()
                if txt:
                    print(f"Font: {span['font']}, Size: {span['size']:.1f}pt, Text: {txt[:40]}")
