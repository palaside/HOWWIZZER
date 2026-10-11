#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPERCLONE Production Engine
Document: บันทึกรายงานผลการตรวจประจำสัปดาห์โดยผู้บังคับบัญชา สป.สาย สพ. (อาวุธ) (ประจำสัปดาห์)
Authority: ระเบียบ ทบ. ว่าด้วยการตรวจอาวุธฯ พ.ศ. ๒๔๙๗ / คำสั่ง พล.ร.๔ ที่ ๓๙๔/๒๕๖๙
Unit: ป.๔ พัน.๔ ร้อย.๒
Period: สัปดาห์ที่ ๓ ตั้งแต่วันที่ ๑๕ มิ.ย. – ๑๙ มิ.ย. ๖๙
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
BLUEPRINT_PATH = os.path.join(os.path.dirname(__file__), "table_layout_weekly_inspection.json")
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

    # Signatures HTML using signature_engine (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1)
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    p1_sig_html = render_signature_html(p1_sig_data, margin_left_px=0, gap_pt=24, font_size_pt=17)

    # Page 3 Double Signatures (Corrector + Inspector)
    p3_sig_corrector_data = {
        "type": "signature_block",
        "label": sd1["signatures"]["corrector"]["role"],
        "rank": sd1["signatures"]["corrector"]["rank"],
        "name": sd1["signatures"]["corrector"]["name"],
        "position": sd1["signatures"]["corrector"]["position"]
    }
    p3_sig_corrector_html = render_signature_html(p3_sig_corrector_data, margin_left_px=0, gap_pt=18, font_size_pt=14)

    p3_sig_inspector_data = {
        "type": "signature_block",
        "label": sd1["signatures"]["inspector"]["role"],
        "rank": sd1["signatures"]["inspector"]["rank"],
        "name": sd1["signatures"]["inspector"]["name"],
        "position": sd1["signatures"]["inspector"]["position"],
        "date": sd1["signatures"]["inspector"]["date_text"]
    }
    p3_sig_inspector_html = render_signature_html(p3_sig_inspector_data, margin_left_px=0, gap_pt=18, font_size_pt=14)

    # Page 4 Photo Sheet Signature
    p4_sig_data = {
        "type": "signature_block",
        "label": ps["signature"]["label"],
        "rank": ps["signature"]["rank"],
        "name": ps["signature"]["name"],
        "position": ps["signature"]["position"],
        "date": ps["signature"]["date_text"]
    }
    p4_sig_html = render_signature_html(p4_sig_data, margin_left_px=0, gap_pt=20, font_size_pt=16)

    # Page 5 Gun Record Signature (Landscape)
    gr_sig = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"],
        "date": gr["signature"]["date_text"]
    }
    gr_sig_html = render_signature_html(gr_sig, margin_left_px=0, gap_pt=20, font_size_pt=16)

    # Build Attachments List
    att_rows_html = ""
    for att in p1["attachments"]:
        att_rows_html += f"""
        <div class="memo-att-row">
            <div class="memo-att-desc"><b>{att["num"]}</b> {att["desc"]}</div>
            <div class="memo-att-qty">{att["qty"]}</div>
        </div>
        """

    # Build Page 2 Table Rows (Section 1 + Section 2)
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
        <td class="font-bold" style="padding-left: 5mm;">{sub1["subtitle"]}</td>
        <td></td>
    </tr>
    """
    for it in sub1["items"]:
        s2_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 10mm;">- {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Section 2.2 Rows
    s2_2_rows_html = f"""
    <tr>
        <td></td>
        <td class="font-bold" style="padding-left: 5mm;">{sub2["subtitle"]}</td>
        <td></td>
    </tr>
    """
    for it in sub2["items"]:
        s2_2_rows_html += f"""
        <tr>
            <td></td>
            <td style="padding-left: 10mm;">- {it["text"]}</td>
            <td class="text-center">{it["result"]}</td>
        </tr>
        """

    # Build Page 3 Table Rows (Section 3 + Section 4 + Section 5)
    s3 = sd1["section_3"]
    s4 = sd1["section_4"]
    s5 = sd1["section_5"]

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

    # Build Page 5 Table Rows
    p5_rows_html = ""
    for idx, it in enumerate(gr["items"]):
        first_col = f'<td rowspan="{len(gr["items"])}" class="text-center align-top font-bold" style="line-height: 1.4;">{gr["date_col"].replace(chr(10), "<br>")}</td>' if idx == 0 else ""
        p5_rows_html += f"""
        <tr>
            {first_col}
            <td style="padding-left: 4mm;">{it["topic"]}</td>
            <td class="text-center">{it["found"]}</td>
            <td class="text-center">{it["fix_needed"]}</td>
            <td class="text-center">{it["resolution"]}</td>
            <td class="text-center">{it["note"]}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>{bp["title"]}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        @page portrait-page {{
            size: A4 portrait;
            margin: 0;
        }}
        @page landscape-page {{
            size: A4 landscape;
            margin: 0;
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: #525659;
            font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', Tahoma, sans-serif;
            font-size: 11pt;
            line-height: 1.25;
            color: #000000;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
        }}

        /* OpenType Thai Numeral Engine */
        .thai-numerals, body {{
            font-variant-numeric: tabular-nums;
            font-feature-settings: "locl" 1, "numr" 1;
        }}

        .page-portrait {{
            page: portrait-page;
            width: 210mm;
            min-height: 297mm;
            height: 297mm;
            background-color: #ffffff;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
            margin-bottom: 25px;
            padding: 15mm 20mm 15mm 25mm;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .page-landscape {{
            page: landscape-page;
            width: 297mm;
            min-height: 210mm;
            height: 210mm;
            background-color: #ffffff;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
            margin-bottom: 25px;
            padding: 18mm 22mm 18mm 25mm;
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
            .page-portrait {{
                box-shadow: none;
                margin: 0;
                page-break-after: always;
                height: 297mm;
            }}
            .page-landscape {{
                box-shadow: none;
                margin: 0;
                page-break-after: always;
                height: 210mm;
            }}
        }}

        /* Universal Red Line Signature Engine CSS (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            position: relative;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .sig-verify {{
            margin-bottom: 24pt;
            font-size: 12pt;
            line-height: 1.0;
            text-align: left;
            font-weight: bold;
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
            bottom: calc(100% + 20px);
            white-space: nowrap;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .sig-role-anchor, .sig-label-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 20px);
            white-space: nowrap;
            text-align: right;
            font-weight: bold;
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
        .sig-date {{
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 12pt;
            display: block;
        }}

        /* ================= PAGE 1: MEMO ================= */
        .memo-copy-label {{
            font-size: 13pt;
            text-align: center;
            margin-bottom: 2mm;
        }}
        .memo-header-container {{
            position: relative;
            width: 100%;
            height: 25mm;
            margin-bottom: 3mm;
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
            font-weight: bold;
            line-height: 1.1;
            padding-top: 3mm;
            letter-spacing: 0.5px;
        }}
        .meta-section {{
            width: 100%;
            margin-bottom: 0mm;
        }}
        .meta-row {{
            display: flex;
            align-items: flex-end;
            margin-bottom: 3.2mm;
            font-size: 17pt;
        }}
        .meta-row:last-child {{
            margin-bottom: 0mm;
        }}
        .meta-label {{
            font-weight: bold;
            font-size: 20pt;
            line-height: 1.0;
            white-space: nowrap;
            margin-right: 2.5mm;
            padding-bottom: 1px;
        }}
        .meta-fill-dotted {{
            flex: 1;
            border-bottom: 1px dotted #000;
            display: flex;
            align-items: flex-end;
            padding-bottom: 1px;
            font-size: 17pt;
            line-height: 1.1;
        }}
        .meta-half-col {{
            flex: 1;
            display: flex;
            align-items: flex-end;
        }}
        .salutation-row {{
            margin-top: 4.5mm; /* 1 เอนเตอร์ จาก เรื่อง */
            margin-bottom: 2.5mm;
            font-size: 17pt;
            line-height: 1.20;
        }}
        .reference-section {{
            margin-bottom: 2.5mm;
            font-size: 17pt;
            line-height: 1.20;
        }}
        .attachment-section {{
            margin-bottom: 3mm;
            font-size: 17pt;
            line-height: 1.20;
        }}
        .memo-body {{
            font-size: 17pt;
            line-height: 1.20;
            text-align: justify;
            text-justify: inter-cluster;
            text-indent: 25mm;
            margin-top: 3mm;
            margin-bottom: 2.5mm;
        }}
        .memo-closing {{
            font-size: 17pt;
            line-height: 1.20;
            text-indent: 25mm;
            margin-bottom: 0mm;
        }}
        .memo-sig-wrap {{
            margin-left: 105mm; /* 130mm from left edge of paper (25mm padding-left) */
            margin-top: 22mm; /* ยศ ห่างจาก จึงเรียนมาเพื่อกรุณาทราบ 5 เอนเตอร์ */
        }}
        .memo-footer-staff {{
            margin-top: auto;
            display: flex;
            justify-content: flex-end;
        }}
        .staff-grid {{
            display: grid;
            grid-template-columns: 24mm 24mm 24mm;
            font-size: 13.5pt;
            line-height: 1.25;
            text-align: center;
        }}

        /* ================= PAGE 2 & 3: FORM SD.1 ================= */
        .form-header-title {{
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.2;
            margin-bottom: 0.5mm;
        }}
        .form-header-sub {{
            font-size: 12.5pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.2;
            margin-bottom: 1.5mm;
        }}
        .form-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14pt;
            line-height: 1.15;
        }}
        .form-table th, .form-table td {{
            border: 1px solid #000000;
            padding: 0.55mm 1.5mm;
            vertical-align: middle;
        }}
        .form-table th {{
            background-color: #ffffff;
            font-weight: bold;
            text-align: center;
            padding: 1.0mm 1.5mm;
        }}
        .col-no {{ width: 14mm; text-align: center; }}
        .col-topic {{ width: 115mm; }}
        .col-result {{ width: 35mm; text-align: center; }}

        /* DOUBLE SIGNATURE BLOCK ROW (PAGE 3 - RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .page3-sig-wrap {{
            margin-top: 20mm; /* เคาะลงมา 3 เอนเตอร์ จากขอบล่างของตาราง */
            margin-left: 100mm;
            display: flex;
            flex-direction: column;
            gap: 18mm;
        }}

        /* ================= PAGE 4: PHOTO SHEET ================= */
        .photo-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4mm;
            margin-top: 4mm;
            margin-bottom: 4mm;
            width: 100%;
        }}
        .photo-card {{
            width: 100%;
            height: 52mm;
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
            font-size: 16pt;
            font-weight: bold;
            text-align: center;
            margin-top: 3mm;
            line-height: 1.35;
        }}
        .photo-sig-wrap {{
            margin-top: 4mm;
            margin-left: 105mm;
            display: flex;
            justify-content: flex-start;
        }}

        /* ================= PAGE 5: GUN RECORD (LANDSCAPE) ================= */
        .gun-rec-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 15pt;
            line-height: 1.22;
            margin-top: 3mm;
        }}
        .gun-rec-table th, .gun-rec-table td {{
            border: 1px solid #000000;
            padding: 1.6mm 2mm;
            vertical-align: middle;
        }}
        .gun-rec-table th {{
            background-color: #ffffff;
            font-weight: bold;
            text-align: center;
        }}

        .text-center {{ text-align: center; }}
        .text-right {{ text-align: right; }}
        .font-bold {{ font-weight: bold; }}
        .align-top {{ vertical-align: top; }}
    </style>
