# ✍️ UNIVERSAL SIGNATURE BLOCK ENGINE RULES
**Rule ID:** `RULE-UNIVERSAL-SIGNATURE-BLOCK-V1`  
**Scope:** บังคับใช้กับส่วนลงนาม/บล็อกลายเซ็น (Signature Block) ในเอกสารราชการ, เอกสารทหาร, เอกสารพยานหลักฐาน, แบบฟอร์ม ทบ., Word (.docx), Excel (.xlsx), และ HTML/Print Templates ทั้งหมด

---

## 📌 1. CORE MANDATE & UNIVERSAL PRINCIPLE
บล็อกการลงนามในเอกสารราชการไทยและเอกสารทางทหาร มีข้อกำหนดทางเรขาคณิต (Mathematical Geometry) ที่ต้องเป็น **Universal 100%** ไม่ว่าบุคคลจะมียศสั้นหรือยาว (เช่น `ส.ต.` ถึง `พ.อ.พิเศษ`), ชื่อ-สกุลสั้นหรือยาว, หรือตำแหน่งจะยาวเพียงใด เลย์เอาต์ต้องล็อกระนาบอย่างแม่นยำ ไม่เลื่อนหลุดเด็ดขาด

### 🤖 กฎการตรวจจับบล็อกลงนามอัตโนมัติ (Autonomous Signature Detection Heuristic)
ระบบต้องตรวจจับและจัดประเภทบล็อกลงนามเป็น `signature_block` อัตโนมัติทันทีที่พบ:
1. **Pattern ก (Full Signature):** มี `[ยศ/คำนำหน้า]` + `[(ชื่อ)]` + `[ตำแหน่ง]`
2. **Pattern ข (Role/Verification Label):** มีคำกำกับบทบาท เช่น `ผู้ตรวจสอบ`, `ผู้ตรวจ`, `ผู้เบิก`, `ผู้จ่าย`, `ผู้รับ`, `ตรวจถูกต้อง`, `ผบ.ร้อย`, `หน.คลัง`
3. **Pattern ค (Dotted Fill-in):** มีบล็อกเติมคำหรือจุดไข่ปลาลงนาม เช่น `(ลงชื่อ)............................` หรือ `....../......​/......`
* **Single Source of Truth Module:** ในสคริปต์คอมไพล์เอกสารทั้งหมด ต้องเรียกใช้ฟังก์ชันจาก **`signature_engine.py`** เพื่อเรนเดอร์ HTML, DOCX, XLSX
* **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามใช้ `WD_ALIGN_PARAGRAPH.CENTER` หรือจัดกึ่งกลางรวบยศกับชื่อใน Word (.docx) และ Excel (.xlsx) เด็ดขาด ต้องใช้ Tab Stop ชนแกนดิ่ง Red Line Standard เท่านั้น

---

## 📐 2. MANDATORY DUAL-AXIS RULES

### กฎข้อที่ 1: แกนเส้นสีแดง — มาตรฐานท้ายยศชนวงเล็บเปิด (Red Line Standard)
* **นิยามแกน (Vertical Alignment Axis):**
  - เครื่องหมายจุด **`.`** ตัวสุดท้ายของยศ (หรือตัวอักขระท้ายสุดของยศ) ต้องอยู่บน **แนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด `(` ของชื่อ พอดีเป๊ะ 100%**
* **พฤติกรรมเรขาคณิต (Anchor Behavior):**
  - **ฝั่งซ้ายของแกน:** คำว่ายศทั้งหมดทอดตัวไปทางซ้าย โดยมีจุด `.` แตะแกนเส้นดิ่งพอดี (Right-aligned to axis) ยศยาวเท่าใดให้งอกถอยหลังไปทางซ้าย ห้ามดันชื่อเด็ดขาด
  - **ฝั่งขวาของแกน:** บรรทัดชื่อเริ่มต้นด้วยเครื่องหมาย `(` แตะแกนเส้นดิ่งแล้วทอดตัวไปทางขวา (Left-aligned to axis)
* **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):**
  - **ห้าม** จับยศไปจัดกึ่งกลางรวมกับชื่อเด็ดขาด
  - **ห้าม** ยึดยศเข้ากับความกว้างของกล่องข้อความตำแหน่ง เพราะหากตำแหน่งยาวกว่าชื่อ จะทำให้ยศหลุดลอยออกไปทางซ้ายและเกิดช่องว่างผิดแบบ

