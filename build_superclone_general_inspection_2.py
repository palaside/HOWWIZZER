#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUPERCLONE Production Engine (100% Authentic Military Standard)
Document: บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ ๒) ประจำปี ๒๕๖๙ (ครบทั้ง ๑๘ หน้า)
Reference: D:\\Project\\WEPAPP\\docs\\thai-docx.skill\\ระบบเอกสาร\\17.บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ 2).pdf
Standard: RULE-PROD-DOC-ENGINE-V1 / RULE-UNIVERSAL-SIGNATURE-BLOCK-V1 (Red Line Standard)
Upgraded Tuning:
  - Font Size: 16 pt (Official Thai Royal Army standard)
  - Cascade Indentation: 4-tier hierarchy matching original scan
  - Authentic Dotted Fill Lines in Header Metadata
  - Columnar Tab Alignment for 4 Commanders
  - Thai Numerals 100%
Outputs:
  - HTML: บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html (18 Pages A4 Portrait)
  - DOCX: บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.docx (18 Pages A4 Portrait)
  - XLSX: บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.xlsx (7 Sheets A4 Portrait Print Ready)
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

# -----------------------------------------------------------------------------
# Base Garuda PNG
# -----------------------------------------------------------------------------
GARUDA_BASE64 = (
    "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"
    "QmCC"
)

# Thai Numeral Converter
THAI_DIGITS = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
def to_thai(val):
    return str(val).translate(THAI_DIGITS)

# Continuation Slugs
SLUGS = {
    (1, 1): "/๒.๒.๓ การใช้วัสดุ...",
    (2, 1): "/ถ้ารายใด...",
    (2, 2): "/ตามผนวก...",
    (2, 3): "/ลงใน...",
    (2, 4): "/๒.๓ ข้อบกพร่อง...",
    (3, 1): "/...๑. ข้อ ๔๑.๑ การสำรวจสิ่งอุปกรณ์",
    (3, 2): "/...ข้อ ๒. วิธีระวังรักษา",
    (3, 3): "/...ข. เมื่อชำรุดผิดปกติหรือสูญหาย",
    (4, 1): "/...ข้อเสนอแนะ",
    (4, 2): "/...ข้อเสนอแนะ",
    (6, 1): "/...หมายเหตุ"
}

# Load SSOT JSON
JSON_PATH = "table_layout_general_inspection_2.json"
with open(JSON_PATH, "r", encoding="utf-8") as f:
    DATA = json.load(f)

print(f"Loaded SSOT Blueprint: {DATA['document_info']['title']} ({DATA['document_info']['total_pages']} pages)")

