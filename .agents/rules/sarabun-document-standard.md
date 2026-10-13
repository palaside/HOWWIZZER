# 🏛️ SARABUN DOCUMENT ENGINE STANDARD (กฎระเบียบงานสารบรรณขั้นสูงสุด)
**Rule ID:** RULE-SARABUN-DOC-STANDARD-V1  
**Scope:** บังคับใช้กับเอกสารราชการ, หนังสือภายนอก, หนังสือภายใน (บันทึกข้อความ), รายงาน, แบบฟอร์ม ทบ., และเอกสารทุกชุด/ทุกฉบับในโปรเจกต์ ๑๐๐%

---

## 📌 1. CORE MANDATE (พันธกิจหลัก)
1. **เอกสารทุกชุดและทุกฉบับ ต้องผ่าน Reference ของระเบียบงานสารบรรณ** (ระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ พ.ศ. ๒๕๒๖ และธรรมเนียมทหาร) อย่างเคร่งครัด
2. **ขจัดปัญหาการรีเฟรชหรือคอมไพล์ใหม่แล้วการจัดหน้า/ฟอนต์/บล็อกหลุดโดยเด็ดขาด (Zero Regression)**
3. ระบบต้องยึดถือมาตรฐานนี้เป็น Single Source of Truth (SSOT) ร่วมกับแม่แบบ Gold Standard ใน eferences/

---

## 🔤 2. TYPOGRAPHY & FONT SPECIFICATION (มาตรฐานฟอนต์และน้ำหนัก)

### 2.1 ฟอนต์หลัก (Primary Font Family)
* กำหนดใช้ **TH Sarabun New** และ **TH Sarabun PSK** ต้นฉบับราชการแท้ (SIPA / กรมทรัพย์สินทางปัญญา DIP) เป็นฟอนต์หลัก
* ต้องฝังไฟล์ฟอนต์แท้ (.ttf) ใน `fonts/` (`THSarabunNew.ttf`, `THSarabunNew-Bold.ttf`, `THSarabunPSK.ttf`, `THSarabunPSK-Bold.ttf`) พร้อมประกาศ `@font-face`
* จัดลำดับ `font-family: 'TH Sarabun New', 'TH Sarabun PSK', 'THSarabunNew', 'THSarabunPSK', 'Sarabun', sans-serif !important;` โดยให้ฟอนต์แท้ราชการมีลำดับความสำคัญก่อน Google Fonts

### 2.2 ขนาดฟอนต์มาตรฐาน (Font Size = 17pt Standard)
* **ขนาดตัวอักษรเนื้อหาหลัก (Standard Body Size):** **17pt**
* **ความสูงบรรทัด (Line Height):** line-height: 1.25 ถึง 1.30
* **ข้อยกเว้นเฉพาะจุดตามระเบียบงานสารบรรณ:**
  * **หัวเรื่องใหญ่ บันทึกข้อความ (Title):** 29pt ตัวหนา (ont-weight: 700;)
  * **หัวข้อแถบข้อมูลราชการ (Meta Labels):** 20pt ตัวหนา (ont-weight: 700;) เช่น ส่วนราชการ, ที่, วันที่, เรื่อง
  * **บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน (Staff Footer):** 13.5pt ถึง 14pt ตัวบาง (ont-weight: 300;)

### 2.3 มาตรฐานน้ำหนักฟอนต์ (Strict Font-Weight Hierarchy)
* **หัวข้อหลัก (Headings / Labels / Titles):** ต้องใช้ **ตัวหนามาตรฐาน Microsoft Word (font-weight: 600 / Bold)**
  * ป้ายกำกับ: ส่วนราชการ, ที่, วันที่, เรื่อง, เรียน, สิ่งที่ส่งมาด้วย (เฉพาะคำหัวข้อ)
  * หัวตาราง (th) และชื่อฟอร์ม/รายงาน
  * **ข้อห้าม:** ห้ามใช้ตัวหนาถมดำตันจัดแบบ Google Fonts 700 display ให้ใช้ความหนาโปร่งคมชัดตามลายเส้นราชการแท้ (Stroke Weight 600)
* **ส่วนที่ไม่ใช่หัวข้อ (Non-headings / Body / Content / Tables / Footers):** ต้องใช้ **ตัวบาง (Thin/Light: font-weight: 300)** เสมอ!
  * เนื้อหาบันทึกข้อความ (.content-para, .memo-body)
  * ข้อความเติมในเส้นประ (.meta-fill-dotted)
  * รายละเอียดสิ่งที่ส่งมาด้วย และจำนวน
  * ยศ ชื่อ ตำแหน่งในบล็อกลงนาม (.sig-rank-anchor, .sig-name, .sig-pos)
  * บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน (.staff-grid)

---

## ✍️ 3. SIGNATURE BLOCK ENGINE (บล็อกลงนามมาตรฐาน Red Line Standard)
ต้องปฏิบัติตาม **[RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md)** อย่างเคร่งครัด ๑๐๐%:

