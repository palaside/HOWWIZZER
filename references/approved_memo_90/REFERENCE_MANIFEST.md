# REFERENCE MANIFEST: REF-MEMO-90-V1

## 📌 ข้อมูลอ้างอิงเอกสารที่ผ่านการอนุมัติ (Gold Standard)
- **รหัสอ้างอิง:** `REF-MEMO-90-V1`
- **ชื่อเอกสาร:** บันทึกข้อความ ขอส่งใบติดตามใบส่งซ่อมเกิน ๙๐ วัน
- **ประเภทเอกสาร:** A4 แนวตั้ง 1 หน้า (Single-page A4 Portrait Official Military Memo)
- **วันที่บันทึกเป็น Reference:** 11 ตุลาคม 2569
- **สถานะ:** PASS 100% (อนุมัติเป็น Gold Standard แม่แบบบันทึกข้อความ)

---

## 🏆 กฎและมาตรฐานที่ใช้ในการสร้าง (Active Rules Applied)
1. **[RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md)**
   - ความแม่นยำระดับพิกเซลบนมาตรฐานกระดาษ A4 แนวตั้ง (210mm x 297mm)
   - ฟอนต์ภาษาไทยสารบรรณ `TH Sarabun PSK` / `Sarabun`, น้ำหนัก Thin/Light (`font-weight: 300`), ขนาดเนื้อหา 12 pt, Line-height 1.5
   - ใช้ตราครุฑเวกเตอร์ 3 ซม. (`garuda_vector_official.png`)
   - ตัวเลขไทย 100% ทั้งเอกสาร
   - เส้นประจุดสำหรับส่วนราชการ, ที่ และวันที่ (เว้น 10 เคาะสำหรับวันที่)
   - บรรทัด "เรื่อง" ข้อความบรรทัดเดียว ไม่ขึ้นบรรทัดใหม่ และไม่มีเส้นไข่ปลา
   - คงสภาพ Single Source of Truth ผ่าน `table_layout_memo_90.json`

2. **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)**
   - **พิกัดตำแหน่งการลงนามมาตรฐาน:**
     - แนวตั้ง / บันทึกข้อความ: ห่างจากขอบกระดาษทางซ้าย **130 มม.** (`padding-left: 105mm;` เมื่อ Margin ซ้าย 25mm)
     - เคาะลงมา **5 Enter จากบรรทัดข้อความสุดท้าย** (`จึงเรียนมาเพื่อกรุณาพิจารณา`) ก่อนเริ่มยศลงนาม (`margin-top: 55pt;` / `space_before: Pt(55)`)
   - **Universal Red Line Standard (`signature` skill):**
     - จุด `.` ท้ายสุดของยศ (`ร.อ.`) ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อเป๊ะ 100% (`right: 100%` ของ `.sig-name-wrapper`)
     - ชื่อและตำแหน่งจัดกึ่งกลางร่วมกันเสมอ

---

## 📂 รายการไฟล์ในแพ็กเกจ Reference
- **HTML Blueprint:** [บันทึกข้อความ_90_วัน_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.html)
- **DOCX Template:** [บันทึกข้อความ_90_วัน_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.docx)
- **XLSX Sheet:** [บันทึกข้อความ_90_วัน_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.xlsx)
- **SSOT Blueprint Schema:** [table_layout_memo_90.json](file:///d:/Project/WEPAPP/references/approved_memo_90/table_layout_memo_90.json)
