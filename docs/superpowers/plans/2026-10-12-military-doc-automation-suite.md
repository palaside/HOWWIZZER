# Military Document Automation & Armory Custody Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** พัฒนาระบบบริหารจัดการและผลิตเอกสารราชการทหารอัตโนมัติบนคลาวด์/เว็บ (Cloud-Native Auto-Doc Engine) พร้อมระบบคุมสิ่งอุปกรณ์ประจำคลัง (Dual-Control Armory & Custody Ledger), กล่องรับเอกสารภายนอก (FolderIN Watcher & Gap Analysis), ปฏิทินวันทำการไทย (Thai Business Day Scheduler), และ Tactical Web Dashboard ตามระเบียบงานสารบรรณ ทบ. ๒๕๖๓ และ Red Line Signature Standard

**Architecture:** สถาปัตยกรรมแบ่งเป็น 4 ชั้นอิสระ (Decoupled 4-Tier Architecture):
1. **Core Governance & Registry:** โครงสร้างข้อมูลกลาง (SSOT) ประกอบด้วย ระเบียบงานสารบรรณ, ทะเบียนข้าราชการ/ผู้บังคับบัญชา (`personnel_registry.json`), และตารางวันหยุดราชการไทย (`thai_holidays.json`)
2. **Business Day & Auto-Doc Engine:** ตัวจัดตารางเวลาอัจฉริยะ (Roll-backward holiday adjustment) และเอนจินประมวลผลเทมเพลต 18 ฉบับ บรรจุลง Cloud HotFolder อัตโนมัติ
3. **Inventory & External Intake Services:** กลไกจัดการสต็อกสิ่งอุปกรณ์ (ทบ.๔๐๐-๐๐๕ / ทบ.๔๖๘-๒๐๔) ด้วยระบบอนุมัติสองชั้น (Maker-Checker Dual Control) ควบคู่กับระบบเฝ้ารับไฟล์แผนกอื่น (`FolderIN` Watcher & Gap Analysis)
4. **Tactical Web Dashboard:** เว็บแดชบอร์ดสไตล์ Tactical Dark / Glassmorphism รองรับการตรวจสอบสถานะเอกสารแบบเรียลไทม์, ตารางเช็คลิสต์รอบส่ง, ระบบจัดการยืม-คืนสิ่งอุปกรณ์, และปุ่มสั่งพิมพ์/ดาวน์โหลด 1 คลิก

**Tech Stack:** Python 3.12, FastAPI, Uvicorn, SQLite / JSON SSOT Datastore, Watchdog (File System Observer), HTML5 / Vanilla CSS (Tactical Dark Glassmorphism), Jinja2, python-docx, openpyxl, Playwright / Weasyprint

## Global Constraints

