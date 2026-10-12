# REFERENCE MANIFEST: REF-MEMO-INQUIRY-90-V1

## 📌 ข้อมูลอ้างอิงเอกสารที่ผ่านการอนุมัติ (Gold Standard)
- **รหัสอ้างอิง:** `REF-MEMO-INQUIRY-90-V1`
- **ชื่อเอกสาร:** ขอส่งใบติดตามทวงถาม ๙๐ วัน (บันทึกข้อความ และ ทบ.๔๐๐-๐๗๑ แบบ ข ใบติดตามใบเบิก)
- **ประเภทเอกสาร:** A4 แนวตั้ง 1 หน้า + US Legal แนวนอน 2 หน้า (3-Page Hybrid Multi-Page Document)
- **วันที่บันทึกเป็น Reference:** 11 ตุลาคม 2569
- **สถานะ:** PASS 100% (อนุมัติเป็น Gold Standard แม่แบบบันทึกข้อความพร้อมแบบฟอร์ม ทบ.๔๐๐-๐๗๑)

---

## 🏆 กฎและมาตรฐานที่ใช้ในการสร้าง (Active Rules Applied)
1. **[RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md)**
   - สถาปัตยกรรมเอกสารแบบไฮบริดหลายหน้า:
     - หน้า ๑: A4 แนวตั้ง (210mm x 297mm) เป็นบันทึกข้อความราชการทหาร
     - หน้า ๒-๓: US Legal แนวนอน (355.6mm x 215.9mm) เป็นแบบฟอร์ม ทบ.๔๐๐-๐๗๑ แบบ ข การเบิกเกิน ๙๐ วัน
   - การควบคุม `@page portrait-page` และ `@page landscape-page` ปลอดภัยต่อการพิมพ์ 100%
   - ฟอนต์ภาษาไทยสารบรรณ `TH Sarabun PSK` / `Sarabun` ขนาด 11-12 pt
   - ตราครุฑเวกเตอร์ 3 ซม. (`garuda_vector_official.png`)
   - ตัวเลขไทย 100% ทั้งเอกสาร
   - โครงสร้าง SSOT ผ่าน `table_layout_memo_inquiry_90.json`

2. **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)**
   - **หน้า ๑ บันทึกข้อความ:**
     - เคาะลงมา **5 Enter จากบรรทัดข้อความสุดท้าย** (`จึงเรียนมาเพื่อกรุณาพิจารณาดำเนินการต่อไป`)
     - พิกัดซ้าย **130 มม.** จากขอบกระดาษ
     - ผู้ลงนาม: ร.อ. (กฤติน  นราพงษ์) ผบ.ป.พัน.๔ ร้อย.๒
   - **หน้า ๒-๓ ทบ.๔๐๐-๐๗๑ (Double Signature Block):**
     - **ฝั่งซ้าย (ผบ.ร้อย):** ยศ `ร.อ.`, ชื่อ `(กฤติน  นราพงษ์)`, ตำแหน่ง `ผบ.ป.พัน.๔ ร้อย.๒`, วันที่ `          มิ.ย. ๕๔`
     - **ฝั่งขวา (ผู้ตรวจสอบ):** หัวข้อ `ผู้ตรวจสอบ`, ยศ `จ.ส.อ.`, ชื่อ `(ณัฐชัย  รักษาวงษ์)`, ตำแหน่ง `ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒`, วันที่ `          มิ.ย. ๕๔`
     - **Universal Red Line Standard (`signature_engine.py`):**
       - จุด `.` ท้ายสุดของยศ ตรงกับแนวเส้นดิ่งเดียวกันกับวงเล็บเปิด `(` ของชื่อเป๊ะ 100%
       - ใน Word (.docx) ใช้ระบบ Tab Stop Anchor (`WD_TAB_ALIGNMENT.RIGHT` สำหรับยศ และ `WD_TAB_ALIGNMENT.LEFT` สำหรับชื่อ)
       - ใน Excel (.xlsx) แยกคอลัมน์ยศชิดขวา และชื่อชิดซ้าย โดยเส้นแบ่งคอลัมน์ทำหน้าที่เป็นแกนดิ่ง Red Line

---

## 📂 รายการไฟล์ในแพ็กเกจ Reference
- **HTML Blueprint:** [ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html)
- **DOCX Template:** [ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx)
- **XLSX Sheet:** [ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx)
- **SSOT Blueprint Schema:** [table_layout_memo_inquiry_90.json](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/table_layout_memo_inquiry_90.json)
