# 📊 PROJECT STATUS: WEPAPP
> **Evaluation Mode:** Reverse Engineering & Chain of Thought (CoT)  
> **Persona:** SENIOR FULL-STACK DEVELOPER AGENT  
> **Date:** 2026-10-14  

---

## 🏆 Project Overview
`WEPAPP` เป็นระบบบริหารจัดการคลังยุทโธปกรณ์และผลิตเอกสารราชการระดับ Production สำหรับกองทัพบก ขับเคลื่อนด้วยสถาปัตยกรรม **SUPERCLONE Engine** และ **Universal Sarabun Gold Standard** รองรับการทำงานทั้งบน Web UI (FastAPI/HTML5/Vanilla JS) และการสร้างเอกสารข้ามแพลตฟอร์ม (HTML, Word `.docx`, Excel `.xlsx`)

---

## 📋 Feature Tracking Matrix

### 1. Informal Equipment Inventory & Loan Tracking System
- [x] **Database & Balance Engine (`backend/services/informal_equipment_service.py`):**
  - [x] Section 1: สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (๔๓ รายการ)
  - [x] Section 2: สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (๒๙ รายการ)
  - [x] ระบบคำนวณยอดคงเหลือ (Balance Amount), ยอดเบิกยืม (Loan Amount), ยอดส่งซ่อม (Repair Amount)
  - [x] การตัดสต็อกและบันทึกประวัติการยืม-คืน
  - [x] ระบบแจ้งเตือนรายการยืมเกินกำหนด (Overdue Loans Alert)
  - [x] ระบบบันทึกการส่งคืนแยกประเภท: คืนปกติ (นำกลับเข้าคลัง) และคืนชำรุดเสียหาย (ย้ายเข้าหมวดส่งซ่อม)
  - [x] การสกัดสาเหตุ (Cause) และอาการชำรุด (Symptom) ออกเป็น ๒ ฟิลด์อิสระ

### 2. Universal RTA Memo Standard Engine (`table_layout_damage_memo.json`)
- [x] **การอ้างอิงตรงจากระเบียบราชการ:**
  - [x] ระเบียบ ทบ. ว่าด้วยงานสารบรรณ พ.ศ. ๒๕๖๓ ผนวก ก อนุผนวก ๑ (แบบที่ ๑ หน้า ๒๙ - แบบพิมพ์ในโปรแกรมคอมพิวเตอร์)
  - [x] ระเบียบสำนักนายกรัฐมนตรี ว่าด้วยงานสารบรรณ พ.ศ. ๒๕๒๖ และที่แก้ไขเพิ่มเติม
- [x] **มิติเรขาคณิตตราครุฑและระยะขอบกระดาษ:**
  - [x] ตราครุฑ: สูง ๑๕ มม. กว้าง ๑๓.๘ มม. ชิดมุมบนซ้าย ห่างจากขอบกระดาษด้านบน ๑๕ มม.
  - [x] ขอบกระดาษ: บน ๑๕ มม., ซ้าย ๓๐ มม., ขวา ๒๐ มม., ล่าง ๒๐ มม.
- [x] **โครงสร้างเนื้อความ ๓ ภาค (3-Tier Paragraph Division):**
  - [x] `paragraph_1_reason` (ข้อความภาคเหตุ)
  - [x] `paragraph_2_intention` (ข้อความภาคความประสงค์)
  - [x] `paragraph_3_summary` (ข้อความภาคสรุป)
  - [x] ทุกภาคกั้นหน้าย่อหน้า ๒.๕ ซม. (`text-indent: 25mm`) และจัดชิดขอบ inter-cluster
- [x] **ระบบพิมพ์แพ็กเกจคู่ขนาน ๒ ชุด (Dual-Copy Engine):**
  - [x] ฉบับตัวจริง: ซ่อนแถบสำเนา และซ่อนบล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน
  - [x] สำเนาคู่ฉบับ: แสดงแถบ `(สำเนาคู่ฉบับ)` กึ่งกลางบน และแสดงบล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน
- [x] **บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน ๔ คอลัมน์ ๒ แกนดิ่ง (Staff Review Footer Dual-Axis):**
  - [x] โครงสร้าง ๔ คอลัมน์ (ยศ, บทบาท, วันที่, เดือนปี)
  - [x] แกนตัวอักษรแรกของยศตรงกันเป๊ะ และแกนคำว่าเดือนปีตรงกันเป๊ะ โดยมีปี พ.ศ. ขนานกับขอบขวาของเนื้อหาเป๊ะ ๑๐๐%
- [x] **ระบบป้องกันคำขาดภาษาไทย (Zero Split Words):**
  - [x] แทรก Zero-Width Space (`\u200b`) ผ่าน `thai_typography_engine.py` คุ้มครองแท็ก HTML และคำย่อทหาร

### 3. Core Universal Engines & Governance
- [x] **Universal Signature Engine (`signature_engine.py`):**
  - [x] Red Line Standard ๑๓๐ มม. จุดท้ายยศชนวงเล็บเปิดของชื่อ ๑๐๐%
  - [x] ระยะเคาะมาตรฐาน ๕ Enter ใต้ข้อความสุดท้าย
- [x] **Zero-Overflow PageFit Engine (`RULE-PAGEFIT-TUNING-V1`):**
  - [x] รับประกันเอกสารฟิตพอดีหน้า A4 หน้าละ ๑ แผ่น ๑๐๐% ปราศจากหน้าขาวส่วนเกิน
- [x] **One-Click Launchers:**
  - [x] `run_webapp.bat`: รัน FastAPI และเปิดเบราว์เซอร์อัตโนมัติ
  - [x] `run_superclone.bat`: คอมไพล์เอกสารออฟไลน์

---

## 🔍 Visual QA & Verification Status
- **ฉบับตัวจริง (`verified_memo_page1_new_schema.png`):** PASS (ฟิตพอดี ๑ หน้า A4, ตราครุฑ 15x13.8 มม., ระยะขอบเป๊ะตามหน้า ๒๙)
- **สำเนาคู่ฉบับ (`verified_memo_page2_new_schema.png`):** PASS (ฟิตพอดี ๑ หน้า A4, มีแถบสำเนาคู่ฉบับ, บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน ๔ คอลัมน์ พ.ศ. ขนานขอบขวา)
