# 🏆 APPROVED REFERENCE: บันทึกข้อความ (ขอส่งใบติดตามใบส่งซ่อมเกิน ๔๕ วัน)

**Document ID:** `REF-MEMO-LATEST-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** หนังสือราชการภายใน / บันทึกข้อความ ทางทหาร (Royal Thai Army Official Internal Memorandum)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **บันทึกข้อความ** ตามระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ พ.ศ. ๒๕๒๖ และธรรมเนียมทหาร สังกัดกองพันทหารปืนใหญ่ที่ ๔ กรมทหารปืนใหญ่ที่ ๔ (ป.๔ พัน.๔ ร้อย.๒):
1. **การควบคุมขนาดหน้าเอกสาร (Paper & Margin Standards):**
   - กระดาษขนาด **A4 แนวตั้ง (Portrait: 210mm x 297mm)**
   - ระยะขอบมาตรฐาน: ขอบบน ๒.๕ ซม., ขอบล่าง ๒.๐ ซม., ขอบซ้าย ๓.๐ ซม., ขอบขวา ๒.๐ ซม.
   - บรรจุเนื้อหาจบลงตัวภายใน **๑ หน้าพอดีเป๊ะ (Single-page Portrait)**
2. **ตราครุฑและหัวเรื่อง (Header & Emblem):**
   - ตราครุฑขนาดความสูง **๑.๕ ซม.** ชิดขอบบนซ้ายตามแบบงานสารบรรณบันทึกข้อความ
   - ข้อความ **"บันทึกข้อความ"** ขนาดฟอนต์ 29pt ตัวหนา กึ่งกลางหน้ากระดาษ
3. **แถบข้อมูลราชการ (Metadata Rows):**
   - `ส่วนราชการ`, `ที่`, `วันที่`, `เรื่อง` ใช้เส้นประนำสายตา (Dotted Leader) รองรับข้อความชัดเจน
4. **บล็อกลงนามมาตรฐานสากล (Universal Red Line Standard):**
   - ปฏิบัติตามกฎ [RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)
   - จุด `.` ท้ายสุดของยศ (`ร.ท.`) ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อ `(กฤติน  นราพงษ์)` พอดีเป๊ะ 100%
   - ชื่อและตำแหน่ง (`ผบ.ป.๔ พัน.๔ ร้อย.๒`) จัดกึ่งกลางร่วมกัน ห่างกัน ๑ Enter (Space After 0 pt)
   - ระดับยศปรับลดลงมา ๑ เอนเตอร์ตามคำสั่งอนุมัติของผู้ใช้งาน

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html)**
   - สเปก: 1-Page A4 แนวตั้ง (Portrait 210mm x 297mm) ฝังตราครุฑ Base64 พร้อมคำสั่ง `@page` สั่งพิมพ์ได้ทันที
2. **[บันทึกข้อความล่าสุดสุด_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word A4 Portrait, กั้นระยะขอบและ Tab Stop มาตรฐานงานสารบรรณ พร้อมรูปภาพครุฑ
3. **[บันทึกข้อความล่าสุดสุด_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.xlsx)**
   - สเปก: ตาราง Excel จัดรูปแบบบันทึกข้อความพิมพ์ลง A4 พอดี ๑ หน้า
4. **[table_layout_memo.json](file:///d:/Project/WEPAPP/references/approved_memo_latest/table_layout_memo.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ครอบคลุมโครงสร้างและข้อความทั้งหมด
5. **[build_superclone_memo.py](file:///d:/Project/WEPAPP/references/approved_memo_latest/build_superclone_memo.py)**
   - สคริปต์คอมไพเลอร์อัตโนมัติ 3 ฟอร์แมต (HTML, XLSX, DOCX)
6. **[take_memo_vision.py](file:///d:/Project/WEPAPP/references/approved_memo_latest/take_memo_vision.py)**
   - สคริปต์ Playwright สำหรับรัน Automated Visual QA
7. **[garuda_memo.png](file:///d:/Project/WEPAPP/references/approved_memo_latest/garuda_memo.png)**
   - ตราครุฑความละเอียดสูงขนาดมาตรฐาน 1.5 ซม.
8. **ภาพเรนเดอร์จริง Visual QA:**
   - [memo_latest_rebuild_full.png](file:///d:/Project/WEPAPP/references/approved_memo_latest/memo_latest_rebuild_full.png) (ภาพรวมทั้งหน้า)
   - [memo_latest_header_crop.png](file:///d:/Project/WEPAPP/references/approved_memo_latest/memo_latest_header_crop.png) (ส่วนหัวและตราครุฑ)
   - [memo_latest_meta_crop.png](file:///d:/Project/WEPAPP/references/approved_memo_latest/memo_latest_meta_crop.png) (แถบข้อมูลราชการ)
   - [memo_latest_sig_crop.png](file:///d:/Project/WEPAPP/references/approved_memo_latest/memo_latest_sig_crop.png) (บล็อกลงนามมาตรฐาน)