1. **แกนดิ่ง Red Line Standard:**
   * จุด . ท้ายสุดของยศ (เช่น ร.ท., จ.ส.อ.) ต้องตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมายวงเล็บเปิด ( ของชื่อเป๊ะ ๑๐๐% (ight: 100% ของ .sig-name-wrapper)
2. **การจัดกึ่งกลางชื่อและตำแหน่ง:**
   * ชื่อในวงเล็บและตำแหน่ง ต้องจัดกึ่งกลางร่วมกันเสมอ
   * ห่างกัน ๑ Enter (margin-top: 0; line-height: 1.15;)
   * มีระยะเว้นสำหรับลงลายมือชื่อจริงเหนือชื่อประมาณ ๒-๓ Enter (๑๒ - ๑๔ มม.)
3. **พิกัดตำแหน่งบล็อกลงนาม:**
   * **บันทึกข้อความ / แนวตั้ง (Portrait):** เว้นระยะห่างจากขอบกระดาษทางซ้าย **๑๓๐ มม.** (หรือจัดชิดขวาใน Container กว้าง ๗๕ มม.)
   * เคาะลงมา **๕ Enter (๑๘ - ๒๒ มม.)** จากบรรทัดข้อความสุดท้าย (เช่น จึงเรียนมาเพื่อกรุณาพิจารณา) ก่อนเริ่มยศ
   * **แนวนอน (Landscape):** เว้นระยะห่างจากขอบกระดาษทางซ้าย **๒๓๐ มม.**
4. **ข้อห้ามเด็ดขาด (STRICT PROHIBITION):**
   * ห้ามจับยศไปจัดกึ่งกลางรวบกับชื่อใน Word (.docx) หรือ Excel (.xlsx) เด็ดขาด ต้องใช้ Tab Stop หรือชิดแกนดิ่งเท่านั้น

---

## 📝 4. STAFF REVIEW FOOTER (บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน)
ต้องปฏิบัติตาม **[RULE-STAFF-REVIEW-FOOTER-V1](file:///d:/Project/WEPAPP/.agents/rules/staff-review-footer.md)** อย่างเคร่งครัด ๑๐๐%:

1. **ระยะห่างแนวดิ่ง (5-Enter Invariant):**
   * บล็อกผู้ร่าง/ตรวจ/พิมพ์/ทาน ต้องเคาะลงมาเป็นระยะ **๕ Enter (๒๒ มม.)** ใต้บรรทัดตำแหน่งของผู้บังคับบัญชาผู้ลงนาม (เช่น ใต้ ผบ.ป.๔ พัน.๔ ร้อย.๒)
2. **โครงสร้าง ๔ คอลัมน์มาตรฐาน (Standard 4-Column Grid):**
   `html
   <div class=memo-footer-staff>
       <div class=staff-grid>
           <div>จ.ส.อ.</div>
           <div>ร่าง/ตรวจ</div>
           <div></div>
           <div>พ.ย. ๖๙</div>
           <div>ส.ท. วรากรฯ</div>
           <div>พิมพ์/ทาน</div>
           <div style=text-align: right; padding-right: 2.5mm;>๕</div>
           <div>พ.ย. ๖๙</div>
       </div>
   </div>
   `
3. **สเปก CSS มาตรฐาน:**
   `css
   .memo-footer-staff {
       margin-top: 22mm;
       display: flex;
       justify-content: flex-end;
   }
   .staff-grid {
       display: grid;
       grid-template-columns: 26mm 22mm 8mm 20mm;
       font-size: 13.5pt;
       font-weight: 300;
       line-height: 1.25;
       text-align: left;
   }
   `
4. **มาตรฐาน ๒ แกนดิ่งคู่ขนาน (Dual-Axis Alignment):**
   * **แกนตัวอักษรแรกของยศ:** ตัวแรกของยศแถวบน (จ) และแถวล่าง (ส) ต้องเริ่มต้นที่แนวเส้นดิ่งเดียวกัน (	ext-align: left;)
   * **แกนเดือนและปี:** ตัวแรกของเดือนแถวบนและล่าง ต้องเริ่มต้นที่แนวเส้นดิ่งเดียวกัน โดยมีช่องวันที่ชิดขวาอยู่ข้างหน้าเดือนในแถวล่าง
5. **ระบบ Dual-Copy Engine:**
   * **ฉบับตัวจริง:** บล็อกนี้ถูกซ่อนอัตโนมัติ (display: none !important;)
   * **สำเนาคู่ฉบับ:** บล็อกนี้แสดงผลพร้อมวันที่เสนอเซ็นที่ถูกต้องตามวันทำการ (จันทร์-พฤหัสบดี)

---

## 🛡️ 5. THAI TYPOGRAPHY & ZERO SPLIT WORDS (การตัดคำและกั้นหน้า-หลัง)
1. ทุกข้อความภาษาไทยต้องผ่านกระบวนการแทรก Zero-Width Space (\u200b) ผ่าน 	hai_typography_engine.py เพื่อป้องกันคำขาดครึ่งท่อน
2. เอกสารต้องตั้งค่า CSS กั้นหน้า-กั้นหลังตรง:
   `css
   text-align: justify;
   text-justify: inter-cluster;
   word-break: keep-all;
   overflow-wrap: break-word;
   `
3. ตัวเลขไทย-อารบิก, วันที่, และรหัสสิ่งอุปกรณ์ (เช่น ปบค.๙๕, ๑๐๕ มม., เอ็ม ๑๐๑ เอ ๑) ต้องไม่ถูกตัดทอนหรือแยกส่วน

---

## 🚫 6. ZERO-REGRESSION ENFORCEMENT (การป้องกันการแก้แล้วหลุด)
* **เมื่อมีการ Refresh, Re-generate, หรือรัน Build Script:** สคริปต์คอมไพล์ทุกตัวต้องอ่านกฎนี้และนำโครงสร้างทั้ง ๕ ข้อไปคอมไพล์ลงเอกสารทันที ห้ามตกหล่นฟอนต์ 17pt, ห้ามลืม Thin 300, ห้ามลืม Red Line Signature, และห้ามลืมบล็อก ร่าง/ตรวจ/พิมพ์/ทาน เด็ดขาด!
