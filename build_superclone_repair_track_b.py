#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPERCLONE Production Engine
Document: ทบ.๔๐๐-๐๗๑ แบบ ข ใบติดตามใบส่งซ่อม (การเบิกเกิน ๙๐ วัน)
Authority: ระเบียบกองทัพบกว่าด้วยการส่งกำลังสิ่งอุปกรณ์ ประเภท ๒ และ ๔ พ.ศ. ๒๕๓๔
Unit: ป.๔ พัน.๔ ร้อย.๒
Formats: HTML (A4 Landscape Single Page), DOCX (Single Page Landscape), XLSX (Single Sheet)
Standard: RULE-PROD-DOC-ENGINE-V1 / RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard)
Ref Model: REF-REPAIR-TRACK-A-V1
"""

import os
import sys
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

from signature_engine import (
    render_signature_html,
    render_signature_docx,
    render_signature_xlsx,
    is_signature_block
)

# Load SSOT Blueprint
BLUEPRINT_PATH = os.path.join(os.path.dirname(__file__), "table_layout_repair_track_b.json")
with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    bp = json.load(f)

p1_data = bp["page_1_form"]


# ==============================================================================
# 1. HTML GENERATOR (Pixel-Perfect A4 Landscape Single-Page Rebuild)
# ==============================================================================
def generate_html():
    out_html_path = os.path.join(os.path.dirname(__file__), "ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.html")
    
    # Signatures
    left_sig_data = p1_data["signatures"][0]
    right_sig_data = p1_data["signatures"][1]
    
    left_sig_html = render_signature_html({
        "rank": left_sig_data["rank"],
        "name": left_sig_data["name"],
        "position": left_sig_data["position"],
        "date": left_sig_data.get("date", left_sig_data.get("date_text", ""))
    }, margin_left_px=45, gap_pt=20)
    
    right_sig_html = render_signature_html({
        "label": right_sig_data.get("label", ""),
        "rank": right_sig_data["rank"],
        "name": right_sig_data["name"],
        "position": right_sig_data["position"],
        "date": right_sig_data.get("date", right_sig_data.get("date_text", ""))
    }, margin_left_px=45, gap_pt=20)
    
    # Table rows
    table_rows_html = ""
    for r in p1_data["table"]["rows"]:
        table_rows_html += f"""
        <tr>
            <td style="text-align: center; vertical-align: middle;">{r["seq"]}</td>
            <td style="text-align: left; vertical-align: middle; padding-left: 3mm; line-height: 1.25;">{r["item_desc"]}</td>
            <td style="text-align: center; vertical-align: middle;">{r["item_number"]}</td>
            <td style="text-align: center; vertical-align: middle;">{r["doc_ref"]}</td>
            <td style="text-align: center; vertical-align: middle;">{r["doc_date"]}</td>
            <td style="text-align: center; vertical-align: middle;">{r["track_date"]}</td>
            <td style="text-align: left; vertical-align: middle;">{r["notes"]}</td>
        </tr>
        """
        
    blank_rows_count = p1_data["table"].get("blank_rows_count", 9)
    for _ in range(blank_rows_count):
        table_rows_html += """
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp["title"]}</title>
    <style>
        @page landscape-page {{
            size: A4 landscape;
            margin: 0;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        body {{
            margin: 0;
            padding: 20px 0;
            background-color: #525659;
            font-family: 'Sarabun', 'TH Sarabun PSK', 'THSarabunNew', sans-serif;
            font-size: 12pt;
            font-weight: 400;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
            color: #000000;
            line-height: 1.35;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .page-landscape {{
            width: 297mm;
            min-height: 210mm;
            height: 210mm;
            padding: 8mm 12mm 6mm 15mm;
            background-color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            page: landscape-page;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        @media print {{
            body {{
                background-color: transparent;
                padding: 0;
            }}
            .page-landscape {{
                margin-bottom: 0;
                box-shadow: none;
                page-break-after: always;
                break-after: page;
            }}
        }}

        /* Header Layout */
        .form-top-header {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: flex-start;
            margin-bottom: 1.5mm;
        }}
        .doc-title {{
            font-size: 15pt;
            font-weight: bold;
            text-align: center;
            letter-spacing: 0.5px;
            margin-top: 1mm;
        }}
        .header-top-right {{
            text-align: right;
            font-size: 12pt;
            line-height: 1.25;
        }}
        .form-code {{
            font-weight: bold;
            font-size: 12.5pt;
        }}
        .form-subcode {{
            font-size: 11.5pt;
            margin-top: 1px;
        }}

        /* Meta block */
        .meta-block {{
            margin-bottom: 2mm;
            font-size: 12pt;
            line-height: 1.3;
        }}
        .meta-line {{
            margin-bottom: 0.5mm;
        }}
        .meta-label {{
            display: inline-block;
            width: 12mm;
        }}
        .instruction-line {{
            padding-left: 20mm;
            margin-top: 1.5mm;
            margin-bottom: 2mm;
            font-size: 12pt;
        }}

        /* Grid Table (7 columns) */
        .grid-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5pt;
            margin-bottom: 2mm;
        }}
        .grid-table th, .grid-table td {{
            border: 1px solid #000000;
        }}
        .grid-table th {{
            text-align: center;
            font-size: 11pt;
            font-weight: 600;
            background-color: #ffffff;
            vertical-align: middle;
            line-height: 1.28;
            padding: 1.6mm 1mm;
        }}
        .grid-table td {{
            padding: 1.2mm 1.2mm;
            height: 6.8mm;
        }}

        /* Universal Signature Engine Styles (Red Line Standard) */
        .sig-block {{
            position: relative;
            display: inline-block;
            font-family: inherit;
        }}
        .sig-verify {{
            font-weight: bold;
            font-size: 12pt;
            text-align: left;
            margin-bottom: 20pt;
        }}
        .sig-name-pos-group {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 20pt;
        }}
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 18px);
            white-space: nowrap;
            font-size: 12pt;
            line-height: 1.0;
            margin-right: 2px;
        }}
        .sig-name {{
            display: inline-block;
            font-weight: normal;
            font-size: 12pt;
            line-height: 1.15;
            white-space: nowrap;
        }}
        .sig-pos {{
            text-align: center;
            white-space: pre-line;
            line-height: 1.2;
            margin-top: 2px;
            font-size: 12pt;
        }}
        .sig-date {{
            text-align: center;
            margin-top: 3px;
            font-size: 12pt;
            white-space: nowrap;
        }}

        .double-sig-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-top: 4mm;
            padding: 0 15mm;
        }}
        .sig-col-left {{
            width: 45%;
            display: flex;
            justify-content: center;
        }}
        .sig-col-right {{
            width: 45%;
            display: flex;
            justify-content: center;
        }}

        /* Footer Note */
        .footer-note {{
            text-align: center;
            margin-top: 2mm;
            margin-bottom: 1mm;
            font-size: 10.5pt;
        }}
    </style>