---

### กฎข้อที่ 2: แกนชื่อและตำแหน่ง (Name to Position Center Alignment)
* **การจัดแนวระนาบ:**
  - บรรทัดชื่อ `(ยศ/ชื่อ   สกุล)` และบรรทัดตำแหน่ง ต้องจัดกึ่งกลางร่วมกัน (Center Alignment)
* **ระยะห่างบรรทัด:**
  - ระหว่างบรรทัดชื่อและบรรทัดตำแหน่ง เว้นห่างกัน **1 Enter** เท่านั้น
  - ตั้งค่าระยะห่างย่อหน้าเป็นศูนย์ (`Space After = 0 pt` / `margin = 0`) ไม่ใส่ Paragraph Spacing แทรกกลาง

---

### กฎข้อที่ 3: คำรับรอง (Verification Text) และการยึดถือต้นฉบับ 100% (Original Source Fidelity)
* **การมีอยู่ของคำรับรอง:**
  - **ต้นฉบับจะมีคำรับรอง (เช่น `ตรวจถูกต้อง`) หรือไม่ก็ได้** ต้องตรวจสอบและยึดถือจากเอกสารต้นฉบับเป็นหลัก (หากต้นฉบับมีให้ใส่ หากไม่มีให้งดเด็ดขาด)
* **ระยะห่างของคำรับรอง:**
  - เมื่อมีคำรับรอง ให้วางชิดบนซ้ายของบล็อกลงนาม และ**เคาะ 1 Enter แบบมีระยะห่างหลังย่อหน้า (Space After: ~32px / 24pt)** ก่อนลงมาถึงยศ เพื่อรักษาระยะห่างตามแบบฉบับเอกสารราชการ
* **ยศ ชื่อ ตำแหน่ง (Rank, Name, Position):**
  - **ต้องยึดถือ ยศ ชื่อ ตำแหน่ง จากเอกสารต้นฉบับอย่างเคร่งครัด 100%** ห้ามคิดเอง ปรับเปลี่ยน หรือแต่งเติมข้อความเด็ดขาด

---

## 📍 3. MANDATORY POSITIONING COORDINATES (พิกัดตำแหน่งการลงนามมาตรฐาน)

กำหนดพิกัดตำแหน่งของบล็อกลงนาม (วัดระยะจากขอบกระดาษทางซ้าย) เป็นมาตรฐานกลางของเอกสาร และสามารถปรับแต่งได้ตามความเหมาะสมของเลย์เอาต์:

1. **เอกสารแนวตั้ง / หน้าบันทึกข้อความ (Portrait / Official Memo Standard - A4 210 มม.):**
   - **พิกัดแนวราบ (Horizontal Coordinate):** ห่างจากขอบกระดาษทางซ้าย **130 มม.** (`left: 130mm;`) ถือเป็นมาตรฐานกลาง
   - **ระยะห่างแนวดิ่ง (Vertical Spacing):** ในเอกสาร **"บันทึกข้อความ"** กำหนดให้บล็อกลงนาม **เคาะลงมา 5 Enter จากบรรทัดข้อความสุดท้าย** (เช่น เคาะลงมา 5 บรรทัดจากคำว่า `จึงเรียนมาเพื่อกรุณาทราบ`) แล้วจึงเริ่มบล็อกการลงนาม ถือเป็นมาตรฐานคงที่ป้องกันระยะห่างมากเกินไป (สามารถปรับเปลี่ยนได้ตามความเหมาะสมของเลย์เอาต์)
2. **เอกสารแนวนอน (Landscape Standard - A4 297 มม.):**
   - **พิกัดแนวราบ (Horizontal Coordinate):** ห่างจากขอบกระดาษทางซ้าย **230 มม.** (`left: 230mm;` หรือเทียบเท่าแนวชิดขวาของตาราง) ถือเป็นมาตรฐานกลาง (สามารถปรับเปลี่ยนได้ตามความเหมาะสมของเลย์เอาต์)

---

## 💻 4. PRODUCTION CODE TEMPLATES (SSOT)

