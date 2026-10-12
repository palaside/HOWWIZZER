# 🏆 APPROVED REFERENCE: ทบ.๔๐๐-๐๑๒ ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์

**Document ID:** `REF-TB-400-012-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** แบบฟอร์มรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์ ทบ. (Royal Thai Army Survey & Inventory Comparison Report)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **ทบ.๔๐๐-๐๑๒** ใช้เป็นบรรทัดฐานอ้างอิงในการโคลนเอกสาร, การควบคุมขนาดตัวอักษร, การจัดโครงสร้างตารางคู่ขนาน (Master Header & Data Table Alignment), และการวางบล็อกลงนามคณะกรรมการหลายฝ่ายตามระเบียบกองทัพบก

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[ทบ_400_012_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.html)**
   - สเปก: 2-Page Legal แนวนอน (Landscape), ขนาด 340mm x 205mm
   - หัวตาราง (Table Header): ขนาด 11pt ตัวปกติ (`font-weight: normal`) พร้อมระยะ Padding ป้องกันอักขระล้นขอบ
   - ข้อมูลในตาราง (Table Body): ขนาด 11.5pt ตัวปกติ 100% สระไม่ชิดขอบบน (`padding-top: 4px`) คำว่า "กระบอก" และ "กระโจม" พอดีช่องตาราง
   - บล็อกข้อมูลทะเบียน (Admin Box): บรรทัด `ที่เก็บหลักฐานการตรวจสอบ` เว้นระยะห่าง 1 Enter กับ `ป.๔ พัน.๔ ร้อย.๒`
2. **[ทบ_400_012_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word Legal Landscape, คอลัมน์ 14 ช่องตรงแนวตารางบนเป๊ะ
   - ตัวอักษรหัวตารางและเนื้อหา 11pt-11.5pt Regular ไม่ใช้ตัวหนา
3. **[ทบ_400_012_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.xlsx)**
   - สเปก: Data Integrity 100%, ตัวเลขแท้สูตรคำนวณและแสดงผลตัวเลขไทยด้วยรหัสฟอร์แมต `[$-th-TH,26]#,##0`
   - หัวตารางแถว 8 และ 9 ใช้ `font_regular` ไม่ใช้ตัวหนา
4. **[table_layout_400_012.json](file:///d:/Project/WEPAPP/references/approved_tb_400_012/table_layout_400_012.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัลของเอกสาร ทบ.๔๐๐-๐๑๒
5. **[vision_table_body_p1.png](file:///d:/Project/WEPAPP/references/approved_tb_400_012/vision_table_body_p1.png)**
   - ภาพเรนเดอร์จริงหน้า 1 ตรวจสอบคอลัมน์หน่วยนับ "กระบอก" พอดีช่อง
6. **[vision_table_body_p2.png](file:///d:/Project/WEPAPP/references/approved_tb_400_012/vision_table_body_p2.png)**
   - ภาพเรนเดอร์จริงหน้า 2 ตรวจสอบคอลัมน์หน่วยนับ "กระโจม" พอดีช่อง
7. **[vision_admin_box_enter.png](file:///d:/Project/WEPAPP/references/approved_tb_400_012/vision_admin_box_enter.png)**
   - ภาพเรนเดอร์จริงกล่องทะเบียน เว้นระยะ 1 Enter และสระไม่ติดขอบ

---

## 📐 3. สเปกมาตรฐานที่ผ่านการอนุมัติ (Approved Specs)
- **การจัดแนวเส้นกริดเชื่อมโยง (Grid Line Alignment):**
  - แนวเส้นคอลัมน์ระหว่าง Header Master Table และ Main Data Table ล็อกตรงกันที่ **61.5%** เป๊ะ 100%
- **ลำดับชั้นและน้ำหนักตัวอักษร (Typography Hierarchy):**
  - หัวตาราง (Table Header): **11pt ตัวปกติ (Regular)**
  - เนื้อหาข้อมูลในตาราง (Table Body): **11.5pt ตัวปกติ (Regular)**
  - ตัวแปรในช่องลงนาม/ผู้สั่งการสำรวจ: **12pt ตัวปกติ (Regular)** โดย `พ.ท. พรชัย  มากเทพพงษ์` อยู่บรรทัดเดียวกัน
  - วันที่อนุมัติ: `๑๗ / พ.ย. / ๖๔` อยู่แนวกึ่งกลางร่วมกับชื่อ-สกุล
- **การจัดระยะสระและบรรทัด (Vertical Rhythm):**
  - สระบนในเซลล์ตารางมีระยะห่างจากเส้นขอบบน (`padding-top: 4px`) ไม่ชนขอบ
  - ช่องที่เก็บหลักฐานการตรวจสอบ เว้นระยะบรรทัด 1 Enter จากชื่อหน่วย