</head>
<body>

    <!-- ==================== PAGE: ใบติดตามใบส่งซ่อม แบบ ข (A4 Landscape 1 หน้าจบ) ==================== -->
    <div class="page-landscape">
        <div>
            <!-- Form Top Header -->
            <div class="form-top-header">
                <div></div>
                <div class="doc-title">{p1_data["title"]}</div>
                <div class="header-top-right">
                    <div class="form-code">{p1_data["form_code"]}</div>
                    <div class="form-subcode">{p1_data["form_type"]}</div>
                </div>
            </div>

            <!-- Meta block -->
            <div class="meta-block">
                <div class="meta-line">{p1_data["header_fields"]["doc_number"]}</div>
                <div class="meta-line">{p1_data["header_fields"]["subject"]}</div>
                <div class="meta-line">
                    <span class="meta-label">ถึง</span>
                    <span>{p1_data["header_fields"]["to"]}</span>
                </div>
                <div class="meta-line">
                    <span class="meta-label">จาก</span>
                    <span>{p1_data["header_fields"]["from"]}</span>
                </div>
                <div class="instruction-line">
                    {p1_data["instruction"]}
                </div>
            </div>

            <!-- Table (7 columns) -->
            <table class="grid-table">
                <thead>
                    <tr>
                        <th style="width: 5%;">ลำดับ</th>
                        <th style="width: 19%;">รายการ สป.</th>
                        <th style="width: 15%;">หมายเลข สป.</th>
                        <th style="width: 16%;"><span style="white-space: nowrap;">ที่ใบส่งซ่อม</span><br><span style="white-space: nowrap;">ที่ทะเบียนหน่วยจ่าย</span></th>
                        <th style="width: 14%;"><span style="white-space: nowrap;">วันที่ส่งหรือวาง</span><br><span style="white-space: nowrap;">ใบส่งซ่อม</span></th>
                        <th style="width: 15%;"><span style="white-space: nowrap;">วันติดตามใบส่งซ่อม</span><br><span style="white-space: nowrap;">ครั้งที่ ๓</span></th>
                        <th style="width: 16%;"><span style="white-space: nowrap;">หมายเหตุ</span><br><span style="white-space: nowrap;">(บันทึกโดยหน่วยจ่าย)</span></th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>

        <div>
            <!-- Double Signature Block (Universal Red Line Standard) -->
            <div class="double-sig-row">
                <div class="sig-col-left">
                    {left_sig_html}
                </div>
                <div class="sig-col-right">
                    {right_sig_html}
                </div>
            </div>

            <!-- Footer note (ด้านล่างในหน้าเดียวกัน) -->
            <div class="footer-note">
                {p1_data["footer_note"]}
            </div>
        </div>
    </div>

