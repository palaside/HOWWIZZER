# 🏛️ WEPAPP - Royal Thai Army Production Document & Armament Inventory Suite
> **Software Preservation & Reproducibility Standard (Immortal Project Protocol)**  
> **Official Git Remote Repository:** [https://github.com/palaside/HOWWIZZER.git](https://github.com/palaside/HOWWIZZER.git)  
> **Production Cloud Live (Vercel):** [https://howwizzer-five.vercel.app](https://howwizzer-five.vercel.app)

---

## 📌 บทนำและภาพรวมของระบบ (Project Overview)
**WEPAPP (HOWWIZZER)** คือระบบบริหารจัดการยุทโธปกรณ์ คลังสิ่งอุปกรณ์ และระบบคอมไพล์เอกสารแบบฟอร์มราชการกองทัพบกไทยระดับ Production เกรดเอ (Pixel-Perfect Superclone Production Engine) พัฒนาตาม **ระเบียบงานสารบรรณสำนักนายกรัฐมนตรี พ.ศ. ๒๕๒๖ / ระเบียบกองทัพบก พ.ศ. ๒๕๖๓** รองรับการส่งออกคู่ขนานทั้ง **HTML, Microsoft Word (.docx), และ Microsoft Excel (.xlsx)** โดยควบคุมความแม่นยำระดับพิกเซลและรักษาความสมบูรณ์ของสูตรคำนวณและตัวเลขไทย ๑๐๐%

---

## 🚀 การสั่งงานแบบคลิกเดียว (Zero-Command Launcher)
ไม่ต้องจำคำสั่งคอนโซลหรือพิมพ์คำสั่งผ่าน Terminal:

1. **ดับเบิลคลิกไฟล์:** `run_webapp.bat`
   - ระบบจะเปิดเบราว์เซอร์อัตโนมัติไปที่ `http://127.0.0.1:8000`
   - รัน FastAPI / Uvicorn Server อัตโนมัติ รองรับ hot-reload
2. **สำหรับคอมไพล์เอกสารแบบฟอร์ม Batch:**
   - ดับเบิลคลิกไฟล์: `run_superclone.bat`

---

## 🏛️ สถาปัตยกรรมหลัก ๔ เสา (The 4 Architectural Pillars)
1. **Universal Red Line Standard (`signature_engine.py`):**
   - มาตรฐานการจัดบล็อกลงนามราชการระดับสากล ยศและวงเล็บเปิดของชื่อชนแกนดิ่งเดียวกันเป๊ะ ๑๐๐% (`right: 100%`) ห่างจากขอบกระดาษซ้าย ๑๓๐ มม. (แนวตั้ง) และเคาะลงมา ๕ Enter จากเนื้อความสุดท้าย
2. **Dual-Copy Package Engine (ตัวจริง + สำเนาคู่ฉบับ):**
   - ๑ คำสั่งพิมพ์ เรนเดอร์คู่ขนานทั้งฉบับตัวจริง และฉบับสำเนาคู่ฉบับที่มีตารางผู้ร่าง/ตรวจ/พิมพ์/ทาน แกนดิ่งคู่ขนาน ๔ คอลัมน์ (ตาม `RULE-STAFF-REVIEW-FOOTER-V1`)
3. **Typography & OpenType PSK Standard:**
   - ฟอนต์หลัก `TH Sarabun PSK` (Bold 600 สำหรับหัวข้อ / Thin 300 สำหรับเนื้อหาและผลการตรวจ) พร้อมระบบตัดคำภาษาไทย Zero-Width Space ป้องกันคำขาดครึ่งท่อน
4. **Single Source of Truth (SSOT Blueprints):**
   - ควบคุมโครงสร้างเอกสารผ่าน JSON Blueprint (`table_layout.json`, `memo_layout.json`, `table_layout_damage_memo.json`) ป้องกัน Layout Drift ๑๐๐%

---

## 📦 การติดตั้งและการรันระบบ (Installation & Runtime)

### ความต้องการของระบบ:
- **Python:** 3.12 ขึ้นไป
- **Node.js:** v18+ (สำหรับ build/dev tools)

### ติดตั้ง Dependencies:
```powershell
pip install -r requirements.txt
```

### การรันระบบ Local:
```powershell
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🌐 Cloud Production Deployment (Vercel Serverless)
- **Production URL:** [https://howwizzer-five.vercel.app](https://howwizzer-five.vercel.app)
- **Runtime:** Python 3.12 Serverless + Static Assets CDN
- **Deploy Command:** `vercel --prod`
