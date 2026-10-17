import os
from pathlib import Path
from datetime import date, datetime
from typing import Optional

# Added for performance enhancements
from fastapi.middleware.gzip import GZipMiddleware
from starlette.responses import Response

from fastapi import FastAPI, HTTPException, Body, UploadFile, File, Header, Depends, Form
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
AWAITING_RECORDS_FILE = WORKSPACE_ROOT / "backend" / "data" / "awaiting_service_records.json"
# Ensure the data directory exists
(AWAITING_RECORDS_FILE.parent).mkdir(parents=True, exist_ok=True)
# Initialise empty JSON array if file does not exist
if not AWAITING_RECORDS_FILE.exists():
    AWAITING_RECORDS_FILE.write_text("[]", encoding="utf-8")
FRONTEND_DIR = WORKSPACE_ROOT / "frontend"

app = FastAPI(
    title="Military Document & Tactical HotFolder Management System",
    description="ระบบบริหารจัดการและจัดทำเอกสารราชการทหารอัตโนมัติ (ทบ. ๒๕๖๓)",
    version="1.0.0"
)

# Enable GZip compression for responses larger than 500 bytes
app.add_middleware(GZipMiddleware, minimum_size=500)

# Simple Cache‑Control middleware (adds a short‑term public cache header)
@app.middleware("http")
async def add_cache_control(request, call_next):
    response: Response = await call_next(request)
    # Static assets can be cached for 1 hour; HTML for 5 minutes
    if request.url.path.startswith(('/static/', '/docs/', '/frontend/static/')):
        response.headers["Cache-Control"] = "public, max-age=3600"
    else:
        response.headers["Cache-Control"] = "public, max-age=300"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Hotfolder asset mounts
for d in [HOTFOLDER_OUT, HOTFOLDER_IN, FRONTEND_DIR / "static", FRONTEND_DIR / "templates"]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

