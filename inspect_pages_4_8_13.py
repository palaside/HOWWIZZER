import fitz

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

with open(r"d:\Project\WEPAPP\pages_4_8_13_text.txt", "w", encoding="utf-8") as out:
    for p in [4, 8, 13]:
        out.write(f"\n================ FULL TEXT PAGE {p} ================\n")
        out.write(doc[p-1].get_text())

print("Done")