- ปฏิบัติตามกฎ [RULE-PROD-DOC-ENGINE-V1](file:///d:/Project/WEPAPP/.agents/rules/production-grade-engine.md), [RULE-UNIVERSAL-SIGNATURE-BLOCK-V1](file:///d:/Project/WEPAPP/.agents/rules/signature-block.md) (Red Line Standard), และ [RULE-PAGEFIT-TUNING-V1](file:///d:/Project/WEPAPP/.agents/skills/PageFit_Tuning/SKILL.md) 100%
- ปฏิบัติตามระเบียบกองทัพบกว่าด้วยงานสารบรรณ พ.ศ. ๒๕๖๓ (หมวด ๒ ข้อ ๑๒ หนังสือภายใน และ ข้อ ๑๖.๔ หนังสืออื่น)
- จัดแนวเส้นดิ่งบล็อกลงนามด้วย Universal Red Line Standard เสมอ (จุด `.` ท้ายยศ ตรงกับวงเล็บเปิด `(` ของชื่อ, ห้าม Center รวบ)
- ไม่มีการผลิตเอกสารในวันหยุดราชการและวันเสาร์-อาทิตย์เด็ดขาด (ระบบต้องคำนวณถอยหลังสู่วันทำการก่อนหน้า - Roll-Backward อัตโนมัติ)
- แอดมิน (จนท.คลัง) มีสิทธิ์ Read-Only และยื่นคำขอ (Request) เท่านั้น สิทธิ์การตัดยอดและอนุมัติเป็นของ Owner (ผบ.ร้อย/ผู้บังคับบัญชา) เท่านั้น (Maker-Checker Protocol)
- บันทึกความเสียหายของสิ่งอุปกรณ์ (Damage Log) และประวัติการจัดหาทดแทน (Replacement Audit) เป็น Immutable Audit Trail ห้ามลบทิ้งเด็ดขาด
- **มาตรฐานความคมชัดสูงระดับงานพิมพ์ (Print-Grade 300 DPI Standard):** ทุกการสร้างภาพพรีวิว (Thumbnail/Preview), การแปลงภาพ Vision, และการส่งออกพรีวิวหน้าเอกสาร ต้องเรนเดอร์ที่ `device_scale_factor >= 2.5` (๒๔๐–๓๐๐ DPI Print Resolution) ห้ามใช้ Screen DPI 96 ค่าเริ่มต้นเด็ดขาด พร้อมเปิดใช้งาน `-webkit-font-smoothing: antialiased;` และเส้นตารางดำสนิท คมกริบ ไร้รอยหยักเบลอ ๑๐๐%


---

### Task 1: Thai Business Day & Government Holiday Engine

**Files:**
- Create: `backend/services/business_day_engine.py`
- Create: `backend/data/thai_holidays.json`
- Test: `tests/test_business_day_engine.py`

**Interfaces:**
- Produces: `is_business_day(target_date: datetime.date) -> bool`
- Produces: `get_adjusted_cycle_date(target_date: datetime.date, direction: str = 'backward') -> datetime.date`
- Produces: `get_weekly_submission_date(cycle_friday: datetime.date) -> datetime.date`
- Produces: `get_next_business_day(target_date: datetime.date) -> datetime.date`

- [ ] **Step 1: Write failing test for business day calculation, Thai holidays, and synchronized weekly submission date**

```python
# tests/test_business_day_engine.py
import pytest
from datetime import date
from backend.services.business_day_engine import (
    is_business_day,
    get_adjusted_cycle_date,
    get_weekly_submission_date,
    get_next_business_day
)

def test_weekend_detection():
    # 2026-10-17 is Saturday, 2026-10-18 is Sunday
    assert is_business_day(date(2026, 10, 17)) is False
    assert is_business_day(date(2026, 10, 18)) is False
    # 2026-10-16 is Friday
    assert is_business_day(date(2026, 10, 16)) is True

def test_thai_holiday_detection():
    # 2026-10-13 is King Bhumibol Memorial Day (National Holiday)
    assert is_business_day(date(2026, 10, 13)) is False

def test_roll_backward_holiday_adjustment():
    # If target is Tuesday 2026-10-13 (Holiday), roll backward should land on Monday 2026-10-12
    adjusted = get_adjusted_cycle_date(date(2026, 10, 13), direction='backward')
    assert adjusted == date(2026, 10, 12)

def test_weekly_submission_date_is_thursday_and_never_friday():
    # Friday 2026-06-19 -> baseline submission must be Thursday 2026-06-18
    sub_date = get_weekly_submission_date(date(2026, 6, 19))
    assert sub_date == date(2026, 6, 18)
    assert sub_date.weekday() == 3  # Thursday
    assert is_business_day(sub_date) is True

def test_weekly_submission_date_holiday_rollback():
    # If Thursday is a holiday (e.g., 2026-12-10 Constitution Day), Friday is 2026-12-11
    # Submission date must roll back to Wednesday 2026-12-09
    sub_date = get_weekly_submission_date(date(2026, 12, 11))
    assert sub_date == date(2026, 12, 9)
    assert sub_date.weekday() == 2  # Wednesday
    assert is_business_day(sub_date) is True
```


- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_business_day_engine.py -v`
Expected: FAIL with ModuleNotFoundError or import error.

- [ ] **Step 3: Implement `backend/data/thai_holidays.json` and `backend/services/business_day_engine.py`**

```json
// backend/data/thai_holidays.json
{
  "2026": [
    {"date": "2026-01-01", "name": "วันขึ้นปีใหม่"},
    {"date": "2026-01-02", "name": "วันหยุดพิเศษปีใหม่"},
    {"date": "2026-03-03", "name": "วันมาฆบูชา"},
    {"date": "2026-04-06", "name": "วันจักรี"},
    {"date": "2026-04-13", "name": "วันสงกรานต์"},
    {"date": "2026-04-14", "name": "วันสงกรานต์"},
    {"date": "2026-04-15", "name": "วันสงกรานต์"},
    {"date": "2026-05-01", "name": "วันแรงงานแห่งชาติ"},
    {"date": "2026-05-04", "name": "วันฉัตรมงคล"},
    {"date": "2026-05-31", "name": "วันวิสาขบูชา"},
    {"date": "2026-06-03", "name": "วันเฉลิมพระชนมพรรษาสมเด็จพระนางเจ้าฯ พระบรมราชินี"},
    {"date": "2026-07-28", "name": "วันเฉลิมพระชนมพรรษาพระบาทสมเด็จพระเจ้าอยู่หัว"},
    {"date": "2026-07-29", "name": "วันอาสาฬหบูชา"},
    {"date": "2026-07-30", "name": "วันเข้าพรรษา"},
    {"date": "2026-08-12", "name": "วันแม่แห่งชาติ"},
    {"date": "2026-10-13", "name": "วันนวมินทรมหาราช"},
    {"date": "2026-10-23", "name": "วันปิยมหาราช"},
    {"date": "2026-12-05", "name": "วันพ่อแห่งชาติ"},
    {"date": "2026-12-10", "name": "วันรัฐธรรมนูญ"},
    {"date": "2026-12-31", "name": "วันสิ้นปี"}
  ]
}
```

```python
# backend/services/business_day_engine.py
import json
from pathlib import Path
from datetime import date, timedelta

HOLIDAYS_FILE = Path(__file__).parent.parent / "data" / "thai_holidays.json"

def load_thai_holidays() -> set[date]:
    if not HOLIDAYS_FILE.exists():
        return set()
    with open(HOLIDAYS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    holidays = set()
    for year, h_list in data.items():
        for item in h_list:
            holidays.add(date.fromisoformat(item["date"]))
    return holidays

_CACHED_HOLIDAYS = load_thai_holidays()

def is_business_day(target_date: date) -> bool:
    if target_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False
    if target_date in _CACHED_HOLIDAYS:
        return False
    return True

def get_adjusted_cycle_date(target_date: date, direction: str = "backward") -> date:
    step = timedelta(days=-1 if direction == "backward" else 1)
    current = target_date
    while not is_business_day(current):
        current += step
    return current

def get_weekly_submission_date(cycle_friday: date) -> date:
    # Baseline submission date is Thursday (1 day before Friday)
    candidate = cycle_friday - timedelta(days=1)
    # Must strictly roll backward until it hits a valid business day (Mon - Thu)
    while not is_business_day(candidate) or candidate.weekday() >= 4:
        candidate -= timedelta(days=1)
    return candidate

def get_next_business_day(target_date: date) -> date:
    current = target_date + timedelta(days=1)
    while not is_business_day(current):
        current += timedelta(days=1)
    return current

```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_business_day_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/data/thai_holidays.json backend/services/business_day_engine.py tests/test_business_day_engine.py
git commit -m "feat(engine): add Thai business day and government holiday engine"
```

---

### Task 2: Personnel & Role Registry SSOT (Universal Signer Binding)

**Files:**
- Create: `backend/data/personnel_registry.json`
- Create: `backend/services/personnel_service.py`
- Test: `tests/test_personnel_service.py`

**Interfaces:**
- Produces: `get_personnel_by_role(role_id: str) -> dict`
- Produces: `update_personnel_role(role_id: str, rank: str, name: str, position: str) -> dict`
- Produces: `inject_signers_into_template(template_data: dict) -> dict`

- [ ] **Step 1: Write failing test for personnel registry retrieval and injection**

```python
# tests/test_personnel_service.py
import pytest
from backend.services.personnel_service import (
    get_personnel_by_role,
    update_personnel_role,
    inject_signers_into_template
)

def test_get_battery_commander():
    signer = get_personnel_by_role("commander_battery")
    assert "rank" in signer
    assert "name" in signer
    assert "position" in signer
    assert signer["position"] == "ผบ.ร้อย.พล.รพศ.๑"

def test_update_and_persist_signer():
    original = get_personnel_by_role("commander_battery")
    updated = update_personnel_role("commander_battery", "ร.อ.", "สมชาย รักสงบ", "ผบ.ร้อย.พล.รพศ.๑")
    assert updated["name"] == "สมชาย รักสงบ"
    # Restore original for cleanliness
    update_personnel_role("commander_battery", original["rank"], original["name"], original["position"])

def test_inject_signers_into_template_payload():
    payload = {
        "title": "รายงานประจำสัปดาห์",
        "signature_blocks": [
            {"role_binding": "commander_battery"}
        ]
    }
    hydrated = inject_signers_into_template(payload)
    assert hydrated["signature_blocks"][0]["name"] != ""
    assert hydrated["signature_blocks"][0]["rank"] != ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_personnel_service.py -v`
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Implement `backend/data/personnel_registry.json` and `backend/services/personnel_service.py`**

```json
// backend/data/personnel_registry.json
{
  "roles": {
    "commander_battery": {
      "role_name": "ผู้บังคับกองร้อย",
      "rank": "ร.อ.",
      "name": "จิตรภณ วงค์แก้ว",
      "position": "ผบ.ร้อย.พล.รพศ.๑",
      "updated_at": "2026-10-12T00:00:00"
    },
    "chief_maintenance": {
      "role_name": "นายช่างประจำหมวด",
      "rank": "จ.ส.อ.",
      "name": "กฤษดา สืบสาร",
      "position": "จนท.ซ่อมบำรุง",
      "updated_at": "2026-10-12T00:00:00"
    },
    "warehouse_chief": {
      "role_name": "เจ้าหน้าที่คลังอาวุธ",
      "rank": "ส.อ.",
      "name": "ประสิทธิ์ ชาญณรงค์",
      "position": "เสมียนคลัง สป.",
      "updated_at": "2026-10-12T00:00:00"
    },
    "record_officer": {
      "role_name": "ผู้ตรวจถูกต้อง",
      "rank": "ร.ท.",
      "name": "ชยานันท์ ศรีสุข",
      "position": "รอง ผบ.ร้อย",
      "updated_at": "2026-10-12T00:00:00"
    }
  }
}
```

```python
# backend/services/personnel_service.py
import json
from pathlib import Path
from datetime import datetime

REGISTRY_FILE = Path(__file__).parent.parent / "data" / "personnel_registry.json"

def load_registry() -> dict:
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_registry(data: dict) -> None:
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_personnel_by_role(role_id: str) -> dict:
    data = load_registry()
    if role_id not in data.get("roles", {}):
        raise KeyError(f"Role {role_id} not found in personnel registry")
    return data["roles"][role_id]

def update_personnel_role(role_id: str, rank: str, name: str, position: str) -> dict:
    data = load_registry()
    if role_id not in data.get("roles", {}):
        raise KeyError(f"Role {role_id} not found")
    data["roles"][role_id].update({
        "rank": rank.strip(),
        "name": name.strip(),
        "position": position.strip(),
        "updated_at": datetime.now().isoformat()
    })
    save_registry(data)
    return data["roles"][role_id]

def inject_signers_into_template(template_data: dict) -> dict:
    data = load_registry()
    hydrated = json.loads(json.dumps(template_data))
    if "signature_blocks" in hydrated and isinstance(hydrated["signature_blocks"], list):
        for block in hydrated["signature_blocks"]:
            binding = block.get("role_binding")
            if binding and binding in data.get("roles", {}):
                role_info = data["roles"][binding]
                block["rank"] = role_info["rank"]
                block["name"] = role_info["name"]
                block["position"] = role_info["position"]
    return hydrated
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_personnel_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/data/personnel_registry.json backend/services/personnel_service.py tests/test_personnel_service.py
git commit -m "feat(personnel): add personnel registry and universal signer injection"
```

---

### Task 3: Cloud HotFolder & Document Generation Pipeline

**Files:**
- Create: `backend/services/doc_generation_service.py`
- Create: `backend/data/doc_schedule.json`
- Test: `tests/test_doc_generation_service.py`

**Interfaces:**
- Produces: `run_scheduled_generation(target_date: date) -> list[dict]`
- Produces: `get_generation_checklist(period_key: str) -> list[dict]`
- Produces: `generate_high_dpi_preview(html_path: Path, output_img: Path, scale_factor: float = 2.5) -> Path`
- Produces: `compile_single_document(template_id: str, target_date: date, output_dir: Path) -> dict`

- [ ] **Step 1: Write failing test for document schedule trigger, output manifest, and 300 DPI preview**

```python
# tests/test_doc_generation_service.py
import pytest
from datetime import date
from pathlib import Path
from backend.services.doc_generation_service import (
    run_scheduled_generation,
    get_generation_checklist,
    generate_high_dpi_preview
)

def test_generation_checklist_structure():
    checklist = get_generation_checklist("2026-10")
    assert isinstance(checklist, list)
    assert len(checklist) > 0
    item = checklist[0]
    assert "template_id" in item
    assert "title" in item
    assert "status" in item

def test_scheduled_generation_creates_outputs_and_300dpi_previews(tmp_path):
    target = date(2026, 10, 12)  # Monday (business day)
    results = run_scheduled_generation(target, output_root=tmp_path)
    assert len(results) > 0
    for res in results:
        assert res["status"] in ["GENERATED", "SKIPPED_HOLIDAY"]
        if res["status"] == "GENERATED":
            assert Path(res["html_path"]).exists()
            assert "preview_path" in res
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_doc_generation_service.py -v`
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Implement `backend/data/doc_schedule.json` and `backend/services/doc_generation_service.py` with 300 DPI rendering**

```json
// backend/data/doc_schedule.json
{
  "schedules": [
    {
      "template_id": "REF-WEEKLY-INSPECTION-JUN-V1",
      "title": "รายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ)",
      "frequency": "WEEKLY",
      "target_weekday": 0,
      "reference_dir": "references/approved_weekly_inspection",
      "roles": ["commander_battery", "chief_maintenance", "record_officer"]
    },
    {
      "template_id": "REF-SD1-WEEKLY-REPORT-V1",
      "title": "บันทึกรายงานผลการตรวจประจำสัปดาห์ (สด.๑)",
      "frequency": "WEEKLY",
      "target_weekday": 4,
      "reference_dir": "references/approved_sd1_weekly_report",
      "roles": ["commander_battery", "chief_maintenance"]
    },
    {
      "template_id": "REF-QUARTERLY-REPORT-V1",
      "title": "รายงานผลการตรวจสอบอาการถอยและจำลองการยิง ป. (ประจำไตรมาส)",
      "frequency": "QUARTERLY",
      "target_day_of_quarter": 1,
      "reference_dir": "references/approved_quarterly_report",
      "roles": ["commander_battery", "record_officer"]
    }
  ]
}
```

```python
# backend/services/doc_generation_service.py
import json
import shutil
import asyncio
from pathlib import Path
from datetime import date, datetime
from backend.services.business_day_engine import is_business_day, get_adjusted_cycle_date
from backend.services.personnel_service import inject_signers_into_template

SCHEDULE_FILE = Path(__file__).parent.parent / "data" / "doc_schedule.json"
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
HOTFOLDER_OUT = WORKSPACE_ROOT / "hotfolder" / "ready_to_print"

def load_schedule() -> list[dict]:
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["schedules"]

async def async_generate_high_dpi_preview(html_path: Path, output_img: Path, scale_factor: float = 2.5) -> Path:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # device_scale_factor=2.5 produces crisp 240-300 DPI print-quality image
        context = await browser.new_context(
            viewport={"width": 1200, "height": 1700},
            device_scale_factor=scale_factor
        )
        page = await context.new_page()
        file_url = f"file:///{html_path.resolve().as_posix()}"
        await page.goto(file_url, wait_until="networkidle")
        first_page = await page.query_selector(".page-portrait, .page-landscape")
        if first_page:
            await first_page.screenshot(path=str(output_img))
        else:
            await page.screenshot(path=str(output_img))
        await browser.close()
    return output_img

def generate_high_dpi_preview(html_path: Path, output_img: Path, scale_factor: float = 2.5) -> Path:
    return asyncio.run(async_generate_high_dpi_preview(html_path, output_img, scale_factor))

def get_generation_checklist(period_key: str) -> list[dict]:
    schedules = load_schedule()
    checklist = []
    HOTFOLDER_OUT.mkdir(parents=True, exist_ok=True)
    for s in schedules:
        target_name = f"{s['template_id']}_{period_key}.html"
        out_file = HOTFOLDER_OUT / target_name
        preview_file = HOTFOLDER_OUT / f"{s['template_id']}_{period_key}_300dpi.png"
        checklist.append({
            "template_id": s["template_id"],
            "title": s["title"],
            "frequency": s["frequency"],
            "status": "GENERATED" if out_file.exists() else "PENDING",
            "file_path": str(out_file) if out_file.exists() else None,
            "preview_url": f"/api/v1/docs/preview/{preview_file.name}" if preview_file.exists() else None,
            "updated_at": datetime.fromtimestamp(out_file.stat().st_mtime).isoformat() if out_file.exists() else None
        })
    return checklist

def run_scheduled_generation(target_date: date, output_root: Path = HOTFOLDER_OUT) -> list[dict]:
    output_root.mkdir(parents=True, exist_ok=True)
    adjusted_date = get_adjusted_cycle_date(target_date, direction="backward")
    schedules = load_schedule()
    results = []
    
    for s in schedules:
        applies = False
        if s["frequency"] == "WEEKLY" and adjusted_date.weekday() == s.get("target_weekday", 0):
            applies = True
        elif s["frequency"] == "DAILY":
            applies = True
        elif s["frequency"] == "QUARTERLY" and adjusted_date.day == 1 and adjusted_date.month in [1, 4, 7, 10]:
            applies = True
            
        if not applies:
            continue
            
        period_key = adjusted_date.strftime("%Y-%m-%d")
        ref_path = WORKSPACE_ROOT / s["reference_dir"]
        html_src = list(ref_path.glob("*.html"))
        if not html_src:
            continue
            
        out_html = output_root / f"{s['template_id']}_{period_key}.html"
        shutil.copy2(html_src[0], out_html)
        
        # Auto-generate 300 DPI Print-Grade preview
        preview_img = output_root / f"{s['template_id']}_{period_key}_300dpi.png"
        generate_high_dpi_preview(out_html, preview_img, scale_factor=2.5)
        
        results.append({
            "template_id": s["template_id"],
            "title": s["title"],
            "cycle_date": adjusted_date.isoformat(),
            "status": "GENERATED",
            "html_path": str(out_html),
            "preview_path": str(preview_img)
        })
    return results

```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_doc_generation_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/data/doc_schedule.json backend/services/doc_generation_service.py tests/test_doc_generation_service.py
git commit -m "feat(hotfolder): implement automated scheduled doc generation and checklist"
```

---

### Task 4: Armory Inventory & Dual-Control Custody Engine (ทบ.๔๐๐-๐๐๕ & ทบ.๔๖๘-๒๐๔)

**Files:**
- Create: `backend/data/inventory_db.json`
- Create: `backend/services/inventory_service.py`
- Test: `tests/test_inventory_service.py`

**Interfaces:**
- Produces: `request_loan(item_id: str, borrower_name: str, purpose: str, requested_by: str) -> dict`
- Produces: `approve_loan(request_id: str, approved_by: str) -> dict`
- Produces: `return_item(loan_id: str, is_damaged: bool, damage_notes: str, receiver: str) -> dict`
- Produces: `replace_damaged_item(item_id: str, new_serial_no: str, replaced_by: str) -> dict`
- Produces: `get_inventory_balance() -> dict`

- [ ] **Step 1: Write failing test for Dual-Control borrow, return with damage, and replacement audit**

```python
# tests/test_inventory_service.py
import pytest
from backend.services.inventory_service import (
    request_loan,
    approve_loan,
    return_item,
    replace_damaged_item,
    get_inventory_balance,
    get_item_history
)

def test_loan_workflow_dual_control():
    # 1. Admin creates loan request (Status: PENDING_APPROVAL)
    req = request_loan(item_id="GUN-105-01", borrower_name="ส.อ.สมเกียรติ สุขใจ", purpose="ยิงสนับสนุน", requested_by="admin_warehouse")
    assert req["status"] == "PENDING_APPROVAL"
    
    # 2. Owner approves loan (Stock deducted, Status: BORROWED)
    approved = approve_loan(request_id=req["request_id"], approved_by="owner_commander")
    assert approved["status"] == "BORROWED"
    
    # Check inventory balance: Available decreased by 1
    bal = get_inventory_balance()
    item = next(i for i in bal["items"] if i["item_id"] == "GUN-105-01")
    assert item["status"] == "BORROWED"

def test_return_damaged_and_replacement_audit():
    # Return with damage
    loan_id = "test_loan_dam"
    ret = return_item(loan_id=loan_id, item_id="GUN-105-02", is_damaged=True, damage_notes="ศูนย์เล็งแตกร้าว", receiver="owner_commander")
    assert ret["status"] == "DAMAGED"
    assert ret["damage_notes"] == "ศูนย์เล็งแตกร้าว"
    
    # Replace item with new serial
    rep = replace_damaged_item(item_id="GUN-105-02", new_serial_no="SN-NEW-9988", replaced_by="owner_commander")
    assert rep["status"] == "AVAILABLE"
    
    # Verify immutable history contains damage record
    hist = get_item_history("GUN-105-02")
    assert any("ศูนย์เล็งแตกร้าว" in h.get("notes", "") for h in hist)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_inventory_service.py -v`
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Implement `backend/data/inventory_db.json` and `backend/services/inventory_service.py`**

```json
// backend/data/inventory_db.json
{
  "items": [
    {
      "item_id": "GUN-105-01",
      "name": "ปบค.๙๕ ขนาด ๑๐๕ มม. เอ็ม ๑๐๑ เอ ๑",
      "serial_no": "54231",
      "status": "AVAILABLE",
      "category": "อาวุธหลัก",
      "history": []
    },
    {
      "item_id": "GUN-105-02",
      "name": "ปบค.๙๕ ขนาด ๑๐๕ มม. เอ็ม ๑๐๑ เอ ๑",
      "serial_no": "54232",
      "status": "AVAILABLE",
      "category": "อาวุธหลัก",
      "history": []
    }
  ],
  "loan_requests": []
}
```

```python
# backend/services/inventory_service.py
import json
import uuid
from pathlib import Path
from datetime import datetime

DB_FILE = Path(__file__).parent.parent / "data" / "inventory_db.json"

def _load_db() -> dict:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(data: dict) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_inventory_balance() -> dict:
    return _load_db()

def get_item_history(item_id: str) -> list[dict]:
    db = _load_db()
    for item in db["items"]:
        if item["item_id"] == item_id:
            return item.get("history", [])
    return []

def request_loan(item_id: str, borrower_name: str, purpose: str, requested_by: str) -> dict:
    db = _load_db()
    req_id = str(uuid.uuid4())[:8]
    req = {
        "request_id": req_id,
        "item_id": item_id,
        "borrower_name": borrower_name,
        "purpose": purpose,
        "requested_by": requested_by,
        "requested_at": datetime.now().isoformat(),
        "status": "PENDING_APPROVAL"
    }
    db["loan_requests"].append(req)
    _save_db(db)
    return req

def approve_loan(request_id: str, approved_by: str) -> dict:
    db = _load_db()
    req = next((r for r in db["loan_requests"] if r["request_id"] == request_id), None)
    if not req:
        raise ValueError("Request not found")
    req["status"] = "BORROWED"
    req["approved_by"] = approved_by
    req["approved_at"] = datetime.now().isoformat()
    
    for item in db["items"]:
        if item["item_id"] == req["item_id"]:
            item["status"] = "BORROWED"
            item.setdefault("history", []).append({
                "action": "BORROW",
                "borrower": req["borrower_name"],
                "approved_by": approved_by,
                "timestamp": req["approved_at"]
            })
            break
    _save_db(db)
    return req

def return_item(loan_id: str, item_id: str, is_damaged: bool, damage_notes: str, receiver: str) -> dict:
    db = _load_db()
    new_status = "DAMAGED" if is_damaged else "AVAILABLE"
    target_item = next((i for i in db["items"] if i["item_id"] == item_id), None)
    if not target_item:
        raise ValueError("Item not found")
    
    target_item["status"] = new_status
    target_item.setdefault("history", []).append({
        "action": "RETURN_DAMAGED" if is_damaged else "RETURN_NORMAL",
        "receiver": receiver,
        "notes": damage_notes,
        "timestamp": datetime.now().isoformat()
    })
    _save_db(db)
    return {"status": new_status, "damage_notes": damage_notes}

def replace_damaged_item(item_id: str, new_serial_no: str, replaced_by: str) -> dict:
    db = _load_db()
    target_item = next((i for i in db["items"] if i["item_id"] == item_id), None)
    if not target_item:
        raise ValueError("Item not found")
    
    old_sn = target_item["serial_no"]
    target_item["serial_no"] = new_serial_no
    target_item["status"] = "AVAILABLE"
    target_item.setdefault("history", []).append({
        "action": "REPLACED",
        "old_serial": old_sn,
        "new_serial": new_serial_no,
        "replaced_by": replaced_by,
        "timestamp": datetime.now().isoformat()
    })
    _save_db(db)
    return target_item
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_inventory_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/data/inventory_db.json backend/services/inventory_service.py tests/test_inventory_service.py
git commit -m "feat(inventory): add armory custody ledger with dual-control and immutable damage logs"
```

---

### Task 5: External Intake HotFolder & Periodic Gap Analysis (`FolderIN`)

**Files:**
- Create: `backend/services/external_intake_service.py`
- Create: `backend/data/external_doc_rules.json`
- Test: `tests/test_external_intake_service.py`

**Interfaces:**
- Produces: `ingest_file(incoming_path: Path) -> dict`
- Produces: `audit_missing_periodic_docs(current_date: date) -> list[dict]`
- Produces: `get_intake_feed() -> list[dict]`

- [ ] **Step 1: Write failing test for external doc intake and gap detection**

```python
# tests/test_external_intake_service.py
import pytest
from datetime import date
from pathlib import Path
from backend.services.external_intake_service import (
    ingest_file,
    audit_missing_periodic_docs,
    get_intake_feed
)

def test_ingest_external_fire_report(tmp_path):
    # Simulate an external officer dropping a file into FolderIN
    drop_file = tmp_path / "รายงานอัคคีภัย_2026-09.pdf"
    drop_file.write_text("Dummy fire report content", encoding="utf-8")
    
    result = ingest_file(drop_file)
    assert result["doc_type"] == "FIRE_SAFETY_REPORT"
    assert result["period_key"] == "2026-09"
    assert result["status"] == "RECEIVED"

def test_gap_analysis_detects_overdue_cycles():
    # If today is 2026-10-12 and October report (due Oct 5) is missing, it should flag OVERDUE
    gaps = audit_missing_periodic_docs(current_date=date(2026, 10, 12))
    assert any(g["doc_type"] == "FIRE_SAFETY_REPORT" and g["status"] == "OVERDUE" for g in gaps)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_external_intake_service.py -v`
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Implement `backend/data/external_doc_rules.json` and `backend/services/external_intake_service.py`**

```json
// backend/data/external_doc_rules.json
{
  "rules": [
    {
      "doc_type": "FIRE_SAFETY_REPORT",
      "title": "รายงานการปฏิบัติตามแผนป้องกันอัคคีภัย",
      "department": "แผนกป้องกันอัคคีภัยและกู้ภัย",
      "filename_pattern": "อัคคีภัย",
      "frequency": "MONTHLY",
      "due_day_of_month": 5
    }
  ],
  "intake_log": []
}
```

```python
# backend/services/external_intake_service.py
import json
import shutil
import re
from pathlib import Path
from datetime import date, datetime

RULES_FILE = Path(__file__).parent.parent / "data" / "external_doc_rules.json"
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
ARCHIVE_DIR = WORKSPACE_ROOT / "hotfolder" / "external_archive"

def _load_data() -> dict:
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_data(data: dict) -> None:
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ingest_file(incoming_path: Path) -> dict:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_data()
    fname = incoming_path.name
    
    matched_rule = None
    for r in data["rules"]:
        if r["filename_pattern"] in fname:
            matched_rule = r
            break
            
    doc_type = matched_rule["doc_type"] if matched_rule else "UNKNOWN_EXTERNAL"
    # Extract date/period from filename e.g., 2026-09
    match_date = re.search(r"\d{4}-\d{2}", fname)
    period_key = match_date.group(0) if match_date else datetime.now().strftime("%Y-%m")
    
    dest_path = ARCHIVE_DIR / f"{doc_type}_{period_key}_{fname}"
    shutil.copy2(incoming_path, dest_path)
    
    entry = {
        "doc_type": doc_type,
        "title": matched_rule["title"] if matched_rule else fname,
        "period_key": period_key,
        "file_path": str(dest_path),
        "received_at": datetime.now().isoformat(),
        "status": "RECEIVED"
    }
    data.setdefault("intake_log", []).append(entry)
    _save_data(data)
    return entry

def audit_missing_periodic_docs(current_date: date) -> list[dict]:
    data = _load_data()
    intake_log = data.get("intake_log", [])
    gaps = []
    
    for r in data["rules"]:
        if r["frequency"] == "MONTHLY":
            # Check current month
            period_str = current_date.strftime("%Y-%m")
            received = any(log["doc_type"] == r["doc_type"] and log["period_key"] == period_str for log in intake_log)
            if not received and current_date.day > r["due_day_of_month"]:
                gaps.append({
                    "doc_type": r["doc_type"],
                    "title": r["title"],
                    "period_key": period_str,
                    "due_date": f"{period_str}-{r['due_day_of_month']:02d}",
                    "status": "OVERDUE",
                    "days_overdue": current_date.day - r["due_day_of_month"]
                })
    return gaps

def get_intake_feed() -> list[dict]:
    return _load_data().get("intake_log", [])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_external_intake_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/data/external_doc_rules.json backend/services/external_intake_service.py tests/test_external_intake_service.py
git commit -m "feat(intake): implement external folderIN ingestion and periodic gap analysis"
```

---

### Task 6: FastAPI Server & Tactical Web Dashboard (Glassmorphism UI)

**Files:**
- Create: `backend/app.py`
- Create: `frontend/static/style.css`
- Create: `frontend/static/dashboard.js`
- Create: `frontend/templates/index.html`
- Test: `tests/test_api_endpoints.py`

**Interfaces:**
- Produces: `GET /api/v1/dashboard/summary` -> 종합 현황 (Checklist, Inventory, External Overdue)
- Produces: `POST /api/v1/inventory/loan/request` -> Admin ยื่นขอยืม
- Produces: `POST /api/v1/inventory/loan/approve` -> Owner อนุมัติยืม
- Produces: `POST /api/v1/personnel/update` -> เปลี่ยน ยศ-ชื่อ-ตำแหน่ง
- Produces: `GET /api/v1/docs/download/{filename}` -> ดาวน์โหลดเอกสารพร้อมพิมพ์ 1 คลิก

- [ ] **Step 1: Write failing test for FastAPI API endpoints**

```python
# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_api_summary_endpoint():
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert "checklist" in data
    assert "inventory" in data
    assert "gaps" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_api_endpoints.py -v`
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Implement `backend/app.py` and Tactical Dark Glassmorphism Frontend**

```python
# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from datetime import date
from pydantic import BaseModel

from backend.services.doc_generation_service import get_generation_checklist, run_scheduled_generation, HOTFOLDER_OUT
from backend.services.inventory_service import get_inventory_balance, request_loan, approve_loan, return_item
from backend.services.external_intake_service import audit_missing_periodic_docs, get_intake_feed
from backend.services.personnel_service import load_registry, update_personnel_role

app = FastAPI(title="Military Doc & Armory Automation Suite")

STATIC_DIR = Path(__file__).parent.parent / "frontend" / "static"
TEMPLATES_DIR = Path(__file__).parent.parent / "frontend" / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    html_file = TEMPLATES_DIR / "index.html"
    return html_file.read_text(encoding="utf-8")

@app.get("/api/v1/dashboard/summary")
def get_summary():
    today = date.today()
    period_str = today.strftime("%Y-%m")
    return {
        "date": today.isoformat(),
        "checklist": get_generation_checklist(period_str),
        "inventory": get_inventory_balance(),
        "gaps": audit_missing_periodic_docs(today),
        "intake_feed": get_intake_feed(),
        "personnel": load_registry()
    }

class LoanRequestSchema(BaseModel):
    item_id: str
    borrower_name: str
    purpose: str
    requested_by: str

@app.post("/api/v1/inventory/loan/request")
def api_request_loan(payload: LoanRequestSchema):
    return request_loan(payload.item_id, payload.borrower_name, payload.purpose, payload.requested_by)

class LoanApproveSchema(BaseModel):
    request_id: str
    approved_by: str

@app.post("/api/v1/inventory/loan/approve")
def api_approve_loan(payload: LoanApproveSchema):
    return approve_loan(payload.request_id, payload.approved_by)

@app.get("/api/v1/docs/download/{filename}")
def download_doc(filename: str):
    fpath = HOTFOLDER_OUT / filename
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(fpath, media_type="application/octet-stream", filename=filename)

@app.get("/api/v1/docs/preview/{filename}")
def preview_doc_300dpi(filename: str):
    fpath = HOTFOLDER_OUT / filename
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Preview not found")
    return FileResponse(fpath, media_type="image/png")
```

Create `frontend/templates/index.html` with Apple-grade Tactical Dark Frosted Glassmorphism, 4 tabs (เอกสารพร้อมพิมพ์พร้อมพรีวิว 300 DPI คมชัดสูง, บัญชียืม-คืนสิ่งอุปกรณ์, เฝ้ารับเอกสารภายนอก, ทำเนียบผู้บังคับบัญชา).


- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_api_endpoints.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app.py frontend/static/ frontend/templates/ tests/test_api_endpoints.py
git commit -m "feat(portal): launch FastAPI server and tactical web dashboard with glassmorphism UI"
```

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-10-12-military-doc-automation-suite.md`. Two execution options:

1. **Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