### มาตรฐาน HTML / CSS:
```html
<div class="sig-block">
    <!-- คำรับรอง (ถ้ามี) -->
    <div class="sig-verify">ตรวจถูกต้อง</div>
    
    <div class="sig-name-pos-group">
        <!-- sig-name-wrapper ทำหน้าที่เป็นตัวยึดแกนเส้นดิ่งวงเล็บเปิด ( โดยเฉพาะ -->
        <div class="sig-name-wrapper">
            <span class="sig-rank-anchor">จ.ส.อ.</span>
            <div class="sig-name">(ณัฐชัย   รักษาวงษ์)</div>
        </div>
        <!-- ตำแหน่งจัดกึ่งกลางร่วมกับชื่อ -->
        <div class="sig-pos">ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒</div>
    </div>
</div>
```

```css
.sig-block {
    display: inline-flex;
    flex-direction: column;
    align-items: flex-start;
    font-size: 16pt;
    line-height: 1.0;
}
.sig-verify {
    margin-bottom: 32px; /* 1 Enter พร้อมระยะห่างหลังย่อหน้าตามแบบฉบับราชการ */
    font-size: 16pt;
}
.sig-name-pos-group {
    display: inline-flex;
    flex-direction: column;
    align-items: center; /* ชื่อและตำแหน่งจัดกึ่งกลางร่วมกัน */
    position: relative;
    margin-left: 95px;
}
/* กรอบชื่อ: ครอบเฉพาะตัวหนังสือชื่อเท่านั้น เพื่อให้ขอบซ้ายคือ ( พอดี 100% */
.sig-name-wrapper {
    position: relative;
    display: inline-block;
    white-space: nowrap;
    margin-top: 30px; /* พื้นที่สำหรับลงลายมือชื่อจริง */
}
/* บรรทัดยศ: สั่ง right: 100% เพื่อให้จุด . ชนขอบซ้ายของกรอบชื่อ ( ชน ( พอดีเป๊ะ) */
.sig-rank-anchor {
    position: absolute;
    right: 100%;
    bottom: calc(100% + 20px);
    white-space: nowrap;
    font-size: 16pt;
    line-height: 1.0;
}
.sig-name, .sig-pos {
    margin: 0;
    line-height: 1.15;
    text-align: center;
    white-space: nowrap;
    font-size: 16pt;
    display: block;
}
```

---

### มาตรฐาน Microsoft Word (.docx via python-docx):
```python
# 1. Verification text (1 Enter พร้อมระยะห่างหลังย่อหน้า)
if sig.get("verification_text"):
    p_v = cell.paragraphs[0]
    p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_v.paragraph_format.space_after = Pt(24)
    p_v.add_run(sig["verification_text"])

axis_red_line = Inches(1.40) # แกนเส้นดิ่งร่วม

# 2. Rank -> Right Tab ชนแกน (จุด . ชนเส้นดิ่งพอดี)
if sig.get("rank"):
    p_rk = cell.add_paragraph()
    p_rk.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_rk.paragraph_format.space_after = Pt(24) # เว้นลงลายมือชื่อ
    p_rk.paragraph_format.tab_stops.add_tab_stop(axis_red_line, WD_TAB_ALIGNMENT.RIGHT)
    p_rk.add_run("\t" + sig["rank"])

# 3. Full Name -> Left Tab ชนแกน (วงเล็บเปิด ( ชนเส้นดิ่งพอดี)
p_nm = cell.add_paragraph()
p_nm.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_nm.paragraph_format.space_after = Pt(0)
p_nm.paragraph_format.tab_stops.add_tab_stop(axis_red_line, WD_TAB_ALIGNMENT.LEFT)
p_nm.add_run("\t" + sig["full_name"])

# 4. Position -> จัดกึ่งกลางร่วมกับชื่อ (Space After 0 pt)
p_pos = cell.add_paragraph()
p_pos.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_pos.paragraph_format.space_after = Pt(0)
pos_axis = Inches(1.20)
p_pos.paragraph_format.tab_stops.add_tab_stop(pos_axis, WD_TAB_ALIGNMENT.LEFT)
p_pos.add_run("\t" + sig["position"])
```

---

## 🔍 4. MANDATORY VISUAL QA & VERIFICATION
* **ห้ามเคลมว่าเอกสารเสร็จสมบูรณ์** หากยังไม่ได้เรนเดอร์ดูภาพจริง
* ให้ตรวจสอบเสมอว่า:
  1. จุด `.` ท้ายยศชนกับแนวเส้นดิ่งของ `(` หรือไม่
  2. ชื่อและตำแหน่งอยู่กึ่งกลางร่วมกันหรือไม่
  3. ระยะห่างระหว่างชื่อและตำแหน่งคือ 1 Enter (ไม่มีระยะย่อหน้า) หรือไม่
