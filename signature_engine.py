# -*- coding: utf-8 -*-
"""
===============================================================================
UNIVERSAL SIGNATURE BLOCK ENGINE (signature_engine.py)
Standard: RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard)
Architecture: Single Source of Truth for Signature Rendering across HTML, DOCX, XLSX
===============================================================================
กฎเหล็ก:
1. จุด '.' ตัวสุดท้ายของยศ ต้องอยู่ตรงกับแนวเส้นดิ่งเดียวกันกับเครื่องหมาย '(' ของชื่อเป๊ะ 100%
2. ห้ามจับยศไปจัดกึ่งกลาง (Center-align) ร่วมกับชื่อใน DOCX และ XLSX เด็ดขาด
3. ระหว่างบรรทัดชื่อและตำแหน่ง ห่างกัน 1 Enter (Space After = 0 pt)
"""

import re
from typing import Dict, Any, Optional

# Docx imports (conditional / resilient)
try:
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
except ImportError:
    pass

# OpenPyXL imports
try:
    from openpyxl.styles import Font, Alignment
except ImportError:
    pass


# -----------------------------------------------------------------------------
# 1. AUTONOMOUS SIGNATURE DETECTION (HEURISTIC ENGINE)
# -----------------------------------------------------------------------------
RANK_REGEX = re.compile(
    r"(พล\.อ\.|พล\.ท\.|พล\.ต\.|พ\.อ\.|พ\.ท\.|พ\.ต\.|ร\.อ\.|ร\.ท\.|ร\.ต\.|"
    r"จ\.ส\.อ\.|จ\.ส\.ท\.|จ\.ส\.ต\.|ส\.อ\.|ส\.ท\.|ส\.ต\.|นาย|นาง|นางสาว|น\.ส\.)"
)

ROLE_REGEX = re.compile(
    r"(ผู้ตรวจสอบ|ผู้ตรวจ|ผู้เบิก|ผู้จ่าย|ผู้รับ|ผู้ส่ง|ตรวจถูกต้อง|รับรองความถูกต้อง|"
    r"ผบ\.ร้อย|ผบ\.พัน|ผบ\.หน่วย|หน\.คลัง|เจ้าหน้าที่บันทึก|นายทหาร)"
)

DOTTED_SIGNATURE_REGEX = re.compile(
    r"(\(ลงชื่อ\)|\.{4,}|…{2,})"
)

NAME_IN_PAREN_REGEX = re.compile(
    r"\([ก-๙a-zA-Z\s\.]+\)"
)


def is_signature_block(data: Any) -> bool:
    """
    ตรวจสอบว่าข้อมูลนี้เข้าข่ายเป็น 'บล็อกการลงนาม' (Signature Block) หรือไม่
    Pattern ก: มียศ/คำนำหน้า + ชื่อในวงเล็บ + ตำแหน่ง
    Pattern ข: มีคำกำกับบทบาท/คำรับรอง (เช่น ผู้ตรวจสอบ, ตรวจถูกต้อง)
    Pattern ค: มีบล็อกเติมคำลงนาม (ลงชื่อ).........
    """
    if isinstance(data, dict):
        if data.get("type") == "signature_block":
            return True
        if any(k in data for k in ["rank", "full_name", "position", "verification_text"]):
            return True
        text_dump = " ".join(str(v) for v in data.values())
    elif isinstance(data, str):
        text_dump = data
    else:
        return False

    has_rank = bool(RANK_REGEX.search(text_dump))
    has_name_paren = bool(NAME_IN_PAREN_REGEX.search(text_dump))
    has_role = bool(ROLE_REGEX.search(text_dump))
    has_dotted = bool(DOTTED_SIGNATURE_REGEX.search(text_dump))

    # เข้าข่ายบล็อกลงนามเมื่อตรงเงื่อนไข
    if has_rank and (has_name_paren or has_role):
        return True
    if has_role and (has_name_paren or has_dotted):
        return True
    if has_dotted and (has_rank or has_role):
        return True

    return False