</body>
</html>
"""
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[HTML] Built: {out_html_path}")


# ==============================================================================
# 2. DOCX GENERATOR (Word Single Page Landscape Rebuild)
# ==============================================================================
def set_cell_margins(cell, top=50, bottom=50, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'auto'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def generate_docx():
    out_docx_path = os.path.join(os.path.dirname(__file__), "ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.docx")
    doc = Document()
    font_name = "TH Sarabun PSK"
    
    # Page Setup (A4 Landscape)
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width = Inches(11.69)
    sec.page_height = Inches(8.27)
    sec.top_margin = Inches(0.35)
    sec.bottom_margin = Inches(0.25)
    sec.left_margin = Inches(0.59)
    sec.right_margin = Inches(0.47)
    
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, size=12, space_before=0, space_after=0, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = font_name
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    # Top Header 3 Columns Table
    t_hdr = doc.add_table(rows=1, cols=3)
    t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr.autofit = False
    
    c_left = t_hdr.rows[0].cells[0]
    c_mid = t_hdr.rows[0].cells[1]
    c_right = t_hdr.rows[0].cells[2]
    
    c_left.width = Inches(3.0)
    c_mid.width = Inches(4.7)
    c_right.width = Inches(3.0)
    
    # Title Mid
    p_title = c_mid.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(0)
    r_t = p_title.add_run(p1_data["title"])
    r_t.font.name = font_name
    r_t.font.size = Pt(15)
    r_t.font.bold = True
    
    # Code Right
    p_code1 = c_right.paragraphs[0]
    p_code1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_code1.paragraph_format.space_before = Pt(0)
    p_code1.paragraph_format.space_after = Pt(0)
    r_c1 = p_code1.add_run(p1_data["form_code"])
    r_c1.font.name = font_name
    r_c1.font.size = Pt(12)
    r_c1.font.bold = True
    
    p_code2 = c_right.add_paragraph()
    p_code2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_code2.paragraph_format.space_before = Pt(0)
    p_code2.paragraph_format.space_after = Pt(0)
    r_c2 = p_code2.add_run(p1_data["form_type"])
    r_c2.font.name = font_name
    r_c2.font.size = Pt(11)
    
    # Meta Block
    add_p(p1_data["header_fields"]["doc_number"], size=12, space_before=2, space_after=1)
    add_p(p1_data["header_fields"]["subject"], size=12, space_before=0, space_after=1)
    
    # ถึง & จาก
    p_to = add_p("ถึง    ", size=12, space_before=0, space_after=1)
    r_to_val = p_to.add_run(p1_data["header_fields"]["to"])
    r_to_val.font.name = font_name
    r_to_val.font.size = Pt(12)
    
    p_from = add_p("จาก  ", size=12, space_before=0, space_after=1)
    r_from_val = p_from.add_run(p1_data["header_fields"]["from"])
    r_from_val.font.name = font_name
    r_from_val.font.size = Pt(12)
    
    # Instruction Text with indent
    add_p(f"        {p1_data['instruction']}", size=12, space_before=2, space_after=4)
    
    # Main Table (7 cols: 5%, 19%, 15%, 16%, 14%, 15%, 16%)
    col_widths = [Inches(0.53), Inches(2.05), Inches(1.60), Inches(1.70), Inches(1.50), Inches(1.60), Inches(1.75)]
    total_rows = 1 + len(p1_data["table"]["rows"]) + p1_data["table"].get("blank_rows_count", 9)
    t_main = doc.add_table(rows=total_rows, cols=7)
    t_main.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_main.autofit = False
    
    # Headers
    headers = [
        "ลำดับ",
        "รายการ สป.",
        "หมายเลข สป.",
        "ที่ใบส่งซ่อม\nที่ทะเบียนหน่วยจ่าย",
        "วันที่ส่งหรือวาง\nใบส่งซ่อม",
        "วันติดตามใบส่งซ่อม\nครั้งที่ ๓",
        "หมายเหตุ\n(บันทึกโดยหน่วยจ่าย)"
    ]
    
    hdr_row = t_main.rows[0]
    for idx, (title, w) in enumerate(zip(headers, col_widths)):
        cell = hdr_row.cells[idx]
        cell.width = w
        set_cell_border(cell, top={'sz': 4}, bottom={'sz': 4}, left={'sz': 4}, right={'sz': 4})
        set_cell_margins(cell, top=65, bottom=65, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.25
        r = p.add_run(title)
        r.font.name = font_name
        r.font.size = Pt(11)
        r.font.bold = True
        
    # Data Row (Row 1)
    data_row = t_main.rows[1]
    row_data = p1_data["table"]["rows"][0]
    row_values = [
        (row_data["seq"], WD_ALIGN_PARAGRAPH.CENTER),
        (row_data["item_desc"].replace("<br>", "\n"), WD_ALIGN_PARAGRAPH.LEFT),
        (row_data["item_number"], WD_ALIGN_PARAGRAPH.CENTER),
        (row_data["doc_ref"], WD_ALIGN_PARAGRAPH.CENTER),
        (row_data["doc_date"], WD_ALIGN_PARAGRAPH.CENTER),
        (row_data["track_date"], WD_ALIGN_PARAGRAPH.CENTER),
        (row_data["notes"], WD_ALIGN_PARAGRAPH.LEFT)
    ]
    
    for idx, ((val, align), w) in enumerate(zip(row_values, col_widths)):
        cell = data_row.cells[idx]
        cell.width = w
        set_cell_border(cell, top={'sz': 4}, bottom={'sz': 4}, left={'sz': 4}, right={'sz': 4})
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(val)
        r.font.name = font_name
        r.font.size = Pt(11.5)
        
    # Blank Rows (Row 2 to total_rows - 1)
    for r_idx in range(2, total_rows):
        b_row = t_main.rows[r_idx]
        for c_idx, w in enumerate(col_widths):
            cell = b_row.cells[c_idx]
            cell.width = w
            set_cell_border(cell, top={'sz': 4}, bottom={'sz': 4}, left={'sz': 4}, right={'sz': 4})
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run("")
            r.font.name = font_name
            r.font.size = Pt(11.5)
            
    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(0)
    
    # Double Signature Block Table (2 columns)
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = False
    
    c_sig_left = t_sig.rows[0].cells[0]
    c_sig_right = t_sig.rows[0].cells[1]
    
    c_sig_left.width = Inches(5.3)
    c_sig_right.width = Inches(5.3)
    
    # Left Sig (ผบ.ร้อย)
    render_signature_docx(
        target=c_sig_left,
        sig=p1_data["signatures"][0],
        axis_inch=1.5,
        font_name=font_name,
        font_size=12,
        space_after_rank_pt=20
    )
    
    # Right Sig (จ.ส.อ.)
    render_signature_docx(
        target=c_sig_right,
        sig=p1_data["signatures"][1],
        axis_inch=1.5,
        font_name=font_name,
        font_size=12,
        space_after_rank_pt=20
    )
    
    # Footer Note
    p_ft = doc.add_paragraph()
    p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ft.paragraph_format.space_before = Pt(8)
    p_ft.paragraph_format.space_after = Pt(0)
    r_ft = p_ft.add_run(p1_data["footer_note"])
    r_ft.font.name = font_name
    r_ft.font.size = Pt(10.5)
    
    doc.save(out_docx_path)
    print(f"[DOCX] Built: {out_docx_path}")


# ==============================================================================
# 3. XLSX GENERATOR (Excel Single Sheet Rebuild)
# ==============================================================================
def generate_xlsx():
    out_xlsx_path = os.path.join(os.path.dirname(__file__), "ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.xlsx")
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "ใบติดตามใบส่งซ่อม (แบบ ข)"
    
    # Page Setup
    ws1.page_setup.orientation = ws1.ORIENTATION_LANDSCAPE
    ws1.page_setup.paperSize = ws1.PAPERSIZE_A4
    ws1.page_setup.fitToPage = True
    ws1.page_setup.fitToWidth = 1
    ws1.page_setup.fitToHeight = 1
    ws1.sheet_properties.pageSetUpPr.fitToPage = True
    
    font_name = "TH Sarabun PSK"
    f_title = Font(name=font_name, size=15, bold=True)
    f_header = Font(name=font_name, size=12, bold=True)
    f_normal = Font(name=font_name, size=12)
    f_tbl_hdr = Font(name=font_name, size=11, bold=True)
    f_tbl_body = Font(name=font_name, size=11.5)
    f_footer = Font(name=font_name, size=10.5)
    
    thin_border_side = Side(border_style="thin", color="000000")
    thin_box = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    
    # Columns: A (Seq 5%), B (Desc 19%), C (Num 15%), D (Ref 16%), E (Date 14%), F (Track 15%), G (Notes 16%)
    col_widths = {
        "A": 7,
        "B": 23,
        "C": 18,
        "D": 20,
        "E": 18,
        "F": 20,
        "G": 22
    }
    for col, width in col_widths.items():
        ws1.column_dimensions[col].width = width
        
    # Row 1: Header Top Right (Form Code) & Title Center
    ws1["A1"] = p1_data["title"]
    ws1["A1"].font = f_title
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("A1:F1")
    
    ws1["G1"] = p1_data["form_code"]
    ws1["G1"].font = f_header
    ws1["G1"].alignment = Alignment(horizontal="right", vertical="center")
    
    ws1["G2"] = p1_data["form_type"]
    ws1["G2"].font = f_normal
    ws1["G2"].alignment = Alignment(horizontal="right", vertical="center")
    
    # Fields Left (Rows 3 - 6)
    ws1["A3"] = p1_data["header_fields"]["doc_number"]
    ws1["A3"].font = f_normal
    ws1.merge_cells("A3:D3")
    
    ws1["A4"] = p1_data["header_fields"]["subject"]
    ws1["A4"].font = f_normal
    ws1.merge_cells("A4:D4")
    
    ws1["A5"] = f"ถึง    {p1_data['header_fields']['to']}"
    ws1["A5"].font = f_normal
    ws1.merge_cells("A5:D5")
    
    ws1["A6"] = f"จาก  {p1_data['header_fields']['from']}"
    ws1["A6"].font = f_normal
    ws1.merge_cells("A6:D6")
        
    # Instruction Text (Row 7)
    ws1["A7"] = f"        {p1_data['instruction']}"
    ws1["A7"].font = f_normal
    ws1["A7"].alignment = Alignment(horizontal="left", vertical="center")
    ws1.merge_cells("A7:G7")
    
    # Main Table Headers (Row 9)
    headers = [
        ("A", "ลำดับ"),
        ("B", "รายการ สป."),
        ("C", "หมายเลข สป."),
        ("D", "ที่ใบส่งซ่อม\nที่ทะเบียนหน่วยจ่าย"),
        ("E", "วันที่ส่งหรือวาง\nใบส่งซ่อม"),
        ("F", "วันติดตามใบส่งซ่อม\nครั้งที่ ๓"),
        ("G", "หมายเหตุ\n(บันทึกโดยหน่วยจ่าย)")
    ]
    ws1.row_dimensions[9].height = 36
    for col, txt in headers:
        cell = ws1[f"{col}9"]
        cell.value = txt
        cell.font = f_tbl_hdr
        cell.border = thin_box
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
    # Data Row (Row 10)
    ws1.row_dimensions[10].height = 28
    row_data = p1_data["table"]["rows"][0]
    
    row_cells = [
        ("A", row_data["seq"], "center"),
        ("B", row_data["item_desc"].replace("<br>", "\n"), "left"),
        ("C", row_data["item_number"], "center"),
        ("D", row_data["doc_ref"], "center"),
        ("E", row_data["doc_date"], "center"),
        ("F", row_data["track_date"], "center"),
        ("G", row_data["notes"], "left")
    ]
    for col, val, align in row_cells:
        cell = ws1[f"{col}10"]
        cell.value = val
        cell.font = f_tbl_body
        cell.border = thin_box
        cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
        
    # Blank Rows (Rows 11 to 19)
    for r in range(11, 20):
        ws1.row_dimensions[r].height = 20
        for col_letter in ["A", "B", "C", "D", "E", "F", "G"]:
            cell = ws1[f"{col_letter}{r}"]
            cell.value = ""
            cell.border = thin_box
            
    # Double Signature Block (Row 22 - 26)
    left_sig = p1_data["signatures"][0]
    right_sig = p1_data["signatures"][1]
    
    # Left Sig: Rank B22, Name B23, Pos B24, Date B25
    ws1["B22"] = left_sig["rank"]
    ws1["B22"].font = f_normal
    ws1["B22"].alignment = Alignment(horizontal="right", vertical="center")
    
    ws1["C22"] = left_sig["name"]
    ws1["C22"].font = f_normal
    ws1["C22"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws1["B23"] = left_sig["position"]
    ws1["B23"].font = f_normal
    ws1["B23"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("B23:C23")
    
    ws1["B24"] = f"          {left_sig['date']}"
    ws1["B24"].font = f_normal
    ws1["B24"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("B24:C24")
    
    # Right Sig: Rank E22, Name F22, Pos E23:F23, Date E24:F24
    ws1["E22"] = right_sig["rank"]
    ws1["E22"].font = f_normal
    ws1["E22"].alignment = Alignment(horizontal="right", vertical="center")
    
    ws1["F22"] = right_sig["name"]
    ws1["F22"].font = f_normal
    ws1["F22"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws1["E23"] = right_sig["position"]
    ws1["E23"].font = f_normal
    ws1["E23"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("E23:F23")
    
    ws1["E24"] = f"          {right_sig['date']}"
    ws1["E24"].font = f_normal
    ws1["E24"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("E24:F24")
    
    # Footer Note (Row 26)
    ws1["A26"] = p1_data["footer_note"]
    ws1["A26"].font = f_footer
    ws1["A26"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.merge_cells("A26:G26")
    
    wb.save(out_xlsx_path)
    print(f"[XLSX] Built: {out_xlsx_path}")


if __name__ == "__main__":
    generate_html()
    generate_docx()
    generate_xlsx()
    print("All SUPERCLONE documents generated successfully for แบบ ข!")
