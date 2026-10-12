# 🏆 APPROVED REFERENCE: ประวัติการใช้อาวุธ (ป.หมู่ ๒ ถึง ๖)

**Document ID:** `REF-GUN-HIST-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** ทะเบียนประวัติการใช้อาวุธประจำหมู่ปืนใหญ่ (Royal Thai Army Artillery Squad Weapon History Form)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **ประวัติการใช้อาวุธ (ป.หมู่ ๒ ถึง ๖)** ใช้เป็นบรรทัดฐานอ้างอิงในการโคลนเอกสารทะเบียนประวัติอาวุธ, การจัดตาราง 4 คอลัมน์ (30% / 24% / 23% / 23%), การแยกบรรทัดบันทึกการยิงครั้งสุดท้ายออกเป็น 2 บรรทัดด้วย 1 Enter, และการจัดบล็อกลงนามมาตรฐาน Universal Red Line Standard พร้อมการเว้นระยะห่างหลังย่อหน้าของคำรับรองตามแบบราชการ

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[ประวัติการใช้อาวุธ_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.html)**
   - สเปก: 5-Page A4 แนวตั้ง (Portrait), ขนาด 210mm x 297mm
   - โครงสร้างตารางหลัก 4 คอลัมน์:
     - คอลัมน์ 1 `ส่วนประกอบ`: กว้าง 30% จัดกึ่งกลาง (`text-center`) รองรับชื่ออุปกรณ์ยาวโดยไม่ตกบรรทัด
     - คอลัมน์ 2 `หมายเลขแบบ`: กว้าง 24% จัดกึ่งกลาง (`text-center`)
     - คอลัมน์ 3 `หมายเลข`: กว้าง 23% จัดกึ่งกลาง (`text-center`) แปลงตัวเลขเป็นเลขไทย 100%
     - คอลัมน์ 4 `หมายเหตุ`: กว้าง 23% จัดกึ่งกลาง (`text-center`)
   - ระยะห่างด้านบน: ตารางห่าง 1 Enter (24pt) จากชื่อแบบฟอร์ม
   - บรรทัดบันทึกการยิง: แยกเป็น 2 บรรทัด เคาะห่างกัน 1 Enter
     - บรรทัดที่ 1: `วัน เดือน ปี ที่ยิงครั้งสุดท้าย   ........./............../............../`
     - บรรทัดที่ 2: `จำนวนนัดที่ยิงมาแล้ว ............  นัด`
   - บล็อกลงนามและการรับรอง: Universal Red Line Standard
     - คำรับรอง: `ตรวจถูกต้อง` เคาะ 1 Enter แบบมีระยะห่างหลังย่อหน้า (`margin-bottom: 32px`) ก่อนถึงยศ
     - จุด `.` ท้ายสุดของยศ `ร.อ.` ตรงกับแนวเส้นดิ่งเดียวกันกับวงเล็บเปิด `(` ของชื่อเป๊ะ 100%
     - ชื่อ `(กฤติน  นราพงษ์)` และตำแหน่ง `ผบ.ป.๔ พัน.๔ ร้อย.๒` จัดกึ่งกลางร่วมกัน ห่างกัน 1 Enter Space After 0 pt
2. **[ประวัติการใช้อาวุธ_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word A4 Portrait, คอลัมน์ตาราง [2.06 in, 1.65 in, 1.58 in, 1.58 in]
   - บันทึกการยิง 2 บรรทัด และบล็อกลงนาม Tab Axis กึ่งกลางตามมาตรฐาน
3. **[ประวัติการใช้อาวุธ_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.xlsx)**
   - สเปก: 5 Worksheets แยกตาม ป.หมู่ ๒ ถึง ๖, ฟอนต์ TH Sarabun PSK 16pt
   - ข้อมูลและตัวเลขไทยคงสภาพสมบูรณ์แบบ
4. **[table_layout_gun_history.json](file:///d:/Project/WEPAPP/references/approved_gun_history/table_layout_gun_history.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ครอบคลุมทั้ง 5 ป.หมู่
5. **[build_superclone_gun_history.py](file:///d:/Project/WEPAPP/references/approved_gun_history/build_superclone_gun_history.py)**
   - สคริปต์คอมไพเลอร์ผลิตเอกสารแบบอัตโนมัติครบ 3 ฟอร์แมต (HTML, XLSX, DOCX)
6. **[gun_history_page_1_full.png](file:///d:/Project/WEPAPP/references/approved_gun_history/gun_history_page_1_full.png)**
   - ภาพเรนเดอร์จริงหน้าเต็ม ป.หมู่ ๒
7. **[gun_history_sig_crop.png](file:///d:/Project/WEPAPP/references/approved_gun_history/gun_history_sig_crop.png)**
   - ภาพเรนเดอร์จริงบล็อกลงนามและคำรับรองตรวจถูกต้องตาม Universal Red Line Standard
8. **[gun_history_table_crop.png](file:///d:/Project/WEPAPP/references/approved_gun_history/gun_history_table_crop.png)**
   - ภาพเรนเดอร์จริงตาราง 4 คอลัมน์

---

## 📐 3. สเปกมาตรฐานที่ผ่านการอนุมัติ (Approved Specs)
- **อัตราส่วนตาราง 4 คอลัมน์ (Master Column Ratio):**
  - คอลัมน์ 1: **ส่วนประกอบ** (30%)
  - คอลัมน์ 2: **หมายเลขแบบ** (24%)
  - คอลัมน์ 3: **หมายเลข** (23%)
  - คอลัมน์ 4: **หมายเหตุ** (23%)
- **การแยกบรรทัดบันทึกการยิง:**
  - บรรทัดที่ 1: `วัน เดือน ปี ที่ยิงครั้งสุดท้าย   ........./............../............../`
  - บรรทัดที่ 2: `จำนวนนัดที่ยิงมาแล้ว ............  นัด` (ห่างกัน 1 Enter)
- **บล็อกลงนามและการรับรอง (Original Source Fidelity & Universal Red Line Standard):**
  - คำรับรอง: `ตรวจถูกต้อง` (เคาะ 1 Enter พร้อมระยะห่างหลังย่อหน้า 32px / 24pt)
  - จุด `.` ท้ายสุดของยศ `ร.อ.` ตรงกับแนวเส้นดิ่งเดียวกันกับวงเล็บเปิด `(` ของชื่อ `(กฤติน  นราพงษ์)` 100%
  - ชื่อและตำแหน่ง `ผบ.ป.๔ พัน.๔ ร้อย.๒` จัดกึ่งกลางร่วมกัน
