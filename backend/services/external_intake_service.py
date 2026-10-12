import json
import re
from pathlib import Path
from datetime import date, datetime

WORKSPACE_ROOT = Path(__file__).parent.parent.parent
RULES_FILE = Path(__file__).parent.parent / "data" / "external_doc_rules.json"
HOTFOLDER_IN = WORKSPACE_ROOT / "hotfolder" / "FolderIN"

def _load_rules_data() -> dict:
    if not RULES_FILE.exists():
        return {"rules": [], "ingested_records": []}
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_rules_data(data: dict) -> None:
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scan_and_ingest_hotfolder(folder_in: Path = HOTFOLDER_IN) -> list[dict]:
    """
    Scans FolderIN. Matches against regex patterns.
    Fallback (Requirement 4): If regex doesn't match, classifies as UNCLASSIFIED_EXTERNAL
    with ACTION_REQUIRED alert so admin can specify cadence in 1 click.
    """
    folder_in.mkdir(parents=True, exist_ok=True)
    data = _load_rules_data()
    rules = data.get("rules", [])
    
    results = []
    for file_path in folder_in.glob("*.*"):
        if file_path.is_dir() or file_path.name.startswith("."):
            continue
            
        matched_rule = None
        period_key = None
        for r in rules:
            m = re.search(r["pattern"], file_path.stem)
            if m:
                matched_rule = r
                period_key = m.group(1) if m.groups() else datetime.now().strftime("%Y-%m")
                break
                
        if matched_rule:
            rec = {
                "filename": file_path.name,
                "file_path": str(file_path),
                "doc_type": matched_rule["doc_type"],
                "title": matched_rule["title"],
                "period_key": period_key,
                "status": "INGESTED",
                "ingested_at": datetime.now().isoformat()
            }
        else:
            # Fallback for unclassified files
            rec = {
                "filename": file_path.name,
                "file_path": str(file_path),
                "doc_type": "UNCLASSIFIED_EXTERNAL",
                "title": "เอกสารภายนอกยังไม่ระบุประเภท",
                "period_key": "UNKNOWN",
                "status": "ACTION_REQUIRED",
                "alert": "ชื่อไฟล์ไม่ตรงรูปแบบมาตรฐาน ต้องการให้ระบุวงรอบด้วยตนเอง (คลิกเพื่อระบุ)",
                "ingested_at": datetime.now().isoformat()
            }
            
        # Update or record in database
        existing = next((x for x in data["ingested_records"] if x["filename"] == file_path.name), None)
        if existing:
            existing.update(rec)
        else:
            data["ingested_records"].append(rec)
            
        results.append(rec)
        
    _save_rules_data(data)
    return results

def classify_external_doc(filename: str, doc_type: str, period_key: str) -> dict:
    """1-Click admin fallback resolution to assign doc_type and cadence period."""
    data = _load_rules_data()
    rec = next((x for x in data["ingested_records"] if x["filename"] == filename), None)
    if not rec:
        rec = {
            "filename": filename,
            "file_path": str(HOTFOLDER_IN / filename),
            "ingested_at": datetime.now().isoformat()
        }
        data["ingested_records"].append(rec)
        
    rule = next((r for r in data["rules"] if r["doc_type"] == doc_type), None)
    title = rule["title"] if rule else doc_type
    
    rec.update({
        "doc_type": doc_type,
        "title": title,
        "period_key": period_key,
        "status": "CLASSIFIED",
        "classified_at": datetime.now().isoformat()
    })
    rec.pop("alert", None)
    _save_rules_data(data)
    return rec

def check_external_cadence_gaps(current_date: date) -> list[dict]:
    """Analyzes periodic cadence gaps and flags missing/overdue external reports."""
    data = _load_rules_data()
    rules = data.get("rules", [])
    ingested = data.get("ingested_records", [])
    
    gaps = []
    curr_month_str = current_date.strftime("%Y-%m")
    curr_quarter = (current_date.month - 1) // 3 + 1
    curr_quarter_str = f"{current_date.year}-Q{curr_quarter}"
    
    for r in rules:
        expected_period = curr_month_str if r["cadence"] == "MONTHLY" else curr_quarter_str
        has_record = any(
            x["doc_type"] == r["doc_type"] and x.get("period_key") == expected_period
            for x in ingested
        )
        
        deadline_day = r.get("deadline_day_of_month", 15)
        is_past_deadline = current_date.day > deadline_day
        
        status = "RECEIVED" if has_record else ("OVERDUE" if is_past_deadline else "PENDING")
        gaps.append({
            "doc_type": r["doc_type"],
            "title": r["title"],
            "cadence": r["cadence"],
            "expected_period": expected_period,
            "deadline_day": deadline_day,
            "status": status,
            "gap_alert": f"ขาดส่งรายงานรอบ {expected_period} เกินกำหนดแล้ว!" if status == "OVERDUE" else None
        })
    return gaps
