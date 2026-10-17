"""
Informal Equipment Inventory & Loan/Damage Management Service
Production-grade engine handling:
- Section 1: สิ่งอุปกรณ์ในโรงเก็บปืนใหญ่ (ลำดับ 1 - 43)
- Section 2: สิ่งอุปกรณ์ในคลัง บก.โรงเก็บปืนใหญ่ (ลำดับ 1 - 29)
- Loan tracking, stock deduction, overdue alerts
- Damage reporting with separate cause & symptom fields
- Generation of Royal Thai Army Memo (บันทึกข้อความ) for Battery Commander
"""
import json
import os
import base64
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = WORKSPACE_ROOT / "backend" / "data" / "informal_equipment_inventory.json"

def get_garuda_base64() -> str:
    """Loads and base64-encodes authentic military Garuda emblem."""
    candidates = [
        WORKSPACE_ROOT / "garuda_vector_official.png",
        WORKSPACE_ROOT / "garuda_memo.png",
        WORKSPACE_ROOT / "weekly_assets" / "garuda_weekly.png"
    ]
    for p in candidates:
        if p.exists():
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""

THAI_MONTHS = [
    "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]

THAI_FULL_MONTHS = [
    "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

def to_thai_digits(num_str: Any) -> str:
    """Converts Arabic digits to Thai digits."""
    s = str(num_str)
    thai_digits = "๐๑๒๓๔๕๖๗๘๙"
    arabic_digits = "0123456789"
    trans = str.maketrans(arabic_digits, thai_digits)
    return s.translate(trans)

def format_thai_date(iso_date: str) -> str:
    """Formats ISO date YYYY-MM-DD into Thai date string e.g. ๖ พฤศจิกายน ๒๕๖๙"""
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        day = to_thai_digits(dt.day)
        month = THAI_FULL_MONTHS[dt.month]
        year = to_thai_digits(dt.year + 543)
        return f"{day} {month} {year}"
    except Exception:
        return to_thai_digits(iso_date)

def load_inventory_db() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Database file not found: {DATA_FILE}")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_inventory_db(data: Dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_inventory_overview() -> Dict[str, Any]:
    """Returns inventory with summary counts for both sections."""
    db = load_inventory_db()
    
    # Calculate live statistics
    s1_items = db["sections"]["gun_shed"]["items"]
    s2_items = db["sections"]["hq_warehouse"]["items"]

    s1_stats = {
        "total_items": len(s1_items),
        "physical_sum": sum(item.get("physical_amount", 0) for item in s1_items),
        "loan_sum": sum(item.get("loan_amount", 0) for item in s1_items),
        "repair_sum": sum(item.get("repair_amount", 0) for item in s1_items),
        "balance_sum": sum(item.get("balance_amount", 0) for item in s1_items),
    }

    s2_stats = {
        "total_items": len(s2_items),
        "physical_sum": sum(item.get("physical_amount", 0) for item in s2_items),
        "loan_sum": sum(item.get("loan_amount", 0) for item in s2_items),
        "repair_sum": sum(item.get("repair_amount", 0) for item in s2_items),
        "balance_sum": sum(item.get("balance_amount", 0) for item in s2_items),
    }

    # Check overdue status for all loans
    today_iso = date.today().isoformat()
    loans = db.get("loans", [])
    overdue_count = 0
    for loan in loans:
        if loan.get("status") == "borrowed":
            exp = loan.get("expected_return_date", "")
            if exp and exp < today_iso:
                loan["is_overdue"] = True
                overdue_count += 1
            else:
                loan["is_overdue"] = False

    return {
        "metadata": db.get("metadata", {}),
        "stats": {
            "gun_shed": s1_stats,
            "hq_warehouse": s2_stats,
            "active_loans_count": sum(1 for l in loans if l.get("status") == "borrowed"),
            "overdue_loans_count": overdue_count
        },
        "sections": db["sections"],
        "loans": loans
    }

def find_item_in_db(db: Dict[str, Any], item_id: str) -> Optional[Dict[str, Any]]:
    for sec_key in ["gun_shed", "hq_warehouse"]:
        for itm in db["sections"][sec_key]["items"]:
            if itm["id"] == item_id:
                return itm
    return None

def create_loan_record(
    item_id: str,
    borrower_rank: str,
    borrower_name: str,
    quantity: int,
    loan_date: str,
    expected_return_date: str,
    borrower_position: str = "พลปืน"
) -> Dict[str, Any]:
    """Creates a loan and deducts from active stock balance."""
    db = load_inventory_db()
    item = find_item_in_db(db, item_id)
    if not item:
        raise ValueError(f"ไม่พบสิ่งอุปกรณ์รหัส {item_id}")

    current_balance = item.get("balance_amount", 0)
    if quantity <= 0:
        raise ValueError("จำนวนที่เบิกยืมต้องมากกว่า ๐")
    if quantity > current_balance:
        raise ValueError(f"จำนวนคงเหลือไม่เพียงพอ (คงเหลือเพียง {current_balance} รายการ)")

    # Deduct stock balance and add to loan count
    item["balance_amount"] = current_balance - quantity
    item["loan_amount"] = item.get("loan_amount", 0) + quantity

    loan_id = f"LN-{datetime.now().strftime('%y%m%d-%H%M%S')}"
    new_loan = {
        "loan_id": loan_id,
        "item_id": item_id,
        "item_name": item.get("name", ""),
        "item_full_name": item.get("full_name", item.get("name", "")),
        "section": item.get("section", ""),
        "section_title": item.get("section_title", ""),
        "borrower_rank": borrower_rank.strip(),
        "borrower_name": borrower_name.strip(),
        "borrower_fullname": f"{borrower_rank.strip()} {borrower_name.strip()}",
        "borrower_position": borrower_position.strip(),
        "quantity": int(quantity),
        "loan_date": loan_date,
        "expected_return_date": expected_return_date,
        "actual_return_date": None,
        "status": "borrowed",  # borrowed, returned_normal, returned_damaged
        "is_overdue": False,
        "damage_info": {
            "has_damage": False,
            "cause": "",
            "symptom": "",
            "reported_to_commander": False,
            "memo_generated": False
        }
    }

    if "loans" not in db:
        db["loans"] = []
    db["loans"].insert(0, new_loan)
    save_inventory_db(db)
    return new_loan

def process_return_record(
    loan_id: str,
    actual_return_date: str,
    has_damage: bool = False,
    cause: str = "",
    symptom: str = ""
) -> Dict[str, Any]:
    """
    Processes item return.
    If damaged:
    - Transfers stock from loan to 'ส่งซ่อม' (repair_amount)
    - Records cause and symptom separately
    - Prepares data for official Memo (บันทึกข้อความ)
    """
    db = load_inventory_db()
    target_loan = None
    for l in db.get("loans", []):
        if l["loan_id"] == loan_id:
            target_loan = l
            break

    if not target_loan:
        raise ValueError(f"ไม่พบประวัติการยืมรหัส {loan_id}")
    if target_loan["status"] != "borrowed":
        raise ValueError(f"รายการยืมนี้ได้รับการคืนไปแล้ว (สถานะ: {target_loan['status']})")

    item = find_item_in_db(db, target_loan["item_id"])
    qty = target_loan.get("quantity", 1)

    # Deduct from loan amount
    if item:
        item["loan_amount"] = max(0, item.get("loan_amount", 0) - qty)

    target_loan["actual_return_date"] = actual_return_date

    if has_damage:
        # Move stock into repair slot (ส่งซ่อม)
        if item:
            item["repair_amount"] = item.get("repair_amount", 0) + qty
        target_loan["status"] = "returned_damaged"
        target_loan["damage_info"] = {
            "has_damage": True,
            "cause": cause.strip(),
            "symptom": symptom.strip(),
            "reported_to_commander": False,
            "memo_generated": True
        }
    else:
        # Return normally to available balance
        if item:
            item["balance_amount"] = item.get("balance_amount", 0) + qty
        target_loan["status"] = "returned_normal"
        target_loan["damage_info"] = {
            "has_damage": False,
            "cause": "",
            "symptom": "",
            "reported_to_commander": False,
            "memo_generated": False
        }

    save_inventory_db(db)
    return target_loan

def get_overdue_alerts() -> List[Dict[str, Any]]:
    """Returns all overdue loans for alert popup."""
    db = load_inventory_db()
    today_iso = date.today().isoformat()
    today_dt = date.today()
    overdue_list = []

    for l in db.get("loans", []):
        if l.get("status") == "borrowed":
            exp_str = l.get("expected_return_date", "")
            if exp_str and exp_str < today_iso:
                try:
                    exp_dt = datetime.strptime(exp_str, "%Y-%m-%d").date()
                    days_overdue = (today_dt - exp_dt).days
                except Exception:
                    days_overdue = 1
                l_copy = dict(l)
                l_copy["days_overdue"] = days_overdue
                l_copy["days_overdue_thai"] = to_thai_digits(days_overdue)
                overdue_list.append(l_copy)
    return overdue_list

def generate_damage_memo_html(loan_id: str, signing_date_iso: Optional[str] = None) -> str:
    """
    Generates a Royal Thai Army Standard Memo (บันทึกข้อความ)
    Reporting equipment damage from borrowing to the Battery Commander (ผบ.ร้อย).
    Compiled directly from Single Source of Truth Blueprint: table_layout_damage_memo.json
    Adheres strictly to:
    - RULE-RTA-MEMO-STANDARD-V1 (SSOT JSON Blueprint, Dotted line hugging, Dual-Copy Package)
    - RULE-SARABUN-DOC-STANDARD-V1 (PSK font, Bold 600, Thin 300)
    - RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard 130mm, 5 enters)
    - RULE-STAFF-REVIEW-FOOTER-V1 (Dual-Axis 4 columns, 5 enters)
    - RULE-PROD-DOC-ENGINE-V1 (Official Mon-Thu business day calculation)
    """
    import json
    from pathlib import Path

    # 1. Load SSOT Blueprint
    bp_candidates = [
        Path("d:/Project/WEPAPP/table_layout_damage_memo.json"),
        Path(__file__).resolve().parent.parent.parent / "table_layout_damage_memo.json",
        Path(__file__).resolve().parent.parent.parent / "references" / "informal_equipment" / "table_layout_damage_memo.json",
    ]
    bp = None
    for p in bp_candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                bp = json.load(f)
            break

    if not bp:
        raise FileNotFoundError("ไม่พบไฟล์พิมพ์เขียว table_layout_damage_memo.json")

    # 2. Load Loan & Damage Database Records
    db = load_inventory_db()
    loan = None
    for l in db.get("loans", []):
        if l["loan_id"] == loan_id:
            loan = l
            break

    if not loan:
        raise ValueError(f"ไม่พบข้อมูลการยืมรหัส {loan_id}")

    damage = loan.get("damage_info", {})
    item_name = loan.get("item_full_name", loan.get("item_name", "สิ่งอุปกรณ์"))
    qty_thai = to_thai_digits(loan.get("quantity", 1))
    borrower_fullname = loan.get("borrower_fullname", "เจ้าหน้าที่ผู้ยืม")
    loan_date_thai = format_thai_date(loan.get("loan_date", date.today().isoformat()))
    cause_text = damage.get("cause") or "การปฏิบัติภารกิจภาคสนาม"
    symptom_text = damage.get("symptom") or "ชำรุดเสียหาย ไม่สามารถใช้งานได้ตามปกติ"

    # 3. Compute Official Signing Date (Mon-Thu business day, no holiday, no Friday)
    from backend.services.business_day_engine import is_business_day
    if signing_date_iso:
        try:
            base_dt = datetime.strptime(signing_date_iso, "%Y-%m-%d").date()
        except Exception:
            base_dt = date.today()
    else:
        base_dt = date.today()

    candidate = base_dt
    while not is_business_day(candidate) or candidate.weekday() >= 4:
        candidate -= timedelta(days=1)

    day_thai = to_thai_digits(candidate.day)
    short_month_thai = THAI_MONTHS[candidate.month]
    short_year_thai = to_thai_digits(str(candidate.year + 543)[-2:])
    date_display_thai = f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{short_month_thai} {short_year_thai}"
    month_year_display_thai = f"{short_month_thai} {short_year_thai}"

    # 4. Resolve Blueprint Data
    page_setup = bp.get("page_setup", {})
    margins = page_setup.get("margins_mm", {"top": 25, "bottom": 20, "left": 30, "right": 20})
    header_block = bp.get("header_block", {})
    metadata_block = bp.get("metadata_block", {})
    body_block = bp.get("body_block", {})
    sig_block_def = bp.get("signature_block", {})
    staff_footer_def = bp.get("staff_footer_block", {})

    garuda_b64 = get_garuda_base64()
    garuda_src = f"data:image/png;base64,{garuda_b64}" if garuda_b64 else "/garuda.png"

    # Fill metadata values
    agency_val = metadata_block.get("agency", {}).get("value", "ป.๔ พัน.๔ ร้อย.๒  ( โทร. ๓๑๑๙๓ )")
    doc_num_val = metadata_block.get("doc_number", {}).get("value", "กห ๐๔๘๓.๑.๔.๑/")
    date_val = metadata_block.get("date", {}).get("value", "{date_thai}").replace("{date_thai}", date_display_thai)
    subject_val = metadata_block.get("subject", {}).get("value", "รายงานการชำรุดเสียหายของสิ่งและอุปกรณ์ จากการเบิกยืม")

    # Fill body values
    salutation = body_block.get("salutation", "เรียน  ผบ.ป.๔ พัน.๔ ร้อย.๒")
    references = body_block.get("references", [])
    attachments = body_block.get("attachments", [])
    resolved_attachments = []
    for att in attachments:
        item_text = att.get("item", "").replace("{borrower_fullname}", borrower_fullname)
        qty_text = att.get("qty", "จำนวน  ๑  ฉบับ")
        resolved_attachments.append((item_text, qty_text))

    # Support structured_paragraphs (3-tier division: reason, intention, summary) or fallback paragraphs
    structured_paras = body_block.get("structured_paragraphs", {})
    if structured_paras:
        p1 = structured_paras.get("paragraph_1_reason", {}).get("content", "")
        p2 = structured_paras.get("paragraph_2_intention", {}).get("content", "")
        p3_obj = structured_paras.get("paragraph_3_summary", {})
        if "content_lines" in p3_obj:
            p3_lines = p3_obj["content_lines"]
        elif "content" in p3_obj:
            p3_lines = [p3_obj["content"]]
        else:
            p3_lines = []
        paragraphs = [p1, p2] + p3_lines
    else:
        paragraphs = body_block.get("paragraphs", [])

    resolved_paragraphs = []
    for p in paragraphs:
        p_res = (p.replace("{borrower_fullname}", borrower_fullname)
                  .replace("{loan_date_thai}", loan_date_thai)
                  .replace("{item_name}", item_name)
                  .replace("{qty_thai}", qty_thai)
                  .replace("{cause_text}", cause_text)
                  .replace("{symptom_text}", symptom_text))
        resolved_paragraphs.append(p_res)

    # Signature Block Values
    sig_rank = sig_block_def.get("rank", "ร.อ.")
    sig_name = sig_block_def.get("name", "(กฤติน  นราพงษ์)")
    if not sig_name.startswith("("):
        sig_name = f"({sig_name})"
    sig_pos = sig_block_def.get("position", "ผบ.ป.๔ พัน.๔ ร้อย.๒")

    # Staff Review Footer Values
    drafter = staff_footer_def.get("drafter_inspector", {})
    typist = staff_footer_def.get("typist_reviewer", {})
    drafter_rank = drafter.get("rank", "จ.ส.อ.")
    drafter_role = drafter.get("role", "ร่าง/ตรวจ")
    drafter_my = drafter.get("month_year", "{month_year_thai}").replace("{month_year_thai}", month_year_display_thai)

    typist_rank = typist.get("rank", "ส.ท.")
    typist_role = typist.get("role", "พิมพ์/ทาน")
    typist_day = typist.get("date", "{day_thai}").replace("{day_thai}", day_thai)
    typist_my = typist.get("month_year", "{month_year_thai}").replace("{month_year_thai}", month_year_display_thai)

    # 5. Build HTML Markup
    memo_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>{bp.get('document_title', 'บันทึกข้อความ')}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');

    /* Local TH Sarabun PSK font embeddings */
    @font-face {{
      font-family: 'TH Sarabun PSK';
      font-style: normal;
      font-weight: 300;
      src: local('TH Sarabun PSK'), local('THSarabunPSK'),
           url('/fonts/THSarabunPSK.ttf') format('truetype'),
           url('fonts/THSarabunPSK.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'TH Sarabun PSK';
      font-style: normal;
      font-weight: 400;
      src: local('TH Sarabun PSK'), local('THSarabunPSK'),
           url('/fonts/THSarabunPSK.ttf') format('truetype'),
           url('fonts/THSarabunPSK.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'TH Sarabun PSK';
      font-style: normal;
      font-weight: 600;
      src: local('TH Sarabun PSK Bold'), local('THSarabunPSK-Bold'),
           url('/fonts/THSarabunPSK-Bold.ttf') format('truetype'),
           url('fonts/THSarabunPSK-Bold.ttf') format('truetype');
    }}
    @font-face {{
      font-family: 'TH Sarabun PSK';
      font-style: normal;
      font-weight: 700;
      src: local('TH Sarabun PSK Bold'), local('THSarabunPSK-Bold'),
           url('/fonts/THSarabunPSK-Bold.ttf') format('truetype'),
           url('fonts/THSarabunPSK-Bold.ttf') format('truetype');
    }}

    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    body {{
      margin: 0;
      padding: 0;
      background-color: #525659;
      font-family: 'TH Sarabun PSK', 'THSarabunPSK', 'TH Sarabun New', 'THSarabunNew', 'Sarabun', sans-serif !important;
      font-size: 16pt;
      line-height: 1.22;
      color: #000000;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .a4-page {{
      width: 210mm;
      min-height: 297mm;
      height: 297mm;
      padding: {margins['top']}mm {margins['right']}mm {margins['bottom']}mm {margins['left']}mm; /* บน 25 มม., ขวา 20 มม., ล่าง 20 มม., ซ้าย 30 มม. */
      background-color: #ffffff;
      margin-bottom: 20px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    @media print {{
      body {{
        background-color: transparent;
        padding: 0;
      }}
      .a4-page {{
        margin: 0;
        box-shadow: none;
        page-break-after: always;
        height: 297mm;
      }}
      .no-print {{
        display: none !important;
      }}
    }}
    .copy-banner {{
      position: absolute;
      top: 10mm;
      left: 0;
      right: 0;
      text-align: center;
      font-size: 14pt;
      font-weight: 300;
      color: #333333;
    }}
    .memo-garuda-container {{
      position: relative;
      width: 100%;
      height: {max(18, header_block.get('garuda', {}).get('height_mm', 15) + 3)}mm;
      margin-bottom: 2mm;
    }}
    .memo-garuda {{
      position: absolute;
      left: 0;
      top: 0;
      height: {header_block.get('garuda', {}).get('height_mm', 15)}mm;
      width: {header_block.get('garuda', {}).get('width_mm', 13.8)}mm;
      object-fit: contain;
    }}
    .memo-title {{
      text-align: center;
      font-size: 29pt;
      font-weight: 600;
      line-height: 1.1;
      padding-top: {header_block.get('title_top_mm', 0)}mm;
      letter-spacing: 0.5px;
    }}

    /* METADATA BLOCK WITH DOTTED UNDERLINE HUGGING */
    .meta-section {{
      width: 100%;
      margin-top: 2.5mm;
      margin-bottom: 3.5mm;
    }}
    .meta-row {{
      display: flex;
      align-items: flex-end;
      margin-bottom: 2mm;
      font-size: 16pt;
    }}
    .meta-label {{
      font-size: 20pt;
      font-weight: 600;
      white-space: nowrap;
      margin-right: 2.5mm;
      padding-bottom: 1px;
    }}
    .meta-dots {{
      flex: 1;
      border-bottom: 1px dotted #000;
      display: inline-block;
      min-height: 1.05em;
      line-height: 1.05;
      padding-bottom: 1.5px;
      font-weight: 300;
      font-size: 16pt;
    }}

    /* BODY BLOCK */
    .memo-body {{
      font-size: 16pt;
      line-height: 1.22;
      font-weight: 300;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .salutation-row {{
      font-size: 16pt;
      margin-bottom: 3mm;
    }}
    .salutation-label {{
      font-weight: 600;
    }}
    .ref-section {{
      margin-bottom: 2.5mm;
    }}
    .ref-label {{
      font-weight: 600;
      white-space: nowrap;
    }}
    .ref-item {{
      font-weight: 300;
      font-size: 16pt;
      line-height: 1.22;
    }}
    .att-section {{
      margin-bottom: 3.5mm;
    }}
    .att-label {{
      font-weight: 600;
      white-space: nowrap;
    }}
    .memo-para {{
      text-indent: 25mm; /* กั้นหน้าย่อหน้า 2.5 ซม. */
      text-align: justify;
      text-justify: inter-cluster;
      word-break: keep-all;
      overflow-wrap: break-word;
      font-weight: 300;
      margin-bottom: 3.5mm;
    }}

    /* UNIVERSAL SIGNATURE BLOCK (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
    .sig-container {{
      width: 100%;
      margin-top: 22mm; /* 5 Enter */
      /* Page left padding is 30mm; 130mm - 30mm = 100mm from content left edge */
      padding-left: 100mm;
      display: flex;
      justify-content: flex-start;
    }}
    .sig-block {{
      display: inline-flex;
      flex-direction: column;
      align-items: flex-start;
      font-size: 16pt;
      line-height: 1.0;
    }}
    .sig-name-pos-group {{
      display: inline-flex;
      flex-direction: column;
      align-items: center; /* ชื่อและตำแหน่งจัดกึ่งกลางร่วมกัน */
      position: relative;
    }}
    .sig-name-wrapper {{
      position: relative;
      display: inline-block;
      white-space: nowrap;
      margin-top: 24pt; /* พื้นที่สำหรับลงลายมือชื่อจริง (Signature Gap) */
    }}
    .sig-rank-anchor {{
      position: absolute;
      right: 100%;
      bottom: calc(100% + 18px); /* อยู่คนละบรรทัด ลอยเหนือลายมือชื่อ โดยจุด . ชนแนวเส้นดิ่ง ( พอดีเป๊ะ 100% */
      white-space: nowrap;
      font-size: 16pt;
      line-height: 1.0;
      font-weight: 300;
    }}
    .sig-name {{
      margin: 0;
      line-height: 1.15;
      text-align: center;
      white-space: nowrap;
      font-size: 16pt;
      font-weight: 300;
      display: block;
    }}
    .sig-pos {{
      margin: 0;
      line-height: 1.15;
      text-align: center;
      white-space: nowrap;
      font-size: 16pt;
      font-weight: 300;
      display: block;
    }}

    /* STAFF REVIEW FOOTER (RULE-STAFF-REVIEW-FOOTER-V1) */
    .memo-footer-staff {{
      margin-top: 22mm; /* 5 Enter ใต้บล็อกลงนาม */
      width: 100%;
      display: flex;
      justify-content: flex-end;
    }}
    .staff-grid {{
      display: grid;
      grid-template-columns: 26mm 22mm 8mm max-content;
      font-size: 13.5pt;
      line-height: 1.25;
      font-weight: 300;
    }}
    .staff-col-rank {{
      text-align: left;
    }}
    .staff-col-role {{
      text-align: left;
    }}
    .staff-col-day {{
      text-align: right;
      padding-right: 1.5mm;
    }}
    .staff-col-month {{
      text-align: left;
    }}
  </style>
</head>
<body>

  <!-- Controls for Export and Print (Screen Only) -->
  <div class="no-print" style="width: 210mm; background: #1e293b; padding: 14px 20px; margin: 15px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
    <div style="color: #fff; font-size: 14px; font-weight: 600;">
      📄 พรีวิวบันทึกข้อความ: รายงานการชำรุดเสียหายจากการเบิกยืม (รหัส {loan.get('loan_id')})
    </div>
    <div style="display: flex; gap: 10px;">
      <button onclick="window.print()" style="background: #0ea5e9; color: #fff; border: none; padding: 7px 16px; border-radius: 6px; font-weight: 600; cursor: pointer;">
        🖨️ สั่งพิมพ์ (Print 300 DPI)
      </button>
      <button onclick="window.close()" style="background: rgba(255,255,255,0.1); color: #94a3b8; border: 1px solid rgba(255,255,255,0.2); padding: 7px 14px; border-radius: 6px; cursor: pointer;">
        ✕ ปิดหน้าต่าง
      </button>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- 1. ฉบับตัวจริง (ORIGINAL COPY)                             -->
  <!-- ======================================================== -->
  <div class="a4-page">
    <div class="memo-garuda-container">
      <img src="{garuda_src}" alt="ตราครุฑ" class="memo-garuda">
      <div class="memo-title">{header_block.get('title', 'บันทึกข้อความ')}</div>
    </div>

    <!-- Metadata Section -->
    <div class="meta-section">
      <!-- Row 1: ส่วนราชการ (จุดไข่ปลายาวจนสุดขอบ) -->
      <div class="meta-row">
        <span class="meta-label">ส่วนราชการ</span>
        <div class="meta-dots">{agency_val}</div>
      </div>

      <!-- Row 2: ที่ & วันที่ (ที่ จุดไข่ปลายาวถึงวันที่) -->
      <div class="meta-row">
        <div style="flex: 1.15; display: flex; align-items: flex-end; margin-right: 6mm;">
          <span class="meta-label">ที่</span>
          <div class="meta-dots">{doc_num_val}</div>
        </div>
        <div style="flex: 0.85; display: flex; align-items: flex-end;">
          <span class="meta-label">วันที่</span>
          <div class="meta-dots" style="text-align: center;">{date_val}</div>
        </div>
      </div>

      <!-- Row 3: เรื่อง (จุดไข่ปลายาวจนสุดขอบ) -->
      <div class="meta-row">
        <span class="meta-label">เรื่อง</span>
        <div class="meta-dots">{subject_val}</div>
      </div>
    </div>

    <div class="memo-body">
      <!-- Salutation -->
      <div class="salutation-row">
        <span class="salutation-label">เรียน</span>&nbsp;&nbsp;{salutation.replace('เรียน', '').strip()}
      </div>

      <!-- References (อ้างถึง) -->
      <div class="ref-section">
        <span class="ref-label">อ้างถึง</span>&nbsp;&nbsp;<span class="ref-item">{references[0] if len(references) > 0 else ''}</span><br>
        <span style="display: inline-block; width: 13.5mm;"></span><span class="ref-item">{references[1] if len(references) > 1 else ''}</span>
      </div>

      <!-- Attachments (สิ่งที่ส่งมาด้วย) -->
      <div class="att-section">
        <span class="att-label">สิ่งที่ส่งมาด้วย</span>&nbsp;&nbsp;<span style="font-weight: 300;">{resolved_attachments[0][0] if resolved_attachments else ''}</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-weight: 300;">{resolved_attachments[0][1] if resolved_attachments else ''}</span>
      </div>

      <!-- Content Paragraphs -->
      <div class="memo-para">
        {resolved_paragraphs[0] if len(resolved_paragraphs) > 0 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[1] if len(resolved_paragraphs) > 1 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[2] if len(resolved_paragraphs) > 2 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[3] if len(resolved_paragraphs) > 3 else ''}
      </div>

      <!-- Universal Signature Block (130mm from page left, 5 enters) -->
      <div class="sig-container">
        <div class="sig-block">
          <div class="sig-name-pos-group">
            <div class="sig-name-wrapper">
              <span class="sig-rank-anchor">{sig_rank}</span>
              <div class="sig-name">{sig_name}</div>
            </div>
            <div class="sig-pos">{sig_pos}</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- 2. สำเนาคู่ฉบับ (DUAL COPY PACKAGE)                        -->
  <!-- ======================================================== -->
  <div class="a4-page">
    <div class="copy-banner">(สำเนาคู่ฉบับ)</div>
    <div class="memo-garuda-container">
      <img src="{garuda_src}" alt="ตราครุฑ" class="memo-garuda">
      <div class="memo-title">{header_block.get('title', 'บันทึกข้อความ')}</div>
    </div>

    <!-- Metadata Section -->
    <div class="meta-section">
      <!-- Row 1: ส่วนราชการ (จุดไข่ปลายาวจนสุดขอบ) -->
      <div class="meta-row">
        <span class="meta-label">ส่วนราชการ</span>
        <div class="meta-dots">{agency_val}</div>
      </div>

      <!-- Row 2: ที่ & วันที่ (ที่ จุดไข่ปลายาวถึงวันที่) -->
      <div class="meta-row">
        <div style="flex: 1.15; display: flex; align-items: flex-end; margin-right: 6mm;">
          <span class="meta-label">ที่</span>
          <div class="meta-dots">{doc_num_val}</div>
        </div>
        <div style="flex: 0.85; display: flex; align-items: flex-end;">
          <span class="meta-label">วันที่</span>
          <div class="meta-dots" style="text-align: center;">{date_val}</div>
        </div>
      </div>

      <!-- Row 3: เรื่อง (จุดไข่ปลายาวจนสุดขอบ) -->
      <div class="meta-row">
        <span class="meta-label">เรื่อง</span>
        <div class="meta-dots">{subject_val}</div>
      </div>
    </div>

    <div class="memo-body">
      <!-- Salutation -->
      <div class="salutation-row">
        <span class="salutation-label">เรียน</span>&nbsp;&nbsp;{salutation.replace('เรียน', '').strip()}
      </div>

      <!-- References (อ้างถึง) -->
      <div class="ref-section">
        <span class="ref-label">อ้างถึง</span>&nbsp;&nbsp;<span class="ref-item">{references[0] if len(references) > 0 else ''}</span><br>
        <span style="display: inline-block; width: 13.5mm;"></span><span class="ref-item">{references[1] if len(references) > 1 else ''}</span>
      </div>

      <!-- Attachments (สิ่งที่ส่งมาด้วย) -->
      <div class="att-section">
        <span class="att-label">สิ่งที่ส่งมาด้วย</span>&nbsp;&nbsp;<span style="font-weight: 300;">{resolved_attachments[0][0] if resolved_attachments else ''}</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="font-weight: 300;">{resolved_attachments[0][1] if resolved_attachments else ''}</span>
      </div>

      <!-- Content Paragraphs -->
      <div class="memo-para">
        {resolved_paragraphs[0] if len(resolved_paragraphs) > 0 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[1] if len(resolved_paragraphs) > 1 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[2] if len(resolved_paragraphs) > 2 else ''}
      </div>
      <div class="memo-para">
        {resolved_paragraphs[3] if len(resolved_paragraphs) > 3 else ''}
      </div>

      <!-- Universal Signature Block (130mm from page left, 5 enters) -->
      <div class="sig-container">
        <div class="sig-block">
          <div class="sig-name-pos-group">
            <div class="sig-name-wrapper">
              <span class="sig-rank-anchor">{sig_rank}</span>
              <div class="sig-name">{sig_name}</div>
            </div>
            <div class="sig-pos">{sig_pos}</div>
          </div>
        </div>
      </div>

      <!-- บล็อกเจ้าหน้าที่ทำหนังสือ (Dual-Axis 4 Columns Staff Footer, 5 enters) -->
      <div class="memo-footer-staff">
        <div class="staff-grid">
          <div class="staff-col-rank">{drafter_rank}</div>
          <div class="staff-col-role">{drafter_role}</div>
          <div class="staff-col-day"></div>
          <div class="staff-col-month">{drafter_my}</div>

          <div class="staff-col-rank">{typist_rank}</div>
          <div class="staff-col-role">{typist_role}</div>
          <div class="staff-col-day">{typist_day}</div>
          <div class="staff-col-month">{typist_my}</div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>"""

    # Apply Thai typography Zero-Width Space engine
    try:
        from thai_typography_engine import insert_thai_zws
        memo_html = insert_thai_zws(memo_html)
    except Exception:
        pass

    return memo_html