# -----------------------------------------------------------------------------
# 2. HTML RENDERER (CSS RED LINE STANDARD)
# -----------------------------------------------------------------------------
def render_signature_html(sig: Dict[str, Any], margin_left_px: int = 55, gap_pt: int = 22, font_size_pt: int = 12) -> str:
    """
    เรนเดอร์ HTML ด้วย Signature Block Engine v1.0
    จุด . ท้ายยศ ชนกับ ( ของชื่อเป๊ะ 100% ด้วย .sig-rank-anchor { right: 100% }
    คำกำกับบทบาท (เช่น ผู้แก้ไข, ผู้ตรวจ) และคำรับรอง (เช่น ตรวจถูกต้อง)
    อยู่เหนือยศไปทางซ้าย โดยตัวอักษรสุดท้ายตรงกับแนวอักษรสุดท้ายของยศ (right: 100%)
    """
    label_html = ""
    lbl_text = sig.get("label") or sig.get("verification_text")
    if lbl_text:
        label_html = f'<span class="sig-label-anchor" style="position: absolute; right: 100%; bottom: calc(100% + {gap_pt}pt + 18pt); text-align: right; font-weight: bold; font-size: {font_size_pt}pt; white-space: nowrap;">{lbl_text}</span>'
    elif sig.get("placeholder_height"):
        label_html = f'<div style="height: {sig.get("placeholder_height", "12pt")}; margin-bottom: 24pt;">&nbsp;</div>'

    rank = sig.get("rank", "")
    name = sig.get("name") or sig.get("full_name", "")
    if name and not name.startswith("("):
        name = f"({name})"
    position = sig.get("position", "")
    date_str = sig.get("date", "")
    date_html = ""
    if date_str:
        date_html = f'<div class="sig-date" style="margin-top: 4px; font-size: {font_size_pt}pt; text-align: center; white-space: nowrap;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{date_str}</div>'

    role = sig.get("role", "")
    role_html = ""
    if role:
        role_html = f'<span class="sig-role-anchor" style="position: absolute; right: 100%; bottom: calc(100% + {gap_pt}pt + 18pt); text-align: right; font-weight: bold; font-size: {font_size_pt}pt; white-space: nowrap;">{role}</span>'

    html = f"""
    <div class="sig-block" style="font-size: {font_size_pt}pt; line-height: 1.0;">
        <div class="sig-name-pos-group" style="margin-left: {margin_left_px}px;">
            <div class="sig-name-wrapper" style="margin-top: {gap_pt}pt;">
                {label_html}
                {role_html}
                <span class="sig-rank-anchor" style="font-size: {font_size_pt}pt;">{rank}</span>
                <div class="sig-name" style="font-size: {font_size_pt}pt;">{name}</div>
            </div>
            <div class="sig-pos" style="font-size: {font_size_pt}pt;">{position}</div>
            {date_html}
        </div>
    </div>
    """
    return html.strip()