if (FRONTEND_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
    app.mount("/frontend/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="frontend_static")

# Serve pre‑generated document HTML/CSS/images via a dedicated static route
if (WORKSPACE_ROOT / "static" / "docs").exists():
    app.mount(
        "/docs",
        StaticFiles(directory=str(WORKSPACE_ROOT / "static" / "docs"), html=True),
        name="docs",
    )

if HOTFOLDER_OUT.exists():
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

# --- Weekly Inspection Photos (4 Photos) ---
INSPECTION_PHOTOS_FILE = WORKSPACE_ROOT / "backend" / "data" / "inspection_photos.json"

@app.get("/api/v1/inspection/photos")
def get_inspection_photos():
    if INSPECTION_PHOTOS_FILE.exists():
        try:
            import json
            with open(INSPECTION_PHOTOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    default_slot = "/static/default_inspection_photo.jpg"
    return {"is_custom": False, "photos": [default_slot, default_slot, default_slot, default_slot]}

@app.post("/api/v1/inspection/photos")
def update_inspection_photos(payload: dict = Body(...)):
    photos = payload.get("photos", [])
    if not isinstance(photos, list):
        raise HTTPException(status_code=400, detail="photos must be a list")
    try:
        import json
        INSPECTION_PHOTOS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(INSPECTION_PHOTOS_FILE, "w", encoding="utf-8") as f:
            json.dump({"is_custom": True, "photos": photos}, f, ensure_ascii=False, indent=2)
        return {"status": "SUCCESS", "is_custom": True, "count": len(photos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

DEFAULT_INSPECTION_PHOTOS_FILE = WORKSPACE_ROOT / "backend" / "data" / "default_inspection_photos.json"

@app.post("/api/v1/inspection/photos/reset")
def reset_inspection_photos():
    try:
        import json
        if DEFAULT_INSPECTION_PHOTOS_FILE.exists():
            with open(DEFAULT_INSPECTION_PHOTOS_FILE, "r", encoding="utf-8") as f:
                default_data = json.load(f)
            with open(INSPECTION_PHOTOS_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
            return {"status": "SUCCESS", "message": "Reset to default photos", "photos": default_data.get("photos", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "SUCCESS", "message": "Reset to default photos"}


# --- Awaiting service: Upload defect photos ---
@app.post("/api/v1/Awaiting service")
def upload_defect_photo(
    file: UploadFile = File(...),
    printer_rank: str = Form(""),
    printer_name: str = Form(""),
    printer_position: str = Form(""),
    approver_rank: str = Form(""),
    approver_name: str = Form(""),
    approver_position: str = Form(""),
    report_date: str = Form(""),
    cause: str = Form(""),
    symptoms: str = Form(""),
    role: str = Form("owner")
):
    """Endpoint to upload defect photos with metadata and store a record in SSOT."""
    import json, uuid, datetime
    # Save uploaded file
    dest_dir = Path(__file__).resolve().parent.parent / "static" / "uploads" / "defect_photos"
    dest_dir.mkdir(parents=True, exist_ok=True)
    file_path = dest_dir / file.filename
    with open(file_path, "wb") as out_file:
        out_file.write(file.file.read())
    # Build record dictionary with the 2 sections (printer/reviewer & approver)
    record = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "file": file.filename,
        "printer": {"rank": printer_rank, "name": printer_name, "position": printer_position},
        "approver": {"rank": approver_rank, "name": approver_name, "position": approver_position},
        "report_date": report_date,
        "cause": cause,
        "symptoms": symptoms,
        "uploader_role": role
    }
    # Append to JSON SSOT file
    try:
        existing = json.loads(AWAITING_RECORDS_FILE.read_text(encoding="utf-8"))
    except Exception:
        existing = []
    existing.append(record)
    AWAITING_RECORDS_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "SUCCESS", "record_id": record["id"], "filename": file.filename}



# --- Informal Equipment Inventory & Loan/Damage Management ---
from backend.services.informal_equipment_service import (
    get_inventory_overview,
    create_loan_record,
    process_return_record,
    get_overdue_alerts,
    generate_damage_memo_html
)

@app.get("/api/v1/informal-equipment")
def api_get_informal_equipment():
    return get_inventory_overview()

@app.get("/api/v1/informal-equipment/overdue-alerts")
def api_get_overdue_alerts():
    return {"overdue_loans": get_overdue_alerts()}

@app.post("/api/v1/informal-equipment/loan")
def api_create_loan(payload: dict = Body(...)):
    try:
        return create_loan_record(
            item_id=payload.get("item_id"),
            borrower_rank=payload.get("borrower_rank", ""),
            borrower_name=payload.get("borrower_name", ""),
            quantity=int(payload.get("quantity", 1)),
            loan_date=payload.get("loan_date", date.today().isoformat()),
            expected_return_date=payload.get("expected_return_date", ""),
            borrower_position=payload.get("borrower_position", "พลปืน")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/informal-equipment/return")
def api_return_loan(payload: dict = Body(...)):
    try:
        return process_return_record(
            loan_id=payload.get("loan_id"),
            actual_return_date=payload.get("actual_return_date", date.today().isoformat()),
            has_damage=bool(payload.get("has_damage", False)),
            cause=payload.get("cause", ""),
            symptom=payload.get("symptom", "")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/informal-equipment/report/{loan_id}", response_class=HTMLResponse)
def api_get_damage_memo(loan_id: str, target_date: Optional[str] = None):
    try:
        html = generate_damage_memo_html(loan_id, signing_date_iso=target_date)
        return HTMLResponse(content=html)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Frontend Portal UI ---
@app.get("/", response_class=HTMLResponse)
@app.get("/frontend/templates/index.html", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
def index():
    template_path = FRONTEND_DIR / "templates" / "index.html"
    if template_path.exists():
        return HTMLResponse(template_path.read_text(encoding="utf-8"))
    root_index = WORKSPACE_ROOT / "index.html"
    if root_index.exists():
        return HTMLResponse(root_index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Tactical Military Document Automation Suite</h1>")

@app.get("/upload_form.html", response_class=HTMLResponse)
@app.get("/upload-form", response_class=HTMLResponse)
def serve_upload_form():
    template_path = FRONTEND_DIR / "templates" / "upload_form.html"
    if template_path.exists():
        return HTMLResponse(template_path.read_text(encoding="utf-8"))
    raise HTTPException(status_code=404, detail="Upload form template not found")


# --- Root Document Fallback Serving ---
@app.get("/{filename:path}")
def serve_root_docs(filename: str):
    import urllib.parse
    decoded = urllib.parse.unquote(filename).strip("/")
    base_name = Path(decoded).name

    # Prefer the dedicated /docs static mount for document assets
    docs_path = WORKSPACE_ROOT / "static" / "docs" / base_name
    if docs_path.is_file():
        if docs_path.suffix.lower() == ".html":
            return HTMLResponse(content=docs_path.read_text(encoding="utf-8"))
        return FileResponse(docs_path)

    # Fallback to generic locations (kept for backward compatibility)
    candidates = [
        FRONTEND_DIR / "static" / "docs" / base_name,
        WORKSPACE_ROOT / base_name,
        FRONTEND_DIR / "static" / decoded,
        WORKSPACE_ROOT / decoded,
    ]
    for cand in candidates:
        if cand.is_file():
            if cand.suffix.lower() == ".html":
                return HTMLResponse(content=cand.read_text(encoding="utf-8"))
            return FileResponse(cand)

    raise HTTPException(status_code=404, detail=f"File '{decoded}' not found")