</head>
<body>

    <!-- ========================================== -->
    <!-- PAGE 1: บันทึกข้อความนำส่ง                    -->
    <!-- ========================================== -->
    <div class="page-portrait" style="padding: 22mm 20mm 15mm 25mm;">
        <div class="memo-copy-label">{p1["copy_notice"]}</div>

        <div class="memo-header-container">
            <img src="data:image/png;base64,{GARUDA_B64}" class="memo-garuda" alt="ตราครุฑ">
            <div class="memo-title">บันทึกข้อความ</div>
        </div>

        <!-- METADATA ROWS WITH DOTTED UNDERLINES -->
        <div class="meta-section">
            <!-- Row 1: ส่วนราชการ -->
            <div class="meta-row">
                <span class="meta-label">ส่วนราชการ</span>
                <div class="meta-fill-dotted">{p1["agency"]}</div>
            </div>

            <!-- Row 2: ที่ & วันที่ -->
            <div class="meta-row">
                <div class="meta-half-col" style="margin-right: 4mm;">
                    <span class="meta-label">ที่</span>
                    <div class="meta-fill-dotted">{p1["doc_number"]}</div>
                </div>
                <div class="meta-half-col">
                    <span class="meta-label">วันที่</span>
                    <div class="meta-fill-dotted" style="padding-left: 20mm;">{p1["date_text"]}</div>
                </div>
            </div>

            <!-- Row 3: เรื่อง -->
            <div class="meta-row">
                <span class="meta-label">เรื่อง</span>
                <div class="meta-fill-dotted">{p1["subject"]}</div>
            </div>
        </div>

        <!-- SALUTATION -->
        <div class="salutation-row">
            <span class="font-bold">เรียน</span>  {p1["to"]}
        </div>

        <!-- REFERENCES -->
        <div class="reference-section">
            <div style="display: flex;">
                <span class="font-bold" style="white-space: nowrap; margin-right: 3mm;">อ้างถึง</span>
                <div>
                    <div>{p1["references"][0]}</div>
                    <div style="margin-top: 1mm;">{p1["references"][1]}</div>
                </div>
            </div>
        </div>

        <!-- ATTACHMENTS -->
        <div class="attachment-section">
            <div style="display: flex;">
                <span class="font-bold" style="white-space: nowrap; margin-right: 3mm;">สิ่งที่ส่งมาด้วย</span>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1.2mm;">
                        <div>{p1["attachments"][0]["num"]} {p1["attachments"][0]["desc"]}</div>
                        <div style="white-space: nowrap; margin-left: 10mm;">{p1["attachments"][0]["qty"]}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1.2mm;">
                        <div>{p1["attachments"][1]["num"]} {p1["attachments"][1]["desc"]}</div>
                        <div style="white-space: nowrap; margin-left: 10mm;">{p1["attachments"][1]["qty"]}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div>{p1["attachments"][2]["num"]} {p1["attachments"][2]["desc"]}</div>
                        <div style="white-space: nowrap; margin-left: 10mm;">{p1["attachments"][2]["qty"]}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- CONTENT BODY -->
        <div class="memo-body">
            {p1["body"]}
        </div>

        <!-- CLOSING -->
        <div class="memo-closing">
            {p1["closing"]}
        </div>

        <!-- SIGNATURE BLOCK (Universal Red Line Standard) -->
        <div class="memo-sig-wrap">
            {p1_sig_html}
        </div>

        <!-- BOTTOM RIGHT STAFF INITIALS -->
        <div class="memo-footer-staff">
            <div class="staff-grid">
                <div>จ.ส.อ.</div>
                <div>ร่าง/ตรวจ</div>
                <div>มิ.ย. ๖๙</div>
                <div>ส.ท. วรากรฯ</div>
                <div>พิมพ์/ทาน</div>
                <div style="display: flex; justify-content: space-between;"><span>๑๙</span><span>มิ.ย. ๖๙</span></div>
            </div>
        </div>
    </div>


    <!-- ========================================== -->
    <!-- PAGE 2: แบบรายงานผลการตรวจ สด.๑ (แผ่น ๑)   -->
    <!-- ========================================== -->
    <div class="page-portrait" style="padding: 10mm 18mm 10mm 22mm;">
        <div class="form-header-title">{sd1["title"]}</div>
        <div class="form-header-sub">
            <div>{sd1["unit"]}</div>
            <div>{sd1["week_text"]}</div>
            <div>{sd1["inspection_time"]}</div>
        </div>

        <table class="form-table">
            <thead>
                <tr>
                    <th class="col-no">ลำดับ</th>
                    <th class="col-topic">หัวข้อการตรวจ</th>
                    <th class="col-result">ผลการตรวจ</th>
                </tr>
            </thead>
            <tbody>
                {s1_rows_html}
                {s2_rows_html}
                {s2_2_rows_html}
            </tbody>
        </table>
    </div>


    <!-- ========================================== -->
    <!-- PAGE 3: แบบรายงานผลการตรวจ สด.๑ (แผ่น ๒)   -->
    <!-- ========================================== -->
    <div class="page-portrait" style="padding: 12mm 18mm 12mm 22mm;">
        <table class="form-table">
            <thead>
                <tr>
                    <th class="col-no">ลำดับ</th>
                    <th class="col-topic">หัวข้อการตรวจ</th>
                    <th class="col-result">ผลการตรวจ</th>
                </tr>
            </thead>
            <tbody>
                {s3_rows_html}
                {s4_rows_html}
                {s5_rows_html}
            </tbody>
        </table>

        <!-- บล็อกลงนามคู่: ผู้แก้ไข + ผู้ตรวจ (Universal Red Line Standard ตาม RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) -->
        <div class="page3-sig-wrap">
            <!-- บล็อก ๑: ผู้แก้ไข -->
            {p3_sig_corrector_html}

            <!-- บล็อก ๒: ผู้ตรวจ -->
            {p3_sig_inspector_html}
        </div>
    </div>


    <!-- ========================================== -->
    <!-- PAGE 4: ภาพถ่ายการตรวจ โรงเก็บปืนใหญ่          -->
    <!-- ========================================== -->
    <div class="page-portrait">
        <div class="form-header-title" style="margin-top: 2mm;">{ps["title"]}</div>
        <div class="form-header-sub" style="margin-bottom: 2mm;">{ps["unit"]}</div>

        <div class="photo-grid">
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{PHOTO_B64S[0]}" class="photo-img" alt="ภาพถ่ายที่ ๑">
            </div>
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{PHOTO_B64S[1]}" class="photo-img" alt="ภาพถ่ายที่ ๒">
            </div>
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{PHOTO_B64S[2]}" class="photo-img" alt="ภาพถ่ายที่ ๓">
            </div>
            <div class="photo-card">
                <img src="data:image/jpeg;base64,{PHOTO_B64S[3]}" class="photo-img" alt="ภาพถ่ายที่ ๔">
            </div>
        </div>

        <div class="photo-cert-text" style="margin-top: 5mm;">
            {ps["certification_text"]}
        </div>
    </div>


    <!-- ========================================== -->
    <!-- PAGE 5: บันทึกผลการตรวจอาวุธ (แนวนอน)        -->
    <!-- ========================================== -->
    <div class="page-landscape">
        <div class="form-header-title">{gr["title"]}</div>
        <div class="form-header-sub" style="margin-bottom: 3mm;">{gr["unit"]}</div>

        <table class="gun-rec-table">
            <thead>
                <tr>
                    <th style="width: 48mm;">{gr["headers"][0]}</th>
                    <th style="width: 75mm;">{gr["headers"][1]}</th>
                    <th style="width: 32mm;">{gr["headers"][2]}</th>
                    <th style="width: 32mm;">{gr["headers"][3]}</th>
                    <th style="width: 30mm;">{gr["headers"][4]}</th>
                    <th style="width: 25mm;">{gr["headers"][5]}</th>
                </tr>
            </thead>
            <tbody>
                {p5_rows_html}
            </tbody>
        </table>

        <!-- บล็อกลงนามแนวนอน Red Line Standard -->
        <div style="margin-top: 22mm; display: flex; justify-content: flex-end; padding-right: 15mm;">
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
    r_copy.font.size = Pt(13)
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
    r_t.font.size = Pt(29)
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
        r_lbl.font.size = Pt(20)
        r_lbl.font.bold = True
        r_val = p_m.add_run(val)
        r_val.font.name = "TH Sarabun PSK"
        r_val.font.size = Pt(17)

    def add_p(text, bold_prefix="", indent_in=0.0):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.20
        if indent_in > 0:
            p.paragraph_format.left_indent = Inches(indent_in)
        if bold_prefix:
            r_b = p.add_run(bold_prefix + "  ")
            r_b.font.name = "TH Sarabun PSK"
            r_b.font.size = Pt(17)
            r_b.font.bold = True
        r_t = p.add_run(text)
        r_t.font.name = "TH Sarabun PSK"
        r_t.font.size = Pt(17)
        return p

    p_to = add_p(p1["to"], bold_prefix="เรียน")
    p_to.paragraph_format.space_before = Pt(14) # 1 เอนเตอร์ จาก เรื่อง

    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(2)
    p_ref.paragraph_format.line_spacing = 1.20
    r_rf = p_ref.add_run("อ้างถึง  ")
    r_rf.font.name = "TH Sarabun PSK"
    r_rf.font.size = Pt(17)
    r_rf.font.bold = True
    r_rf1 = p_ref.add_run(f'{p1["references"][0]}\n')
    r_rf1.font.name = "TH Sarabun PSK"
    r_rf1.font.size = Pt(17)
    p_ref.paragraph_format.left_indent = Inches(0.4)
    r_rf2 = p_ref.add_run(p1["references"][1])
    r_rf2.font.name = "TH Sarabun PSK"
    r_rf2.font.size = Pt(17)

    p_att_lbl = doc.add_paragraph()
    p_att_lbl.paragraph_format.space_after = Pt(2)
    p_att_lbl.paragraph_format.line_spacing = 1.20
    r_at = p_att_lbl.add_run("สิ่งที่ส่งมาด้วย")
    r_at.font.name = "TH Sarabun PSK"
    r_at.font.size = Pt(17)
    r_at.font.bold = True

    for att in p1["attachments"]:
        p_at = doc.add_paragraph()
        p_at.paragraph_format.left_indent = Inches(0.6)
        p_at.paragraph_format.space_after = Pt(1)
        p_at.paragraph_format.line_spacing = 1.20
        r1 = p_at.add_run(f'{att["num"]}  {att["desc"]}')
        r1.font.name = "TH Sarabun PSK"
        r1.font.size = Pt(17)
        r2 = p_at.add_run(f'\t\t\t\t\t{att["qty"]}')
        r2.font.name = "TH Sarabun PSK"
        r2.font.size = Pt(17)

    # Body
    p_b = doc.add_paragraph()
    p_b.paragraph_format.space_after = Pt(3)
    p_b.paragraph_format.line_spacing = 1.20
    p_b.paragraph_format.first_line_indent = Inches(0.8)
    r_b = p_b.add_run(p1["body"])
    r_b.font.name = "TH Sarabun PSK"
    r_b.font.size = Pt(17)

    p_cl = doc.add_paragraph()
    p_cl.paragraph_format.space_after = Pt(70) # ยศ ห่างจาก จึงเรียนมาเพื่อกรุณาทราบ 5 เอนเตอร์
    p_cl.paragraph_format.line_spacing = 1.20
    p_cl.paragraph_format.first_line_indent = Inches(0.8)
    r_cl = p_cl.add_run(p1["closing"])
    r_cl.font.name = "TH Sarabun PSK"
    r_cl.font.size = Pt(17)

    # Signature Page 1 using signature_engine
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    render_signature_docx(doc, p1_sig_data, axis_inch=5.1, font_size=17, space_after_rank_pt=24)

    # Staff Box
    p_st = doc.add_paragraph()
    p_st.paragraph_format.space_before = Pt(16)
    p_st.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_st = p_st.add_run(f'{p1["staff_initials"]["draft_inspect"]}\n{p1["staff_initials"]["type_verify"]}')
    r_st.font.name = "TH Sarabun PSK"
    r_st.font.size = Pt(13)
    r_st.font.color.rgb = RGBColor(100, 100, 100)


    # --- DOCX PAGE 2: แบบรายงาน สด.๑ (แผ่น ๑) ---
    doc.add_page_break()

    p_h1 = doc.add_paragraph()
    p_h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = p_h1.add_run(sd1["title"])
    r_h1.font.name = "TH Sarabun PSK"
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    p_h1.paragraph_format.space_after = Pt(1)

    p_h2 = doc.add_paragraph()
    p_h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h2 = p_h2.add_run(f'{sd1["unit"]}\n{sd1["week_text"]}\n{sd1["inspection_time"]}')
    r_h2.font.name = "TH Sarabun PSK"
    r_h2.font.size = Pt(13)
    r_h2.font.bold = True
    p_h2.paragraph_format.space_after = Pt(4)

    # Table Page 2
    t2 = doc.add_table(rows=1, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    col_w = [Inches(0.6), Inches(4.5), Inches(1.3)]
    for idx, w in enumerate(col_w):
        t2.columns[idx].width = w

    hdr2 = t2.rows[0]
    headers_txt = ["ลำดับ", "หัวข้อการตรวจ", "ผลการตรวจ"]
    for i, title in enumerate(headers_txt):
        c = hdr2.cells[i]
        c.text = title
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "TH Sarabun PSK"
        p.runs[0].font.size = Pt(14)
        p.runs[0].font.bold = True
        set_cell_margins(c, 60, 60, 80, 80)
        set_cell_border(c, top={'val':'single'}, bottom={'val':'single'}, left={'val':'single'}, right={'val':'single'})

    def add_table_row(table, col0, col1, col2, is_bold=False, indent_in=0.0, align2=WD_ALIGN_PARAGRAPH.CENTER):
        row = table.add_row()
        for idx, w in enumerate(col_w):
            row.cells[idx].width = w

        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.text = col0
        c1.text = col1
        c2.text = col2

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p0.runs:
            p0.runs[0].font.name = "TH Sarabun PSK"
            p0.runs[0].font.size = Pt(14)
            p0.runs[0].font.bold = is_bold

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if indent_in > 0:
            p1.paragraph_format.left_indent = Inches(indent_in)
        if p1.runs:
            p1.runs[0].font.name = "TH Sarabun PSK"
            p1.runs[0].font.size = Pt(14)
            p1.runs[0].font.bold = is_bold

        p2 = c2.paragraphs[0]
        p2.alignment = align2
        if p2.runs:
            p2.runs[0].font.name = "TH Sarabun PSK"
            p2.runs[0].font.size = Pt(14)

        for c in (c0, c1, c2):
            set_cell_margins(c, 40, 40, 80, 80)
            set_cell_border(c, top={'val':'single'}, bottom={'val':'single'}, left={'val':'single'}, right={'val':'single'})

    # Section 1
    s1 = sd1["section_1"]
    add_table_row(t2, s1["id"], s1["title"], "", is_bold=True)
    for it in s1["items"]:
        add_table_row(t2, "", f'{it["code"]} {it["text"]}', it["result"], indent_in=0.25)

    # Section 2
    s2 = sd1["section_2"]
    sub1 = s2["subsections"][0]
    sub2 = s2["subsections"][1]
    add_table_row(t2, s2["id"], s2["title"], "", is_bold=True)
    add_table_row(t2, "", sub1["subtitle"], "", is_bold=True, indent_in=0.15)
    for it in sub1["items"]:
        add_table_row(t2, "", f'- {it["text"]}', it["result"], indent_in=0.3)

    add_table_row(t2, "", sub2["subtitle"], "", is_bold=True, indent_in=0.15)
    for it in sub2["items"]:
        add_table_row(t2, "", f'- {it["text"]}', it["result"], indent_in=0.3)


    # --- DOCX PAGE 3: แบบรายงาน สด.๑ (แผ่น ๒) ---
    doc.add_page_break()

    t3 = doc.add_table(rows=1, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    for idx, w in enumerate(col_w):
        t3.columns[idx].width = w

    hdr3 = t3.rows[0]
    for i, title in enumerate(headers_txt):
        c = hdr3.cells[i]
        c.text = title
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "TH Sarabun PSK"
        p.runs[0].font.size = Pt(14)
        p.runs[0].font.bold = True
        set_cell_margins(c, 60, 60, 80, 80)
        set_cell_border(c, top={'val':'single'}, bottom={'val':'single'}, left={'val':'single'}, right={'val':'single'})

    # Section 3
    s3 = sd1["section_3"]
    add_table_row(t3, s3["id"], s3["title"], "", is_bold=True)
    for it in s3["items"]:
        add_table_row(t3, "", f'{it["code"]} {it["text"]}', it["result"], indent_in=0.25)

    # Section 4
    s4 = sd1["section_4"]
    add_table_row(t3, s4["id"], s4["title"], "", is_bold=True)
    for it in s4["items"]:
        add_table_row(t3, "", f'{it["code"]} {it["text"]}', it["result"], indent_in=0.25)

    # Section 5
    s5 = sd1["section_5"]
    add_table_row(t3, s5["id"], s5["title"], "", is_bold=True)
    for it in s5["items"]:
        add_table_row(t3, "", f'{it["code"]} {it["text"]}', it["result"], indent_in=0.25)

    # Page 3 Signatures: เคาะลงมา 3 เอนเตอร์ จากขอบล่างของตาราง
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36) # เคาะลงมา 3 เอนเตอร์

    corr_sig_data = {
        "type": "signature_block",
        "role": sd1["signatures"]["corrector"]["role"],
        "rank": sd1["signatures"]["corrector"]["rank"],
        "name": sd1["signatures"]["corrector"]["name"],
        "position": sd1["signatures"]["corrector"]["position"]
    }
    insp_sig_data = {
        "type": "signature_block",
        "role": sd1["signatures"]["inspector"]["role"],
        "rank": sd1["signatures"]["inspector"]["rank"],
        "name": sd1["signatures"]["inspector"]["name"],
        "position": sd1["signatures"]["inspector"]["position"],
        "date": sd1["signatures"]["inspector"]["date_text"]
    }

    # 1. Corrector Block (Universal Red Line Standard)
    render_signature_docx(doc, corr_sig_data, axis_inch=4.5, font_size=14, space_after_rank_pt=20)

    # Spacer between blocks
    p_sp_mid = doc.add_paragraph()
    p_sp_mid.paragraph_format.space_before = Pt(8)

    # 2. Inspector Block (Universal Red Line Standard)
    render_signature_docx(doc, insp_sig_data, axis_inch=4.5, font_size=14, space_after_rank_pt=20)


    # --- DOCX PAGE 4: ภาพถ่ายการตรวจ ---
    doc.add_page_break()

    p_p4_t = doc.add_paragraph()
    p_p4_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p4_t = p_p4_t.add_run(ps["title"])
    r_p4_t.font.name = "TH Sarabun PSK"
    r_p4_t.font.size = Pt(16)
    r_p4_t.font.bold = True
    p_p4_t.paragraph_format.space_after = Pt(1)

    p_p4_u = doc.add_paragraph()
    p_p4_u.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p4_u = p_p4_u.add_run(ps["unit"])
    r_p4_u.font.name = "TH Sarabun PSK"
    r_p4_u.font.size = Pt(14)
    r_p4_u.font.bold = True
    p_p4_u.paragraph_format.space_after = Pt(8)

    # 2x2 Photo Table
    t_pic = doc.add_table(rows=2, cols=2)
    t_pic.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_pic.columns[0].width = Inches(3.1)
    t_pic.columns[1].width = Inches(3.1)

    pic_paths = [os.path.join(os.path.dirname(__file__), p) for p in ps["images"]]
    for idx, path in enumerate(pic_paths):
        r_idx = idx // 2
        c_idx = idx % 2
        cell = t_pic.rows[r_idx].cells[c_idx]
        p_cell = cell.paragraphs[0]
        p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if os.path.exists(path):
            p_cell.add_run().add_picture(path, width=Inches(3.0))
        set_cell_margins(cell, 30, 30, 30, 30)

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(12)
    p_cert.paragraph_format.space_after = Pt(4)
    r_cert = p_cert.add_run(ps["certification_text"])
    r_cert.font.name = "TH Sarabun PSK"
    r_cert.font.size = Pt(16)
    r_cert.font.bold = True


    # --- DOCX PAGE 5: บันทึกผลการตรวจอาวุธ (แนวนอน Landscape) ---
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.orientation = WD_ORIENT.LANDSCAPE
    sec2.page_width = Inches(11.69)
    sec2.page_height = Inches(8.27)
    sec2.top_margin = Inches(0.8)
    sec2.bottom_margin = Inches(0.8)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(0.8)

    p_p5_t = doc.add_paragraph()
    p_p5_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p5_t = p_p5_t.add_run(gr["title"])
    r_p5_t.font.name = "TH Sarabun PSK"
    r_p5_t.font.size = Pt(16)
    r_p5_t.font.bold = True
    p_p5_t.paragraph_format.space_after = Pt(1)

    p_p5_u = doc.add_paragraph()
    p_p5_u.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p5_u = p_p5_u.add_run(gr["unit"])
    r_p5_u.font.name = "TH Sarabun PSK"
    r_p5_u.font.size = Pt(14)
    r_p5_u.font.bold = True
    p_p5_u.paragraph_format.space_after = Pt(4)

    # Landscape Table
    t5 = doc.add_table(rows=1, cols=6)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5.autofit = False
    col5_w = [Inches(1.8), Inches(3.2), Inches(1.3), Inches(1.3), Inches(1.2), Inches(1.0)]
    for idx, w in enumerate(col5_w):
        t5.columns[idx].width = w

    hdr5 = t5.rows[0]
    for i, title in enumerate(gr["headers"]):
        c = hdr5.cells[i]
        c.text = title
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "TH Sarabun PSK"
        p.runs[0].font.size = Pt(15)
        p.runs[0].font.bold = True
        set_cell_margins(c, 60, 60, 80, 80)
        set_cell_border(c, top={'val':'single'}, bottom={'val':'single'}, left={'val':'single'}, right={'val':'single'})

    for idx, it in enumerate(gr["items"]):
        row = t5.add_row()
        for c_i, w in enumerate(col5_w):
            row.cells[c_i].width = w

        c0, c1, c2, c3, c4, c5 = row.cells
        if idx == 0:
            c0.text = gr["date_col"]
            p0 = c0.paragraphs[0]
            p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p0.runs[0].font.name = "TH Sarabun PSK"
            p0.runs[0].font.size = Pt(15)
            p0.runs[0].font.bold = True
        else:
            c0.text = ""

        c1.text = it["topic"]
        c2.text = it["found"]
        c3.text = it["fix_needed"]
        c4.text = it["resolution"]
        c5.text = it["note"]

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.left_indent = Inches(0.1)
        p1.runs[0].font.name = "TH Sarabun PSK"
        p1.runs[0].font.size = Pt(15)

        for cell in (c2, c3, c4, c5):
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = "TH Sarabun PSK"
            p.runs[0].font.size = Pt(15)

        for cell in (c0, c1, c2, c3, c4, c5):
            set_cell_margins(cell, 40, 40, 60, 60)
            set_cell_border(cell, top={'val':'single'}, bottom={'val':'single'}, left={'val':'single'}, right={'val':'single'})

    # Merge date cell vertically
    a = t5.rows[1].cells[0]
    b = t5.rows[len(gr["items"])].cells[0]
    a.merge(b)

    # Signature Block Page 5
    gr_sig_data = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"],
        "date": gr["signature"]["date_text"]
    }
    render_signature_docx(doc, gr_sig_data, axis_inch=8.0, font_size=16, space_after_rank_pt=20)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")