# -----------------------------------------------------------------------------
# 3. DOCX RENDERER (TAB STOP RED LINE STANDARD)
# -----------------------------------------------------------------------------
def render_signature_docx(
    target,  # docx Document or Table Cell
    sig: Dict[str, Any],
    axis_inch: float = 3.0,
    font_name: str = "TH Sarabun PSK",
    font_size: int = 12,
    space_after_rank_pt: int = 22,
    space_before_block_pt: int = 0
):
    """
    เรนเดอร์บล็อกลงนามลงใน Word (.docx) ตาม Universal Red Line Standard
    - ใช้ Tab Stop ชิดขวา (WD_TAB_ALIGNMENT.RIGHT) ที่แนวแกนดิ่ง ทำให้จุด '.' ท้ายยศชนแกนเป๊ะ 100%
    - คำรับรองและคำกำกับบทบาทอยู่เหนือยศ ชิดขวาชนแกนดิ่งเดียวกัน (WD_TAB_ALIGNMENT.RIGHT)
    - ใช้ Tab Stop ชิดซ้าย (WD_TAB_ALIGNMENT.LEFT) ที่แนวแกนดิ่ง ทำให้ '(' ของชื่อเริ่มต้นที่แกนเป๊ะ 100%
    - ตำแหน่งและวันที่จัดกึ่งกลางใต้ชื่อ (Space After = 0 pt)
    - ห้ามจัด Center รวบยศกับชื่อเด็ดขาด!
    """
    def set_font(run, size_pt, bold=False):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold

    # 1. Label / Verification text (ถ้ามี)
    lbl = sig.get("label") or sig.get("verification_text")
    if lbl:
        p_lbl = target.add_paragraph() if hasattr(target, "add_paragraph") else target.paragraphs[0]
        p_lbl.paragraph_format.tab_stops.add_tab_stop(Inches(axis_inch), WD_TAB_ALIGNMENT.RIGHT)
        p_lbl.paragraph_format.space_before = Pt(space_before_block_pt)
        p_lbl.paragraph_format.space_after = Pt(2)
        r_lbl = p_lbl.add_run(f"\t{lbl}")
        set_font(r_lbl, font_size, bold=True)
    elif sig.get("add_top_spacer"):
        p_sp = target.add_paragraph() if hasattr(target, "add_paragraph") else target.paragraphs[0]
        p_sp.paragraph_format.space_after = Pt(16)
        p_sp.add_run("")

    # 1.5 Role (ผู้แก้ไข / ผู้ตรวจ - เหนือยศ ชนแกนขวา)
    role = sig.get("role")
    if role:
        p_role = target.add_paragraph()
        p_role.paragraph_format.tab_stops.add_tab_stop(Inches(axis_inch), WD_TAB_ALIGNMENT.RIGHT)
        p_role.paragraph_format.space_before = Pt(space_before_block_pt if not lbl and not sig.get("add_top_spacer") else 0)
        p_role.paragraph_format.space_after = Pt(2)
        r_role = p_role.add_run(f"\t{role}")
        set_font(r_role, font_size, bold=True)

    # 2. Rank (Right-aligned to Axis)
    p_rk = target.add_paragraph()
    p_rk.paragraph_format.tab_stops.add_tab_stop(Inches(axis_inch), WD_TAB_ALIGNMENT.RIGHT)
    p_rk.paragraph_format.space_before = Pt(0)
    p_rk.paragraph_format.space_after = Pt(space_after_rank_pt) # เว้นลงลายมือชื่อจริง
    r_rk = p_rk.add_run(f"\t{sig.get('rank', '')}")
    set_font(r_rk, font_size, bold=False)

    # 3. Name (Left-aligned to Axis)
    name = sig.get("name") or sig.get("full_name", "")
    if name and not name.startswith("("):
        name = f"({name})"
    p_nm = target.add_paragraph()
    p_nm.paragraph_format.tab_stops.add_tab_stop(Inches(axis_inch), WD_TAB_ALIGNMENT.LEFT)
    p_nm.paragraph_format.space_before = Pt(0)
    p_nm.paragraph_format.space_after = Pt(0)
    r_nm = p_nm.add_run(f"\t{name}")
    set_font(r_nm, font_size, bold=False)

    # 4. Position (Centered under Name, Space After = 0 pt)
    # คำนวณจุดกึ่งกลางของชื่อโดยเฉลี่ย
    name_center_offset = Inches(0.70 if font_size <= 12 else 0.95)
    name_center_axis = Inches(axis_inch) + name_center_offset

    pos = sig.get("position", "")
    if pos:
        pos_lines = [l.strip() for l in pos.replace("<br>", "\n").split("\n") if l.strip()]
        for line in pos_lines:
            p_pos = target.add_paragraph()
            p_pos.paragraph_format.tab_stops.add_tab_stop(name_center_axis, WD_TAB_ALIGNMENT.CENTER)
            p_pos.paragraph_format.space_before = Pt(0)
            p_pos.paragraph_format.space_after = Pt(0)
            r_pos = p_pos.add_run(f"\t{line}")
            set_font(r_pos, font_size, bold=False)

    # 5. Date (Centered under Name with space for day)
    date_val = sig.get("date", "")
    if date_val:
        p_dt = target.add_paragraph()
        p_dt.paragraph_format.tab_stops.add_tab_stop(name_center_axis, WD_TAB_ALIGNMENT.CENTER)
        p_dt.paragraph_format.space_before = Pt(0)
        p_dt.paragraph_format.space_after = Pt(0)
        date_text = date_val if date_val.startswith(" ") else f"          {date_val}"
        r_dt = p_dt.add_run(f"\t{date_text}")
        set_font(r_dt, font_size, bold=False)


