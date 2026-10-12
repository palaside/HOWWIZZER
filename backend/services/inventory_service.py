import json
import uuid
from pathlib import Path
from datetime import datetime

DB_FILE = Path(__file__).parent.parent / "data" / "inventory_db.json"

def _load_db() -> dict:
    if not DB_FILE.exists():
        return {"items": [], "loan_requests": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(data: dict) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def request_loan(item_id: str, borrower_name: str, purpose: str, requested_by: str) -> dict:
    """Maker step: Admin creates loan request with status PENDING_APPROVAL."""
    data = _load_db()
    item = next((i for i in data["items"] if i["item_id"] == item_id), None)
    if not item:
        raise KeyError(f"Item {item_id} not found in inventory")
    if item["status"] != "AVAILABLE":
        raise ValueError(f"Item {item_id} is not currently AVAILABLE (status: {item['status']})")
        
    req_id = f"LOAN-{uuid.uuid4().hex[:8].upper()}"
    new_req = {
        "request_id": req_id,
        "item_id": item_id,
        "borrower_name": borrower_name,
        "purpose": purpose,
        "requested_by": requested_by,
        "requested_at": datetime.now().isoformat(),
        "status": "PENDING_APPROVAL",
        "approved_by": None,
        "approved_at": None
    }
    data["loan_requests"].append(new_req)
    _save_db(data)
    return new_req

def approve_loan(request_id: str, approved_by: str) -> dict:
    """Checker step: Custodian/Owner approves loan request, updates item status to BORROWED."""
    data = _load_db()
    req = next((r for r in data["loan_requests"] if r["request_id"] == request_id), None)
    if not req:
        raise KeyError(f"Loan request {request_id} not found")
        
    req["status"] = "BORROWED"
    req["approved_by"] = approved_by
    req["approved_at"] = datetime.now().isoformat()
    
    # Update item status and append immutable audit log
    item = next((i for i in data["items"] if i["item_id"] == req["item_id"]), None)
    if item:
        item["status"] = "BORROWED"
        item["history"].append({
            "action": "LOAN_APPROVED",
            "request_id": request_id,
            "borrower": req["borrower_name"],
            "by": approved_by,
            "timestamp": datetime.now().isoformat(),
            "notes": f"อนุมัติการยืม: {req['purpose']}"
        })
    _save_db(data)
    return req

def return_item(loan_id: str, item_id: str, is_damaged: bool = False, damage_notes: str = "", receiver: str = "") -> dict:
    """Returns an item. If damaged, sets status to DAMAGED and records damage details."""
    data = _load_db()
    item = next((i for i in data["items"] if i["item_id"] == item_id), None)
    if not item:
        raise KeyError(f"Item {item_id} not found")
        
    new_status = "DAMAGED" if is_damaged else "AVAILABLE"
    item["status"] = new_status
    item["history"].append({
        "action": "ITEM_RETURNED",
        "loan_id": loan_id,
        "is_damaged": is_damaged,
        "damage_notes": damage_notes,
        "receiver": receiver,
        "timestamp": datetime.now().isoformat(),
        "notes": f"รับคืนสิ่งอุปกรณ์: {damage_notes if is_damaged else 'สภาพสมบูรณ์'}"
    })
    _save_db(data)
    return {
        "item_id": item_id,
        "status": new_status,
        "damage_notes": damage_notes,
        "receiver": receiver,
        "returned_at": datetime.now().isoformat()
    }

def replace_damaged_item(item_id: str, new_serial_no: str, replaced_by: str) -> dict:
    """Replaces damaged serial number with replacement stock and records immutable history."""
    data = _load_db()
    item = next((i for i in data["items"] if i["item_id"] == item_id), None)
    if not item:
        raise KeyError(f"Item {item_id} not found")
        
    old_serial = item["serial_no"]
    item["serial_no"] = new_serial_no
    item["status"] = "AVAILABLE"
    item["history"].append({
        "action": "ITEM_REPLACED",
        "old_serial_no": old_serial,
        "new_serial_no": new_serial_no,
        "replaced_by": replaced_by,
        "timestamp": datetime.now().isoformat(),
        "notes": f"เปลี่ยนทดแทนหมายเลขยุทโธปกรณ์: เดิม {old_serial} เป็น {new_serial_no}"
    })
    _save_db(data)
    return item

def get_inventory_balance() -> dict:
    """Returns inventory items and calculated summary for document template data injection."""
    data = _load_db()
    items = data.get("items", [])
    
    summary = {}
    for it in items:
        m_key = it.get("model_key", "DEFAULT")
        if m_key not in summary:
            summary[m_key] = {"total": 0, "received": 0, "issued": 0, "balance": 0}
        summary[m_key]["total"] += 1
        summary[m_key]["received"] += 1
        if it["status"] == "BORROWED":
            summary[m_key]["issued"] += 1
        else:
            summary[m_key]["balance"] += 1
            
    return {
        "items": items,
        "summary": summary
    }

def get_item_history(item_id: str) -> list[dict]:
    """Retrieves immutable audit trail for an equipment item."""
    data = _load_db()
    item = next((i for i in data["items"] if i["item_id"] == item_id), None)
    if not item:
        raise KeyError(f"Item {item_id} not found")
    return item.get("history", [])
