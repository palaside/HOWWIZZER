# 🏆 APPROVED REFERENCE: บัญชีคุมสิ่งอุปกรณ์ของหน่วย (ทบ.๔๐๐-๐๐๕)

**Document ID:** `REF-TB-400-005-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** บัตรบัญชีคุมสิ่งอุปกรณ์ กองทัพบก สาย สพ. / พธ. (Unit Property Book Card)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **ทบ.๔๐๐-๐๐๕ บัญชีสิ่งอุปกรณ์ของหน่วย** ประจำกองร้อยทหารปืนใหญ่ กองพันทหารปืนใหญ่ที่ ๔ กรมทหารปืนใหญ่ที่ ๔ (ป.๔ พัน.๔ ร้อย.๒):
1. **การควบคุมขนาดหน้าเอกสาร (Paper & Form Layout Standard):**
   - กระดาษขนาด **A5 แนวตั้ง (Portrait: 148mm x 210mm)**
   - ระยะขอบมาตรฐาน: ขอบบน ๕.๐ มม., ขอบล่าง ๕.๐ มม., ขอบซ้าย ๗.๐ มม., ขอบขวา ๗.๐ มม.
   - บัตรสิ่งอุปกรณ์แต่ละรายการจบลงตัวพอดีเป๊ะ **หน้าละ ๑ ฝั่ง (Single-page Portrait per side)** ไม่มีการตกหล่นหรือล้นข้ามหน้า
2. **การฟื้นฟูข้อผิดพลาดต้นฉบับ (35-Page Word Overflow Bug Remediation):**
   - ต้นฉบับ PDF ๓๕ หน้าเกิดจากตาราง Word แตกกระจายข้ามหน้าอย่างไร้ระเบียบ SUPERCLONE ทำการรวบรวมและประกอบใหม่เป็นระบบโครงสร้างที่ถูกต้อง:
     - **หน้า ๑:** สารบัญสิ่งอุปกรณ์ สป.๒-๔ สาย สพ. (อจย.๖-๒๗) + บันทึกผลการตรวจของผู้บังคับบัญชา + คำรับรองทรัพย์สิน + บล็อกลงนาม
     - **หน้า ๒ ถึง ๓๑ (๑๕ รายการ):** บัตรสิ่งอุปกรณ์รายการละ ๒ หน้า (ด้านหน้า: บันทึกการเบิกจ่าย ๑๒ บรรทัด + ตารางสเปกด้านล่าง ๕ แถว / ด้านหลัง: รายการสถานที่อยู่ของสิ่งอุปกรณ์ ๒๐ บรรทัด)
3. **บล็อกลงนามมาตรฐานสากล (Universal Red Line Standard):**
   - ปฏิบัติตามกฎ [RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)
   - ยศของผู้บังคับบัญชาปรับเป็น **`ร.อ.`** ตามคำสั่งอนุมัติของผู้ใช้งาน
   - จุด `.` ท้ายสุดของยศ (`ร.อ.`) ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อ `(กฤติน  นราพงษ์)` พอดีเป๊ะ 100%
   - ชื่อและตำแหน่ง (`ผบ.ป.๔ พัน.๔ ร้อย.๒`) จัดกึ่งกลางร่วมกัน ห่างกัน ๑ Enter (Space After 0 pt)

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html)**
   - สเปก: 31-Page A5 Portrait (148mm x 210mm) รองรับคำสั่งพิมพ์ `@page` ตัดหน้ากระดาษแม่นยำระดับพิกเซล
2. **[บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word A5 Portrait (31 ตาราง, 15 บัตรสิ่งอุปกรณ์หน้า-หลัง)
3. **[บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.xlsx)**
   - สเปก: Excel Multi-Sheet Ledger (๑๖ แผ่นงาน: สารบัญ + บัตรคุมทั้ง ๑๕ รายการ)
4. **[table_layout_400_005.json](file:///d:/Project/WEPAPP/references/approved_tb_400_005/table_layout_400_005.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ควบคุมข้อมูลยุทโธปกรณ์ ประวัติเบิกจ่าย และสเปก
5. **[build_superclone_tb400_005.py](file:///d:/Project/WEPAPP/references/approved_tb_400_005/build_superclone_tb400_005.py)**
   - สคริปต์คอมไพเลอร์อัตโนมัติ 3 ฟอร์แมต (HTML, DOCX, XLSX)
6. **[take_tb400_005_vision.py](file:///d:/Project/WEPAPP/references/approved_tb_400_005/take_tb400_005_vision.py)**
   - สคริปต์ Playwright สำหรับรัน Automated Visual QA
7. **ภาพเรนเดอร์จริง Visual QA:**
   - [tb400_005_page_toc.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_page_toc.png) (หน้าสารบัญและคำรับรอง)
   - [tb400_005_cert_sig_crop.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_cert_sig_crop.png) (กล่องคำรับรองและบล็อกลงนาม)
   - [tb400_005_sig_only_crop.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_sig_only_crop.png) (บล็อกลงนาม ร.อ. Red Line Standard)
   - [tb400_005_card_1_front.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_card_1_front.png) (บัตรรายการที่ ๑ ด้านหน้า ปบค.95)
   - [tb400_005_card_1_footer_crop.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_card_1_footer_crop.png) (ตารางสเปกด้านล่าง)
   - [tb400_005_card_1_back.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_card_1_back.png) (บัตรรายการที่ ๑ ด้านหลัง รายการสถานที่อยู่ ๒๐ บรรทัด)
   - [tb400_005_card_4_front.png](file:///d:/Project/WEPAPP/references/approved_tb_400_005/tb400_005_card_4_front.png) (บัตรรายการที่ ๔ ด้านหน้า ลำกล้องปืนหลอดฯ)
