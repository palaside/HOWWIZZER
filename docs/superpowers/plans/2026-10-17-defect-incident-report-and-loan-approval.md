# Implementation Plan: ระบบใบแจ้งเหตุชำรุดและอาการ & ป๊อปอัปรายละเอียดและการอนุมัติการยืม

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** พัฒนาระบบ "ใบแจ้งเหตุชำรุดและอาการ" พร้อมระบบแนบภาพถ่ายหลักฐานไม่จำกัดเพื่อประกอบรายงานส่งซ่อม และ "ป๊อปอัปดูรายละเอียด & การอนุมัติการยืม" โดย ส.หน.สย. ในหน้าแท็บที่ ๕ ของ WEPAPP

**Architecture:** 
- ขยาย Backend API (`informal_inventory_db.json` & FastAPI endpoints) รองรับการจัดเก็บข้อมูลการอนุมัติการยืม และข้อมูลรายงานความชำรุดพร้อมภาพถ่ายหลักฐาน (Base64 / Data URL)
- สร้าง Document Engine สำหรับส่งออก "บันทึกข้อความรายงานความชำรุดและขออนุมัติส่งซ่อม" มาตรฐาน ทบ. 300 DPI (พิมพ์คู่ขนาน ๒ ชุด ฉบับตัวจริง & สำเนาคู่ฉบับ) พร้อมแผ่นภาพถ่ายหลักฐานประกอบ (Evidence Photo Appendix Sheet)
- เพิ่ม Frontend UI ๒ โมดูลใน `index.html` และ `dashboard.js`: ป๊อปอัป `#loanDetailsApprovalModal` (อนุมัติโดย ส.หน.สย. จ.ส.อ. ณัฐชัย รักษาวงษ์) และ `#defectReportModal` (แบบฟอร์มแจ้งเหตุชำรุด + Drag-and-Drop Unlimited Photo Gallery)

**Tech Stack:** Vanilla JavaScript (ES6+), HTML5 Glassmorphism UI, Python 3.12, FastAPI, OpenType TH Sarabun PSK

## Global Constraints

- ฟอนต์หลักเอกสาร: `TH Sarabun PSK` น้ำหนัก Thin 300 สำหรับเนื้อหา และ Bold 600 สำหรับหัวข้อ (ตามระเบียบ `RULE-SARABUN-DOC-STANDARD-V1`)
- บล็อกลงนาม: Universal Red Line Standard ห่างขอบซ้าย ๑๓๐ มม. เคาะ ๕ Enter (ตามระเบียบ `RULE-UNIVERSAL-SIGNATURE-BLOCK-V1`)
- ผู้อนุมัติการยืม: **ส.หน.สย. (จ.ส.อ. ณัฐชัย รักษาวงษ์)** จาก `personnel_registry.json`
- พิมพ์คู่ขนาน ๒ ชุด: ตัวจริง และ สำเนาคู่ฉบับ (ตามระเบียบ `RULE-PROD-DOC-ENGINE-V1`)
- ห้ามดัดแปลงแก้ไขหน้าที่ ๒-๑๘ ของเอกสารตรวจกิจการทั่วไปที่ผ่านการอนุมัติไปแล้ว

---

### Task 1: Data Backend & Schema Extension

**Files:**
- Modify: `backend/data/informal_inventory_db.json`
- Modify: `backend/app.py` (หรือไฟล์ route ที่เกี่ยวข้อง)
- Test: `tests/test_informal_approval_and_defects.py`

**Interfaces:**
- Produces: 
  - `POST /api/informal/loans/{loan_id}/approval` -> `{status: "success", loan: {...}}`
  - `POST /api/informal/defects` -> `{status: "success", defect: {...}, updated_item: {...}}`
  - `GET /api/informal/loans/{loan_id}` -> `{status: "success", loan: {...}}`

- [ ] **Step 1: Write the failing test for API endpoints**

