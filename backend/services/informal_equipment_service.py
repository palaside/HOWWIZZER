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
    Adheres strictly to:
    - RULE-SARABUN-DOC-STANDARD-V1 (PSK font, Bold 600, Thin 300)
    - RULE-RTA-MEMO-STANDARD-V1 (Dotted line hugging, Dual-Copy Package)
    - RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard 130mm, 5 enters)
    - RULE-STAFF-REVIEW-FOOTER-V1 (Dual-Axis 4 columns)
    """
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

    # Compute official signing date (Mon-Thu business day, no holiday, no Friday)
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
    month_thai = THAI_FULL_MONTHS[candidate.month]
    year_thai = to_thai_digits(candidate.year + 543)
    date_display_thai = f"{day_thai} {month_thai} {year_thai}"

    # Load personnel registry for signers
    from backend.services.personnel_service import load_registry
    reg = load_registry()
    roles = reg.get("roles", {})
    commander = roles.get("commander_battery", {
        "rank": "ร.อ.",
        "name": "กฤติน นราพงษ์",
        "position": "ผบ.ป.๔ พัน.๔ ร้อย.๒"
    })
    chief_ops = roles.get("chief_operations", {
        "rank": "จ.ส.อ.",
        "name": "ณัฐชัย รักษาวงษ์",
        "position": "ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒"
    })

    # Red Line Standard Universal Signature Block (130mm left, 5 enters / 22mm)
    rank_str = commander.get("rank", "ร.อ.")
    name_str = commander.get("name", "กฤติน นราพงษ์")
    pos_str = "ผบ.ป.๔ พัน.๔ ร้อย.๒"
    sig_block_html = f'''
      <div class="sig-block-container" style="margin-left: 130mm; margin-top: 22mm; font-size: 16pt; line-height: 1.25;">
        <div style="position: relative; display: inline-block;">
          <span style="position: absolute; right: 100%; top: 0; white-space: nowrap; font-weight: 300;">{rank_str}</span>
          <div style="text-align: center; white-space: nowrap; font-weight: 300;">({name_str})</div>
          <div style="text-align: center; margin-top: 2px; white-space: nowrap; font-weight: 300;">{pos_str}</div>
        </div>
      </div>
    '''

    garuda_b64 = get_garuda_base64()
    garuda_src = f"data:image/png;base64,{garuda_b64}" if garuda_b64 else "/garuda.png"

    memo_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>บันทึกข้อความ - รายงานการชำรุดเสียหายของสิ่งและอุปกรณ์ จากการเบิกยืม</title>
  <style>
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
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .a4-page {{
      width: 210mm;
      min-height: 297mm;
      padding: 25mm 20mm 20mm 25mm; /* ขอบซ้าย 25mm สำหรับเข้าเล่ม */
      background-color: #ffffff;
      margin-bottom: 20px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      position: relative;
    }}
    @media print {{
      body {{
        background-color: #ffffff;
        padding: 0;
      }}
      .a4-page {{
        margin: 0;
        box-shadow: none;
        page-break-after: always;
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
      height: 25mm;
      margin-bottom: 2mm;
    }}
    .memo-garuda {{
      position: absolute;
      left: 0;
      top: 0;
      height: 18mm;
      width: auto;
    }}
    .memo-title {{
      text-align: center;
      font-size: 29pt;
      font-weight: 600;
      line-height: 1.1;
      padding-top: 3mm;
      letter-spacing: 0.5px;
    }}
    .meta-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 4mm;
      font-size: 16pt;
    }}
    .meta-table td {{
      padding: 2.5px 0;
      vertical-align: bottom;
    }}
    .meta-label {{
      font-size: 20pt;
      font-weight: 600;
      white-space: nowrap;
    }}
    .meta-dots {{
      border-bottom: 1px dotted #000;
      display: inline-block;
      width: 100%;
      min-height: 1.1em;
      line-height: 1.05;
      padding-bottom: 1.5px;
      font-weight: 300;
    }}
    .memo-body {{
      margin-top: 6mm;
      font-size: 16pt;
      line-height: 1.25;
      text-align: justify;
      text-justify: inter-cluster;
      font-weight: 300;
    }}
    .memo-para {{
      text-indent: 25mm; /* ย่อหน้า 2.5 ซม. */
      margin-bottom: 4mm;
    }}
    .memo-ref {{
      margin-left: 25mm;
      margin-bottom: 2mm;
    }}
    /* Draft review footer 4 cols */
    .staff-footer-container {{
      margin-top: 22mm;
      width: 80mm;
      font-size: 13.5pt;
      line-height: 1.25;
      font-weight: 300;
    }}
    .staff-row {{
      display: flex;
      align-items: baseline;
    }}
    .staff-col-rank {{ width: 26mm; text-align: left; }}
    .staff-col-role {{ width: 22mm; text-align: left; }}
    .staff-col-day  {{ width: 8mm; text-align: right; padding-right: 1.5mm; }}
    .staff-col-month{{ width: 20mm; text-align: left; }}
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
      <div class="memo-title">บันทึกข้อความ</div>
    </div>

    <table class="meta-table">
      <tr>
        <td style="width: 105mm;">
          <span class="meta-label">ส่วนราชการ</span>
          <span class="meta-dots" style="width: calc(100% - 32mm);">ป.๔ พัน.๔ ร้อย.๒ ( โทร. ๓๑๑๙๓ )</span>
        </td>
        <td style="width: 10mm;"></td>
        <td style="width: 75mm;"></td>
      </tr>
      <tr>
        <td>
          <span class="meta-label">ที่</span>
          <span class="meta-dots" style="width: calc(100% - 8mm);">กห ๐๔๘๓.๑.๔.๑/</span>
        </td>
        <td></td>
        <td>
          <span class="meta-label">วันที่</span>
          <span class="meta-dots" style="width: calc(100% - 15mm);">{date_display_thai}</span>
        </td>
      </tr>
      <tr>
        <td colspan="3">
          <span class="meta-label">เรื่อง</span>
          <span class="meta-dots" style="width: calc(100% - 14mm);">รายงานการชำรุดเสียหายของสิ่งและอุปกรณ์ จากการเบิกยืม</span>
        </td>
      </tr>
    </table>

    <div class="memo-body">
      <div style="margin-top: 4mm; margin-bottom: 3mm;">
        <span class="meta-label" style="font-size: 16pt;">เรียน</span>&nbsp;&nbsp;ผบ.ป.๔ พัน.๔ ร้อย.๒
      </div>

      <div style="margin-bottom: 2mm;">
        <span style="font-weight: 600;">อ้างถึง</span>&nbsp;&nbsp;๑. ระเบียบ ทบ. ว่าด้วยการส่งกำลังสิ่งอุปกรณ์ ประเภท ๒ และ ๔ พ.ศ. ๒๕๓๔<br>
        <span style="display: inline-block; width: 13.5mm;"></span>๒. ระเบียบ ทบ. ว่าด้วยการคุมและปรนนิบัติบำรุงยุทโธปกรณ์ สาย สพ.
      </div>

      <div style="margin-bottom: 4mm;">
        <span style="font-weight: 600;">สิ่งที่ส่งมาด้วย</span>&nbsp;&nbsp;รายงานของ {borrower_fullname} จำนวน ๑ ฉบับ
      </div>

      <!-- ย่อหน้าต้น (เหตุผลและความเป็นมา) -->
      <div class="memo-para">
        เนื่องด้วย กระผม จ.ส.อ. ณัฐชัย&nbsp;&nbsp;รักษาวงษ์ ตำแหน่ง ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒ ขอรายงานการชำรุดและเสียหาย โดยเมื่อวัน {loan_date_thai} {borrower_fullname} ได้มีการเบิก {item_name} จำนวน {qty_thai} รายการ ไปใช้งาน และเกิดเหตุ {cause_text} จึงทำให้ {item_name} เกิดการชำรุดเสียหาย
      </div>

      <!-- ย่อหน้ากลาง (รายละเอียดและผลกระทบ) -->
      <div class="memo-para">
        จากเหตุการณ์ครั้งนี้ มีการตรวจสอบพบว่า ยุทโธปกรณ์มีอาการ{symptom_text} จากความเสียหายดังกล่าว ส่งผลให้ไม่สามารถใช้งานได้ตามปกติ จำนวน {qty_thai} รายการ โดยรายละเอียดได้แนบมาพร้อมกับ รายงานความผิด ของ {borrower_fullname}
      </div>

      <!-- ย่อหน้าท้าย (ข้อพิจารณาและข้อเสนอ) -->
      <div class="memo-para">
        ขออนุมัติการดำเนินการส่งซ่อมตามสายการปรนณิบัติบำรุงต่อไป
      </div>

      <div class="memo-para">
        จึงเรียนมาเพื่อกรุณาพิจารณา
      </div>

      <!-- บล็อกการลงนาม (Signature Block) -->
      {sig_block_html}
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- 2. สำเนาคู่ฉบับ (DUAL COPY PACKAGE)                        -->
  <!-- ======================================================== -->
  <div class="a4-page">
    <div class="copy-banner">(สำเนาคู่ฉบับ)</div>
    <div class="memo-garuda-container">
      <img src="{garuda_src}" alt="ตราครุฑ" class="memo-garuda">
      <div class="memo-title">บันทึกข้อความ</div>
    </div>

    <table class="meta-table">
      <tr>
        <td style="width: 105mm;">
          <span class="meta-label">ส่วนราชการ</span>
          <span class="meta-dots" style="width: calc(100% - 32mm);">ป.๔ พัน.๔ ร้อย.๒ ( โทร. ๓๑๑๙๓ )</span>
        </td>
        <td style="width: 10mm;"></td>
        <td style="width: 75mm;"></td>
      </tr>
      <tr>
        <td>
          <span class="meta-label">ที่</span>
          <span class="meta-dots" style="width: calc(100% - 8mm);">กห ๐๔๘๓.๑.๔.๑/</span>
        </td>
        <td></td>
        <td>
          <span class="meta-label">วันที่</span>
          <span class="meta-dots" style="width: calc(100% - 15mm);">{date_display_thai}</span>
        </td>
      </tr>
      <tr>
        <td colspan="3">
          <span class="meta-label">เรื่อง</span>
          <span class="meta-dots" style="width: calc(100% - 14mm);">รายงานการชำรุดเสียหายของสิ่งและอุปกรณ์ จากการเบิกยืม</span>
        </td>
      </tr>
    </table>

    <div class="memo-body">
      <div style="margin-top: 4mm; margin-bottom: 3mm;">
        <span class="meta-label" style="font-size: 16pt;">เรียน</span>&nbsp;&nbsp;ผบ.ป.๔ พัน.๔ ร้อย.๒
      </div>

      <div style="margin-bottom: 2mm;">
        <span style="font-weight: 600;">อ้างถึง</span>&nbsp;&nbsp;๑. ระเบียบ ทบ. ว่าด้วยการส่งกำลังสิ่งอุปกรณ์ ประเภท ๒ และ ๔ พ.ศ. ๒๕๓๔<br>
        <span style="display: inline-block; width: 13.5mm;"></span>๒. ระเบียบ ทบ. ว่าด้วยการคุมและปรนนิบัติบำรุงยุทโธปกรณ์ สาย สพ.
      </div>

      <div style="margin-bottom: 4mm;">
        <span style="font-weight: 600;">สิ่งที่ส่งมาด้วย</span>&nbsp;&nbsp;รายงานของ {borrower_fullname} จำนวน ๑ ฉบับ
      </div>

      <!-- ย่อหน้าต้น -->
      <div class="memo-para">
        เนื่องด้วย กระผม จ.ส.อ. ณัฐชัย&nbsp;&nbsp;รักษาวงษ์ ตำแหน่ง ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒ ขอรายงานการชำรุดและเสียหาย โดยเมื่อวัน {loan_date_thai} {borrower_fullname} ได้มีการเบิก {item_name} จำนวน {qty_thai} รายการ ไปใช้งาน และเกิดเหตุ {cause_text} จึงทำให้ {item_name} เกิดการชำรุดเสียหาย
      </div>

      <!-- ย่อหน้ากลาง -->
      <div class="memo-para">
        จากเหตุการณ์ครั้งนี้ มีการตรวจสอบพบว่า ยุทโธปกรณ์มีอาการ{symptom_text} จากความเสียหายดังกล่าว ส่งผลให้ไม่สามารถใช้งานได้ตามปกติ จำนวน {qty_thai} รายการ โดยรายละเอียดได้แนบมาพร้อมกับ รายงานความผิด ของ {borrower_fullname}
      </div>

      <!-- ย่อหน้าท้าย -->
      <div class="memo-para">
        ขออนุมัติการดำเนินการส่งซ่อมตามสายการปรนณิบัติบำรุงต่อไป
      </div>

      <div class="memo-para">
        จึงเรียนมาเพื่อกรุณาพิจารณา
      </div>

      <!-- บล็อกการลงนาม (Signature Block) -->
      {sig_block_html}

      <!-- บล็อกเจ้าหน้าที่ทำหนังสือ (Dual-Axis 4 Columns Footer) -->
      <div class="staff-footer-container">
        <div class="staff-row">
          <div class="staff-col-rank">จ.ส.อ.</div>
          <div class="staff-col-role">ร่าง/ตรวจ</div>
          <div class="staff-col-day"></div>
          <div class="staff-col-month"></div>
        </div>
        <div class="staff-row">
          <div class="staff-col-rank">ส.ท.</div>
          <div class="staff-col-role">พิมพ์/ทาน</div>
          <div class="staff-col-day">{to_thai_digits(datetime.now().day)}</div>
          <div class="staff-col-month">{THAI_MONTHS[datetime.now().month]}&nbsp;{to_thai_digits(str(datetime.now().year + 543)[-2:])}</div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>"""

    # Ensure Thai typography zero-width space is inserted
    try:
        from thai_typography_engine import insert_thai_zws
        memo_html = insert_thai_zws(memo_html)
    except Exception:
        pass

    return memo_html