# -----------------------------------------------------------------------------
# 1. BUILD HTML MULTI-PAGE DOCUMENT (18 Pages A4 Portrait)
# -----------------------------------------------------------------------------
def build_html():
    html_out = "บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html"
    
    html = []
    html.append("""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>บันทึกผลการตรวจกิจการทั่วไป (ชุดตรวจที่ ๒) - SUPERCLONE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');

        @page {
            size: A4 portrait;
            margin: 0;
        }

        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: #525659;
            font-family: 'TH Sarabun New', 'TH Sarabun PSK', 'Sarabun', sans-serif;
            font-size: 15.5pt;
            font-weight: 400;
            line-height: 1.24;
            color: #000;
        }

        .page-portrait {
            width: 210mm;
            min-height: 297mm;
            height: 297mm;
            background: #ffffff;
            margin: 15px auto;
            padding: 12mm 18mm 10mm 22mm;
            position: relative;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        @media print {
            body {
                background-color: transparent;
            }
            .page-portrait {
                margin: 0;
                box-shadow: none;
                width: 210mm;
                height: 297mm;
                page-break-after: always;
            }
        }

        /* MEMO PAGE 1 STYLES */
        .memo-header-container {
            position: relative;
            width: 100%;
            height: 26mm;
            margin-bottom: 2mm;
        }

        .garuda-img {
            position: absolute;
            left: 0;
            top: -2mm;
            height: 18mm;
            width: auto;
        }

        .memo-stamps-container {
            position: absolute;
            right: 0;
            top: -5mm;
            display: flex;
            gap: 2.5mm;
            z-index: 5;
        }

        .stamp-box {
            border: 1.5px solid #1a3c87;
            color: #1a3c87;
            font-size: 8.5pt;
            line-height: 1.2;
            padding: 1.2mm 2mm;
            border-radius: 3px;
            background: rgba(235, 243, 255, 0.4);
            min-width: 33mm;
        }

        .stamp-title {
            font-weight: bold;
            font-size: 8.5pt;
            text-align: center;
            border-bottom: 0.5px solid #1a3c87;
            padding-bottom: 1px;
            margin-bottom: 1px;
        }

        .stamp-row {
            display: flex;
            justify-content: space-between;
        }

        .stamp-val {
            font-weight: bold;
        }

        .memo-doc-title {
            font-size: 29pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.1;
            padding-top: 3mm;
            letter-spacing: 0.5px;
            margin-left: 15mm;
            margin-right: 68mm;
        }

        .memo-meta-section {
            width: 100%;
            margin-bottom: 2.5mm;
        }

        .memo-meta-row {
            display: flex;
            align-items: flex-end;
            margin-bottom: 2mm;
            font-size: 15.5pt;
        }

        .memo-meta-label {
            font-weight: 600;
            font-size: 20pt;
            line-height: 1.05;
            white-space: nowrap;
            margin-right: 0;
            padding-bottom: 1.5px;
        }

        .memo-meta-fill {
            flex: 1;
            border-bottom: 1px dotted #444;
            display: flex;
            align-items: flex-end;
            padding-left: 2ch;
            padding-bottom: 1.5px;
            font-size: 16pt;
            line-height: 1.15;
        }

        .memo-body {
            font-size: 15.5pt;
            line-height: 1.30;
            text-align: justify;
            text-justify: inter-cluster;
            margin-top: 2.5mm;
        }

        .memo-para {
            text-indent: 25mm;
            margin-bottom: 3mm;
        }

        /* SIGNATURE ENGINE RED LINE CSS */
        .sig-block {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 15.5pt;
            line-height: 1.2;
        }
        .sig-name-pos-group {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }
        .sig-name-wrapper {
            position: relative;
            display: inline-block;
            white-space: nowrap;
        }
        .sig-rank-anchor {
            position: absolute;
            right: 100%;
            bottom: 0;
            white-space: nowrap;
            padding-right: 2px;
        }
        .sig-name {
            white-space: nowrap;
            text-align: center;
        }
        .sig-pos {
            white-space: nowrap;
            text-align: center;
            margin-top: 1px;
        }

        /* REPORT PAGES 2-18 STYLES (ทบ. ๑๐๕-๐๐๙) */
        .report-form-code {
            text-align: right;
            font-size: 13.5pt;
            font-weight: bold;
            margin-bottom: 0.6mm;
        }

        .report-title {
            text-align: center;
            font-size: 16.5pt;
            font-weight: bold;
            line-height: 1.15;
            margin-bottom: 0.8mm;
        }

        .report-subtitle {
            text-align: center;
            font-size: 15pt;
            font-weight: bold;
            line-height: 1.2;
            margin-bottom: 1.5mm;
        }

        .report-meta-grid {
            width: 100%;
            font-size: 14.5pt;
            line-height: 1.22;
            margin-bottom: 1.2mm;
        }

        .meta-line {
            display: flex;
            align-items: baseline;
            margin-bottom: 0.8mm;
        }

        .meta-lbl {
            white-space: nowrap;
        }

        .meta-val-dots {
            border-bottom: 1px dotted #333;
            padding: 0 4px;
            display: inline-block;
            vertical-align: bottom;
            line-height: 1.10;
            min-height: 4.8mm;
        }

        .report-subnote {
            text-align: center;
            font-size: 12.5pt;
            margin-top: 0.4mm;
            margin-bottom: 1.2mm;
        }

        .report-divider {
            border-top: 1.5px solid #000;
            margin-bottom: 1.5mm;
        }

        /* SECTION 1: 4 COMMANDERS */
        .sec1-title {
            font-size: 14.5pt;
            font-weight: bold;
            margin-top: 0.8mm;
            margin-bottom: 0.8mm;
        }

        .cmd-list {
            margin-left: 10mm;
            margin-bottom: 1.5mm;
        }

        .cmd-row {
            display: flex;
            font-size: 14.5pt;
            line-height: 1.22;
            margin-bottom: 0.5mm;
        }

        .cmd-unit {
            width: 60mm;
        }

        .cmd-rank-name {
            width: 42mm;
        }

        .cmd-surname {
            width: 45mm;
        }

        /* SECTION 2: CASCADE HIERARCHY */
        .sec2-title {
            font-size: 14pt;
            font-weight: bold;
            margin-top: 1mm;
            margin-bottom: 0.6mm;
        }

        .tier2-title {
            font-size: 14pt;
            font-weight: bold;
            margin-left: 8mm;
            margin-top: 0.6mm;
            margin-bottom: 0.5mm;
        }

        .tier2-text {
            font-size: 13.5pt;
            line-height: 1.18;
            text-align: justify;
            text-justify: inter-cluster;
            text-indent: 10mm;
            margin-left: 8mm;
            margin-bottom: 1mm;
        }

        .tier2-subitem {
            font-size: 13.5pt;
            line-height: 1.18;
            text-align: justify;
            text-justify: inter-cluster;
            margin-left: 14mm;
            margin-bottom: 0.6mm;
        }

        .finding-block {
            margin-left: 8mm;
            margin-bottom: 1mm;
            font-size: 13.5pt;
            line-height: 1.18;
            text-align: justify;
            text-justify: inter-cluster;
        }

        .finding-code-title {
            font-weight: bold;
        }

        .rec-container {
            margin-top: 0.5mm;
            margin-bottom: 0.6mm;
        }

        .rec-header {
            text-align: center;
            font-weight: bold;
            font-size: 13.5pt;
            margin-top: 0.4mm;
            margin-bottom: 0.4mm;
            margin-left: 15mm;
            margin-right: 15mm;
        }

        .rec-item {
            margin-left: 14mm;
            margin-bottom: 0.6mm;
            font-size: 13.5pt;
            line-height: 1.18;
            text-align: justify;
            text-justify: inter-cluster;
        }

        .rec-subitem-deep {
            margin-left: 32mm;
            margin-bottom: 0.6mm;
            font-size: 14pt;
            line-height: 1.22;
        }

        .deficiencies-block {
            margin-left: 8mm;
            margin-top: 1.5mm;
            margin-bottom: 1.5mm;
            font-size: 14pt;
        }

        .def-row {
            display: flex;
            width: 55mm;
            justify-content: space-between;
            margin-bottom: 0.6mm;
        }

        .legal-disclaimer {
            font-size: 12.5pt;
            line-height: 1.22;
            margin-top: 1.5mm;
            margin-bottom: 1.5mm;
            text-align: justify;
            text-justify: inter-cluster;
            border-top: 0.5px solid #999;
            padding-top: 1.2mm;
        }

        /* BOTTOM SIGNATURE BLOCK (ทบ. ๑๐๕-๐๐๙) */
        .bottom-sig-container {
            width: 100%;
            margin-top: auto;
            padding-top: 1mm;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            font-size: 13.5pt;
            line-height: 1.18;
        }

        .slug-line {
            font-size: 12.5pt;
            margin-bottom: 0.8mm;
            font-style: italic;
        }

        .bottom-sig-line {
            white-space: nowrap;
            margin-bottom: 0.5mm;
        }

        .bottom-date-line {
            white-space: nowrap;
            margin-right: 16mm;
        }
    </style>
</head>
<body>
""")

    # -------------------------------------------------------------------------
    # PAGE 1: MEMO
    # -------------------------------------------------------------------------
    p1 = DATA["page_1_memo"]
    stamps = p1["stamps"]
    h = p1["header"]
    sig = p1["signature"]

    # Render memo signature HTML via signature_engine
    sig_html = render_signature_html({
        "rank": sig["rank"],
        "name": sig["name"],
        "position": sig["position"],
        "left_margin_mm": 125,
        "name_gap_mm": 14
    })

    html.append(f"""
    <!-- PAGE 1: OFFICIAL MEMO -->
    <div class="page-portrait" id="page-1">
        <div>
            <div class="memo-header-container">
                <img src="data:image/png;base64,{GARUDA_BASE64}" alt="Garuda" class="garuda-img">
                <div class="memo-doc-title">{h['title']}</div>
                <div class="memo-stamps-container">
                    <div class="stamp-box">
                        <div class="stamp-title">{stamps[0]['line1']}</div>
                        <div class="stamp-row"><span>เลขที่รับ</span><span class="stamp-val">{stamps[0]['reg_no']}</span></div>
                        <div class="stamp-row"><span>วันที่</span><span class="stamp-val">{stamps[0]['date']}</span></div>
                        <div class="stamp-row"><span>เวลา</span><span class="stamp-val">{stamps[0]['time']}</span></div>
                    </div>
                    <div class="stamp-box">
                        <div class="stamp-title">{stamps[1]['line1']}<br>{stamps[1]['line2']}</div>
                        <div class="stamp-row"><span>เลขที่รับ</span><span class="stamp-val">{stamps[1]['reg_no']}</span></div>
                        <div class="stamp-row"><span>วันที่</span><span class="stamp-val">{stamps[1]['date']}</span></div>
                        <div class="stamp-row"><span>เวลา</span><span class="stamp-val">{stamps[1]['time']}</span></div>
                    </div>
                </div>
            </div>

            <div class="memo-meta-section">
                <div class="memo-meta-row">
                    <span class="memo-meta-label">ส่วนราชการ</span>
                    <div class="memo-meta-fill">{h['dept']}</div>
                </div>
                <div class="memo-meta-row">
                    <div style="flex: 1.1; display: flex; align-items: flex-end; margin-right: 4mm;">
                        <span class="memo-meta-label">ที่</span>
                        <div class="memo-meta-fill">{h['doc_no']}</div>
                    </div>
                    <div style="flex: 0.9; display: flex; align-items: flex-end;">
                        <span class="memo-meta-label">วันที่</span>
                        <div class="memo-meta-fill">{h['date']}</div>
                    </div>
                </div>
                <div class="memo-meta-row">
                    <span class="memo-meta-label">เรื่อง</span>
                    <div class="memo-meta-fill">{h['subject']}</div>
                </div>
                <div class="memo-meta-row">
                    <span class="memo-meta-label">เรียน</span>
                    <div class="memo-meta-fill">{h['to']}</div>
                </div>
                <div class="memo-meta-row" style="align-items: flex-start;">
                    <span class="memo-meta-label">อ้างถึง</span>
                    <div style="flex: 1; display: flex; flex-direction: column; align-items: flex-start; padding-left: 2ch; font-size: 16pt; line-height: 1.25;">
                        <div>{h['references'][0]}</div>
                        <div>{h['references'][1]}</div>
                    </div>
                </div>
                <div class="memo-meta-row" style="align-items: flex-start;">
                    <span class="memo-meta-label">สิ่งที่ส่งมาด้วย</span>
                    <div style="flex: 1; display: flex; justify-content: space-between; align-items: baseline; padding-left: 2ch; font-size: 16pt; line-height: 1.25;">
                        <div>บันทึกผลการตรวจของนายทหารจเร ทบ. ๑๐๕-๐๐๙</div>
                        <div style="white-space: nowrap;">จำนวน  ๖  ชุด</div>
                    </div>
                </div>
            </div>

            <div class="memo-body">
                <div class="memo-para">{p1['body_paragraphs'][0]}</div>
                <div class="memo-para">{p1['body_paragraphs'][1]}</div>
            </div>
        </div>

        <!-- SIGNATURE BLOCK (เลื่อนมาทางซ้าย ให้เลข ๙ ตรงกับแนวขวาของเนื้อหา) -->
        <div style="margin-top: 55pt; display: flex; justify-content: flex-end;">
            <div class="sig-block" style="margin-right: 0; font-size: 16pt; line-height: 1.2;">
                <div class="sig-name-pos-group" style="margin-left: 0;">
                    <div class="sig-name-wrapper" style="margin-top: 22pt;">
                        <span class="sig-rank-anchor" style="font-size: 16pt; right: 100%; bottom: 0; padding-right: 4px;">{sig['rank']}</span>
                        <div class="sig-name" style="font-size: 16pt;">({sig['name']})</div>
                    </div>
                    <div class="sig-pos" style="font-size: 16pt; margin-top: 2px;">{sig['position']}</div>
                </div>
            </div>
        </div>
    </div>
""")

    # -------------------------------------------------------------------------
    # PAGES 2-18: INSPECTION SETS (6 Sets)
    # -------------------------------------------------------------------------
    page_counter = 1
    for s_idx, s in enumerate(DATA["inspection_sets"]):
        set_no = s["set_no"]
        title = s["title"]
        inspector = s["inspector"]
        inspectee = s["inspectee"]
        inspectee_pos = s["inspectee_position"]
        day = to_thai(s["date"])
        month = s["month"]
        year = to_thai(s["year"])
        year_short = to_thai(s["year_short"])
        total_sheets = s["total_sheets"]
        commanders = s["commanders"]

        for p_idx, page in enumerate(s["pages"]):
            page_counter += 1
            sheet_no = page["sheet_no"]
            has_hdr = page["has_header_metadata"]
            contents = page["content"]

            html.append(f"""
    <!-- PAGE {page_counter}: SET {set_no} SHEET {sheet_no}/{total_sheets} -->
    <div class="page-portrait" id="page-{page_counter}">
        <div>
""")

            if has_hdr:
                html.append(f"""
            <div class="report-form-code">ทบ. ๑๐๕ - ๐๐๙</div>
            <div class="report-title">บันทึกผลการตรวจของนายทหารจเร</div>
            <div class="report-subtitle">เรื่อง {title}</div>
            
            <div class="report-meta-grid">
                <div class="meta-line">
                    <span class="meta-lbl">หน่วย</span>
                    <span class="meta-val-dots" style="width: 50mm;">ป.๔ พัน.๔</span>
                    <span class="meta-lbl" style="margin-left: auto;">ชื่อ ผบ.หน่วย</span>
                    <span class="meta-val-dots" style="width: 55mm;">พ.ท. พรชัย  มากเทพพงษ์</span>
                </div>
                <div class="meta-line">
                    <span class="meta-lbl">ตรวจเมื่อวันที่</span>
                    <span class="meta-val-dots" style="width: 25mm; text-align: center;">{day}</span>
                    <span class="meta-lbl" style="margin-left: 6mm;">เดือน</span>
                    <span class="meta-val-dots" style="width: 32mm; text-align: center;">{month}</span>
                    <span class="meta-lbl" style="margin-left: 6mm;">พ.ศ.</span>
                    <span class="meta-val-dots" style="width: 32mm; text-align: center;">{year}</span>
                </div>
                <div class="meta-line">
                    <span class="meta-lbl">ผู้รับตรวจ</span>
                    <span class="meta-val-dots" style="width: 48mm;">{inspectee}</span>
                    <span class="meta-lbl" style="margin-left: 4mm;">ตำแหน่ง</span>
                    <span class="meta-val-dots" style="flex: 1;">{inspectee_pos}</span>
                </div>
                <div class="meta-line">
                    <span class="meta-lbl">ผู้ตรวจ</span>
                    <span class="meta-val-dots" style="width: 65mm;">{inspector}</span>
                    <div style="margin-left: auto; display: flex; align-items: baseline;">
                        <span class="meta-lbl">แผ่นที่</span>
                        <span class="meta-val-dots" style="width: 14mm; text-align: center;">{to_thai(sheet_no)}</span>
                        <span class="meta-lbl" style="margin: 0 2mm;">ในจำนวน</span>
                        <span class="meta-val-dots" style="width: 14mm; text-align: center;">{to_thai(total_sheets)}</span>
                        <span class="meta-lbl">แผ่น</span>
                    </div>
                </div>
            </div>
            <div class="report-subnote">(เก็บหลักฐานนี้ไว้เพื่อดำเนินการแก้ไขและแสดงต่อ นายทหารจเรในการตรวจครั้งต่อไป)</div>
            <div class="report-divider"></div>
""")
            else:
                html.append(f"""
            <div class="report-form-code">ทบ. ๑๐๕ - ๐๐๙-๑</div>
            <div class="report-title">บันทึกผลการตรวจของนายทหารจเร (ต่อ)</div>
            <div style="display: flex; justify-content: flex-end; align-items: baseline; font-size: 15pt; margin-bottom: 2mm;">
                <span>แผ่นที่</span>
                <span class="meta-val-dots" style="width: 14mm; text-align: center; margin: 0 2mm;">{to_thai(sheet_no)}</span>
                <span>ในจำนวน</span>
                <span class="meta-val-dots" style="width: 14mm; text-align: center; margin: 0 2mm;">{to_thai(total_sheets)}</span>
                <span>แผ่น</span>
            </div>
            <div class="report-divider"></div>
""")

            # Render page content elements
            for item in contents:
                itype = item.get("type", "")

                if itype == "section_1":
                    html.append(f"""
            <div class="sec1-title">{item['title']}</div>
            <div class="cmd-list">
""")
                    for cmd in commanders:
                        # Split unit and rank-name/surname if possible
                        parts = cmd['commander'].split()
                        rank_first = parts[0] + " " + parts[1] if len(parts) >= 2 else cmd['commander']
                        surname = " ".join(parts[2:]) if len(parts) >= 3 else ""
                        html.append(f"""
                <div class="cmd-row">
                    <span class="cmd-unit">{cmd['unit']}</span>
                    <span class="cmd-rank-name">{rank_first}</span>
                    <span class="cmd-surname">{surname}</span>
                </div>
""")
                    html.append("""            </div>""")

                elif itype == "section_2_intro":
                    html.append(f"""
            <div class="sec2-title">{item['title']}</div>
            <div class="tier2-title">{item['method_title']}</div>
""")
                    if "method_text" in item:
                        html.append(f"""            <div class="tier2-text">{item['method_text']}</div>""")
                    elif "method_items" in item:
                        for m in item["method_items"]:
                            html.append(f"""            <div class="tier2-subitem">{m.replace(chr(10), '<br>')}</div>""")

                elif itype == "continuation_text":
                    formatted_text = item["text"].replace("\n", "<br>")
                    html.append(f"""            <div class="tier2-text" style="text-indent: 0;">{formatted_text}</div>""")

                elif itype == "findings":
                    if "subtitle" in item:
                        html.append(f"""            <div class="tier2-title">{item['subtitle']}</div>""")
                    for f in item["items"]:
                        html.append(f"""
            <div class="finding-block">
                <div><span class="finding-code-title">{f['finding_code']} {f['topic']}</span> {f['finding_text']}</div>
""")
                        if f.get("recommendations"):
                            html.append("""                <div class="rec-container"><div class="rec-header">ข้อเสนอแนะ</div>""")
                            for rec in f["recommendations"]:
                                # Check if rec contains sub-tier rules like ข้าราชการที่มีตำแหน่งตั้งแต่...
                                rec_lines = rec.split("\n")
                                html.append(f"""                    <div class="rec-item">{rec_lines[0]}</div>""")
                                for sub_line in rec_lines[1:]:
                                    html.append(f"""                    <div class="rec-subitem-deep">{sub_line}</div>""")
                            html.append("""                </div>""")
                        html.append("""            </div>""")

                elif itype == "deficiencies_summary":
                    html.append("""            <div class="deficiencies-block">""")
                    for d in item["items"]:
                        html.append(f"""                <div class="def-row"><span style="font-weight: bold;">{d['title']}</span><span>{d['value']}</span></div>""")
                    html.append("""            </div>""")

                elif itype == "legal_disclaimer":
                    html.append(f"""            <div class="legal-disclaimer">{item['text']}</div>""")

            # Continuation Slug & Bottom Signature block on each sheet
            slug_text = SLUGS.get((set_no, sheet_no), "")
            slug_html = f'<div class="slug-line">{slug_text}</div>' if slug_text else ""

            html.append(f"""
        </div>
        <div class="bottom-sig-container">
            {slug_html}
            <div class="bottom-sig-line">ลงชื่อ........................ พ.อ. ................................................................นายทหารจเร  ผู้ตรวจ</div>
            <div class="bottom-date-line">(........{day}......../........{month}......../........{year_short}........)</div>
        </div>
    </div>
""")

    html.append("""</body>
</html>""")

    with open(html_out, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print(f"Successfully generated HTML: {html_out} (18 Pages)")

# -----------------------------------------------------------------------------
# 2. BUILD DOCX MULTI-PAGE DOCUMENT (18 Pages A4 Portrait)
# -----------------------------------------------------------------------------
def build_docx():
    docx_out = "บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.docx"
    doc = Document()

    # Configure Default Style Font: 15.5 pt
    style = doc.styles['Normal']
    font = style.font
    font.name = 'TH Sarabun New'
    font.size = Pt(15.5)
    font.color.rgb = RGBColor(0, 0, 0)
    
    rPr = style.element.get_or_add_rPr()
    rFonts = parse_xml(r'<w:rFonts %s w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New"/>' % nsdecls('w'))
    rPr.append(rFonts)

    def set_run_font(run, size_pt=15.5, bold=False):
        run.font.name = 'TH Sarabun New'
        run.font.size = Pt(size_pt)
        run.bold = bold
        rpr = run._r.get_or_add_rPr()
        rf = parse_xml(r'<w:rFonts %s w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New"/>' % nsdecls('w'))
        rpr.append(rf)

    # Section Margins: Top 2.0cm, Bottom 2.0cm, Left 2.5cm, Right 2.0cm
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.orientation = WD_ORIENT.PORTRAIT
    section.top_margin = Inches(0.79)
    section.bottom_margin = Inches(0.79)
    section.left_margin = Inches(0.98)
    section.right_margin = Inches(0.79)

    # ---------------- PAGE 1: MEMO ----------------
    p1 = DATA["page_1_memo"]
    h = p1["header"]
    sig = p1["signature"]

    # Title "บันทึกข้อความ"
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run(h["title"])
    set_run_font(run_t, 29, bold=True)

    def add_meta(label, value):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(2)
        r_lbl = p.add_run(label + "  ")
        set_run_font(r_lbl, 18, bold=True)
        r_val = p.add_run(value)
        set_run_font(r_val, 16, bold=False)

    add_meta("ส่วนราชการ", h["dept"])
    
    p_num_date = doc.add_paragraph()
    p_num_date.paragraph_format.line_spacing = 1.25
    p_num_date.paragraph_format.space_after = Pt(2)
    r1 = p_num_date.add_run("ที่  ")
    set_run_font(r1, 18, bold=True)
    r2 = p_num_date.add_run(h["doc_no"] + "              ")
    set_run_font(r2, 16, bold=False)
    r3 = p_num_date.add_run("วันที่  ")
    set_run_font(r3, 18, bold=True)
    r4 = p_num_date.add_run(h["date"])
    set_run_font(r4, 16, bold=False)

    add_meta("เรื่อง", h["subject"])
    add_meta("เรียน", h["to"])

    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.line_spacing = 1.25
    p_ref.paragraph_format.space_after = Pt(2)
    r_refl = p_ref.add_run("อ้างถึง  ")
    set_run_font(r_refl, 18, bold=True)
    r_ref1 = p_ref.add_run(h["references"][0] + "\n        " + h["references"][1])
    set_run_font(r_ref1, 16, bold=False)

    add_meta("สิ่งที่ส่งมาด้วย", h["attachments"])

    for para_text in p1["body_paragraphs"]:
        p_body = doc.add_paragraph()
        p_body.paragraph_format.first_line_indent = Inches(0.8)
        p_body.paragraph_format.line_spacing = 1.35
        p_body.paragraph_format.space_after = Pt(4)
        p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_b = p_body.add_run(para_text)
        set_run_font(r_b, 16, bold=False)

    for _ in range(3):
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(0)
        p_sp.paragraph_format.line_spacing = 1.0

    render_signature_docx(doc, {
        "rank": sig["rank"],
        "name": sig["name"],
        "position": sig["position"],
        "center_x_inches": 5.2
    })

    # ---------------- PAGES 2-18: INSPECTION SETS ----------------
    for s in DATA["inspection_sets"]:
        set_no = s["set_no"]
        title = s["title"]
        inspector = s["inspector"]
        inspectee = s["inspectee"]
        inspectee_pos = s["inspectee_position"]
        day = to_thai(s["date"])
        month = s["month"]
        year = to_thai(s["year"])
        year_short = to_thai(s["year_short"])
        total_sheets = s["total_sheets"]
        commanders = s["commanders"]

        for page in s["pages"]:
            doc.add_page_break()
            sheet_no = page["sheet_no"]
            has_hdr = page["has_header_metadata"]
            contents = page["content"]

            p_code = doc.add_paragraph()
            p_code.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p_code.paragraph_format.space_after = Pt(2)
            run_c = p_code.add_run("ทบ. ๑๐๕ - ๐๐๙" if has_hdr else "ทบ. ๑๐๕ - ๐๐๙-๑")
            set_run_font(run_c, 14, bold=True)

            p_rt = doc.add_paragraph()
            p_rt.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_rt.paragraph_format.space_after = Pt(2)
            run_rt = p_rt.add_run("บันทึกผลการตรวจของนายทหารจเร" if has_hdr else "บันทึกผลการตรวจของนายทหารจเร (ต่อ)")
            set_run_font(run_rt, 18, bold=True)

            if has_hdr:
                p_sub = doc.add_paragraph()
                p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_sub.paragraph_format.space_after = Pt(4)
                run_sub = p_sub.add_run(f"เรื่อง {title}")
                set_run_font(run_sub, 16, bold=True)

                p_m1 = doc.add_paragraph()
                p_m1.paragraph_format.line_spacing = 1.3
                p_m1.paragraph_format.space_after = Pt(1)
                r_m1 = p_m1.add_run(f"หน่วย  ป.๔ พัน.๔{' '*35}ชื่อ ผบ.หน่วย  พ.ท. พรชัย  มากเทพพงษ์")
                set_run_font(r_m1, 15)

                p_m2 = doc.add_paragraph()
                p_m2.paragraph_format.line_spacing = 1.3
                p_m2.paragraph_format.space_after = Pt(1)
                r_m2 = p_m2.add_run(f"ตรวจเมื่อวันที่  {day}  เดือน  {month}  พ.ศ.  {year}")
                set_run_font(r_m2, 15)

                p_m3 = doc.add_paragraph()
                p_m3.paragraph_format.line_spacing = 1.3
                p_m3.paragraph_format.space_after = Pt(1)
                r_m3 = p_m3.add_run(f"ผู้รับตรวจ  {inspectee}  ตำแหน่ง  {inspectee_pos}")
                set_run_font(r_m3, 15)

                p_m4 = doc.add_paragraph()
                p_m4.paragraph_format.line_spacing = 1.3
                p_m4.paragraph_format.space_after = Pt(2)
                r_m4 = p_m4.add_run(f"ผู้ตรวจ  {inspector}{' '*30}แผ่นที่  {to_thai(sheet_no)}  ในจำนวน  {to_thai(total_sheets)}  แผ่น")
                set_run_font(r_m4, 15)

                p_note = doc.add_paragraph()
                p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_note.paragraph_format.space_after = Pt(4)
                r_nt = p_note.add_run("(เก็บหลักฐานนี้ไว้เพื่อดำเนินการแก้ไขและแสดงต่อ นายทหารจเรในการตรวจครั้งต่อไป)")
                set_run_font(r_nt, 13.5)
            else:
                p_sh = doc.add_paragraph()
                p_sh.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                p_sh.paragraph_format.space_after = Pt(4)
                r_sh = p_sh.add_run(f"แผ่นที่  {to_thai(sheet_no)}  ในจำนวน  {to_thai(total_sheets)}  แผ่น")
                set_run_font(r_sh, 15)

            p_div = doc.add_paragraph()
            p_div.paragraph_format.space_after = Pt(4)
            p_div_border = parse_xml(r'<w:pBdr %s><w:bottom w:val="single" w:sz="12" w:space="1" w:color="auto"/></w:pBdr>' % nsdecls('w'))
            p_div._p.get_or_add_pPr().append(p_div_border)

            for item in contents:
                itype = item.get("type", "")

                if itype == "section_1":
                    p_s1 = doc.add_paragraph()
                    p_s1.paragraph_format.space_before = Pt(3)
                    p_s1.paragraph_format.space_after = Pt(2)
                    r_s1 = p_s1.add_run(item["title"])
                    set_run_font(r_s1, 15.5, bold=True)

                    for cmd in commanders:
                        p_cmd = doc.add_paragraph()
                        p_cmd.paragraph_format.line_spacing = 1.35
                        p_cmd.paragraph_format.space_after = Pt(1)
                        r_u = p_cmd.add_run(f"    {cmd['unit']}")
                        set_run_font(r_u, 15.5)
                        r_c = p_cmd.add_run(f"{' '*12}{cmd['commander']}")
                        set_run_font(r_c, 15.5)

                elif itype == "section_2_intro":
                    p_s2 = doc.add_paragraph()
                    p_s2.paragraph_format.space_before = Pt(4)
                    p_s2.paragraph_format.space_after = Pt(2)
                    r_s2 = p_s2.add_run(item["title"])
                    set_run_font(r_s2, 15.5, bold=True)

                    p_mth = doc.add_paragraph()
                    p_mth.paragraph_format.space_after = Pt(2)
                    r_mth = p_mth.add_run(f"    {item['method_title']}")
                    set_run_font(r_mth, 15.5, bold=True)

                    if "method_text" in item:
                        p_mt = doc.add_paragraph()
                        p_mt.paragraph_format.first_line_indent = Inches(0.5)
                        p_mt.paragraph_format.line_spacing = 1.32
                        p_mt.paragraph_format.space_after = Pt(3)
                        p_mt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                        r_mt = p_mt.add_run(item["method_text"])
                        set_run_font(r_mt, 15)
                    elif "method_items" in item:
                        for m in item["method_items"]:
                            p_mi = doc.add_paragraph()
                            p_mi.paragraph_format.line_spacing = 1.32
                            p_mi.paragraph_format.space_after = Pt(2)
                            p_mi.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                            r_mi = p_mi.add_run(f"    {m}")
                            set_run_font(r_mi, 15)

                elif itype == "continuation_text":
                    p_cont = doc.add_paragraph()
                    p_cont.paragraph_format.line_spacing = 1.32
                    p_cont.paragraph_format.space_after = Pt(3)
                    p_cont.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    r_ct = p_cont.add_run(item["text"])
                    set_run_font(r_ct, 15)

                elif itype == "findings":
                    if "subtitle" in item:
                        p_subf = doc.add_paragraph()
                        p_subf.paragraph_format.space_before = Pt(3)
                        p_subf.paragraph_format.space_after = Pt(2)
                        r_subf = p_subf.add_run(f"    {item['subtitle']}")
                        set_run_font(r_subf, 15.5, bold=True)

                    for f in item["items"]:
                        p_f = doc.add_paragraph()
                        p_f.paragraph_format.line_spacing = 1.32
                        p_f.paragraph_format.space_after = Pt(2)
                        p_f.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                        
                        r_fhdr = p_f.add_run(f"    {f['finding_code']} {f['topic']} ")
                        set_run_font(r_fhdr, 15, bold=True)
                        r_fbody = p_f.add_run(f"{f['finding_text']}")
                        set_run_font(r_fbody, 15)

                        if f.get("recommendations"):
                            p_rhdr = doc.add_paragraph()
                            p_rhdr.paragraph_format.space_before = Pt(2)
                            p_rhdr.paragraph_format.space_after = Pt(1)
                            p_rhdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            r_rhdr = p_rhdr.add_run("ข้อเสนอแนะ")
                            set_run_font(r_rhdr, 15, bold=True)

                            for rec in f["recommendations"]:
                                rec_lines = rec.split("\n")
                                p_ritem = doc.add_paragraph()
                                p_ritem.paragraph_format.left_indent = Inches(0.6)
                                p_ritem.paragraph_format.line_spacing = 1.32
                                p_ritem.paragraph_format.space_after = Pt(2)
                                p_ritem.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                                r_ri = p_ritem.add_run(rec_lines[0])
                                set_run_font(r_ri, 15)

                                for sub_l in rec_lines[1:]:
                                    p_subl = doc.add_paragraph()
                                    p_subl.paragraph_format.left_indent = Inches(1.2)
                                    p_subl.paragraph_format.line_spacing = 1.32
                                    p_subl.paragraph_format.space_after = Pt(1.5)
                                    r_sli = p_subl.add_run(sub_l)
                                    set_run_font(r_sli, 15)

                elif itype == "deficiencies_summary":
                    for d in item["items"]:
                        p_def = doc.add_paragraph()
                        p_def.paragraph_format.line_spacing = 1.3
                        p_def.paragraph_format.space_after = Pt(1)
                        r_dt = p_def.add_run(f"    {d['title']}")
                        set_run_font(r_dt, 15, bold=True)
                        r_dv = p_def.add_run(f"    {d['value']}")
                        set_run_font(r_dv, 15)

                elif itype == "legal_disclaimer":
                    p_leg = doc.add_paragraph()
                    p_leg.paragraph_format.space_before = Pt(4)
                    p_leg.paragraph_format.space_after = Pt(4)
                    p_leg.paragraph_format.line_spacing = 1.25
                    p_leg.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                    r_lg = p_leg.add_run(item["text"])
                    set_run_font(r_lg, 13.5)

            # Bottom Signature block
            p_bsig = doc.add_paragraph()
            p_bsig.paragraph_format.space_before = Pt(14)
            p_bsig.paragraph_format.space_after = Pt(2)
            p_bsig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_bs = p_bsig.add_run("ลงชื่อ........................ พ.อ. ................................................................นายทหารจเร  ผู้ตรวจ")
            set_run_font(r_bs, 15)

            p_bdate = doc.add_paragraph()
            p_bdate.paragraph_format.space_after = Pt(0)
            p_bdate.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r_bd = p_bdate.add_run(f"(........{day}......../........{month}......../........{year_short}........){' '*8}")
            set_run_font(r_bd, 15)

    doc.save(docx_out)
    print(f"Successfully generated DOCX: {docx_out} (18 Pages)")

# -----------------------------------------------------------------------------
# 3. BUILD XLSX MULTI-SHEET WORKBOOK (7 Sheets, A4 Portrait Print-Ready)
# -----------------------------------------------------------------------------
def build_xlsx():
    xlsx_out = "บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.xlsx"
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    font_title = Font(name="TH Sarabun New", size=18, bold=True)
    font_bold = Font(name="TH Sarabun New", size=15, bold=True)
    font_regular = Font(name="TH Sarabun New", size=15, bold=False)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # 1. Sheet: บันทึกข้อความ
    ws_memo = wb.create_sheet(title="บันทึกข้อความ (หน้า 1)")
    ws_memo.page_setup.orientation = ws_memo.ORIENTATION_PORTRAIT
    ws_memo.page_setup.paperSize = ws_memo.PAPERSIZE_A4
    ws_memo.page_setup.fitToPage = True
    ws_memo.page_setup.fitToWidth = 1
    ws_memo.page_setup.fitToHeight = 1

    p1 = DATA["page_1_memo"]
    h = p1["header"]
    sig = p1["signature"]

    ws_memo.column_dimensions['A'].width = 18
    ws_memo.column_dimensions['B'].width = 30
    ws_memo.column_dimensions['C'].width = 15
    ws_memo.column_dimensions['D'].width = 30

    ws_memo.merge_cells("A2:D2")
    ws_memo["A2"] = "บันทึกข้อความ"
    ws_memo["A2"].font = Font(name="TH Sarabun New", size=26, bold=True)
    ws_memo["A2"].alignment = align_center

    ws_memo["A4"] = "ส่วนราชการ:"
    ws_memo["A4"].font = font_bold
    ws_memo.merge_cells("B4:D4")
    ws_memo["B4"] = h["dept"]
    ws_memo["B4"].font = font_regular

    ws_memo["A5"] = "ที่:"
    ws_memo["A5"].font = font_bold
    ws_memo["B5"] = h["doc_no"]
    ws_memo["B5"].font = font_regular
    ws_memo["C5"] = "วันที่:"
    ws_memo["C5"].font = font_bold
    ws_memo["D5"] = h["date"]
    ws_memo["D5"].font = font_regular

    ws_memo["A6"] = "เรื่อง:"
    ws_memo["A6"].font = font_bold
    ws_memo.merge_cells("B6:D6")
    ws_memo["B6"] = h["subject"]
    ws_memo["B6"].font = font_regular

    ws_memo["A7"] = "เรียน:"
    ws_memo["A7"].font = font_bold
    ws_memo.merge_cells("B7:D7")
    ws_memo["B7"] = h["to"]
    ws_memo["B7"].font = font_regular

    ws_memo["A8"] = "อ้างถึง:"
    ws_memo["A8"].font = font_bold
    ws_memo.merge_cells("B8:D8")
    ws_memo["B8"] = h["references"][0] + "\n" + h["references"][1]
    ws_memo["B8"].font = font_regular
    ws_memo["B8"].alignment = align_left

    ws_memo["A9"] = "สิ่งที่ส่งมาด้วย:"
    ws_memo["A9"].font = font_bold
    ws_memo.merge_cells("B9:D9")
    ws_memo["B9"] = h["attachments"]
    ws_memo["B9"].font = font_regular

    ws_memo.merge_cells("A11:D11")
    ws_memo["A11"] = "    " + p1["body_paragraphs"][0]
    ws_memo["A11"].font = font_regular
    ws_memo["A11"].alignment = align_left
    ws_memo.row_dimensions[11].height = 45

    ws_memo.merge_cells("A13:D13")
    ws_memo["A13"] = "    " + p1["body_paragraphs"][1]
    ws_memo["A13"].font = font_regular
    ws_memo["A13"].alignment = align_left

    ws_memo["C17"] = sig["rank"]
    ws_memo["C17"].font = font_regular
    ws_memo["C17"].alignment = align_right

    ws_memo["D17"] = f"({sig['name']})"
    ws_memo["D17"].font = font_regular
    ws_memo["D17"].alignment = align_center

    ws_memo["D18"] = sig["position"]
    ws_memo["D18"].font = font_regular
    ws_memo["D18"].alignment = align_center

    # 2. Sheets: Each Inspection Set
    for s in DATA["inspection_sets"]:
        set_no = s["set_no"]
        day = to_thai(s["date"])
        month = s["month"]
        year_short = to_thai(s["year_short"])
        title_short = f"ชุดที่ {set_no} ({s['title'][:10]}...)"
        ws = wb.create_sheet(title=title_short)
        ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToPage = True
        ws.page_setup.fitToWidth = 1

        ws.column_dimensions['A'].width = 14
        ws.column_dimensions['B'].width = 35
        ws.column_dimensions['C'].width = 18
        ws.column_dimensions['D'].width = 35

        r_curr = 2
        ws.merge_cells(f"C{r_curr}:D{r_curr}")
        ws[f"C{r_curr}"] = "ทบ. ๑๐๕ - ๐๐๙"
        ws[f"C{r_curr}"].font = font_bold
        ws[f"C{r_curr}"].alignment = align_right
        r_curr += 1

        ws.merge_cells(f"A{r_curr}:D{r_curr}")
        ws[f"A{r_curr}"] = "บันทึกผลการตรวจของนายทหารจเร"
        ws[f"A{r_curr}"].font = font_title
        ws[f"A{r_curr}"].alignment = align_center
        r_curr += 1

        ws.merge_cells(f"A{r_curr}:D{r_curr}")
        ws[f"A{r_curr}"] = f"เรื่อง {s['title']}"
        ws[f"A{r_curr}"].font = font_bold
        ws[f"A{r_curr}"].alignment = align_center
        r_curr += 2

        ws[f"A{r_curr}"] = "หน่วย:"
        ws[f"A{r_curr}"].font = font_bold
        ws[f"B{r_curr}"] = "ป.๔ พัน.๔"
        ws[f"B{r_curr}"].font = font_regular
        ws[f"C{r_curr}"] = "ชื่อ ผบ.หน่วย:"
        ws[f"C{r_curr}"].font = font_bold
        ws[f"D{r_curr}"] = "พ.ท. พรชัย  มากเทพพงษ์"
        ws[f"D{r_curr}"].font = font_regular
        r_curr += 1

        ws[f"A{r_curr}"] = "ตรวจเมื่อวันที่:"
        ws[f"A{r_curr}"].font = font_bold
        ws[f"B{r_curr}"] = f"{to_thai(s['date'])} {s['month']} {to_thai(s['year'])}"
        ws[f"B{r_curr}"].font = font_regular
        r_curr += 1

        ws[f"A{r_curr}"] = "ผู้รับตรวจ:"
        ws[f"A{r_curr}"].font = font_bold
        ws[f"B{r_curr}"] = s["inspectee"]
        ws[f"B{r_curr}"].font = font_regular
        ws[f"C{r_curr}"] = "ตำแหน่ง:"
        ws[f"C{r_curr}"].font = font_bold
        ws[f"D{r_curr}"] = s["inspectee_position"]
        ws[f"D{r_curr}"].font = font_regular
        r_curr += 1

        ws[f"A{r_curr}"] = "ผู้ตรวจ:"
        ws[f"A{r_curr}"].font = font_bold
        ws[f"B{r_curr}"] = s["inspector"]
        ws[f"B{r_curr}"].font = font_regular
        ws[f"C{r_curr}"] = "จำนวนแผ่น:"
        ws[f"C{r_curr}"].font = font_bold
        ws[f"D{r_curr}"] = f"{to_thai(s['total_sheets'])} แผ่น"
        ws[f"D{r_curr}"].font = font_regular
        r_curr += 2

        ws.merge_cells(f"A{r_curr}:D{r_curr}")
        ws[f"A{r_curr}"] = "๑. หน่วยรับตรวจและชื่อ ผบ.หน่วยรับตรวจ"
        ws[f"A{r_curr}"].font = font_bold
        r_curr += 1

        for cmd in s["commanders"]:
            ws.merge_cells(f"A{r_curr}:B{r_curr}")
            ws[f"A{r_curr}"] = cmd["unit"]
            ws[f"A{r_curr}"].font = font_regular
            ws.merge_cells(f"C{r_curr}:D{r_curr}")
            ws[f"C{r_curr}"] = cmd["commander"]
            ws[f"C{r_curr}"].font = font_regular
            r_curr += 1
        r_curr += 1

        ws.merge_cells(f"A{r_curr}:D{r_curr}")
        ws[f"A{r_curr}"] = "๒. สิ่งที่ตรวจพบ ข้อเสนอแนะให้แก้ไขและหลักฐานอ้างอิง"
        ws[f"A{r_curr}"].font = font_bold
        r_curr += 1

        for page in s["pages"]:
            for item in page["content"]:
                itype = item.get("type", "")
                if itype == "findings":
                    for f in item["items"]:
                        ws.merge_cells(f"A{r_curr}:D{r_curr}")
                        ws[f"A{r_curr}"] = f"{f['finding_code']} {f['topic']}: {f['finding_text']}"
                        ws[f"A{r_curr}"].font = font_regular
                        ws[f"A{r_curr}"].alignment = align_left
                        ws.row_dimensions[r_curr].height = 40
                        r_curr += 1

                        if f.get("recommendations"):
                            for rec in f["recommendations"]:
                                ws.merge_cells(f"A{r_curr}:D{r_curr}")
                                ws[f"A{r_curr}"] = "  ข้อเสนอแนะ: " + rec
                                ws[f"A{r_curr}"].font = font_regular
                                ws[f"A{r_curr}"].alignment = align_left
                                ws.row_dimensions[r_curr].height = 40
                                r_curr += 1
                elif itype == "deficiencies_summary":
                    for d in item["items"]:
                        ws[f"A{r_curr}"] = d["title"]
                        ws[f"A{r_curr}"].font = font_bold
                        ws[f"B{r_curr}"] = d["value"]
                        ws[f"B{r_curr}"].font = font_regular
                        r_curr += 1

        r_curr += 2
        ws.merge_cells(f"B{r_curr}:D{r_curr}")
        ws[f"B{r_curr}"] = "ลงชื่อ........................ พ.อ. ................................................................นายทหารจเร  ผู้ตรวจ"
        ws[f"B{r_curr}"].font = font_regular
        ws[f"B{r_curr}"].alignment = align_right
        r_curr += 1

        ws.merge_cells(f"B{r_curr}:D{r_curr}")
        ws[f"B{r_curr}"] = f"(........{day}......../........{month}......../........{year_short}........)"
        ws[f"B{r_curr}"].font = font_regular
        ws[f"B{r_curr}"].alignment = align_right

    wb.save(xlsx_out)
    print(f"Successfully generated XLSX: {xlsx_out} (7 Sheets)")

if __name__ == "__main__":
    print("Executing SUPERCLONE Production Engine for General Inspection 2...")
    build_html()
    build_docx()
    build_xlsx()
    print("ALL BUILD ARTIFACTS SUCCESSFULLY PRODUCED!")
