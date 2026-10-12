import os
from pathlib import Path
from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from backend.services.personnel_service import (
    load_registry,
    update_personnel_role
)
from backend.services.doc_generation_service import (
    get_generation_checklist,
    run_scheduled_generation,
    HOTFOLDER_OUT
)
from backend.services.inventory_service import (
    get_inventory_balance,
    request_loan,
    approve_loan,
    return_item,
    replace_damaged_item,
    get_item_history
)
from backend.services.business_day_engine import (
    get_weekly_cycle_range
)
from backend.services.external_intake_service import (
    scan_and_ingest_hotfolder,
    classify_external_doc,
    check_external_cadence_gaps,
    HOTFOLDER_IN
)

WORKSPACE_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = WORKSPACE_ROOT / "frontend"

app = FastAPI(
    title="Military Document & Tactical HotFolder Management System",
    description="ระบบบริหารจัดการและจัดทำเอกสารราชการทหารอัตโนมัติ (ทบ. ๒๕๖๓)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Hotfolder asset mounts
HOTFOLDER_OUT.mkdir(parents=True, exist_ok=True)
HOTFOLDER_IN.mkdir(parents=True, exist_ok=True)
(FRONTEND_DIR / "static").mkdir(parents=True, exist_ok=True)
(FRONTEND_DIR / "templates").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
app.mount("/hotfolder/ready", StaticFiles(directory=str(HOTFOLDER_OUT)), name="hotfolder_ready")

# --- System Health ---
@app.get("/api/v1/health")
def health():
    return {
        "status": "HEALTHY",
        "timestamp": datetime.now().isoformat(),
        "hotfolder_ready": str(HOTFOLDER_OUT),
        "hotfolder_in": str(HOTFOLDER_IN)
    }

# --- Personnel & Signer Registry ---
@app.get("/api/v1/personnel")
def get_personnel():
    return load_registry()

@app.get("/api/v1/personnel/operators")
def list_operators():
    from backend.services.personnel_service import get_operators
    return get_operators()

@app.put("/api/v1/personnel/operators/{slot}")
def edit_operator(slot: int, payload: dict = Body(...)):
    from backend.services.personnel_service import update_operator
    try:
        return update_operator(
            slot=slot,
            rank=payload.get("rank", ""),
            name=payload.get("name", ""),
            position=payload.get("position", ""),
            gun_serial=payload.get("gun_serial", "")
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/api/v1/personnel/{role_id}")
def update_personnel(role_id: str, payload: dict = Body(...)):
    try:
        updated = update_personnel_role(
            role_id=role_id,
            rank=payload.get("rank", ""),
            name=payload.get("name", ""),
            position=payload.get("position", "")
        )
        return updated
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Document Production & HotFolder Engine ---
@app.get("/api/v1/docs/checklist")
def get_checklist(period_key: Optional[str] = None):
    p_key = period_key or datetime.now().strftime("%Y-%m")
    return get_generation_checklist(p_key)

@app.get("/api/v1/cycle/info")
def get_cycle_info(target_date: Optional[str] = None):
    from backend.services.business_day_engine import get_weekly_cycle_range
    if target_date:
        try:
            t_date = date.fromisoformat(target_date)
        except ValueError:
            t_date = date.today()
    else:
        t_date = date.today()
    return get_weekly_cycle_range(t_date)

@app.post("/api/v1/docs/generate")
def generate_docs(payload: dict = Body(...)):
    target_date_str = payload.get("target_date")
    if target_date_str:
        target = date.fromisoformat(target_date_str)
    else:
        target = date.today()
        
    results = run_scheduled_generation(target)
    return {
        "cycle_date": target.isoformat(),
        "count": len(results),
        "results": results
    }

@app.get("/api/v1/docs/preview/{filename}")
def get_doc_preview(filename: str):
    file_path = HOTFOLDER_OUT / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Preview file not found")
    return FileResponse(file_path)

# --- Weekly Cycle Engine ---
@app.get("/api/v1/cycle/info")
def get_cycle_info(target_date: Optional[str] = None):
    try:
        c_date = date.fromisoformat(target_date) if target_date else date.today()
        return get_weekly_cycle_range(c_date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Armory Custody & Inventory Engine ---
@app.get("/api/v1/inventory/balance")
def get_inventory():
    return get_inventory_balance()

@app.post("/api/v1/inventory/loan/request")
def make_loan_request(payload: dict = Body(...)):
    try:
        return request_loan(
            item_id=payload["item_id"],
            borrower_name=payload["borrower_name"],
            purpose=payload["purpose"],
            requested_by=payload["requested_by"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/inventory/loan/approve")
def approve_loan_request(payload: dict = Body(...)):
    try:
        return approve_loan(
            request_id=payload["request_id"],
            approved_by=payload["approved_by"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/inventory/item/return")
def return_inventory_item(payload: dict = Body(...)):
    try:
        return return_item(
            loan_id=payload.get("loan_id", ""),
            item_id=payload["item_id"],
            is_damaged=payload.get("is_damaged", False),
            damage_notes=payload.get("damage_notes", ""),
            receiver=payload.get("receiver", "")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/inventory/item/replace")
def replace_item(payload: dict = Body(...)):
    try:
        return replace_damaged_item(
            item_id=payload["item_id"],
            new_serial_no=payload["new_serial_no"],
            replaced_by=payload["replaced_by"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/inventory/item/{item_id}/history")
def get_history(item_id: str):
    try:
        return get_item_history(item_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- External Intake HotFolder & Cadence Gaps ---
@app.get("/api/v1/intake/scan")
def scan_intake():
    return scan_and_ingest_hotfolder()

@app.post("/api/v1/intake/classify")
def classify_intake(payload: dict = Body(...)):
    return classify_external_doc(
        filename=payload["filename"],
        doc_type=payload["doc_type"],
        period_key=payload["period_key"]
    )

@app.get("/api/v1/intake/gaps")
def get_gaps(current_date: Optional[str] = None):
    c_date = date.fromisoformat(current_date) if current_date else date.today()
    return check_external_cadence_gaps(c_date)

# --- Frontend Portal UI ---
@app.get("/", response_class=HTMLResponse)
def index():
    template_path = FRONTEND_DIR / "templates" / "index.html"
    if template_path.exists():
        return HTMLResponse(template_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Tactical Military Document Automation Suite</h1>")
