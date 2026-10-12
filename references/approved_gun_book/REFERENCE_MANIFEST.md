# 🏆 APPROVED REFERENCE: สมุดประวัติการใช้ปืนใหญ่ (๕ หน้า - หัวข้อละ ๑ หน้า)

**Document ID:** `REF-GUN-BOOK-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** สมุดประวัติการใช้งานและซ่อมบำรุงปืนใหญ่ประจำหน่วย (Royal Thai Army Artillery Operation & Firing Record Book)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **สมุดประวัติการใช้ปืนใหญ่** ใช้เป็นบรรทัดฐานอ้างอิงในการสร้างสมุดทะเบียนประวัติอาวุธปืนใหญ่แบบ A4 แนวนอน (Landscape 297mm x 210mm) โดยจัดระเบียบตารางและเนื้อหา **กระชับลงตัวหัวข้อละ ๑ หน้าพอดีเป๊ะ (รวม ๕ หน้า ไม่ล้นไม่กินหน้าถัดไป)**:
1. การวางตราสัญลักษณ์ความละเอียดสูงบนหน้าปก
2. แบบบันทึกประวัติอาวุธ ป.๖
3. การจัดวางตารางคำนวณอายุลำกล้องแบบคู่ขนาน (ข้อมูลลำกล้องแบบ Label บน-Value ล่าง ฟอนต์ 15pt เคียงคู่ตาราง ๔ คอลัมน์)
4. ตารางประวัติการใช้ปืนใหญ่และซ่อมบำรุงแบบหัวตารางซ้อน (๖ คอลัมน์ ๑๓ แถว)
5. ตารางบันทึกหลักฐานการยิงแบบหัวตารางซ้อน (๙ คอลัมน์ ๑๓ แถว)

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html)**
   - สเปก: 5-Page A4 แนวนอน (Landscape: 297mm x 210mm)
   - หน้า ๑: หน้าปก (ตรากองพันทหารปืนใหญ่ที่ ๔ + ข้อมูลปืนใหญ่)
   - หน้า ๒: ประวัติอาวุธ (ป.๖)
   - หน้า ๓: การคำนวณอายุลำกล้อง (ชนิด/หมายเลข/อายุลำกล้องสูงสุด ฟอนต์ 15pt แยกคนละบรรทัด + ตาราง ๔ คอลัมน์ ๑๒ แถว)
   - หน้า ๔: ประวัติการใช้ปืนใหญ่ (ตารางปฏิบัติการและซ่อมบำรุง หัวซ้อน ๖ คอลัมน์ ๑๓ แถว)
   - หน้า ๕: บันทึกหลักฐานการยิง (ตารางบันทึกการยิง หัวซ้อน ๙ คอลัมน์ ๑๓ แถว)
2. **[สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word A4 Landscape, ๕ หน้าแยก Section ชัดเจน ตารางล็อกขนาดพอดีเป๊ะ
3. **[สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.xlsx)**
   - สเปก: ๕ Worksheets (`หน้าปก`, `ประวัติอาวุธ (ป.๖)`, `คำนวณอายุลำกล้อง`, `ประวัติการใช้ปืนใหญ่`, `บันทึกหลักฐานการยิง`)
4. **[table_layout_gun_book.json](file:///d:/Project/WEPAPP/references/approved_gun_book/table_layout_gun_book.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ครอบคลุมทั้ง ๕ หน้า
5. **[build_superclone_gun_book.py](file:///d:/Project/WEPAPP/references/approved_gun_book/build_superclone_gun_book.py)**
   - สคริปต์คอมไพเลอร์ผลิตเอกสารแบบอัตโนมัติครบ 3 ฟอร์แมต (HTML, XLSX, DOCX)
6. **[artillery_emblem.png](file:///d:/Project/WEPAPP/references/approved_gun_book/artillery_emblem.png)**
   - ตราสัญลักษณ์ความละเอียดสูงของกองพันทหารปืนใหญ่ที่ ๔
7. **ภาพเรนเดอร์จริง Visual QA ครบทั้ง ๕ หน้า:**
   - [gun_book_page_1_full.png](file:///d:/Project/WEPAPP/references/approved_gun_book/gun_book_page_1_full.png) (หน้าปก)
   - [gun_book_page_2_full.png](file:///d:/Project/WEPAPP/references/approved_gun_book/gun_book_page_2_full.png) (ป.๖)
   - [gun_book_page_3_full.png](file:///d:/Project/WEPAPP/references/approved_gun_book/gun_book_page_3_full.png) (คำนวณอายุลำกล้อง)
   - [gun_book_page_4_full.png](file:///d:/Project/WEPAPP/references/approved_gun_book/gun_book_page_4_full.png) (ประวัติการใช้ปืนใหญ่)
   - [gun_book_page_5_full.png](file:///d:/Project/WEPAPP/references/approved_gun_book/gun_book_page_5_full.png) (บันทึกหลักฐานการยิง)

---

## 📐 3. สเปกมาตรฐานที่ผ่านการอนุมัติ (Approved Specs)
- **การควบคุมขนาดหน้าเอกสาร (One-Topic-Per-Page Constraint):**
  - ล็อกให้เนื้อหาแต่ละหัวข้อมีความยาวพอดี ๑ หน้า A4 แนวนอน (Landscape) ห้ามล้นหน้าเด็ดขาด
- **หน้า ๓ ข้อมูลลำกล้อง (Barrel Info Layout):**
  - `ชนิดลำกล้อง`, `หมายเลขลำกล้อง`, `อายุลำกล้องสูงสุด` ปรับขนาดฟอนต์ 15pt
  - จัดให้ชื่อรายการ (Label) และข้อมูล (Value) อยู่คนละบรรทัดบนเส้นประ
- **ตารางประวัติการใช้ปืนใหญ่ (Operation Maintenance Table):**
  - ตาราง ๖ คอลัมน์: วัน/เดือน/ปี (12%), ภารกิจ/การปฏิบัติ (34%), ปัญหาข้อขัดข้อง (20%), การดำเนินการ - แก้ไข (11%), ส่งซ่อม (11%), หมายเหตุ (12%)
- **ตารางบันทึกหลักฐานการยิง (Firing Record Table):**
  - ตาราง ๙ คอลัมน์: วัน/เดือน/ปี (8%), ชนิดกระสุน (12%), ส่วนบรรจุ (10%), จำนวนนัด (7%), ค่า EFC (6%), ค่า EFC X จำนวนนัด (11%), อายุลำกล้อง (9%), ลายเซ็น (17%), หมายเหตุ (20%)
