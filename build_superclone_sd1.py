#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPERCLONE Production Engine
Document: บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (สด.๑)
Authority: ระเบียบ ทบ. ว่าด้วยการตรวจอาวุธฯ พ.ศ. ๒๔๙๗ / คำสั่ง พล.ร.๔ ที่ ๓๙๔/๒๕๖๙
Unit: ป.๔ พัน.๔ ร้อย.๒
Formats: HTML (Pixel-Perfect 5-Page Mixed Orientation), DOCX (5 Pages / Sections), XLSX (4 Sheets)
Standard: RULE-PROD-DOC-ENGINE-V1 / RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard)
"""

import os
import sys
import json
import base64

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
BLUEPRINT_PATH = os.path.join(os.path.dirname(__file__), "table_layout_sd1.json")
with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    bp = json.load(f)

# Garuda Crest
GARUDA_PATH = os.path.join(os.path.dirname(__file__), "garuda_vector_official.png")
if not os.path.exists(GARUDA_PATH):
    GARUDA_PATH = os.path.join(os.path.dirname(__file__), "garuda_tr.png")

with open(GARUDA_PATH, "rb") as f:
    GARUDA_B64 = base64.b64encode(f.read()).decode("utf-8")

# Photo Assets for Page 4
PHOTO_B64S = []
for rel_path in bp["photo_sheet"]["images"]:
    full_path = os.path.join(os.path.dirname(__file__), rel_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as pf:
            PHOTO_B64S.append(base64.b64encode(pf.read()).decode("utf-8"))
    else:
        PHOTO_B64S.append("")


# =============================================================================
# 1. GENERATE HTML (5 Pages Hybrid Multi-Page Document)
# =============================================================================
def generate_html(output_path):
    p1 = bp["page_1_memo"]
    sd1 = bp["inspection_form_sd1"]
    ps = bp["photo_sheet"]
    gr = bp["gun_inspection_record"]

    # Signatures HTML using signature_engine
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    p1_sig_html = render_signature_html(p1_sig_data, margin_left_px=55, gap_pt=24)

    # Page 5 Gun Record Signature
    gr_sig = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"],
        "date": gr["signature"]["date_text"]
    }
    gr_sig_html = render_signature_html(gr_sig, margin_left_px=50, gap_pt=22)

    # Build Attachments List
    att_rows_html = ""
    for att in p1["attachments"]:
        att_rows_html += f"""
        <div class="memo-att-row">
            <div class="memo-att-desc"><b>{att["num"]}</b> {att["desc"]}</div>
            <div class="memo-att-qty">{att["qty"]}</div>
        </div>
        """

    # Build Page 2 Table Rows (Section 1 + Section 2.1)
    s1 = sd1["section_1"]
    s2 = sd1["section_2"]
    sub1 = s2["subsections"][0]
    sub2 = s2["subsections"][1]

    # Section 1 Rows
    s1_rows_html = f"""
    <tr>
        <td class="text-center font-bold">{s1["id"]}</td>
        <td class="font-bold">{s1["title"]}</td>
        <td></td>
    </tr>
    """
    for it in s1["items"]:
        s1_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["code"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 2.1 Rows
    s2_rows_html = f"""
    <tr>
        <td class="text-center font-bold">{s2["id"]}</td>
        <td class="font-bold">{s2["title"]}</td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td class="font-bold" style="padding-left: 4mm;">{sub1["subtitle"]}</td>
        <td></td>
    </tr>
    """
    for it in sub1["items"]:
        s2_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["bullet"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 2.2 Rows for Page 3
    s2_2_rows_html = f"""
    <tr>
        <td class="text-center font-bold"></td>
        <td class="font-bold" style="padding-left: 4mm;">{sub2["subtitle"]}</td>
        <td></td>
    </tr>
    """
    for it in sub2["items"]:
        s2_2_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["bullet"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 3 Rows
    s3 = sd1["section_3"]
    s3_rows_html = f"""
    <tr>
        <td class="text-center font-bold">{s3["id"]}</td>
        <td class="font-bold">{s3["title"]}</td>
        <td></td>
    </tr>
    """
    for it in s3["items"]:
        s3_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["code"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 4 Rows
    s4 = sd1["section_4"]
    s4_rows_html = f"""
    <tr>
        <td class="text-center font-bold">{s4["id"]}</td>
        <td class="font-bold">{s4["title"]}</td>
        <td></td>
    </tr>
    """
    for it in s4["items"]:
        s4_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["code"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 5 Rows
    s5 = sd1["section_5"]
    s5_rows_html = f"""
    <tr>
        <td class="text-center font-bold">{s5["id"]}</td>
        <td class="font-bold">{s5["title"]}</td>
        <td></td>
    </tr>
    """
    for it in s5["items"]:
        s5_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 8mm;">{it["code"]} {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Page 4 Photo Grid
    photos_html = ""
    for b64_img in PHOTO_B64S:
        if b64_img:
            photos_html += f"""
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{b64_img}" class="photo-img" alt="ภาพถ่ายการตรวจ">
            </div>
            """

    # Page 5 Gun Record Table Rows
    gr_rows_html = ""
    for idx, it in enumerate(gr["items"]):
        if idx == 0:
            gr_rows_html += f"""
            <tr>
                <td rowspan="5" class="text-center" style="vertical-align: middle; white-space: pre-line;">{gr["date_col"]}</td>
                <td>{it["topic"]}</td>
                <td class="text-center">{it["found"]}</td>
                <td class="text-center">{it["fix_needed"]}</td>
                <td class="text-center">{it["resolution"]}</td>
                <td>{it["note"]}</td>
            </tr>
            """
        else:
            gr_rows_html += f"""
            <tr>
                <td>{it["topic"]}</td>
                <td class="text-center">{it["found"]}</td>
                <td class="text-center">{it["fix_needed"]}</td>
                <td class="text-center">{it["resolution"]}</td>
                <td>{it["note"]}</td>
            </tr>
            """

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp["title"]}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        @page portrait-page {{
            size: A4 portrait;
            margin: 0;
        }}
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
            font-weight: 300;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
            color: #000000;
            line-height: 1.4;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .page-portrait {{
            width: 210mm;
            min-height: 297mm;
            padding: 20mm 20mm 20mm 25mm; /* ขอบซ้าย 25mm สำหรับเย็บเล่ม */
            background-color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            page: portrait-page;
        }}
        .page-landscape {{
            width: 297mm;
            min-height: 210mm;
            padding: 18mm 20mm 18mm 25mm;
            background-color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            page: landscape-page;
        }}
        @media print {{
            body {{
                background-color: #ffffff;
                padding: 0;
            }}
            .page-portrait, .page-landscape {{
                margin: 0;
                box-shadow: none;
                page-break-after: always;
            }}
        }}

        /* UTILITIES */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        .font-bold {{ font-weight: bold; }}
        .font-normal {{ font-weight: normal; }}

        /* ================= PAGE 1: MEMO ================= */
        .memo-copy-label {{
            position: absolute;
            top: 10mm;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 12pt;
            line-height: 1.2;
        }}
        .memo-header-container {{
            position: relative;
            width: 100%;
            height: 30mm;
            margin-top: 2mm;
        }}
        .memo-garuda {{
            position: absolute;
            left: 0;
            top: 0;
            width: 30mm;
            height: 30mm;
            object-fit: contain;
        }}
        .memo-title {{
            position: absolute;
            left: 0;
            right: 0;
            top: 6mm;
            text-align: center;
            font-size: 24pt;
            font-weight: bold;
            line-height: 1;
            font-family: 'TH Sarabun PSK', 'THSarabunNew', 'Sarabun', sans-serif;
        }}
        .memo-meta-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12pt;
            line-height: 1.5;
            margin-top: 2mm;
        }}
        .memo-meta-table td {{
            padding: 1mm 0;
            vertical-align: bottom;
        }}
        .memo-meta-label {{
            font-size: 14pt;
            font-weight: bold;
            white-space: nowrap;
        }}
        .memo-meta-dots {{
            border-bottom: 1px dotted #000;
            padding-left: 2mm;
            padding-bottom: 1px;
        }}
        .memo-content {{
            margin-top: 3mm;
            font-size: 12pt;
            line-height: 1.5;
        }}
        .memo-p {{
            text-indent: 2.5cm;
            margin: 0 0 2.5mm 0;
            text-align: justify;
            text-justify: inter-cluster;
            line-height: 1.5;
            font-size: 12pt;
        }}
        .memo-att-container {{
            margin: 0 0 2.5mm 0;
            font-size: 12pt;
            line-height: 1.5;
        }}
        .memo-att-row {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            width: 100%;
            margin-bottom: 1mm;
        }}
        .memo-att-desc {{
            padding-left: 20mm;
        }}
        .memo-att-qty {{
            text-align: right;
            white-space: nowrap;
        }}

        /* RED LINE SIGNATURE BLOCK ENGINE */
        .sig-container {{
            margin-top: 8mm;
            display: flex;
            justify-content: flex-end;
            width: 100%;
        }}
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            position: relative;
            min-width: 220px;
            margin-right: 20mm;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .sig-verify {{
            margin-bottom: 24pt;
            font-size: 12pt;
            line-height: 1.0;
            text-align: left;
        }}
        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }}
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
        }}
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 18px);
            white-space: nowrap;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .sig-name {{
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 12pt;
            display: block;
        }}
        .sig-pos {{
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 12pt;
            display: block;
        }}

        /* STAFF INITIALS FOOTER */
        .memo-staff-footer {{
            position: absolute;
            bottom: 15mm;
            right: 20mm;
            font-size: 11pt;
            line-height: 1.3;
            text-align: left;
            font-family: 'TH Sarabun PSK', 'THSarabunNew', 'Sarabun', sans-serif;
        }}

        /* ================= PAGES 2 & 3: FORM SD.1 ================= */
        .form-header-title {{
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.2;
            margin-bottom: 1mm;
        }}
        .form-header-sub {{
            font-size: 12pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.3;
            margin-bottom: 3mm;
        }}
        .form-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11pt;
            line-height: 1.25;
        }}
        .form-table th, .form-table td {{
            border: 1px solid #000000;
            padding: 1.2mm 2mm;
            vertical-align: middle;
        }}
        .form-table th {{
            background-color: #ffffff;
            font-weight: bold;
            text-align: center;
        }}
        .col-no {{ width: 14mm; text-align: center; }}
        .col-topic {{ width: 115mm; }}
        .col-result {{ width: 35mm; text-align: center; }}

        /* DOUBLE SIGNATURE BLOCK ROW (PAGE 3) */
        .double-sig-row {{
            margin-top: 8mm;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            width: 100%;
            padding: 0 10mm;
        }}

        /* ================= PAGE 4: PHOTO SHEET ================= */
        .photo-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5mm;
            margin-top: 6mm;
            margin-bottom: 6mm;
            width: 100%;
        }}
        .photo-card {{
            width: 100%;
            height: 58mm;
            border: 1px solid #999;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background-color: #f8f8f8;
        }}
        .photo-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .photo-cert-text {{
            font-size: 13pt;
            font-weight: bold;
            text-align: center;
            margin-top: 5mm;
            line-height: 1.4;
        }}

        /* ================= PAGE 5: GUN RECORD (LANDSCAPE) ================= */
        .gun-rec-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12pt;
            line-height: 1.3;
            margin-top: 4mm;
        }}
        .gun-rec-table th, .gun-rec-table td {{
            border: 1px solid #000000;
            padding: 2mm 2.5mm;
            vertical-align: middle;
        }}
        .gun-rec-table th {{
            background-color: #ffffff;
            font-weight: bold;
            text-align: center;
        }}
    </style>
</head>
<body>

    <!-- ========================================== -->
    <!-- PAGE 1: บันทึกข้อความนำส่ง                    -->
    <!-- ========================================== -->
    <div class="page-portrait">
        <div class="memo-copy-label">{p1["copy_notice"]}</div>

        <div class="memo-header-container">
            <img src="data:image/png;base64,{GARUDA_B64}" class="memo-garuda" alt="ตราครุฑ">
            <div class="memo-title">บันทึกข้อความ</div>
        </div>

        <table class="memo-meta-table">
            <tr>
                <td style="width: 16%;" class="memo-meta-label">ส่วนราชการ</td>
                <td style="width: 84%;" class="memo-meta-dots">{p1["agency"]}</td>
            </tr>
        </table>

        <table class="memo-meta-table">
            <tr>
                <td style="width: 4%;" class="memo-meta-label">ที่</td>
                <td style="width: 46%;" class="memo-meta-dots">{p1["doc_number"]}</td>
                <td style="width: 8%; text-align: right;" class="memo-meta-label">วันที่</td>
                <td style="width: 42%;" class="memo-meta-dots">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{p1["date_text"]}</td>
            </tr>
        </table>

        <table class="memo-meta-table">
            <tr>
                <td style="width: 6%;" class="memo-meta-label">เรื่อง</td>
                <td style="width: 94%;" class="memo-meta-dots">{p1["subject"]}</td>
            </tr>
        </table>

        <div class="memo-content">
            <div style="margin: 3mm 0 2mm 0;">
                <b>เรียน</b>&nbsp;&nbsp;{p1["to"]}
            </div>

            <div style="margin: 0 0 2.5mm 0;">
                <b>อ้างถึง</b>&nbsp;&nbsp;{p1["references"][0]}<br>
                <span style="padding-left: 10.5mm;">{p1["references"][1]}</span>
            </div>

            <div class="memo-att-container">
                <div style="margin-bottom: 1.5mm;"><b>สิ่งที่ส่งมาด้วย</b></div>
                {att_rows_html}
            </div>

            <p class="memo-p" style="margin-top: 3.5mm;">
                {p1["body"]}
            </p>

            <p class="memo-p" style="margin-top: 3.5mm;">
                {p1["closing"]}
            </p>

            <!-- Red Line Standard Signature Block -->
            <div class="sig-container" style="margin-top: 12mm;">
                {p1_sig_html}
            </div>
        </div>

        <div class="memo-staff-footer">
            {p1["staff_initials"]["draft_inspect"]}<br>
            {p1["staff_initials"]["type_verify"]}
        </div>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 2: แบบรายงานผลการตรวจ สด.๑ (แผ่นที่ ๑)  -->
    <!-- ========================================== -->
    <div class="page-portrait">
        <div class="form-header-title">{sd1["title"]}</div>
        <div class="form-header-sub">
            {sd1["unit"]}<br>
            {sd1["week_info"]}<br>
            <span style="font-weight: normal;">{sd1["date_time_info"]}</span>
        </div>

        <table class="form-table">
            <thead>
                <tr>
                    <th class="col-no">{sd1["headers"][0]}</th>
                    <th class="col-topic">{sd1["headers"][1]}</th>
                    <th class="col-result">{sd1["headers"][2]}</th>
                </tr>
            </thead>
            <tbody>
                {s1_rows_html}
                {s2_rows_html}
            </tbody>
        </table>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 3: แบบรายงานผลการตรวจ สด.๑ (แผ่นที่ ๒)  -->
    <!-- ========================================== -->
    <div class="page-portrait">
        <table class="form-table">
            <thead>
                <tr>
                    <th class="col-no">{sd1["headers"][0]}</th>
                    <th class="col-topic">{sd1["headers"][1]}</th>
                    <th class="col-result">{sd1["headers"][2]}</th>
                </tr>
            </thead>
            <tbody>
                {s2_2_rows_html}
                {s3_rows_html}
                {s4_rows_html}
                {s5_rows_html}
            </tbody>
        </table>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 4: ภาพถ่ายการตรวจ โรงเก็บปืนใหญ่         -->
    <!-- ========================================== -->
    <div class="page-portrait">
        <div class="form-header-title" style="margin-top: 5mm; font-size: 15pt;">{ps["title"]}</div>
        <div class="form-header-sub" style="font-size: 13pt; margin-bottom: 5mm;">{ps["unit"]}</div>

        <div class="photo-grid">
            {photos_html}
        </div>

        <div class="photo-cert-text">
            {ps["certification_text"]}
        </div>
    </div>

    <!-- ========================================== -->
    <!-- PAGE 5: บันทึกผลการตรวจอาวุธฯ (แนวนอน)        -->
    <!-- ========================================== -->
    <div class="page-landscape">
        <div class="form-header-title" style="margin-top: 2mm; font-size: 16pt;">{gr["title"]}</div>
        <div class="form-header-sub" style="font-size: 14pt; margin-bottom: 5mm;">{gr["unit"]}</div>

        <table class="gun-rec-table">
            <thead>
                <tr>
                    <th style="width: 18%;">{gr["headers"][0]}</th>
                    <th style="width: 26%;">{gr["headers"][1]}</th>
                    <th style="width: 14%;">{gr["headers"][2]}</th>
                    <th style="width: 14%;">{gr["headers"][3]}</th>
                    <th style="width: 14%;">{gr["headers"][4]}</th>
                    <th style="width: 14%;">{gr["headers"][5]}</th>
                </tr>
            </thead>
            <tbody>
                {gr_rows_html}
            </tbody>
        </table>

        <!-- Red Line Gun Record Signature Block -->
        <div class="sig-container" style="margin-top: 12mm; margin-right: 15mm;">
            {gr_sig_html}
        </div>
    </div>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML: {output_path}")


# =============================================================================
# 2. GENERATE DOCX (5 Pages / Sections with Red Line Standard)
# =============================================================================
def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name, border_style in kwargs.items():
        node = OxmlElement(f'w:{border_name}')
        node.set(qn('w:val'), border_style.get('val', 'single'))
        node.set(qn('w:sz'), str(border_style.get('sz', 4)))
        node.set(qn('w:space'), '0')
        node.set(qn('w:color'), border_style.get('color', '000000'))
        tcBorders.append(node)
    tcPr.append(tcBorders)


def generate_docx(output_path):
    doc = Document()

    # Section 1: Portrait (Pages 1-4)
    sec1 = doc.sections[0]
    sec1.orientation = WD_ORIENT.PORTRAIT
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.top_margin = Inches(0.8)
    sec1.bottom_margin = Inches(0.8)
    sec1.left_margin = Inches(1.0)
    sec1.right_margin = Inches(0.8)

    p1 = bp["page_1_memo"]
    sd1 = bp["inspection_form_sd1"]
    ps = bp["photo_sheet"]
    gr = bp["gun_inspection_record"]

    # --- DOCX PAGE 1: บันทึกข้อความ ---
    p_copy = doc.add_paragraph()
    p_copy.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_copy = p_copy.add_run(p1["copy_notice"])
    r_copy.font.name = "TH Sarabun PSK"
    r_copy.font.size = Pt(12)
    p_copy.paragraph_format.space_after = Pt(2)

    # Header Table (Garuda + Title)
    t_hdr = doc.add_table(rows=1, cols=2)
    t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr.autofit = False
    t_hdr.columns[0].width = Inches(1.2)
    t_hdr.columns[1].width = Inches(5.2)

    c0 = t_hdr.rows[0].cells[0]
    c1 = t_hdr.rows[0].cells[1]
    p_img = c0.paragraphs[0]
    p_img.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(GARUDA_PATH):
        p_img.add_run().add_picture(GARUDA_PATH, width=Inches(1.18))

    p_t = c1.paragraphs[0]
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_t.add_run("\nบันทึกข้อความ")
    r_t.font.name = "TH Sarabun PSK"
    r_t.font.size = Pt(24)
    r_t.font.bold = True

    # Meta Lines
    meta_items = [
        ("ส่วนราชการ", p1["agency"]),
        ("ที่", f'{p1["doc_number"]}\t\t\t\tวันที่          {p1["date_text"]}'),
        ("เรื่อง", p1["subject"])
    ]
    for lbl, val in meta_items:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_after = Pt(2)
        r_lbl = p_m.add_run(lbl + "  ")
        r_lbl.font.name = "TH Sarabun PSK"
        r_lbl.font.size = Pt(14)
        r_lbl.font.bold = True
        r_val = p_m.add_run(val)
        r_val.font.name = "TH Sarabun PSK"
        r_val.font.size = Pt(12)

    # Content
    def add_p(text, bold_prefix="", indent_in=0.0):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        if indent_in:
            p.paragraph_format.left_indent = Inches(indent_in)
        if bold_prefix:
            rb = p.add_run(bold_prefix + "  ")
            rb.font.name = "TH Sarabun PSK"
            rb.font.size = Pt(12)
            rb.font.bold = True
        r = p.add_run(text)
        r.font.name = "TH Sarabun PSK"
        r.font.size = Pt(12)
        return p

    add_p(p1["to"], "เรียน")
    add_p(p1["references"][0], "อ้างถึง")
    add_p(p1["references"][1], indent_in=0.55)

    add_p("", "สิ่งที่ส่งมาด้วย")
    for att in p1["attachments"]:
        add_p(f'{att["num"]}  {att["desc"]}\t\t\t{att["qty"]}', indent_in=0.55)

    p_b = doc.add_paragraph()
    p_b.paragraph_format.left_indent = Inches(0.8)
    p_b.paragraph_format.space_after = Pt(4)
    r_b = p_b.add_run(p1["body"])
    r_b.font.name = "TH Sarabun PSK"
    r_b.font.size = Pt(12)

    p_cl = doc.add_paragraph()
    p_cl.paragraph_format.left_indent = Inches(0.8)
    p_cl.paragraph_format.space_after = Pt(12)
    r_cl = p_cl.add_run(p1["closing"])
    r_cl.font.name = "TH Sarabun PSK"
    r_cl.font.size = Pt(12)

    # P1 Signature Block (signature_engine)
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    render_signature_docx(doc, p1_sig_data, axis_inch=4.2, font_size=12, space_after_rank_pt=22)

    # Staff Initials
    p_st = doc.add_paragraph()
    p_st.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_st.paragraph_format.space_before = Pt(30)
    r_st = p_st.add_run(f'{p1["staff_initials"]["draft_inspect"]}\n{p1["staff_initials"]["type_verify"]}')
    r_st.font.name = "TH Sarabun PSK"
    r_st.font.size = Pt(11)

    # --- DOCX PAGE 2: แบบรายงานผลการตรวจ สด.๑ (แผ่นที่ ๑) ---
    doc.add_page_break()

    p_h1 = doc.add_paragraph()
    p_h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = p_h1.add_run(sd1["title"])
    r_h1.font.name = "TH Sarabun PSK"
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True

    p_h2 = doc.add_paragraph()
    p_h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h2 = p_h2.add_run(f'{sd1["unit"]}\n{sd1["week_info"]}\n{sd1["date_time_info"]}')
    r_h2.font.name = "TH Sarabun PSK"
    r_h2.font.size = Pt(12)
    r_h2.font.bold = True
    p_h2.paragraph_format.space_after = Pt(6)

    # Table Page 2
    t_p2 = doc.add_table(rows=1, cols=3)
    t_p2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_p2.autofit = False
    col_w = [Inches(0.6), Inches(4.5), Inches(1.3)]
    for i, w in enumerate(col_w):
        t_p2.columns[i].width = w

    # Headers
    for i, h_txt in enumerate(sd1["headers"]):
        cell = t_p2.rows[0].cells[i]
        set_cell_border(cell, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "TH Sarabun PSK"
        r.font.size = Pt(11)
        r.font.bold = True

    def add_table_row(tab, c1, c2, c3, bold=False, indent=0.0):
        row = tab.add_row()
        for idx, (val, aln) in enumerate([(c1, WD_ALIGN_PARAGRAPH.CENTER), (c2, WD_ALIGN_PARAGRAPH.LEFT), (c3, WD_ALIGN_PARAGRAPH.CENTER)]):
            cell = row.cells[idx]
            cell.width = col_w[idx]
            set_cell_border(cell, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = aln
            if idx == 1 and indent:
                p.paragraph_format.left_indent = Inches(indent)
            r = p.add_run(val)
            r.font.name = "TH Sarabun PSK"
            r.font.size = Pt(11)
            if bold:
                r.font.bold = True

    # Section 1
    s1 = sd1["section_1"]
    add_table_row(t_p2, s1["id"], s1["title"], "", bold=True)
    for it in s1["items"]:
        add_table_row(t_p2, "", f'{it["code"]} {it["text"]}', it["result"], indent=0.2)

    # Section 2.1
    s2 = sd1["section_2"]
    sub1 = s2["subsections"][0]
    sub2 = s2["subsections"][1]
    add_table_row(t_p2, s2["id"], s2["title"], "", bold=True)
    add_table_row(t_p2, "", sub1["subtitle"], "", bold=True, indent=0.1)
    for it in sub1["items"]:
        add_table_row(t_p2, "", f'{it["bullet"]} {it["text"]}', it["result"], indent=0.2)

    # --- DOCX PAGE 3: แบบรายงานผลการตรวจ สด.๑ (แผ่นที่ ๒) ---
    doc.add_page_break()

    t_p3 = doc.add_table(rows=1, cols=3)
    t_p3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_p3.autofit = False
    for i, w in enumerate(col_w):
        t_p3.columns[i].width = w

    for i, h_txt in enumerate(sd1["headers"]):
        cell = t_p3.rows[0].cells[i]
        set_cell_border(cell, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "TH Sarabun PSK"
        r.font.size = Pt(11)
        r.font.bold = True

    add_table_row(t_p3, "", sub2["subtitle"], "", bold=True, indent=0.1)
    for it in sub2["items"]:
        add_table_row(t_p3, "", f'{it["bullet"]} {it["text"]}', it["result"], indent=0.2)

    for sec in [sd1["section_3"], sd1["section_4"], sd1["section_5"]]:
        add_table_row(t_p3, sec["id"], sec["title"], "", bold=True)
        for it in sec["items"]:
            add_table_row(t_p3, "", f'{it["code"]} {it["text"]}', it["result"], indent=0.2)

    # --- DOCX PAGE 4: ภาพถ่ายการตรวจ โรงเก็บปืนใหญ่ ---
    doc.add_page_break()

    p_pt1 = doc.add_paragraph()
    p_pt1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pt1 = p_pt1.add_run(ps["title"])
    r_pt1.font.name = "TH Sarabun PSK"
    r_pt1.font.size = Pt(15)
    r_pt1.font.bold = True

    p_pt2 = doc.add_paragraph()
    p_pt2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pt2 = p_pt2.add_run(ps["unit"])
    r_pt2.font.name = "TH Sarabun PSK"
    r_pt2.font.size = Pt(13)
    p_pt2.paragraph_format.space_after = Pt(8)

    # Photo 2x2 Grid Table
    t_photo = doc.add_table(rows=2, cols=2)
    t_photo.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_photo.autofit = False
    t_photo.columns[0].width = Inches(3.1)
    t_photo.columns[1].width = Inches(3.1)

    photo_files = [os.path.join(os.path.dirname(__file__), p) for p in ps["images"]]
    for idx, p_file in enumerate(photo_files):
        row_i = idx // 2
        col_i = idx % 2
        cell = t_photo.rows[row_i].cells[col_i]
        set_cell_margins(cell, top=40, bottom=40, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if os.path.exists(p_file):
            p.add_run().add_picture(p_file, width=Inches(2.95))

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(14)
    r_cert = p_cert.add_run(ps["certification_text"])
    r_cert.font.name = "TH Sarabun PSK"
    r_cert.font.size = Pt(13)
    r_cert.font.bold = True

    # --- DOCX PAGE 5: บันทึกผลการตรวจอาวุธฯ (แนวนอน) ---
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.orientation = WD_ORIENT.LANDSCAPE
    sec2.page_width = Inches(11.69)
    sec2.page_height = Inches(8.27)
    sec2.top_margin = Inches(0.8)
    sec2.bottom_margin = Inches(0.8)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(0.8)

    p_gr1 = doc.add_paragraph()
    p_gr1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gr1 = p_gr1.add_run(gr["title"])
    r_gr1.font.name = "TH Sarabun PSK"
    r_gr1.font.size = Pt(16)
    r_gr1.font.bold = True

    p_gr2 = doc.add_paragraph()
    p_gr2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gr2 = p_gr2.add_run(gr["unit"])
    r_gr2.font.name = "TH Sarabun PSK"
    r_gr2.font.size = Pt(14)
    p_gr2.paragraph_format.space_after = Pt(8)

    # Gun Record Table
    t_gr = doc.add_table(rows=6, cols=6)
    t_gr.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_gr.autofit = False
    gr_col_w = [Inches(1.8), Inches(2.6), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.4)]
    for i, w in enumerate(gr_col_w):
        t_gr.columns[i].width = w

    # Headers
    for i, h_txt in enumerate(gr["headers"]):
        cell = t_gr.rows[0].cells[i]
        set_cell_border(cell, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "TH Sarabun PSK"
        r.font.size = Pt(12)
        r.font.bold = True

    # Date cell (rowspan 5: merge rows 1 to 5)
    cell_date = t_gr.rows[1].cells[0]
    cell_date.merge(t_gr.rows[5].cells[0])
    cell_date.width = gr_col_w[0]
    set_cell_border(cell_date, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
    set_cell_margins(cell_date, top=60, bottom=60, left=80, right=80)
    p_d = cell_date.paragraphs[0]
    p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_d.add_run(gr["date_col"])
    r_d.font.name = "TH Sarabun PSK"
    r_d.font.size = Pt(12)

    for idx, it in enumerate(gr["items"]):
        row_i = idx + 1
        cells = t_gr.rows[row_i].cells
        # Fill columns 1..5
        for col_idx, (val, aln) in enumerate([(it["topic"], WD_ALIGN_PARAGRAPH.LEFT), (it["found"], WD_ALIGN_PARAGRAPH.CENTER), (it["fix_needed"], WD_ALIGN_PARAGRAPH.CENTER), (it["resolution"], WD_ALIGN_PARAGRAPH.CENTER), (it["note"], WD_ALIGN_PARAGRAPH.LEFT)], start=1):
            c = cells[col_idx]
            c.width = gr_col_w[col_idx]
            set_cell_border(c, top={'val': 'single'}, bottom={'val': 'single'}, left={'val': 'single'}, right={'val': 'single'})
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = aln
            r = p.add_run(val)
            r.font.name = "TH Sarabun PSK"
            r.font.size = Pt(12)

    # Gun Record Signature
    gr_sig_data = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"]
    }
    render_signature_docx(doc, gr_sig_data, axis_inch=6.5, font_size=12, space_after_rank_pt=22)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")


# =============================================================================
# 3. GENERATE XLSX (4 Sheets with Data Integrity & Formula Preservation)
# =============================================================================
def generate_xlsx(output_path):
    wb = openpyxl.Workbook()
    # Sheet 1: บันทึกข้อความนำส่ง
    ws1 = wb.active
    ws1.title = "บันทึกข้อความ"

    # Sheet 2: แบบรายงาน สด.๑
    ws2 = wb.create_sheet(title="แบบรายงาน สด.๑")

    # Sheet 3: แผ่นภาพถ่ายแนบ
    ws3 = wb.create_sheet(title="ภาพถ่ายการตรวจ")

    # Sheet 4: บันทึกผลการตรวจอาวุธฯ
    ws4 = wb.create_sheet(title="บันทึกผลการตรวจอาวุธ")

    font_regular = Font(name="TH Sarabun PSK", size=12)
    font_bold = Font(name="TH Sarabun PSK", size=12, bold=True)
    font_title = Font(name="TH Sarabun PSK", size=16, bold=True)
    font_large = Font(name="TH Sarabun PSK", size=14, bold=True)

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    p1 = bp["page_1_memo"]
    sd1 = bp["inspection_form_sd1"]
    ps = bp["photo_sheet"]
    gr = bp["gun_inspection_record"]

    # ------------------ SHEET 1: บันทึกข้อความ ------------------
    ws1["A1"] = p1["copy_notice"]
    ws1["A1"].font = font_regular
    ws1["A1"].alignment = align_center

    ws1["C2"] = "บันทึกข้อความ"
    ws1["C2"].font = Font(name="TH Sarabun PSK", size=24, bold=True)
    ws1["C2"].alignment = align_center

    ws1["A4"] = "ส่วนราชการ"
    ws1["A4"].font = font_large
    ws1["B4"] = p1["agency"]
    ws1["B4"].font = font_regular

    ws1["A5"] = "ที่"
    ws1["A5"].font = font_large
    ws1["B5"] = p1["doc_number"]
    ws1["B5"].font = font_regular
    ws1["D5"] = "วันที่"
    ws1["D5"].font = font_large
    ws1["E5"] = p1["date_text"]
    ws1["E5"].font = font_regular

    ws1["A6"] = "เรื่อง"
    ws1["A6"].font = font_large
    ws1["B6"] = p1["subject"]
    ws1["B6"].font = font_regular

    ws1["A8"] = "เรียน"
    ws1["A8"].font = font_bold
    ws1["B8"] = p1["to"]
    ws1["B8"].font = font_regular

    ws1["A9"] = "อ้างถึง"
    ws1["A9"].font = font_bold
    ws1["B9"] = p1["references"][0]
    ws1["B9"].font = font_regular
    ws1["B10"] = p1["references"][1]
    ws1["B10"].font = font_regular

    ws1["A11"] = "สิ่งที่ส่งมาด้วย"
    ws1["A11"].font = font_bold
    for idx, att in enumerate(p1["attachments"], start=11):
        ws1[f"B{idx}"] = f'{att["num"]}  {att["desc"]}'
        ws1[f"B{idx}"].font = font_regular
        ws1[f"E{idx}"] = att["qty"]
        ws1[f"E{idx}"].font = font_regular

    ws1["B15"] = p1["body"]
    ws1["B15"].font = font_regular
    ws1["B16"] = p1["closing"]
    ws1["B16"].font = font_regular

    # Signature Sheet 1 using signature_engine
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    render_signature_xlsx(ws1, p1_sig_data, rank_col="D", name_col="E", start_row=18)

    ws1["E24"] = p1["staff_initials"]["draft_inspect"]
    ws1["E24"].font = font_regular
    ws1["E25"] = p1["staff_initials"]["type_verify"]
    ws1["E25"].font = font_regular

    ws1.column_dimensions["A"].width = 15
    ws1.column_dimensions["B"].width = 40
    ws1.column_dimensions["C"].width = 15
    ws1.column_dimensions["D"].width = 15
    ws1.column_dimensions["E"].width = 25

    # ------------------ SHEET 2: แบบรายงาน สด.๑ ------------------
    ws2["B1"] = sd1["title"]
    ws2["B1"].font = font_title
    ws2["B1"].alignment = align_center

    ws2["B2"] = sd1["unit"]
    ws2["B2"].font = font_bold
    ws2["B2"].alignment = align_center

    ws2["B3"] = sd1["week_info"]
    ws2["B3"].font = font_bold
    ws2["B3"].alignment = align_center

    ws2["B4"] = sd1["date_time_info"]
    ws2["B4"].font = font_regular
    ws2["B4"].alignment = align_center

    # Headers
    headers = sd1["headers"]
    for c_idx, h_txt in enumerate(headers, start=1):
        col_l = get_column_letter(c_idx)
        cell = ws2[f"{col_l}6"]
        cell.value = h_txt
        cell.font = font_bold
        cell.alignment = align_center
        cell.border = thin_border

    row_cursor = 7
    # Section 1
    s1 = sd1["section_1"]
    ws2[f"A{row_cursor}"] = s1["id"]
    ws2[f"A{row_cursor}"].font = font_bold
    ws2[f"A{row_cursor}"].alignment = align_center
    ws2[f"A{row_cursor}"].border = thin_border

    ws2[f"B{row_cursor}"] = s1["title"]
    ws2[f"B{row_cursor}"].font = font_bold
    ws2[f"B{row_cursor}"].border = thin_border

    ws2[f"C{row_cursor}"] = ""
    ws2[f"C{row_cursor}"].border = thin_border
    row_cursor += 1

    for it in s1["items"]:
        ws2[f"A{row_cursor}"] = ""
        ws2[f"A{row_cursor}"].border = thin_border

        ws2[f"B{row_cursor}"] = f'    {it["code"]} {it["text"]}'
        ws2[f"B{row_cursor}"].font = font_regular
        ws2[f"B{row_cursor}"].border = thin_border

        ws2[f"C{row_cursor}"] = it["result"]
        ws2[f"C{row_cursor}"].font = font_regular
        ws2[f"C{row_cursor}"].alignment = align_center
        ws2[f"C{row_cursor}"].border = thin_border
        row_cursor += 1

    # Section 2
    s2 = sd1["section_2"]
    ws2[f"A{row_cursor}"] = s2["id"]
    ws2[f"A{row_cursor}"].font = font_bold
    ws2[f"A{row_cursor}"].alignment = align_center
    ws2[f"A{row_cursor}"].border = thin_border

    ws2[f"B{row_cursor}"] = s2["title"]
    ws2[f"B{row_cursor}"].font = font_bold
    ws2[f"B{row_cursor}"].border = thin_border

    ws2[f"C{row_cursor}"] = ""
    ws2[f"C{row_cursor}"].border = thin_border
    row_cursor += 1

    for sub in s2["subsections"]:
        ws2[f"A{row_cursor}"] = ""
        ws2[f"A{row_cursor}"].border = thin_border
        ws2[f"B{row_cursor}"] = f'  {sub["subtitle"]}'
        ws2[f"B{row_cursor}"].font = font_bold
        ws2[f"B{row_cursor}"].border = thin_border
        ws2[f"C{row_cursor}"] = ""
        ws2[f"C{row_cursor}"].border = thin_border
        row_cursor += 1

        for it in sub["items"]:
            ws2[f"A{row_cursor}"] = ""
            ws2[f"A{row_cursor}"].border = thin_border

            ws2[f"B{row_cursor}"] = f'    {it["bullet"]} {it["text"]}'
            ws2[f"B{row_cursor}"].font = font_regular
            ws2[f"B{row_cursor}"].border = thin_border

            ws2[f"C{row_cursor}"] = it["result"]
            ws2[f"C{row_cursor}"].font = font_regular
            ws2[f"C{row_cursor}"].alignment = align_center
            ws2[f"C{row_cursor}"].border = thin_border
            row_cursor += 1

    # Sections 3, 4, 5
    for sec in [sd1["section_3"], sd1["section_4"], sd1["section_5"]]:
        ws2[f"A{row_cursor}"] = sec["id"]
        ws2[f"A{row_cursor}"].font = font_bold
        ws2[f"A{row_cursor}"].alignment = align_center
        ws2[f"A{row_cursor}"].border = thin_border

        ws2[f"B{row_cursor}"] = sec["title"]
        ws2[f"B{row_cursor}"].font = font_bold
        ws2[f"B{row_cursor}"].border = thin_border

        ws2[f"C{row_cursor}"] = ""
        ws2[f"C{row_cursor}"].border = thin_border
        row_cursor += 1

        for it in sec["items"]:
            ws2[f"A{row_cursor}"] = ""
            ws2[f"A{row_cursor}"].border = thin_border

            ws2[f"B{row_cursor}"] = f'    {it["code"]} {it["text"]}'
            ws2[f"B{row_cursor}"].font = font_regular
            ws2[f"B{row_cursor}"].border = thin_border

            ws2[f"C{row_cursor}"] = it["result"]
            ws2[f"C{row_cursor}"].font = font_regular
            ws2[f"C{row_cursor}"].alignment = align_center
            ws2[f"C{row_cursor}"].border = thin_border
            row_cursor += 1

    ws2.column_dimensions["A"].width = 10
    ws2.column_dimensions["B"].width = 45
    ws2.column_dimensions["C"].width = 15
    ws2.column_dimensions["D"].width = 25

    # ------------------ SHEET 3: แผ่นภาพถ่ายแนบ ------------------
    ws3["A1"] = ps["title"]
    ws3["A1"].font = font_title
    ws3["A2"] = ps["unit"]
    ws3["A2"].font = font_large
    ws3["A4"] = ps["certification_text"]
    ws3["A4"].font = font_large

    # ------------------ SHEET 4: บันทึกผลการตรวจอาวุธฯ ------------------
    ws4["A1"] = gr["title"]
    ws4["A1"].font = font_title
    ws4["A2"] = gr["unit"]
    ws4["A2"].font = font_large

    # Table Header
    for idx, h_txt in enumerate(gr["headers"], start=1):
        col_l = get_column_letter(idx)
        cell = ws4[f"{col_l}4"]
        cell.value = h_txt
        cell.font = font_bold
        cell.alignment = align_center
        cell.border = thin_border

    # Data Rows
    ws4["A5"] = gr["date_col"]
    ws4["A5"].font = font_regular
    ws4["A5"].alignment = align_center
    ws4["A5"].border = thin_border

    for i in range(6, 10):
        ws4[f"A{i}"] = ""
        ws4[f"A{i}"].border = thin_border

    for idx, it in enumerate(gr["items"], start=5):
        ws4[f"B{idx}"] = it["topic"]
        ws4[f"B{idx}"].font = font_regular
        ws4[f"B{idx}"].border = thin_border

        ws4[f"C{idx}"] = it["found"]
        ws4[f"C{idx}"].font = font_regular
        ws4[f"C{idx}"].alignment = align_center
        ws4[f"C{idx}"].border = thin_border

        ws4[f"D{idx}"] = it["fix_needed"]
        ws4[f"D{idx}"].font = font_regular
        ws4[f"D{idx}"].alignment = align_center
        ws4[f"D{idx}"].border = thin_border

        ws4[f"E{idx}"] = it["resolution"]
        ws4[f"E{idx}"].font = font_regular
        ws4[f"E{idx}"].alignment = align_center
        ws4[f"E{idx}"].border = thin_border

        ws4[f"F{idx}"] = it["note"]
        ws4[f"F{idx}"].font = font_regular
        ws4[f"F{idx}"].border = thin_border

    # Signature Sheet 4
    gr_sig_data = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"]
    }
    render_signature_xlsx(ws4, gr_sig_data, rank_col="E", name_col="F", start_row=12)

    ws4.column_dimensions["A"].width = 25
    ws4.column_dimensions["B"].width = 30
    ws4.column_dimensions["C"].width = 16
    ws4.column_dimensions["D"].width = 16
    ws4.column_dimensions["E"].width = 16
    ws4.column_dimensions["F"].width = 18

    wb.save(output_path)
    print(f"Generated XLSX: {output_path}")


# =============================================================================
# MAIN EXECUTOR
# =============================================================================
if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    out_html = os.path.join(base_dir, "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html")
    out_docx = os.path.join(base_dir, "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx")
    out_xlsx = os.path.join(base_dir, "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx")

    generate_html(out_html)
    generate_docx(out_docx)
    generate_xlsx(out_xlsx)
    print("All builds completed successfully!")
