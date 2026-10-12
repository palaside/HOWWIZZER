# 🌟 WORKSPACE GOVERNANCE & PROJECT CONSTITUTION (GEMINI.md)

## 📌 Active Governance Rules
ทุกคำสั่งและทุกงานเอกสารในโปรเจกต์นี้ ต้องปฏิบัติตามกฎมาตรฐานใน `.agents/rules/` โดยเคร่งครัด:

1. **[RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md)**
   - สถาปัตยกรรมเอกสารระดับ Production, การรักษาชนิดข้อมูลตัวเลขใน Excel (`[$-th-TH,26]#,##0.00`), OpenType Feature Tags ใน CSS, และ Single Source of Truth ผ่าน `table_layout.json`
   - **กฎการคำนวณวันเสนอเซ็นหนังสือราชการ:** วันที่บนหัวบันทึกข้อความและวันที่ผู้ร่าง/พิมพ์/ทาน ต้องเป็นวันทำการระหว่างวันจันทร์ ถึง วันพฤหัสบดี เท่านั้น (ห้ามตรงวันหยุดราชการ และห้ามลงวันศุกร์)
   - **ระบบพิมพ์แพ็กเกจคู่ขนาน ๒ ชุด (Dual-Copy Engine):** ๑ คำสั่งพิมพ์ ต้องส่งออกคู่ขนานทั้ง "ฉบับตัวจริง" และ "สำเนาคู่ฉบับ" (มีข้อความสำเนาคู่ฉบับและตารางผู้ร่าง/ตรวจ/พิมพ์/ทาน)
   - **มาตรฐานความคมชัด Print-Grade 300 DPI:** ทุกภาพพรีวิว/Vision ต้องเรนเดอร์ที่ `device_scale_factor >= 2.5` คมกริบ ไร้รอยหยักเบลอ ๑๐๐%