# -----------------------------------------------------------------------------
# 4. XLSX RENDERER (SPLIT-CELL RED LINE STANDARD)
# -----------------------------------------------------------------------------
def render_signature_xlsx(
    ws,
    sig: Dict[str, Any],
    start_row: int,
    rank_col: str,
    name_col: str,
    font_name: str = "TH Sarabun PSK",
    font_size: int = 12
):
    """
    เรนเดอร์บล็อกลงนามลงใน Excel (.xlsx) ตาม Universal Red Line Standard
    - ยศ อยู่ใน rank_col (Right-aligned แตะเส้นแบ่งคอลัมน์)
    - ชื่อ อยู่ใน name_col (Left-aligned แตะเส้นแบ่งคอลัมน์)
    - ตำแหน่ง และ วันที่ Merge ข้าม rank_col:name_col และจัด Center
    """
    f_reg = Font(name=font_name, size=font_size)
    f_bold = Font(name=font_name, size=font_size, bold=True)
    align_center = Alignment(horizontal="center", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")

    curr_row = start_row

    # 1. Label (ถ้ามี - อยู่เหนือยศ ชิดขวาแตะเส้นแบ่งคอลัมน์)
    lbl = sig.get("label") or sig.get("verification_text")
    if lbl:
        ws[f"{rank_col}{curr_row}"] = lbl
        ws[f"{rank_col}{curr_row}"].font = f_bold
        ws[f"{rank_col}{curr_row}"].alignment = align_right
        curr_row += 1

    # 1.5 Role (ผู้แก้ไข / ผู้ตรวจ - อยู่เหนือยศ ชิดขวาแตะเส้นแบ่งคอลัมน์)
    role = sig.get("role")
    if role:
        ws[f"{rank_col}{curr_row}"] = role
        ws[f"{rank_col}{curr_row}"].font = f_bold
        ws[f"{rank_col}{curr_row}"].alignment = align_right
        curr_row += 1

    # 2. Rank & Name (จุด . ท้ายยศ แตะ ( ของชื่อ ผ่านเส้นขอบเซลล์)
    ws[f"{rank_col}{curr_row}"] = sig.get("rank", "")
    ws[f"{rank_col}{curr_row}"].font = f_reg
    ws[f"{rank_col}{curr_row}"].alignment = align_right

    name = sig.get("name") or sig.get("full_name", "")
    if name and not name.startswith("("):
        name = f"({name})"
    ws[f"{name_col}{curr_row}"] = name
    ws[f"{name_col}{curr_row}"].font = f_reg
    ws[f"{name_col}{curr_row}"].alignment = align_left
    curr_row += 1

    # 3. Position (Merged Center)
    pos = sig.get("position", "")
    if pos:
        pos_lines = [l.strip() for l in pos.replace("<br>", "\n").split("\n") if l.strip()]
        for pline in pos_lines:
            ws[f"{rank_col}{curr_row}"] = pline
            ws[f"{rank_col}{curr_row}"].font = f_reg
            ws[f"{rank_col}{curr_row}"].alignment = align_center
            ws.merge_cells(f"{rank_col}{curr_row}:{name_col}{curr_row}")
            curr_row += 1


    # 4. Date (Merged Center with space for day)
    date_val = sig.get("date", "")
    if date_val:
        date_text = date_val if date_val.startswith(" ") else f"          {date_val}"
        ws[f"{rank_col}{curr_row}"] = date_text
        ws[f"{rank_col}{curr_row}"].font = f_reg
        ws[f"{rank_col}{curr_row}"].alignment = align_center
        ws.merge_cells(f"{rank_col}{curr_row}:{name_col}{curr_row}")
        curr_row += 1