```python
# tests/test_informal_approval_and_defects.py
import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_approve_loan_by_chief_ops():
    # Test approval by ส.หน.สย.
    payload = {
        "action": "approve",
        "approver_role": "ส.หน.สย.",
        "approver_rank": "จ.ส.อ.",
        "approver_name": "ณัฐชัย รักษาวงษ์",
        "approval_note": "อนุมัติให้ใช้งานในการฝึกประจำสัปดาห์ ระวังรักษาความสะอาด"
    }
    response = client.post("/api/informal/loans/LN-202610-001/approval", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["loan"]["status"] == "approved"
    assert data["loan"]["approval"]["approver_name"] == "ณัฐชัย รักษาวงษ์"

def test_create_defect_report_with_photos():
    payload = {
        "item_id": "gs_05",
        "quantity": 1,
        "reporter_rank": "จ.ส.อ.",
        "reporter_name": "สมพงษ์ ทหารกล้า",
        "reporter_position": "ผบ.หมู่ ป.๑",
        "incident_date": "2026-10-17",
        "incident_location": "พื้นที่ตั้งยิง ร้อย.๒",
        "cause": "กระทบชั้นหินแข็งใต้ผิวดินระหว่างขุดสนามเพลาะ",
        "symptom": "ด้ามไม้หักสะบั้นและใบจอบบิดงอผิดรูป",
        "urgency": "ด่วน",
        "evidence_photos": [
            {"photo_id": "PHT-001", "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "caption": "ภาพถ่ายด้ามหัก"}
        ]
    }
    response = client.post("/api/informal/defects", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "DEF-" in data["defect"]["defect_id"]
    assert len(data["defect"]["evidence_photos"]) == 1
    # Check that item repair_amount increased
    assert data["updated_item"]["repair_amount"] >= 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_informal_approval_and_defects.py -v`  
Expected: FAIL with 404 or endpoint not found

- [ ] **Step 3: Implement Backend Endpoints & Storage Logic**

Implement in `backend/app.py`:
- Endpoint for `POST /api/informal/loans/{loan_id}/approval`
- Endpoint for `POST /api/informal/defects`
- Endpoint for `GET /api/informal/loans/{loan_id}`
- Automatic stock reconciliation (cuts `balance_amount`, adds to `repair_amount`)
- Update and persist to `backend/data/informal_inventory_db.json`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_informal_approval_and_defects.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/ tests/
git commit -m "feat(api): add endpoints for loan approval and defect incident reporting"
```

---

### Task 2: Dual-Copy Repair Memo & Photo Appendix Generator

**Files:**
- Create: `backend/services/damage_memo_generator.py`
- Test: `tests/test_damage_memo_generator.py`

**Interfaces:**
- Produces: `generate_damage_repair_memo(defect_data: dict) -> dict` returning paths to real copy and office copy HTML files with embedded photo appendix sheets.

- [ ] **Step 1: Write the failing test for memo and photo appendix generation**

```python
# tests/test_damage_memo_generator.py
import os
from backend.services.damage_memo_generator import generate_damage_repair_memo