2. **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)**
   - **กฎการตรวจจับบล็อกลงนามอัตโนมัติ (Autonomous Signature Detection Heuristic):**
     - ทันทีที่พบข้อความหรือช่องตารางที่มี **`[ยศ/คำนำหน้า]` + `[(ชื่อ)]` + `[ตำแหน่ง]`** หรือมีคำกำกับบทบาท (`ผู้ตรวจสอบ`, `ผู้เบิก`, `ผู้จ่าย`, `ผู้รับ`, `ตรวจถูกต้อง`, `ผบ.ร้อย` ฯลฯ) หรือจุดไข่ปลาลงนาม `(ลงชื่อ).....` **ระบบต้องจัดประเภทเป็น `"type": "signature_block"` อัตโนมัติ 100% โดยผู้ใช้ไม่ต้องสั่งซ้ำ**
     - **Single Source of Truth (SSOT):** ทุกสคริปต์คอมไพล์เอกสารต้องเรียกใช้โมดูลกลาง **[signature_engine.py](file:///d:/Project/WEPAPP/signature_engine.py)** ในการเรนเดอร์ HTML, Word (.docx), และ Excel (.xlsx) เสมอ
     - **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามใช้ `WD_ALIGN_PARAGRAPH.CENTER` หรือจัดกึ่งกลางรวบยศกับชื่อใน Word (.docx) และ Excel (.xlsx) เด็ดขาด ต้องใช้ Tab Stop ชนแกนดิ่ง Red Line Standard เท่านั้น
   - **สัญญาการจัดบล็อกลงนามแบบ Universal Red Line Standard:**
     - จุด `.` ท้ายสุดของยศ ต้องตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อเป๊ะ 100% (`right: 100%` ของ `.sig-name-wrapper`)
     - ชื่อและตำแหน่งจัดกึ่งกลางร่วมกันเสมอ ห่างกัน 1 Enter (Space After 0 pt)
     - คำรับรอง (`ตรวจถูกต้อง` / `ผู้ตรวจสอบ`): ต้นฉบับจะมีหรือไม่มีก็ได้ (มีตามต้นฉบับ ไม่มีให้งด) หากมี ให้เคาะ 1 Enter แบบมีระยะห่างหลังย่อหน้า (Space After ~32px / 24pt) ก่อนถึงยศ
     - ยศ ชื่อ ตำแหน่ง (Rank, Name, Position): ต้องยึดถือข้อความจริงจากต้นฉบับ 100% ห้ามแต่งเติมหรือเปลี่ยนแปลง
     - **พิกัดตำแหน่งการลงนามมาตรฐาน:**
       - **แนวตั้ง / บันทึกข้อความ (Portrait / Memo):** ห่างจากขอบกระดาษทางซ้าย **130 มม.** และใน **บันทึกข้อความ** ให้เคาะลงมา **5 Enter จากบรรทัดข้อความสุดท้าย** (เช่น `จึงเรียนมาเพื่อกรุณาทราบ`) ก่อนเริ่มการลงนาม (ถือเป็นมาตรฐาน และสามารถปรับเปลี่ยนได้)
       - **แนวนอน (Landscape):** ห่างจากขอบกระดาษทางซ้าย **230 มม.** (ถือเป็นมาตรฐาน และสามารถปรับเปลี่ยนได้)
     - ห้ามเคลมว่าเอกสารเสร็จสมบูรณ์จนกว่าจะเรนเดอร์จริงและผ่าน Visual QA 100%
3. **[RULE-PAGEFIT-TUNING-V1](file:///d:/Project/WEPAPP/.agents/skills/PageFit_Tuning/SKILL.md)**
   - สกิลวิศวกรรมบีบอัดเอกสารให้ลงพอดีหน้า A4 (Zero-Overflow Micro-Tuning Budget 4 มิติ)
   - เมื่อตรวจพบว่าข้อความหรือบล็อกลงนามล้นขอบกระดาษ ระบบต้องปรับจูนอัตโนมัติ: ปรับ Page Padding ล่างเหลือ 10mm, สเกลเนื้อหาเป็น 13.5pt/line-height: 1.18, กระชับ Margin หัวข้อ และคงระยะปลอดภัยใต้บล็อกลงนามอย่างน้อย 8-12mm เสมอ ห้ามตัดทอนข้อความเด็ดขาด

---

## 🏆 Approved References (Gold Standard)
เอกสารที่ผู้ใช้งานอนุมัติ "ผ่าน" (PASS) และบันทึกเป็น Reference แม่แบบ:

1. **[REF-PBK-95-V1](file:///d:/Project/WEPAPP/references/approved_pbk_95/REFERENCE_MANIFEST.md)** — *บัญชีรายละเอียดหมายเลข ปบค.๙๕ ขนาด ๑๐๕ มม. เอ็ม ๑๐๑ เอ ๑ ปรับปรุง*
   - รูปแบบ: A4 แนวนอน (Single-page Landscape)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_pbk_95/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_pbk_95/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_pbk_95/บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_pbk_95/table_layout.json)

2. **[REF-TB-400-012-V1](file:///d:/Project/WEPAPP/references/approved_tb_400_012/REFERENCE_MANIFEST.md)** — *ทบ.๔๐๐-๐๑๒ ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์*
   - รูปแบบ: Legal แนวนอน 2 หน้า (2-Page Legal Landscape)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_tb_400_012/ทบ_400_012_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_tb_400_012/table_layout_400_012.json)

3. **[REF-TB-468-204-V1](file:///d:/Project/WEPAPP/references/approved_tb_468_204/REFERENCE_MANIFEST.md)** — *ทบ.๔๖๘-๒๐๔ (คส. ๔) บัญชีหมายเลขอาวุธ*
   - รูปแบบ: A4 แนวตั้ง 6 หน้า (6-Page A4 Portrait)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_tb_468_204/ทบ_468_204_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_tb_468_204/table_layout_468_204.json)

4. **[REF-GUN-HIST-V1](file:///d:/Project/WEPAPP/references/approved_gun_history/REFERENCE_MANIFEST.md)** — *ประวัติการใช้อาวุธ (ป.หมู่ ๒ ถึง ๖)*
   - รูปแบบ: A4 แนวตั้ง 5 หน้า (5-Page A4 Portrait)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_gun_history/ประวัติการใช้อาวุธ_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_gun_history/table_layout_gun_history.json)

5. **[REF-GUN-BOOK-V1](file:///d:/Project/WEPAPP/references/approved_gun_book/REFERENCE_MANIFEST.md)** — *สมุดประวัติการใช้ปืนใหญ่*
   - รูปแบบ: A4 แนวนอน 5 หน้า (5-Page A4 Landscape, หัวข้อละ ๑ หน้าพอดีเป๊ะ)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_gun_book/สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_gun_book/table_layout_gun_book.json)

6. **[REF-SURVEY-SP-V1](file:///d:/Project/WEPAPP/references/approved_survey_sp/REFERENCE_MANIFEST.md)** — *ทบ.๔๐๐-๐๑๑ ใบสำรวจสิ่งอุปกรณ์ สาย สพ.*
   - รูปแบบ: Legal แนวนอน 12 หน้า (12-Page US Legal Landscape: 2 Cards/Page, 3 Slips/Card)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_survey_sp/ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_survey_sp/table_layout_survey_sp.json)

7. **[REF-MEMO-LATEST-V1](file:///d:/Project/WEPAPP/references/approved_memo_latest/REFERENCE_MANIFEST.md)** — *บันทึกข้อความ (ขอส่งใบติดตามใบส่งซ่อมเกิน ๔๕ วัน)*
   - รูปแบบ: A4 แนวตั้ง 1 หน้า (1-Page A4 Portrait)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_memo_latest/บันทึกข้อความล่าสุดสุด_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_memo_latest/table_layout_memo.json)

8. **[REF-TB-400-005-V1](file:///d:/Project/WEPAPP/references/approved_tb_400_005/REFERENCE_MANIFEST.md)** — *ทบ.๔๐๐-๐๐๕ บัญชีสิ่งอุปกรณ์ของหน่วย*
   - รูปแบบ: A5 แนวตั้ง 31 หน้า (31-Page A5 Portrait: 1 TOC/Cert Page + 15 Cards Front/Back)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_tb_400_005/บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_tb_400_005/table_layout_400_005.json)

9. **[REF-TB-CAT2-4-V1](file:///d:/Project/WEPAPP/references/approved_tb_cat2_4/REFERENCE_MANIFEST.md)** — *บัญชีคุมสิ่งอุปกรณ์ ประเภท ๒ และ ๔ (ทบ.๔๐๐-๐๐๕)*
   - รูปแบบ: A5 แนวตั้ง 178 หน้า (178-Page A5 Portrait: Cover + Cert + Warning/Insp + Location + 87 Cards Front/Back)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_tb_cat2_4/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_tb_cat2_4/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_tb_cat2_4/บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_tb_cat2_4/table_layout_cat2_4.json)

10. **[REF-TB-468-360-V1](file:///d:/Project/WEPAPP/references/approved_tb_468_360/REFERENCE_MANIFEST.md)** — *ทบ.๔๖๘-๓๖๐ (สพ.๔๖๐) กำหนดการปรนนิบัติบำรุงยุทธภัณฑ์*
   - รูปแบบ: A4 แนวนอน 4 หน้า (4-Page A4 Landscape Booklet)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_tb_468_360/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_tb_468_360/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_tb_468_360/ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_tb_468_360/table_layout_468_360.json)

11. **[REF-QUARTERLY-REPORT-V1](file:///d:/Project/WEPAPP/references/approved_quarterly_report/REFERENCE_MANIFEST.md)** — *รายงานผลการตรวจสอบอาการถอยและจำลองการยิง ป. (ประจำไตรมาส)*
   - รูปแบบ: A4 ไฮบริด 3 หน้า (Page 1-2 Portrait, Page 3 Landscape)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_quarterly_report/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_quarterly_report/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_quarterly_report/รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_quarterly_report/table_layout_quarterly_report.json)

12. **[REF-MEMO-90-V1](file:///d:/Project/WEPAPP/references/approved_memo_90/REFERENCE_MANIFEST.md)** — *บันทึกข้อความ (ขอส่งใบติดตามใบส่งซ่อมเกิน ๙๐ วัน)*
   - รูปแบบ: A4 แนวตั้ง 1 หน้า (1-Page A4 Portrait)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_memo_90/บันทึกข้อความ_90_วัน_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_memo_90/table_layout_memo_90.json)

13. **[REF-MEMO-INQUIRY-90-V1](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/REFERENCE_MANIFEST.md)** — *ขอส่งใบติดตามทวงถาม ๙๐ วัน (บันทึกข้อความ และ ทบ.๔๐๐-๐๗๑ แบบ ข ใบติดตามใบเบิก)*
   - รูปแบบ: ไฮบริด 3 หน้า (หน้า ๑: A4 แนวตั้ง, หน้า ๒-๓: US Legal แนวนอน)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_90/table_layout_memo_inquiry_90.json)

14. **[REF-MEMO-INQUIRY-45-V1](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_45/REFERENCE_MANIFEST.md)** — *ขอส่งใบติดตามทวงถาม ๔๕ วัน (บันทึกข้อความ และ ทบ.๔๐๐-๐๗๑ แบบ ก ใบติดตามใบเบิก)*
   - รูปแบบ: ไฮบริด 3 หน้า (หน้า ๑: A4 แนวตั้ง, หน้า ๒-๓: US Legal แนวนอน)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_45/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_45/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_45/ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_memo_inquiry_45/table_layout_memo_inquiry_45.json)

