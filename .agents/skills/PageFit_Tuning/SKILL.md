---
name: PageFit_Tuning
description: สกิลควบคุมและบีบอัดเอกสาร/แบบฟอร์มราชการให้ลงพอดีหน้า A4 (Single-Page Fit & Vertical Budget Engineering) ป้องกันข้อความหรือบล็อกลงนามล้นตกขอบกระดาษ 100% ด้วยสูตร Micro-Tuning Budget 4 มิติ
---

# 📄 PageFit_Tuning Skill (Zero-Overflow Engineering Engine)

## 📌 บทบาทและวัตถุประสงค์
ใช้เมื่อเอกสาร HTML, DOCX หรือแบบฟอร์มราชการมีเนื้อหายาวจน **"ล้นตกขอบกระดาษ"** หรือ **"ดันแถบลงนามและวันที่หลุดออกไปหน้าถัดไป"** 

สกิลนี้ทำหน้าที่เป็น **"สูตรแก้ปัญหาเชิงวิศวกรรม (Engineering Heuristic)"** สำหรับคำนวณและปรับลดช่องว่างแนวตั้ง (Vertical Budget) โดย**ไม่ทำลายความคมชัดและมาตรฐานความสวยงามของเอกสารราชการไทย**

---

## ⚠️ กฎเหล็กของ PageFit (Golden Rules)
1. **ห้ามลดเฉพาะฟอนต์อย่างเดียว:** การลดฟอนต์ลงเหลือ 11-12pt จะทำให้ดูเหมือนเอกสารร่าง ต้องใช้การเฉลี่ยน้ำหนัก 4 มิติ
2. **ห้ามบีบ line-height ต่ำกว่า 1.15:** ต่ำกว่านี้สระบน (ิ ี ึ ื) และวรรณยุกต์จะชนก้นพยัญชนะบรรทัดบนทันที
3. **รักษาความปลอดภัยขอบล่าง (Bottom Safety Margin):** ต้องเหลือพื้นที่สีขาวใต้บรรทัดลงนามอย่างน้อย **8 - 12 mm** เสมอ

---

## 🧮 ตารางสูตรคำนวณ 4 มิติ (Micro-Tuning Budget Matrix)

เมื่อพบอาการตกขอบ ให้ปรับจูนค่า CSS และ Paragraph Properties ตามตารางนี้ตามลำดับความรุนแรง:

| มิติการปรับจูน | ค่าปกติ (Normal Flow) | เลเวล 1: ล้นเล็กน้อย (1-2 บรรทัด) | เลเวล 2: ล้นหนัก (3-5 บรรทัด) | พื้นที่ที่ได้คืน (Net Gain) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Page Padding (ล่าง/บน)** | บน 20mm / ล่าง 20mm | บน 14mm / ล่าง 12mm | บน 12mm / **ล่าง 10mm** | **คืนมา 10 - 15 mm** |
| **2. Body Font Size** | `15.5pt - 16pt` | `14.5pt` | `13.5pt - 14pt` | **คืนมา 5 - 8 mm** |
| **3. Line-height** | `1.30 - 1.35` | `1.22 - 1.25` | `1.18 - 1.20` | **คืนมา 8 - 12 mm** |
| **4. Section/Item Margins** | บน 2mm / ล่าง 2.5mm | บน 1mm / ล่าง 1.2mm | บน 0.4mm / **ล่าง 0.6mm** | **คืนมา 6 - 10 mm** |
| **5. Bottom Sig Container** | บน 3mm / ล่าง 2mm | บน 1.5mm / ล่าง 1mm | บน 1mm / **ล่าง 0.5mm** | **คืนมา 3 - 5 mm** |

> **ผลรวมสะสม:** เลเวล 2 สามารถดึงเนื้อหากลับขึ้นมาได้ถึง **25 - 35 mm (เทียบเท่า 8 - 10 บรรทัด)**

---

## 💻 Standard Implementation Snippets

### 1. ฝั่ง HTML / CSS (Single-Page Fit Template)
```css
/* Page Shell */
.page-portrait {
    width: 210mm;
    min-height: 297mm;
    height: 297mm;
    padding: 12mm 18mm 10mm 22mm; /* บน ขวา ล่าง ซ้าย */
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

/* Tight Body & Cascade List */
.body-text, .finding-block, .rec-item {
    font-size: 13.5pt;
    line-height: 1.18;
    margin-bottom: 0.6mm;
    text-align: justify;
    text-justify: inter-cluster;
}

/* Micro Gaps on Headers */
.section-title, .rec-header {
    margin-top: 0.8mm;
    margin-bottom: 0.4mm;
    font-size: 14pt;
    font-weight: bold;
}

/* Signature Block Anchor at Page Bottom */
.bottom-sig-container {
    width: 100%;
    margin-top: auto;        /* ดันชิดล่าง */
    padding-top: 1mm;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-size: 13.5pt;
    line-height: 1.18;
}
.bottom-sig-line {
    white-space: nowrap;
    margin-bottom: 0.5mm;
}
.bottom-date-line {
    white-space: nowrap;
    margin-right: 16mm;
}
```

### 2. ฝั่ง Word (.docx / python-docx)
```python
# ปรับ Paragraph Space After และ Line Spacing ใน python-docx
p_format = paragraph.paragraph_format
p_format.space_before = Pt(1)   # กระชับหัว
p_format.space_after = Pt(2)    # กระชับท้าย
p_format.line_spacing = 1.18    # อัตราส่วนความสูงบรรทัด
```

---

## 🔍 Visual Verification Checklist
ก่อนส่งมอบงาน ต้องรันสคริปต์จับภาพหน้าจอและตรวจ 3 ข้อนี้:
- [ ] มีขอบกระดาษสีขาวเหลือใต้บรรทัดสุดท้าย (วันที่/ลายเซ็น) ไม่ต่ำกว่า 8mm หรือไม่?
- [ ] สระบน วรรณยุกต์ และสระล่าง ไม่ซ้อนทับหรือเบียดกันจนอ่านไม่ออกใช่หรือไม่?
- [ ] ไม่มีข้อความโดน CSS `overflow: hidden` กลืนหายไปใช่หรือไม่?