def test_generate_damage_repair_memo_with_photo_sheet():
    defect_sample = {
        "defect_id": "DEF-202610-999",
        "item_name": "จอบขุดดิน",
        "quantity": 1,
        "reporter_rank": "จ.ส.อ.",
        "reporter_name": "สมพงษ์ ทหารกล้า",
        "reporter_position": "ผบ.หมู่ ป.๑",
        "incident_date": "2026-10-17",
        "incident_location": "พื้นที่ตั้งยิง ร้อย.๒",
        "cause": "กระทบชั้นหินแข็งใต้ผิวดิน",
        "symptom": "ด้ามไม้หักสะบั้นและใบจอบบิดงอผิดรูป",
        "urgency": "ด่วน",
        "evidence_photos": [
            {"photo_id": "PHT-001", "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "caption": "ภาพถ่ายด้ามหัก"}
        ]
    }
    result = generate_damage_repair_memo(defect_sample)
    assert os.path.exists(result["real_copy_html"])
    assert os.path.exists(result["copy_html"])
    
    with open(result["real_copy_html"], "r", encoding="utf-8") as f:
        content = f.read()
        assert "บันทึกข้อความ" in content
        assert "ภาพถ่ายความชำรุดเสียหาย" in content
        assert "สมพงษ์ ทหารกล้า" in content
        assert "PHT-001" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_damage_memo_generator.py -v`  
Expected: FAIL with ModuleNotFoundError or FileNotFoundError

- [ ] **Step 3: Implement `damage_memo_generator.py`**

- Complies with `RULE-SARABUN-DOC-STANDARD-V1` (TH Sarabun PSK 16pt Thin 300, 20pt Bold 600)
- Complies with `RULE-UNIVERSAL-SIGNATURE-BLOCK-V1` (130mm from left edge, 5 Enter down)
- Appends Page 2: "แผ่นภาพถ่ายประกอบรายงานการส่งซ่อม" containing:
  - Header: แผ่นภาพถ่ายความชำรุดเสียหายของสิ่งอุปกรณ์
  - Item info: จอบขุดดิน (จำนวน ๑ เล่ม)
  - Photo grid: 2-4 photos per page with borders, centered captions
  - Certification stamp block: "ตรวจรับรองภาพถ่ายความชำรุดถูกต้อง" พร้อมช่องลงนาม

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_damage_memo_generator.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/services/damage_memo_generator.py tests/test_damage_memo_generator.py
git commit -m "feat(docs): implement dual-copy repair memo and photo appendix generator"
```

---

### Task 3: UI - Loan Details & Approval Modal (`#loanDetailsApprovalModal`)

**Files:**
- Modify: `index.html` (Modal markup)
- Modify: `frontend/templates/index.html` (Modal markup)
- Modify: `static/dashboard.js` (Loan table row click, hydration, approval handlers)
- Modify: `frontend/static/dashboard.js`

- [ ] **Step 1: Add Modal HTML markup to `index.html` & `frontend/templates/index.html`**

Add `#loanDetailsApprovalModal` containing:
- Modal title: 📋 รายละเอียดการเบิกยืมสิ่งอุปกรณ์ & พิจารณาอนุมัติ
- Status pill badge
- Borrower information grid (ยศ ชื่อ สกุล, ตำแหน่ง, วันที่ยืม, กำหนดคืน)
- Equipment information grid (ชื่อสิ่งอุปกรณ์, หมวดคลัง, จำนวน)
- Approval box by **ส.หน.สย. (จ.ส.อ. ณัฐชัย รักษาวงษ์)** with notes textarea
- Action buttons: `✅ อนุมัติการยืม`, `❌ ไม่อนุมัติ`, `🖨️ พิมพ์ใบยืมสิ่งอุปกรณ์`, `ปิดหน้าต่าง`

- [ ] **Step 2: Update `dashboard.js` to handle row clicking and modal interactions**

- Add `cursor: pointer;` and hover background to `#informalLoansBody tr`
- Add `onclick="openLoanDetailsModal('${l.loan_id}')"` to row and an action button `👁️ ดูรายละเอียด/อนุมัติ`
- Implement `openLoanDetailsModal(loanId)` to fetch and hydrate loan details
- Implement `submitLoanApproval(loanId, action)` to call approval API, update UI badge, and refresh inventory metrics
- Implement `printLoanSlip(loanId)` to open official printable loan slip

- [ ] **Step 3: Test modal opening and approval action manually & verify in browser**

- Click on a loan row
- Verify loan details display accurately
- Check that approver shows "จ.ส.อ. ณัฐชัย รักษาวงษ์ (ส.หน.สย.)"
- Click "อนุมัติการยืม" and verify status changes to "อนุมัติแล้ว"

- [ ] **Step 4: Commit**

```bash
git add index.html frontend/templates/index.html static/dashboard.js frontend/static/dashboard.js
git commit -m "feat(ui): add loan details and chief operations approval modal"
```

---

### Task 4: UI - Defect & Malfunction Report Form with Unlimited Photo Intake (`#defectReportModal`)

**Files:**
- Modify: `index.html` (Action bar button & Defect modal markup)
- Modify: `frontend/templates/index.html`
- Modify: `static/dashboard.js` (Defect modal logic, multi-photo intake, gallery preview)
- Modify: `frontend/static/dashboard.js`

- [ ] **Step 1: Add Action Bar button and Defect Report Modal HTML**

In `index.html`:
- Add `<button onclick="openDefectReportModal()" class="btn-danger" style="padding: 7px 16px; background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; font-weight: 600; cursor: pointer;">🔴 แจ้งเหตุชำรุด & ส่งซ่อม</button>`
- Add `#defectReportModal` overlay containing:
  - Equipment select dropdown (populated from inventory)
  - Quantity input
  - Reporter info (Rank, Name, Position)
  - Date and location of incident
  - Textarea: สาเหตุที่เกิดความชำรุด (Cause)
  - Textarea: อาการชำรุดที่ตรวจพบ (Symptoms)
  - Urgency selector (ปกติ / ด่วน / ด่วนที่สุด)
  - **Unlimited Photo Upload Zone (`#defectPhotoUploadZone`):**
    - Hidden file input `<input type="file" id="defectPhotoFiles" multiple accept="image/*">`
    - Drag & drop dropzone
    - Gallery container (`#defectPhotoGallery`) showing thumbnails with caption inputs and delete buttons

- [ ] **Step 2: Implement Photo Upload and Defect Submit Logic in `dashboard.js`**

- Implement `handleDefectPhotoSelect(files)`: reads files via `FileReader` as Data URLs, appends to `currentDefectPhotos` array, renders gallery
- Implement `removeDefectPhoto(photoIndex)`
- Implement `updateDefectPhotoCaption(photoIndex, caption)`
- Support clipboard paste (`window.addEventListener('paste', ...)`) when modal is open
- Implement `handleDefectReportSubmit(event)`:
  - Posts defect data to `/api/informal/defects`
  - Updates inventory table: moves count from balance to "ส่งซ่อม"
  - Closes modal, shows success alert
  - Opens `#damageMemoModal` previewing the newly generated repair memo with photo appendix

- [ ] **Step 3: Test defect submission and photo gallery preview**

- Open defect report modal
- Select equipment (e.g. จอบขุดดิน)
- Add 3 photos, specify captions
- Fill cause and symptoms, click submit
- Confirm inventory table updates "ส่งซ่อม" from 0 to 1
- Confirm memo preview opens with embedded photos on Page 2

- [ ] **Step 4: Commit**

```bash
git add index.html frontend/templates/index.html static/dashboard.js frontend/static/dashboard.js
git commit -m "feat(ui): add defect report modal with unlimited evidence photos and memo preview"
```

---

### Task 5: End-to-End Integration, E2E Test & Sync

**Files:**
- Create: `scripts/test_defect_and_loan_approval_e2e.py`
- Modify: `backend/data/informal_inventory_db.json` (seeded state)

- [ ] **Step 1: Write automated E2E test script**

```python
# scripts/test_defect_and_loan_approval_e2e.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_e2e_approval_flow():
    # 1. Fetch loan
    res = requests.get(f"{BASE_URL}/api/informal/loans/LN-202610-001")
    assert res.status_code == 200
    loan = res.json()["loan"]
    
    # 2. Approve by ส.หน.สย.
    app_res = requests.post(f"{BASE_URL}/api/informal/loans/{loan['loan_id']}/approval", json={
        "action": "approve",
        "approver_role": "ส.หน.สย.",
        "approver_rank": "จ.ส.อ.",
        "approver_name": "ณัฐชัย รักษาวงษ์",
        "approval_note": "อนุมัติเรียบร้อย"
    })
    assert app_res.status_code == 200
    assert app_res.json()["loan"]["status"] == "approved"

def test_e2e_defect_reporting_flow():
    # 1. Submit defect with photo
    payload = {
        "item_id": "gs_01",
        "quantity": 1,
        "reporter_rank": "ส.อ.",
        "reporter_name": "สมชาย แสนดี",
        "reporter_position": "พลปืน",
        "incident_date": "2026-10-17",
        "incident_location": "โรงเก็บปืนใหญ่",
        "cause": "การเสื่อมสภาพจากการใช้งาน",
        "symptom": "ชุดลั่นไกขัดข้อง",
        "urgency": "ด่วน",
        "evidence_photos": [
            {"photo_id": "P-1", "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "caption": "ภาพถ่ายชุดลั่นไก"}
        ]
    }
    res = requests.post(f"{BASE_URL}/api/informal/defects", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

if __name__ == "__main__":
    test_e2e_approval_flow()
    test_e2e_defect_reporting_flow()
    print("ALL E2E INTEGRATION TESTS PASSED!")
```

- [ ] **Step 2: Run E2E test and verify**

Run: `python scripts/test_defect_and_loan_approval_e2e.py`  
Expected: `ALL E2E INTEGRATION TESTS PASSED!`

- [ ] **Step 3: Sync static/docs and frontend mirrors**

Ensure all updated files are mirrored in `frontend/` and `static/`.

- [ ] **Step 4: Final Commit**

```bash
git add .
git commit -m "feat(e2e): complete integration and automated test suite for defect reports and loan approval"
```
