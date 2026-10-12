# 🏛️ PRODUCTION-GRADE DOCUMENT & FORENSIC ENGINE RULES
**Rule ID:** `RULE-PROD-DOC-ENGINE-V1`  
**Scope:** บังคับใช้กับงานสร้าง, โคลน, วิศวกรรมย้อนรอย (Reverse Engineering), และเรนเดอร์เอกสารราชการ, แบบฟอร์ม ทบ., เอกสารพยานหลักฐานศาล, Excel (.xlsx), Word (.docx), และ HTML/Print Templates ทั้งหมด

---

## 📌 1. CORE MANDATE & PHILOSOPHY
เมื่อต้องพัฒนาหรือสร้างเอกสารราชการ/ตารางข้อมูล ห้ามทำงานแบบ "ปะผุเฉพาะหน้า (Visual-Only Hacks)" เด็ดขาด การเรนเดอร์ที่ถูกต้องทางสายตาต้องอยู่บนรากฐานของ **Data Integrity, Mathematical Precision, และ OpenType Typography Standards 100%**

---

## 📐 2. MANDATORY ENGINEERING RULES

### กฎข้อที่ 1: การรักษาประเภทข้อมูลและการคำนวณใน Excel (Data-Type-Preserving Number Formatting)
* **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามแปลงข้อมูลตัวเลขเป็นสตริงข้อความ (เช่น บันทึกเป็น `"๓๓๒,๗๑๒.๐๐"`) ใน Data Model ของ Excel โดยเด็ดขาด เพราะจะทำให้ฟังก์ชัน `=SUM()`, `=AVERAGE()` และการคำนวณทางบัญชีกลายเป็นข้อผิดพลาด (Formula Error)
* **ข้อบังคับ (MANDATORY IMPLEMENTATION):**
  - บันทึกค่าลงเซลล์ Excel เป็นตัวเลขดิบ (Raw Decimal/Float/Integer) เสมอ
  - กำหนดการแสดงผลเป็นเลขไทยผ่าน **Culture Number Format Token** ของ Microsoft Excel:
    ```python
    # จำนวนเงินทศนิยม 2 ตำแหน่ง
    cell.value = 332712.00
    cell.number_format = '[$-th-TH,26]#,##0.00'

    # จำนวนนับ / จำนวนเต็ม
    cell.value = 6
    cell.number_format = '[$-th-TH,26]#,##0'
    ```

---

### กฎข้อที่ 2: การควบคุมการแสดงผลและสลับ Glyph ที่ระดับ Font Engine (OpenType Feature Layout)
* **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามแปลงรหัสตัวอักษรแบบ Hardcoded ในเนื้อหาข้อมูล (Content Layer) จาก ASCII 0–9 เป็น Thai Unicode ๐–๙ ในกรณีที่เอกสารต้องการรองรับการค้นหา (Ctrl+F), ยิง Barcode หรือคัดลอก (Copy-Paste)
* **ข้อบังคับ (MANDATORY IMPLEMENTATION):**
  - ในเนื้อหาดิจิทัล คงค่ารหัสตัวอักษรตั้งต้นเป็น ASCII `0-9` (U+0030 ถึง U+0039)
  - สั่งการให้ Font Engine (เช่น TH Sarabun PSK) สลับ Glyph การวาดเส้นเป็นเลขไทยเฉพาะระดับการแสดงผลบนหน้าจอและกระดาษพิมพ์ผ่าน CSS OpenType Feature Tags:
    ```css
    .thai-numeral-display {
        font-variant-numeric: tabular-nums;
        font-feature-settings: "locl" 1, "numr" 1; /* บังคับสลับ Glyph เลขไทยที่ Font Engine */
    }
    ```

---

### กฎข้อที่ 3: สัญญาข้อมูลและตัวแบ่งประเภทเชิงความหมาย (Schema Contract & Context-Aware Rules)
* **ข้อบังคับ (MANDATORY IMPLEMENTATION):**
  - ทุกตารางต้องมีไฟล์พิมพ์เขียว (`table_layout.json`) เป็น **Single Source of Truth (SSOT)** ระบุ `data_type` ชัดเจนในทุกคอลัมน์ (`currency`, `integer`, `code_string`, `text`)
  - **Context-Aware Protection:** รหัสครุภัณฑ์สากล (เช่น NATO Stock Number `1015-00-722-9752`, รหัสรุ่น `M.19`, ขนาดยาง `900-20`) ต้องได้รับการปกป้องตามมาตรฐานเทคนิค ห้ามทำ Blind Replacement เหมารวม

---

### กฎข้อที่ 4: การแยกชั้นเนื้อหากับโครงสร้างด้วยเกราะป้องกัน AST (AST-Safe Parsing Isolation)
* **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามรันฟังก์ชัน Replace ตัวอักษรบนก้อนโค้ด HTML/XML ทั้งก้อน เพราะจะทำให้ตัวเลขใน Tag Attributes พัง เช่น `<td width="100">` กลายเป็น `width="๑๐๐"`
* **ข้อบังคับ (MANDATORY IMPLEMENTATION):**
  - กระบวนการประมวลผลข้อความต้องกระทำเฉพาะบน `TextNode` ของ DOM / AST เท่านั้น
  - ห้ามแตะต้อง Element Attributes (`width`, `height`, `colspan`, `rowspan`, `style`, `class`, `id`) โดยเด็ดขาด

---

### กฎข้อที่ 5: สถาปัตยกรรมตารางเดี่ยวผืนเดียว (Unified Single Master Grid Architecture)
* **ข้อบังคับ (MANDATORY IMPLEMENTATION):**
  - แบบฟอร์มที่มีส่วนหัว (Header Box) และตารางข้อมูล (Data Grid) ห้ามแยกเป็น 2 ตารางอิสระจากกัน
  - ต้องผูกเข้ากับ **Unified Single Master Grid** (เช่น 15 Columns) ผืนเดียวกันทั้งหน้ากระดาษ:
    - **ใน HTML:** ส่วนหัวทั้งหมดต้องอยู่ร่วมใน `<thead>` เดียวกันกับหัวคอลัมน์ข้อมูล คุมด้วย `<colgroup>` สัดส่วนเปอร์เซ็นต์รวม 100.0000%
    - **ใน Word (.docx):** ต้องเป็น `<w:tbl>` เดียวทั้งหน้ากระดาษ กำหนด `<w:tblGrid>` ขนาดรวมคงที่ (เช่น 13,650 dxa) เพื่อรับประกันว่าเส้นแนวตั้งทุกช่องจะตรงกันเป็นเส้นเดียว 100% ปราศจากการเยื้อง
