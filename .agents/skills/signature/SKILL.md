---
name: signature
description: บล็อคการลงลายเซ็นต์และส่วนลงนามมาตรฐานขั้นสูง (Signature Block Engine v1.0) รองรับการจัดแกนอักขระ (Shared Character Anchor Axis) และการจัดแนวปลายยศตรงกับวงเล็บเปิดชื่อ (Rank Endpoint to Open Parenthesis Alignment)
---

# ✍️ SIGNATURE BLOCK ENGINE v1.0

## 1. วัตถุประสงค์และหลักการสำคัญ
บล็อกการลงลายเซ็นต์ในเอกสารราชการและเอกสารทหาร มีกฎการจัดระนาบเฉพาะตัวที่ต้องแยกเป็น 2 แกนอิสระ:
1. **แกนหลัก (Shared Character Anchor Axis):** คำรับรอง (`ตรวจถูกต้อง`) – วงเล็บชื่อ – ตำแหน่ง จัดระนาบอิงจุดกึ่งกลางหรือ Anchor อักขระร่วมกัน
2. **แกนยศ (Rank Alignment Contract):** จุดสิ้นสุดของยศ (เครื่องหมายจุด `.` ตัวท้ายสุดของยศ เช่น `จ.ส.อ.`) ต้องอยู่ตรงกับเครื่องหมายวงเล็บเปิด `(` ของบรรทัดชื่อพอดี (Endpoint-to-Startpoint Alignment)

### 📌 กฎเหล็ก: ยึดถือความถูกต้องตามต้นฉบับ 100% (Original Source Fidelity)
* **การตรวจจับบล็อกลงนามอัตโนมัติ (Autonomous Signature Detection Heuristic):**
  - ระบบต้องตรวจจับและจัดประเภทบล็อกลงนามเป็น `signature_block` อัตโนมัติทันทีที่พบ:
    - **Pattern ก:** `[ยศ/คำนำหน้า]` + `[(ชื่อ)]` + `[ตำแหน่ง]`
    - **Pattern ข:** มีคำกำกับบทบาท เช่น `ผู้ตรวจสอบ`, `ผู้ตรวจ`, `ผู้เบิก`, `ผู้จ่าย`, `ผู้รับ`, `ตรวจถูกต้อง`, `ผบ.ร้อย`
    - **Pattern ค:** บล็อกเติมคำลงนาม `(ลงชื่อ)............................`
  - **Single Source of Truth Module:** ในสคริปต์คอมไพล์เอกสารทั้งหมด ต้องเรียกใช้ฟังก์ชันจาก **`signature_engine.py`** เพื่อเรนเดอร์ HTML, DOCX, XLSX
  - **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):** ห้ามใช้ `WD_ALIGN_PARAGRAPH.CENTER` หรือจัดกึ่งกลางรวบยศกับชื่อใน Word (.docx) และ Excel (.xlsx) เด็ดขาด ต้องใช้ Tab Stop ชนแกนดิ่ง Red Line Standard เท่านั้น
* **คำรับรอง (Verification Text เช่น "ตรวจถูกต้อง"):** 
  - **ต้นฉบับจะมีคำรับรองหรือไม่ก็ได้** ให้ตรวจสอบจากเอกสารต้นฉบับเป็นหลัก (หากต้นฉบับมีให้ใส่ หากไม่มีให้งดเด็ดขาด)
  - กรณีมีคำรับรอง: จัดวางชิดบนซ้ายของบล็อก และ**เคาะ 1 Enter แบบมีระยะห่างหลังย่อหน้า (Space After: ~32px / 24pt)** ก่อนลงมาถึงยศ เพื่อเว้นช่องว่างอย่างสมดุลตามแบบฉบับราชการ
* **ยศ ชื่อ ตำแหน่ง (Rank, Name, Position):**
  - **ต้องยึดถือ ยศ ชื่อ ตำแหน่ง จากเอกสารต้นฉบับอย่างเคร่งครัด 100%** ห้ามคิดเอง ห้ามปรับเปลี่ยน หรือสลับตำแหน่งข้อความเด็ดขาด

---

## 2. โครงสร้างองค์ประกอบ (Component Schema)

```yaml
signature_block:
  verification_text: "ตรวจถูกต้อง"     # Optional: ยึดตามต้นฉบับ (มีให้ใส่ ไม่มีให้งด) + เคาะ 1 Enter พร้อมระยะห่างหลังย่อหน้า
  rank: "จ.ส.อ."                     # Required/Optional: ดึงจากต้นฉบับ จุด . สุดท้ายตรงกับ ( ของชื่อ
  full_name: "(ณัฐชัย   รักษาวงษ์)"    # Required: ดึงจากต้นฉบับ เว้นวรรคตามต้นฉบับ
  position: "ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒" # Required: ดึงจากต้นฉบับ Space After 0 pt
```

---

## 3. สัญญาการจัดรูปแบบและฟอนต์ (Typography Contract)

| คุณสมบัติ | ค่ากำหนดมาตรฐาน |
| :--- | :--- |
| **แบบอักษร (Font Family)** | `TH Sarabun PSK` / `Sarabun` |
| **ขนาดอักษร (Font Size)** | `16 pt` |
| **ระยะบรรทัด (Line Spacing)** | `1.0` (Single) |
| **Paragraph Space Before** | `0 pt` |
| **ระยะห่าง คำรับรอง → ยศ** | **1 Enter แบบมีระยะห่างหลังย่อหน้า** (`margin-bottom: 32px` / `space_after: Pt(24)`) |
| **ระยะห่าง ยศ → ชื่อ** | ระยะเว้นลงลายมือชื่อจริง (`margin-top: 30px` / `space_after: Pt(24)`) |
| **ระยะห่าง ชื่อ → ตำแหน่ง** | `0 pt` (ชิดกัน 1 Enter พอดี ไม่ใส่ระยะห่างย่อหน้า) |

