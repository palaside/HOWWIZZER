# 🏛️ WEPAPP: Royal Thai Army Production Document & Armament Inventory Suite
> **Engineering Blueprint, Universal Sarabun Standards, and Automated Inventory Management System**

---

## 📌 Executive Summary (บทสรุปโครงการ)

`WEPAPP` เป็นระบบบริหารจัดการคลังยุทโธปกรณ์และระบบผลิตเอกสารราชการระดับ Production สำหรับกองทัพบก (RTA) พัฒนาขึ้นด้วยสถาปัตยกรรม **SUPERCLONE Production Engine** และ **Universal Sarabun Gold Standard** ครอบคลุม:
1. **ระบบคลังสิ่งอุปกรณ์และติดตามการเบิกยืม/ส่งซ่อม (Informal Equipment Inventory Engine):**
   - จัดการสิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ ๑ - ๔๓) และคลัง บก. (ลำดับ ๑ - ๒๙)
   - หักยอดคงเหลืออัตโนมัติ ติดตามสถานะยืม-คืน แจ้งเตือนรายการค้างส่งคืน (Overdue Alert)
   - รองรับการรายงานความชำรุดเสียหาย แยกอาการ (Symptom) และสาเหตุ (Cause) พร้อมส่งต่อสายส่งซ่อม
2. **ระบบสร้างบันทึกข้อความมาตรฐานทองคำ (Universal RTA Memo Standard):**
   - อ้างอิงตรงจาก **ระเบียบ ทบ. ว่าด้วยงานสารบรรณ พ.ศ. ๒๕๖๓ ผนวก ก อนุผนวก ๑ (แบบที่ ๑ หน้า ๒๙ แบบพิมพ์ในโปรแกรมคอมพิวเตอร์)**
   - มิติเรขาคณิตตราครุฑ: สูง ๑๕ มม. กว้าง ๑๓.๘ มม. ขอบบน ๑๕ มม., ซ้าย ๓๐ มม., ขวา ๒๐ มม., ล่าง ๒๐ มม.
   - การจำแนกเนื้อความ ๓ ภาค: ภาคเหตุ (`paragraph_1_reason`), ภาคความประสงค์ (`paragraph_2_intention`), ภาคสรุป (`paragraph_3_summary`)
   - ระบบพิมพ์คู่ขนาน ๒ ชุด (Dual-Copy Engine): ฉบับตัวจริง + สำเนาคู่ฉบับ
   - บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน ๔ คอลัมน์ ๒ แกนดิ่งคู่ขนาน (Staff Review Footer Dual-Axis Alignment)
   - ฟอนต์ราชการ TH Sarabun PSK (Thin 300 / Bold 600) พร้อมระบบตัดคำภาษาไทย ZWS ป้องกันคำขาดครึ่งท่อน ๑๐๐%
3. **ระบบบล็อกการลงนามสากล (Universal Red Line Standard):**
   - พิกัดยึดแกนดิ่ง: จุด `.` ท้ายสุดของยศ ตรงกับเครื่องหมายวงเล็บเปิด `(` ของชื่อ ๑๐๐%

---

## 🚀 Quick Start & One-Click Launchers (การเริ่มต้นใช้งานคลิกเดียว)

ระบบมีสคริปต์สั่งงานอัตโนมัติแบบ Zero-Command Launcher โดยไม่ต้องจำคำสั่งคอนโซล:

1. **เปิดแดชบอร์ดระบบเว็บแอปพลิเคชัน (FastAPI Server):**
   - ดับเบิลคลิกไฟล์ **`run_webapp.bat`**
   - ระบบจะเปิดเบราว์เซอร์ไปที่ `http://127.0.0.1:8000` พร้อมเริ่มรันเซิร์ฟเวอร์ทันที
2. **รันตัวคอมไพล์เอกสารออฟไลน์ (SUPERCLONE Compiler):**
   - ดับเบิลคลิกไฟล์ **`run_superclone.bat`**
   - ระบบจะคอมไพล์เอกสารตรวจประจำสัปดาห์ออกมาเป็น HTML, DOCX, และ XLSX อัตโนมัติ

---

## 📦 Dependency Installation (การติดตั้งแพ็กเกจ)

```powershell
pip install -r requirements.txt
playwright install chromium
```

---

## 🌐 Git Remote Repository & Off-site Backup

- **Branch หลัก:** `main`
- **Remote Repository URL:** `https://github.com/palaside/WEPAPP.git` (บันทึกไว้ใน `deploy.json`)
- **การสำรองข้อมูล:** ข้อมูลสถานะและพิมพ์เขียวถูกสำรองคู่ขนานไว้ในโฟลเดอร์ `state/` เสมอ

---

## 🏛️ System Architecture & Governance

โครงการนี้อยู่ภายใต้การควบคุมของ **GEMINI.md** และระเบียบมาตรฐาน:
- **`RULE-RTA-MEMO-STANDARD-V1`**: มาตรฐานบันทึกข้อความ ทบ. และพิมพ์เขียว JSON SSOT
- **`RULE-SARABUN-DOC-STANDARD-V1`**: มาตรฐานฟอนต์ TH Sarabun PSK ตัวหนา 600 และเนื้อหาตัวบาง 300
- **`RULE-UNIVERSAL-SIGNATURE-BLOCK-V1`**: บล็อกการลงนาม Red Line Standard 130 มม. 5 Enter
- **`RULE-STAFF-REVIEW-FOOTER-V1`**: บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน ๔ คอลัมน์ ๒ แกนดิ่งคู่ขนาน
- **`RULE-PAGEFIT-TUNING-V1`**: สกิลบีบอัดเอกสารพอดีหน้า A4 แบบ Zero-Overflow Micro-Tuning
