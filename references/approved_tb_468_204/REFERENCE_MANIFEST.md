# 🏆 APPROVED REFERENCE: ทบ.๔๖๘-๒๐๔ (คส. ๔) บัญชีหมายเลขอาวุธ

**Document ID:** `REF-TB-468-204-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** แบบฟอร์มบัญชีหมายเลขอาวุธและอุปกรณ์ ทบ. (Royal Thai Army Weapon & Equipment Serial Inventory)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **ทบ. ๔๖๘–๒๐๔ (คส. ๔) บัญชีหมายเลขอาวุธ** ใช้เป็นบรรทัดฐานอ้างอิงในการโคลนเอกสารบัญชีหมายเลขอาวุธ, การควบคุมอัตราส่วนคอลัมน์มาตรฐาน (20% / 65% / 15%), การแสดงผลชื่อรายการเต็มโดยไม่ใช้เครื่องหมายละ (`”`), การเว้นระยะ 1 Enter จากชื่อแบบฟอร์ม, และการจัดบล็อกลงนามมาตรฐาน Universal Red Line Standard

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[ทบ_468_204_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.html)**
   - สเปก: 6-Page A4 แนวตั้ง (Portrait), ขนาด 210mm x 297mm
   - โครงสร้างตารางหลัก 3 คอลัมน์:
     - คอลัมน์ 1 `หมายเลข`: กว้าง 20% จัดกึ่งกลาง (`text-center`)
     - คอลัมน์ 2 `รายการ`: กว้าง 65% จัดกึ่งกลาง (`text-center`) แสดงชื่อเต็มทุกแถวตามจำนวน ไม่ใช้เครื่องหมายละ (`”`)
     - คอลัมน์ 3 `หมายเหตุ`: กว้าง 15% จัดกึ่งกลาง (`text-center`)
   - ระยะห่างด้านบน: ตารางห่าง 1 Enter (24pt) จากชื่อแบบฟอร์ม `บัญชีหมายเลขอาวุธ`
   - ข้อความรับรอง: ตัดเครื่องหมาย `( --- )` ออก จัดเรียง 4 บรรทัดกึ่งกลางคอลัมน์รายการ
   - บล็อกลงนาม: Universal Red Line Standard ปลายยศ `ร.อ.` ตรงกับ `(` ของชื่อ
2. **[ทบ_468_204_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word A4 Portrait, คอลัมน์ตารางล็อกขนาด [1.37 in, 4.47 in, 1.03 in]
   - ข้อมูลรายการจัดกึ่งกลาง (`WD_ALIGN_PARAGRAPH.CENTER`) และบล็อกลงนามกำหนด Tab Axis กึ่งกลางเป๊ะ
3. **[ทบ_468_204_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.xlsx)**
   - สเปก: 6 Worksheets แยกแผ่นตามหน้า, ตัวอักษร TH Sarabun PSK 16pt
   - ข้อมูลหมายเลข รายการ และหมายเหตุ จัดกึ่งกลาง (`align_center`) 100%
4. **[table_layout_468_204.json](file:///d:/Project/WEPAPP/references/approved_tb_468_204/table_layout_468_204.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ครอบคลุมทั้ง 6 หน้าอุปกรณ์
5. **[build_superclone_468_204.py](file:///d:/Project/WEPAPP/references/approved_tb_468_204/build_superclone_468_204.py)**
   - สคริปต์คอมไพเลอร์ผลิตเอกสารแบบอัตโนมัติครบ 3 ฟอร์แมต (HTML, XLSX, DOCX)
6. **[weapon_page_2_table_crop.png](file:///d:/Project/WEPAPP/references/approved_tb_468_204/weapon_page_2_table_crop.png)**
   - ภาพเรนเดอร์จริงแผ่นที่ ๒ แสดงรายการ `กล้องเล็งพาโนรามิค` ๙ รายการเต็มชื่อ จัดกึ่งกลางสมบูรณ์
7. **[weapon_cert_sig_crop.png](file:///d:/Project/WEPAPP/references/approved_tb_468_204/weapon_cert_sig_crop.png)**
   - ภาพเรนเดอร์จริงข้อความรับรอง 4 บรรทัด และบล็อกลงนามตามมาตรฐาน Universal Red Line Standard

---

## 📐 3. สเปกมาตรฐานที่ผ่านการอนุมัติ (Approved Specs)
- **อัตราส่วนตาราง 3 คอลัมน์ (Master Column Ratio):**
  - คอลัมน์ 1: **หมายเลข** (ความกว้าง 20%)
  - คอลัมน์ 2: **รายการ** (ความกว้าง 65%)
  - คอลัมน์ 3: **หมายเหตุ** (ความกว้าง 15%)
- **การจัดตำแหน่งรายการ (Data Alignment):**
  - ชื่อรายการทุกแถวแสดงเต็มข้อความ (ห้ามใช้ `”`) และจัดวาง **กึ่งกลางคอลัมน์ (Center Alignment)**
- **ระยะห่างหัวตาราง (Rhythm):**
  - เว้นระยะห่าง 1 Enter (24pt) ชัดเจนระหว่างชื่อแบบฟอร์มกับขอบบนของตาราง
- **ข้อความรับรอง (Certification Block):**
  - บรรทัดที่ 1: `หมดรายการรวม [จำนวน] [หน่วย] ขอรับรองว่า`
  - บรรทัดที่ 2: `[ชื่อรายการ]`
  - บรรทัดที่ 3: `จำนวน [จำนวน] [หน่วย] ตามหมายเลข`
  - บรรทัดที่ 4: `อยู่ครบถ้วน ถูกต้อง ทุกหมายเลข`
  - ไม่ใส่เครื่องหมาย `---` หรือวงเล็บเปิดปิดหน้าหลัง
- **บล็อกลงนาม (Universal Red Line Standard):**
  - จุด `.` ของยศ `ร.อ.` ตรงกับแนวเส้นดิ่งเดียวกันกับวงเล็บเปิด `(` ของชื่อ `(กฤติน  นราพงษ์)` 100%
  - ชื่อและตำแหน่ง `ผบ.ป.๔ พัน.๔ ร้อย.๒` จัดกึ่งกลางร่วมกัน
