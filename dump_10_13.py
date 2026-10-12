import fitz

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

with open(r"d:\Project\WEPAPP\pages_10_13_text.txt", "w", encoding="utf-8") as out:
    for p in range(9, len(doc)):
        out.write(f"\n================ FULL TEXT PAGE {p+1} ================\n")
        out.write(doc[p].get_text())

print("Done")