15. **[REF-SD1-WEEKLY-REPORT-V1](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/REFERENCE_MANIFEST.md)** — *บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (สด.๑)*
   - รูปแบบ: A4 ไฮบริด 5 หน้า (หน้า ๑-๔: A4 แนวตั้ง, หน้า ๕: A4 แนวนอน)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_sd1_weekly_report/table_layout_sd1.json)

16. **[REF-REPAIR-TRACK-A-V1](file:///d:/Project/WEPAPP/references/approved_repair_track_a/REFERENCE_MANIFEST.md)** — *ทบ.๔๐๐-๐๗๑ แบบ ก ใบติดตามใบส่งซ่อม (การเบิกเกิน ๔๕ - ๙๐ วัน)*
   - รูปแบบ: A4 แนวนอน 1 หน้า (1-Page A4 Landscape)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_repair_track_a/ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_repair_track_a/table_layout_repair_track_a.json)

17. **[REF-INSP-GEN2-V1](file:///d:/Project/WEPAPP/references/approved_general_inspection_2/REFERENCE_MANIFEST.md)** — *บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ ๒) ประจำปี ๒๕๖๙*
   - รูปแบบ: A4 แนวตั้ง 18 หน้า (18-Page A4 Portrait: 1 Memo Page + 17 Pages ทบ.๑๐๕-๐๐๙ รวม ๖ ชุดตรวจ)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_general_inspection_2/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_general_inspection_2/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_general_inspection_2/บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_general_inspection_2/table_layout_general_inspection_2.json)

18. **[REF-WEEKLY-INSPECTION-JUN-V1](file:///d:/Project/WEPAPP/references/approved_weekly_inspection/REFERENCE_MANIFEST.md)** — *บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (ประจำสัปดาห์ มิ.ย. ๖๙)*
   - รูปแบบ: A4 ไฮบริด 5 หน้า (หน้า ๑-๔: A4 แนวตั้ง, หน้า ๕: A4 แนวนอน)
   - ไฟล์ต้นแบบ: [HTML](file:///d:/Project/WEPAPP/references/approved_weekly_inspection/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html) | [DOCX](file:///d:/Project/WEPAPP/references/approved_weekly_inspection/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.docx) | [XLSX](file:///d:/Project/WEPAPP/references/approved_weekly_inspection/บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.xlsx) | [SSOT Blueprint](file:///d:/Project/WEPAPP/references/approved_weekly_inspection/table_layout_weekly_inspection.json)


