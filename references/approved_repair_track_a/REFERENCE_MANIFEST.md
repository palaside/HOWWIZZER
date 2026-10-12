# REFERENCE MANIFEST: REF-REPAIR-TRACK-A-V1

## 📌 ข้อมูลอ้างอิงเอกสารที่ผ่านการอนุมัติ (Gold Standard)
- **รหัสอ้างอิง:** `REF-REPAIR-TRACK-A-V1`
- **ชื่อเอกสาร:** ทบ.๔๐๐-๐๗๑ แบบ ก ใบติดตามใบส่งซ่อม (การเบิกเกิน ๔๕ - ๙๐ วัน)
- **ประเภทเอกสาร:** A4 แนวนอน 1 หน้า (Single-page A4 Landscape)
- **วันที่บันทึกเป็น Reference:** 11 ตุลาคม 2569
- **สถานะ:** PASS 100% (อนุมัติเป็น Gold Standard แม่แบบใบติดตามใบส่งซ่อม แบบ ก)

---

## 🏆 กฎและมาตรฐานที่ใช้ในการสร้าง (Active Rules Applied)
1. **[RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md)**
   - ความแม่นยำระดับพิกเซลบนมาตรฐานกระดาษ A4 แนวนอน (297mm x 210mm)
   - ฟอนต์ภาษาไทยสารบรรณ `TH Sarabun PSK` / `Sarabun`, น้ำหนัก Regular/Bold, ขนาดเนื้อหา 11.5 - 12 pt
   - ตัวเลขไทย 100% ทั้งเอกสาร
   - เส้นประจุดสำหรับเลขที่เอกสาร (`ที่…………………………………………….`)
   - หัวตาราง 6 คอลัมน์ ตามระเบียบ ทบ.๔๐๐-๐๗๑:
     - คอลัมน์ ๑ (5%): ลำดับ
     - คอลัมน์ ๒ (21%): รายการ สป.
     - คอลัมน์ ๓ (17%): หมายเลข สป.
     - คอลัมน์ ๔ (18%): `ที่ใบส่งซ่อม ที่ทะเบียนหน่วย`<br>`จ่าย` (จัด ๒ บรรทัดเป๊ะ)
     - คอลัมน์ ๕ (18%): `วันที่ส่งหรือวางใบส่งซ่อม` (บรรทัดเดียวจบ ไม่ตกบรรทัด)
     - คอลัมน์ ๖ (21%): `หมายเหตุ  (บันทึกโดยหน่วยจ่าย)` (บรรทัดเดียวจบ ไม่ตกบรรทัด)
   - ข้อความกำกับด้านล่าง: `( พิมพ์ตามระเบียบกองทัพบกว่าด้วยการส่งกำลังสิ่งอุปกรณ์ ประเภท ๒ และ ๔ พ.ศ. ๒๕๓๔ )`
   - คงสภาพ Single Source of Truth ผ่าน `table_layout_repair_track_a.json`

2. **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)**
   - **บล็อกการลงนามแบบคู่ (Double Signature Block):**
     - **ฝั่งซ้าย (ผู้บังคับหน่วย):**
       - ยศ: `ร.อ.`
       - ชื่อ: `(กฤติน  นราพงษ์)`
       - ตำแหน่ง: `ผบ.ป.๔ พัน.๔ ร้อย.๒`
       - วันที่: `ธ.ค. ๖๘` (เว้นวรรค ๕ เคาะนำหน้าสำหรับลงลายมือเขียน)
     - **ฝั่งขวา (ผู้ตรวจสอบ):**
       - คำรับรอง: `ผู้ตรวจสอบ`
       - ยศ: `จ.ส.อ.`
       - ชื่อ: `(ณัฐชัย  รักษาวงษ์)`
       - ตำแหน่ง: `ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒`
       - วันที่: `ธ.ค. ๖๘` (เว้นวรรค ๕ เคาะนำหน้าสำหรับลงลายมือเขียน)
   - **Universal Red Line Standard (`signature` skill):**
     - จุด `.` ท้ายสุดของยศ ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อเป๊ะ 100% (`right: 100%` ของ `.sig-name-wrapper`)
     - ชื่อและตำแหน่งจัดกึ่งกลางร่วมกันเสมอ ห่างกัน 1 Enter

---

## 📂 รายการไฟล์ในแพ็กเกจ Reference
- **HTML Blueprint:** [ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html)
- **DOCX Template:** [ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.docx)
- **XLSX Sheet:** [ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.xlsx)
- **SSOT Blueprint Schema:** [table_layout_repair_track_a.json](file:///d:/Project/WEPAPP/references/approved_repair_track_a/table_layout_repair_track_a.json)
- **Visual Evidence:** [repair_track_a_playwright_p1.png](file:///d:/Project/WEPAPP/references/approved_repair_track_a/repair_track_a_playwright_p1.png)