# =============================================================================
# 3. GENERATE XLSX (4 Sheets with OpenPyXL & Red Line Standard)
# =============================================================================
def generate_xlsx(output_path):
    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)

    ws1 = wb.create_sheet(title="บันทึกข้อความ")
    ws2 = wb.create_sheet(title="แบบรายงาน สด.๑")
    ws3 = wb.create_sheet(title="ภาพถ่ายการตรวจ")
    ws4 = wb.create_sheet(title="บันทึกผลการตรวจ")

    font_regular = Font(name="TH Sarabun PSK", size=16)
    font_bold = Font(name="TH Sarabun PSK", size=16, bold=True)
    font_title = Font(name="TH Sarabun PSK", size=24, bold=True)
    font_large = Font(name="TH Sarabun PSK", size=18, bold=True)
    font_tbl = Font(name="TH Sarabun PSK", size=14)
    font_tbl_b = Font(name="TH Sarabun PSK", size=14, bold=True)

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
    ws1["A1"].font = Font(name="TH Sarabun PSK", size=13)
    ws1["A1"].alignment = align_center

    ws1["C2"] = "บันทึกข้อความ"
    ws1["C2"].font = Font(name="TH Sarabun PSK", size=29, bold=True)
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

    # Signature Sheet 1 using signature_engine (5 Enters below closing row 16)
    p1_sig_data = {
        "type": "signature_block",
        "rank": p1["signature"]["rank"],
        "name": p1["signature"]["name"],
        "position": p1["signature"]["position"]
    }
    render_signature_xlsx(ws1, p1_sig_data, rank_col="D", name_col="E", start_row=22)

    ws1["E28"] = p1["staff_initials"]["draft_inspect"]
    ws1["E28"].font = font_regular
    ws1["E29"] = p1["staff_initials"]["type_verify"]
    ws1["E29"].font = font_regular

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

    ws2["B3"] = sd1["week_text"]
    ws2["B3"].font = font_bold
    ws2["B3"].alignment = align_center

    ws2["B4"] = sd1["inspection_time"]
    ws2["B4"].font = font_bold
    ws2["B4"].alignment = align_center

    headers2 = ["ลำดับ", "หัวข้อการตรวจ", "ผลการตรวจ"]
    for col_idx, text in enumerate(headers2, start=1):
        col_letter = get_column_letter(col_idx)
        cell = ws2[f"{col_letter}6"]
        cell.value = text
        cell.font = font_bold
        cell.alignment = align_center
        cell.border = thin_border
        cell.fill = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    row_cur = 7
    def add_xl_row(no_val, topic_val, res_val, is_header=False):
        nonlocal row_cur
        c_a = ws2[f"A{row_cur}"]
        c_b = ws2[f"B{row_cur}"]
        c_c = ws2[f"C{row_cur}"]

        c_a.value = no_val
        c_b.value = topic_val
        c_c.value = res_val

        c_a.font = font_tbl_b if is_header else font_tbl
        c_b.font = font_tbl_b if is_header else font_tbl
        c_c.font = font_tbl

        c_a.alignment = align_center
        c_b.alignment = align_left
        c_c.alignment = align_center

        for cell in (c_a, c_b, c_c):
            cell.border = thin_border
        row_cur += 1

    s1 = sd1["section_1"]
    s2 = sd1["section_2"]
    sub1 = s2["subsections"][0]
    sub2 = s2["subsections"][1]
    s3 = sd1["section_3"]
    s4 = sd1["section_4"]
    s5 = sd1["section_5"]

    # Section 1
    add_xl_row(s1["id"], s1["title"], "", is_header=True)
    for it in s1["items"]:
        add_xl_row("", f'{it["code"]} {it["text"]}', it["result"])

    # Section 2
    add_xl_row(s2["id"], s2["title"], "", is_header=True)
    add_xl_row("", sub1["subtitle"], "", is_header=True)
    for it in sub1["items"]:
        add_xl_row("", f'- {it["text"]}', it["result"])

    add_xl_row("", sub2["subtitle"], "", is_header=True)
    for it in sub2["items"]:
        add_xl_row("", f'- {it["text"]}', it["result"])

    # Section 3
    add_xl_row(s3["id"], s3["title"], "", is_header=True)
    for it in s3["items"]:
        add_xl_row("", f'{it["code"]} {it["text"]}', it["result"])

    # Section 4
    add_xl_row(s4["id"], s4["title"], "", is_header=True)
    for it in s4["items"]:
        add_xl_row("", f'{it["code"]} {it["text"]}', it["result"])

    # Section 5
    add_xl_row(s5["id"], s5["title"], "", is_header=True)
    for it in s5["items"]:
        add_xl_row("", f'{it["code"]} {it["text"]}', it["result"])

    # Page 3 Signatures: Stacked Vertically in Column B & C (Universal Red Line Standard)
    row_cur += 2
    render_signature_xlsx(ws2, sd1["signatures"]["corrector"], rank_col="B", name_col="C", start_row=row_cur)
    row_cur += 5
    render_signature_xlsx(ws2, sd1["signatures"]["inspector"], rank_col="B", name_col="C", start_row=row_cur)

    ws2.column_dimensions["A"].width = 10
    ws2.column_dimensions["B"].width = 75
    ws2.column_dimensions["C"].width = 25

    # ------------------ SHEET 3: ภาพถ่ายการตรวจ ------------------
    ws3["B2"] = ps["title"]
    ws3["B2"].font = font_title
    ws3["B2"].alignment = align_center
    ws3["B3"] = ps["unit"]
    ws3["B3"].font = font_bold
    ws3["B3"].alignment = align_center

    ws3["B5"] = "[ภาพถ่ายที่ ๑ ถึง ๔ ได้รับการบันทึกในเอกสาร Word / HTML และคลังภาพ weekly_assets/]"
    ws3["B5"].font = font_regular
    ws3["B5"].alignment = align_center

    ws3["B7"] = ps["certification_text"]
    ws3["B7"].font = font_large
    ws3["B7"].alignment = align_center

    # (การลงนามในแบบบันทึกภาพถ่ายถูกตัดออกเนื่องจากซ้ำซ้อน)

    ws3.column_dimensions["A"].width = 15
    ws3.column_dimensions["B"].width = 65

    # ------------------ SHEET 4: บันทึกผลการตรวจ ------------------
    ws4["C2"] = gr["title"]
    ws4["C2"].font = font_title
    ws4["C2"].alignment = align_center
    ws4["C3"] = gr["unit"]
    ws4["C3"].font = font_bold
    ws4["C3"].alignment = align_center

    for c_i, title in enumerate(gr["headers"], start=1):
        c_let = get_column_letter(c_i)
        cell = ws4[f"{c_let}5"]
        cell.value = title
        cell.font = font_bold
        cell.alignment = align_center
        cell.border = thin_border
        cell.fill = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")

    r_start = 6
    for idx, it in enumerate(gr["items"]):
        row_n = r_start + idx
        if idx == 0:
            ws4[f"A{row_n}"] = gr["date_col"]
            ws4[f"A{row_n}"].alignment = align_center
            ws4[f"A{row_n}"].font = font_bold
        ws4[f"B{row_n}"] = it["topic"]
        ws4[f"C{row_n}"] = it["found"]
        ws4[f"D{row_n}"] = it["fix_needed"]
        ws4[f"E{row_n}"] = it["resolution"]
        ws4[f"F{row_n}"] = it["note"]

        ws4[f"B{row_n}"].alignment = align_left
        for let in ("C", "D", "E", "F"):
            ws4[f"{let}{row_n}"].alignment = align_center

        for let in ("A", "B", "C", "D", "E", "F"):
            ws4[f"{let}{row_n}"].border = thin_border
            ws4[f"{let}{row_n}"].font = font_regular

    # Merge A6:A10 for Date Column
    ws4.merge_cells(f"A{r_start}:A{r_start + len(gr['items']) - 1}")

    # Signature Sheet 4 using signature_engine
    gr_sig_data = {
        "type": "signature_block",
        "label": gr["signature"]["role"],
        "rank": gr["signature"]["rank"],
        "name": gr["signature"]["name"],
        "position": gr["signature"]["position"],
        "date": gr["signature"]["date_text"]
    }
    render_signature_xlsx(ws4, gr_sig_data, rank_col="E", name_col="F", start_row=12)

    ws4.column_dimensions["A"].width = 25
    ws4.column_dimensions["B"].width = 30
    ws4.column_dimensions["C"].width = 15
    ws4.column_dimensions["D"].width = 15
    ws4.column_dimensions["E"].width = 15
    ws4.column_dimensions["F"].width = 25

    wb.save(output_path)
    print(f"Generated XLSX: {output_path}")


# =============================================================================
# MAIN EXECUTION PIPELINE
# =============================================================================
if __name__ == "__main__":
    html_out = "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html"
    docx_out = "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.docx"
    xlsx_out = "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.xlsx"

    print(">>> Executing SUPERCLONE Engine for Weekly Inspection Document...")
    generate_html(html_out)
    generate_docx(docx_out)
    generate_xlsx(xlsx_out)
    print(">>> SUPERCLONE Engine Compilation COMPLETE 100%!")
