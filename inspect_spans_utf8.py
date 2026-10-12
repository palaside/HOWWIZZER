import fitz

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")
page = doc[0]

with open("d:/Project/WEPAPP/spans_analysis.txt", "w", encoding="utf-8") as out:
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" in b:
            for line in b["lines"]:
                for span in line["spans"]:
                    txt = span["text"].strip()
                    if txt:
                        out.write(f"Size: {span['size']:.1f}pt | Font: {span['font']} | Text: {txt}\n")

print("Done")
