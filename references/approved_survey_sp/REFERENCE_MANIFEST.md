# 🏆 APPROVED REFERENCE: ใบสำรวจสิ่งอุปกรณ์ สาย สพ. (ทบ. ๔๐๐ - ๐๑๑)

**Document ID:** `REF-SURVEY-SP-V1`  
**User Decision:** `PASS` (อนุมัติผ่านอย่างเป็นทางการโดยผู้ใช้งาน)  
**Date Approved:** 10 ตุลาคม 2569  
**Category:** แบบพิมพ์สำรวจสิ่งอุปกรณ์ กองทัพบก สายสรรพาวุธ (Royal Thai Army Ordnance Survey Card - 3 Slips Per Card, 2 Cards Per Page)

---

## 📌 1. วัตถุประสงค์และการอ้างอิง (Reference Purpose)
ชุดเอกสารนี้คือ **Gold Standard Reference (แม่แบบมาตรฐานระดับ Production)** ของแบบฟอร์ม **ใบสำรวจสิ่งอุปกรณ์ สาย สพ. (ทบ. ๔๐๐ - ๐๑๑)** สังกัดกองพันทหารปืนใหญ่ที่ ๔ กรมทหารปืนใหญ่ที่ ๔ (ป.๔ พัน.๔ ร้อย.๒):
1. **การควบคุมขนาดหน้าเอกสาร (Paper & Grid Standards):**
   - กระดาษขนาด **US Legal แนวนอน (Legal Landscape: 355.6mm x 215.9mm หรือ 14 in x 8.5 in)**
   - แบ่งเป็น **๒ การ์ดต่อหน้า** (Card 1 ด้านบน, Card 2 ด้านล่าง) คั่นด้วยเส้นประตัดขวาง (`cut-line-h`)
   - แต่ละการ์ดบรรจุ **๓ สลิปย่อยขนานกัน** (Slip 1 ซ้าย, Slip 2 กลาง, Slip 3 ขวา) คั่นด้วยเส้นประตัดแนวดิ่ง (`border-right: 1px dashed`)
   - มีรายการสิ่งอุปกรณ์ครบทั้ง ๒๓ รายการ (1/66 ถึง 23/66) รวม **๑๒ หน้าบริบูรณ์** โดยหน้าที่ ๑๒ การ์ดล่างเป็นแบบฟอร์มเปล่าสมบูรณ์
2. **มาตรฐานแบบอักษร (Typography & Font Weight):**
   - แบบอักษร **ตัวบางทั้งหมด (Regular / Thin Weight: `font-weight: normal`)** ไร้ตัวหนา (`bold`) ครอบคลุมทั้ง HTML, XLSX และ DOCX
3. **ช่องข้อมูล "วันสำรวจ":**
   - ข้อความเดือนและปี (`พ.ย. ๖๖`) เยื้องเลื่อนไปทางขวา **๔ เคาะ** จากจุดศูนย์กลาง
4. **มาตรฐานบล็อกลายเซ็น (Signature Block Standard):**
   - ๓ ช่องลงนามต่อสลิป: `ผู้ตรวจนับ`, `หัวหน้าชุด`, `เจ้าหน้าที่บัญชีคุม`
   - ยศ (`จ.ส.อ.`, `ร.ท.`) จัดชิดมุมบนซ้ายของช่อง
   - เดือนและปี (`พ.ย. ๖๖`) เลื่อนไปทางขวา ๔ เคาะ อยู่ใกล้กับตำแหน่ง
   - ชื่อตำแหน่งจัดชิดขอบล่าง เว้นระยะ 2-3px

---

## 📂 2. รายการไฟล์ต้นแบบ (Artifact Inventory)
1. **[ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html)**
   - สเปก: 12-Page US Legal แนวนอน (Legal Landscape 355.6mm x 215.9mm) CSS @page สั่งพิมพ์ได้ทันที
2. **[ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.docx](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.docx)**
   - สเปก: Microsoft Word Legal Landscape 14"x8.5", ตารางแม่แบบ 3 สลิปคู่บน-ล่าง ขอบเส้นประชัดเจน
3. **[ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.xlsx](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.xlsx)**
   - สเปก: ตาราง Excel โครงสร้าง 18 คอลัมน์ต่อการ์ด รองรับสูตรและคงชนิดข้อมูลด้วย `[$-th-TH,26]#,##0`
4. **[table_layout_survey_sp.json](file:///d:/Project/WEPAPP/references/approved_survey_sp/table_layout_survey_sp.json)**
   - Single Source of Truth (SSOT) พิมพ์เขียวดิจิทัล ครอบคลุมข้อมูลทั้ง 23 รายการ
5. **[build_superclone_survey_sp.py](file:///d:/Project/WEPAPP/references/approved_survey_sp/build_superclone_survey_sp.py)**
   - สคริปต์คอมไพเลอร์อัตโนมัติ 3 ฟอร์แมต (HTML, XLSX, DOCX)
6. **[take_survey_vision.py](file:///d:/Project/WEPAPP/references/approved_survey_sp/take_survey_vision.py)**
   - สคริปต์ Playwright สำหรับรัน Automated Visual QA
7. **ภาพเรนเดอร์จริง Visual QA:**
   - [survey_sp_page_1_full.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_page_1_full.png) (หน้า ๑ แบบเต็ม)
   - [survey_sp_page_2_full.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_page_2_full.png) (หน้า ๒ แบบเต็ม)
   - [survey_sp_page_12_full.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_page_12_full.png) (หน้า ๑๒ แบบเต็ม)
   - [survey_sp_top_card_crop.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_top_card_crop.png) (การ์ดบน ๓ สลิป)
   - [survey_sp_slip_1_crop.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_slip_1_crop.png) (สลิปที่ ๑ เจาะลึก)
   - [survey_sp_meta_crop.png](file:///d:/Project/WEPAPP/references/approved_survey_sp/survey_sp_meta_crop.png) (ช่องวันสำรวจและตารางข้อมูล)