---

## 4. กฎการจัดแนว 2 แกน (Dual Axis Alignment Rules)

### กฎที่ 1: แกนยศ — มาตรฐานท้ายยศชนวงเล็บเปิด (Red Line Standard)
- เครื่องหมายจุด **`.`** ตัวสุดท้ายของยศ (เช่น `จ.ส.อ.`) ต้องอยู่ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด **`(`** ของชื่อ (ณัฐชัย พอดีเป๊ะ 100%
- ฝั่งซ้ายของแกน: คำว่า `จ.ส.อ.` ทั้งหมดอยู่ทางซ้าย โดยจุด `.` ตัวสุดท้ายแตะแกนพอดี
- ฝั่งขวาของแกน: บรรทัดชื่อเริ่มต้นด้วยวงเล็บเปิด `(` แตะแกนแล้วทอดไปทางขวา
- **ห้าม** จับยศไปเซ็นเตอร์ตรงกลางชื่อเด็ดขาด

### กฎที่ 2: แกนชื่อและตำแหน่ง (Name to Position Alignment)
- บรรทัดชื่อ `(ณัฐชัย   รักษาวงษ์)` และบรรทัดตำแหน่ง `ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒`
- จัดวางกึ่งกลางร่วมกันในแนวระนาบ หรือจัด Anchor ตัวอักษรตรงกัน
- ระหว่างบรรทัดชื่อกับตำแหน่ง เว้นห่างกัน 1 Enter (Space After = 0 pt)

### กฎที่ 3: พิกัดตำแหน่งการลงนามมาตรฐาน (Signature Positioning Coordinates)
- **เอกสารแนวตั้ง / หน้าบันทึกข้อความ (Portrait / Official Memo Standard - A4 210 มม.):**
  - กำหนดให้ห่างจากขอบกระดาษทางซ้าย **130 มม.** (`left: 130mm;`) เป็นมาตรฐาน
  - ใน **บันทึกข้อความ** ให้เคาะลงมา **5 Enter จากบรรทัดข้อความสุดท้าย** (เช่น คำว่า `จึงเรียนมาเพื่อกรุณาทราบ`) แล้วจึงเริ่มการลงนาม
- **เอกสารแนวนอน (Landscape Standard - A4 297 มม.):**
  - กำหนดให้ห่างจากขอบกระดาษทางซ้าย **230 มม.** (`left: 230mm;`) เป็นมาตรฐาน และสามารถปรับเปลี่ยนได้ตามความเหมาะสม

---

## 5. การนำไปใช้ในโค้ด (HTML/CSS & DOCX/XLSX)

### สำหรับ HTML / CSS (Red Line Standard):
```html
<div class="sig-block">
    <div class="sig-verify">ตรวจถูกต้อง</div>
    <div class="sig-name-pos-group">
        <!-- sig-name-wrapper เป็นตัวยึดแนวเส้นดิ่งวงเล็บเปิด ( พอดี 100% -->
        <div class="sig-name-wrapper">
            <span class="sig-rank-anchor">จ.ส.อ.</span>
            <div class="sig-name">(ณัฐชัย   รักษาวงษ์)</div>
        </div>
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
    align-items: center;
    position: relative;
    margin-left: 95px;
}
/* กรอบชื่อ: เป็นตัวยึดแกนเส้นดิ่งวงเล็บเปิด ( */
.sig-name-wrapper {
    position: relative;
    display: inline-block;
    white-space: nowrap;
    margin-top: 30px; /* พื้นที่สำหรับลงลายมือชื่อจริง */
}
/* บรรทัดยศ: จุด . ท้ายยศ ชนขอบซ้ายของกรอบชื่อ ซึ่งคือ ( พอดีเป๊ะ 100% */
.sig-rank-anchor {
    position: absolute;
    right: 100%; /* ท้ายจุด . แตะแกนเดียวกับ ( */
    bottom: calc(100% + 20px);
    white-space: nowrap;
    font-size: 16pt;
    line-height: 1.0;
}
/* ชื่อและตำแหน่ง: จัดกึ่งกลางร่วมกัน 1 enter ไม่มีระยะย่อหน้า */
.sig-name {
    margin: 0;
    line-height: 1.15;
    text-align: center;
    white-space: nowrap;
    font-size: 16pt;
    display: block;
}
.sig-pos {
    margin: 0;
    line-height: 1.15;
    text-align: center;
    white-space: nowrap;
    font-size: 16pt;
    display: block;
}
```

### สำหรับ Python-docx:
```python
# Verification (1 Enter พร้อมระยะห่างหลังย่อหน้า)
p_v = cell.paragraphs[0]
p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_v.paragraph_format.space_after = Pt(24)

# Rank: . aligns with ( of name
p_rk = cell.add_paragraph()
p_rk.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_rk.paragraph_format.left_indent = Inches(rank_left_indent) # คำนวณให้ . ชนกับ (
p_rk.paragraph_format.space_after = Pt(24) # เว้นเซ็นชื่อ

# Full Name & Position: 0 pt after, 1 enter apart
p_nm = cell.add_paragraph()
p_nm.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_nm.paragraph_format.space_before = Pt(0)
p_nm.paragraph_format.space_after = Pt(0)

p_pos = cell.add_paragraph()
p_pos.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_pos.paragraph_format.space_before = Pt(0)
p_pos.paragraph_format.space_after = Pt(0)
```
