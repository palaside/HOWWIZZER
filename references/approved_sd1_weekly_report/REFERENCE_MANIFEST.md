# REFERENCE MANIFEST: REF-SD1-WEEKLY-REPORT-V1

## 📌 ข้อมูลอ้างอิงเอกสารที่ผ่านการอนุมัติ (Gold Standard)
- **รหัสอ้างอิง:** `REF-SD1-WEEKLY-REPORT-V1`
- **ชื่อเอกสาร:** บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (สด.๑)
- **ประเภทเอกสาร:** A4 ไฮบริด 5 หน้า (4 หน้าแรก A4 แนวตั้ง + หน้าสุดท้าย A4 แนวนอน)
  - หน้า ๑: บันทึกข้อความนำส่งรายงานผลการตรวจประจำสัปดาห์
  - หน้า ๒-๓: แบบรายงานผลการตรวจอาวุธ และสิ่งอุปกรณ์ประจำโรงเก็บปืนใหญ่ (สด.๑ แผ่น ๑ และ แผ่น ๒)
  - หน้า ๔: ภาพถ่ายการตรวจ โรงเก็บปืนใหญ่ ป.๔ พัน.๔ ร้อย.๒ (๔ ภาพพร้อมข้อความรับรอง)
  - หน้า ๕: บันทึกผลการตรวจอาวุธและเครื่องควบคุมการยิง (ตารางแนวนอน A4 Landscape)
- **วันที่บันทึกเป็น Reference:** 11 ตุลาคม 2569
- **สถานะ:** PASS 100% (อนุมัติเป็น Gold Standard แม่แบบชุดรายงานผลการตรวจ สด.๑)

---

## 🏆 กฎและมาตรฐานที่ใช้ในการสร้าง (Active Rules Applied)
1. **[RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md)**
   - สถาปัตยกรรมเอกสารแบบไฮบริด 5 หน้า (Multi-Page Hybrid Document):
     - หน้า ๑ ถึง ๔: A4 แนวตั้ง (`@page portrait-page`, 210mm x 297mm)
     - หน้า ๕: A4 แนวนอน (`@page landscape-page`, 297mm x 210mm)
   - ฟอนต์มาตรฐานราชการไทย `Sarabun` / `TH Sarabun PSK` ขนาด 11-12 pt
   - รองรับ OpenType Features (`font-feature-settings: "locl" 1, "numr" 1; font-variant-numeric: tabular-nums;`)
   - ตราครุฑเวกเตอร์ 3 ซม. ในหน้า ๑
   - ตัวเลขไทย 100% ตลอดทั้งชุดเอกสาร
   - Single Source of Truth (SSOT) ผ่าน `table_layout_sd1.json`

2. **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)**
   - **การจัดตำแหน่งและการตัดจุดลงนามที่ซ้ำซ้อนตามคำสั่งการอนุมัติ:**
     - **หน้า ๑ บันทึกข้อความ:** คงการลงนามพิกัด 130 มม. จากขอบซ้าย (ร.อ. กฤติน นราพงษ์ ผบ.ป.๔ พัน.๔ ร้อย.๒) พร้อมแกนดิ่ง Red Line Standard
     - **หน้า ๓ (สด.๑ แผ่น ๒):** ตัดบล็อกการลงนามออกตามคำสั่งผู้ใช้งาน (ไม่ซ้ำซ้อน)
     - **หน้า ๔ (ภาพถ่ายการตรวจ):** ตัดบล็อกการลงนามออกตามคำสั่งผู้ใช้งาน (คงเฉพาะข้อความรับรองภาพถ่าย)
     - **หน้า ๕ (บันทึกผลการตรวจ แนวนอน):** คงบล็อกการลงนาม `ตรวจถูกต้อง` ชิดขวา ห่างขอบ 15 มม. (ร.อ. กฤติน นราพงษ์ ผบ.ป.๔ พัน.๔ ร้อย.๒ ส.ค. ๖๙)
   - **Universal Red Line Standard (`signature_engine.py`):**
     - จุด `.` ท้ายสุดของยศ ตรงกับแนวเส้นดิ่งเดียวกันกับวงเล็บเปิด `(` ของชื่อเป๊ะ 100%
     - ใน Word (.docx) ใช้ระบบ Tab Stop Anchor (`WD_TAB_ALIGNMENT.RIGHT` สำหรับยศ และ `WD_TAB_ALIGNMENT.LEFT` สำหรับชื่อ)
     - ใน Excel (.xlsx) จัดแนวแกนคอลัมน์มาตรฐาน

---

## 📂 รายการไฟล์ในแพ็กเกจ Reference
- **HTML Blueprint:** [แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html)
- **DOCX Template:** [แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx)
- **XLSX Sheet:** [แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx)
- **SSOT Blueprint Schema:** [table_layout_sd1.json](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/table_layout_sd1.json)
