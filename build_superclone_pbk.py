# -*- coding: utf-8 -*-
"""
SUPERCLONE Production-Grade Engine
Target: บัญชีรายละเอียดหมายเลข ปบค.95 ขนาด 105 มม. เอ็ม 101 เอ 1 ปรับปรุง (ป.4 พัน.4 ร้อย.2)
Integrated with SIGNATURE BLOCK ENGINE v1.0 (True Red Line Standard):
  - verification_text: ตรวจถูกต้อง (ด้านบนซ้ายของบล็อก)
  - rank: จ.ส.อ. -> ท้ายจุด . ชนแนวเส้นดิ่งเดียวกับวงเล็บเปิด ( ของชื่อ พอดีเป๊ะ 100% (Red Line Axis)
  - full_name: (ณัฐชัย   รักษาวงษ์) (เคาะ 3 เคาะระหว่างชื่อ-นามสกุล)
  - position: ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒ (Space After 0 pt ชิดกัน 1 enter จัดกึ่งกลางร่วมกับชื่อ)
"""

import os
import sys
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

WORKDIR = r"d:\Project\WEPAPP"

# Thai Numeral Converter
THAI_DIGITS = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
def to_th(val):
    if val is None:
        return ""
    return str(val).translate(THAI_DIGITS)

# -------------------------------------------------------------
# 1. Blueprint Specification (table_layout.json)
# -------------------------------------------------------------
blueprint = {
    "document_metadata": {
        "id": "PBK-95-105MM",
        "title_th": "บัญชีรายละเอียดหมายเลข ปบค.๙๕ ขนาด ๑๐๕ มม. เอ็ม ๑๐๑ เอ ๑ ปรับปรุง",
        "unit_th": "ป.๔ พัน.๔ ร้อย.๒",
        "paper_size": "A4",
        "orientation": "landscape",
        "page_dimensions_pt": {"width": 842.04, "height": 595.32},
        "margins_pt": {"top": 35.0, "bottom": 35.0, "left": 25.0, "right": 25.0},
        "default_font": "TH Sarabun PSK",
        "primary_font_size_pt": 15
    },
    "signature_block": {
        "verification_text": "ตรวจถูกต้อง",
        "rank": "จ.ส.อ.",
        "full_name": "(ณัฐชัย   รักษาวงษ์)",
        "position": "ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒",
        "alignment_standard": "rank_endpoint_to_open_parenthesis",
        "description": "ท้ายยศชนวงเล็บเปิด: จุด . สุดท้ายของ จ.ส.อ. แตะแนวเส้นดิ่งเดียวกับ ( ของชื่อ",
        "name_position_shared_center": True,
        "name_position_spacing_pt": 0
    },
    "columns": [
        {"id": "col_seq", "header_th": "ลำดับ", "width_pt": 38, "width_percent": 4.74, "align": "center", "data_type": "integer"},
        {"id": "col_gun_no", "header_th": "หมายเลข\nปบค.๙๕", "width_pt": 57, "width_percent": 7.12, "align": "center", "data_type": "code_string"},
        {"id": "col_barrel", "header_th": "ลำกล้อง\nปืน", "width_pt": 47, "width_percent": 5.87, "align": "center", "data_type": "code_string"},
        {"id": "col_carriage", "header_th": "รถรองปืน\n(เปลปืน)", "width_pt": 56, "width_percent": 6.99, "align": "center", "data_type": "code_string"},
        {"id": "col_recoil", "header_th": "เครื่องรับ\nแรงถอย", "width_pt": 57, "width_percent": 7.12, "align": "center", "data_type": "code_string"},
        {"id": "col_tire_left", "header_th": "ยางซ้าย", "width_pt": 142, "width_percent": 17.73, "align": "center", "data_type": "text"},
        {"id": "col_tire_right", "header_th": "ยางขวา", "width_pt": 135, "width_percent": 16.85, "align": "center", "data_type": "text"},
        {"id": "col_mount_m21", "header_th": "ฐานกล้อง\nเล็ง\nM.๒๑ A.๑", "width_pt": 57, "width_percent": 7.12, "align": "center", "data_type": "code_string"},
        {"id": "col_device_m4", "header_th": "เครื่องให้\nระยิง\nM.๔ A.๑", "width_pt": 49, "width_percent": 6.12, "align": "center", "data_type": "code_string"},
        {"id": "col_mount_m23", "header_th": "ฐานกล้อง\nข้อศอก M.๒๓", "width_pt": 64, "width_percent": 7.99, "align": "center", "data_type": "code_string"},
        {"id": "col_drift", "header_th": "ค่า ตร.", "width_pt": 43, "width_percent": 5.37, "align": "center", "data_type": "decimal"},
        {"id": "col_remark", "header_th": "หมายเหตุ", "width_pt": 56, "width_percent": 6.99, "align": "center", "data_type": "text"}
    ],
    "rows": [
        {
            "seq": 1,
            "gun_no": "24080",
            "barrel": "",
            "carriage": "",
            "recoil": "",
            "tire_left": "",
            "tire_right": "",
            "mount_m21": "",
            "device_m4": "",
            "mount_m23": "",
            "drift": "",
            "remark": "ส่งซ่อม"
        },
        {
            "seq": 2,
            "gun_no": "19609",
            "barrel": "14041",
            "carriage": "3166",
            "recoil": "13740",
            "tire_left": "Superstone  LA070706\n(28  19)",
            "tire_right": "SuperstoneLA070147\n(29  19)",
            "mount_m21": "0283",
            "device_m4": "1932",
            "mount_m23": "9282",
            "drift": "-7.90",
            "remark": ""
        },
        {
            "seq": 3,
            "gun_no": "20670",
            "barrel": "14139",
            "carriage": "12405",
            "recoil": "839",
            "tire_left": "Superstone NP090297\n(38  23)",
            "tire_right": "Superstone NP090049\n(36  23)",
            "mount_m21": "0290",
            "device_m4": "21510",
            "mount_m23": "1122",
            "drift": "-8.21",
            "remark": ""
        },
        {
            "seq": 4,
            "gun_no": "23554",
            "barrel": "14180",
            "carriage": "10780",
            "recoil": "1231",
            "tire_left": "Superstone HC090119\n(38  21)",
            "tire_right": "Superstone HC070147\n(38  21)",
            "mount_m21": "0424",
            "device_m4": "24099",
            "mount_m23": "20925",
            "drift": "-8.41",
            "remark": ""
        },
        {
            "seq": 5,
            "gun_no": "24280",
            "barrel": "15325",
            "carriage": "12595",
            "recoil": "3456",
            "tire_left": "Superstone AA020358\n(09  14)",
            "tire_right": "Superstone AA030298\n(10  14)",
            "mount_m21": "0435",
            "device_m4": "23173",
            "mount_m23": "8312",
            "drift": "-9.06",
            "remark": ""
        },
        {
            "seq": 6,
            "gun_no": "8516",
            "barrel": "14036",
            "carriage": "6955",
            "recoil": "1209",
            "tire_left": "Superstone AA030290\n(11  14)",
            "tire_right": "Superstone AA030345\n(11  14)",
            "mount_m21": "0431",
            "device_m4": "24961",
            "mount_m23": "21967",
            "drift": "-9.12",
            "remark": ""
        }
    ]
}

# Write table_layout.json
json_path = os.path.join(WORKDIR, "table_layout.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)
print("Saved:", json_path)


# -------------------------------------------------------------
# 2. Template HTML & Page Template HTML
# -------------------------------------------------------------
tpl_html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4 landscape;
            margin: 8mm 10mm;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        body {
            font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', 'Angsana New', sans-serif;
            font-size: 16pt;
            line-height: 1.25;
            color: #000;
            background-color: #f5f5f7;
            margin: 0;
            padding: 20px;
            font-feature-settings: "locl" 1, "numr" 1;
            -webkit-font-smoothing: antialiased;
        }
        .page-landscape {
            width: 297mm;
            min-height: 210mm;
            margin: 0 auto;
            padding: 12mm 14mm 10mm 14mm;
            background: white;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            position: relative;
        }
        .doc-header {
            text-align: center;
            margin-bottom: 0;
        }
        .doc-title {
            font-size: 18pt;
            font-weight: bold;
            margin: 0 0 2px 0;
            letter-spacing: 0.3px;
        }
        .doc-unit {
            font-size: 16pt;
            font-weight: bold;
            margin: 0 0 18px 0; /* ห่าง 1 เคาะ (1 บรรทัด) กับหัวตาราง */
            line-height: 1.3;
        }
        table.military-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-bottom: 20px;
            border: 1px solid #000;
        }
        table.military-table th,
        table.military-table td {
            border: 1px solid #000;
            padding: 4px 2px;
            vertical-align: middle;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        table.military-table th {
            text-align: center;
            font-weight: bold;
            font-size: 14pt;
            background-color: #fff;
            line-height: 1.2;
            height: 64px;
        }
        table.military-table td {
            font-size: 14pt;
            height: 46px;
            text-align: center;
            line-height: 1.25;
        }
        .tire-cell {
            padding: 2px 2px !important;
        }
        .tire-text {
            font-size: 12.5pt;
            line-height: 1.18;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: clip;
        }

        /* ========================================================= */
        /* SIGNATURE BLOCK ENGINE v1.0 — TRUE RED LINE ALIGNMENT     */
        /* ท้ายยศชนวงเล็บเปิด: จุด . ของ จ.ส.อ. ชนเส้นแนวดิ่งเดียวกับ ( ของชื่อ */
        /* ========================================================= */
        .doc-footer-grid {
            display: flex;
            justify-content: flex-end;
            margin-top: 25px;
            padding: 0 45px 0 0;
        }
        .sig-block {
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 16pt;
            line-height: 1.0;
        }
        .sig-verify {
            margin-bottom: 8px;
            font-size: 16pt;
            line-height: 1.0;
        }
        
        /* กล่องชื่อและตำแหน่ง */
        .sig-name-pos-group {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            margin-left: 95px;
        }

        /* กรอบชื่อ: ตัวยึดแนววงเล็บเปิด ( */
        .sig-name-wrapper {
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 30px; /* พื้นที่สำหรับลงลายมือชื่อจริง */
        }

        /* บรรทัดยศ: จุด . ท้ายยศ ชนขอบซ้ายของกรอบชื่อ ซึ่งคือ ( พอดีเป๊ะ 100% */
        .sig-rank-anchor {
            position: absolute;
            right: 100%; /* ชนแนวเส้นดิ่งเดียวกับ ( พอดีเป๊ะ */
            bottom: calc(100% + 20px);
            white-space: nowrap;
            font-size: 16pt;
            line-height: 1.0;
        }

        /* ชื่อและตำแหน่ง: จัดกึ่งกลางร่วมกัน 1 enter ไม่มีระยะย่อหน้า */
        .sig-name {
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 16pt;
            display: block;
        }
        .sig-pos {
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 16pt;
            display: block;
        }

        @media print {
            body { background: transparent; padding: 0; }
            .page-landscape { padding: 0; width: 100%; box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="page-landscape">
        {{content}}
    </div>
</body>
</html>
"""

with open(os.path.join(WORKDIR, "template.html"), "w", encoding="utf-8") as f:
    f.write(tpl_html)
with open(os.path.join(WORKDIR, "page_template.html"), "w", encoding="utf-8") as f:
    f.write(tpl_html)
print("Saved template.html and page_template.html")


# -------------------------------------------------------------
# 3. Complete Standalone HTML (บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html)
# -------------------------------------------------------------
table_header_html = "<tr>\n"
for c in blueprint["columns"]:
    th_label = to_th(c["header_th"]).replace("\n", "<br>")
    table_header_html += f'    <th style="width: {c["width_percent"]}%;">{th_label}</th>\n'
table_header_html += "</tr>"

table_rows_html = ""
for r in blueprint["rows"]:
    table_rows_html += "<tr>\n"
    table_rows_html += f'    <td>{to_th(r["seq"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["gun_no"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["barrel"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["carriage"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["recoil"])}</td>\n'
    tire_l = to_th(r["tire_left"]).replace("\n", "<br>")
    table_rows_html += f'    <td class="tire-cell"><span class="tire-text">{tire_l}</span></td>\n'
    tire_r = to_th(r["tire_right"]).replace("\n", "<br>")
    table_rows_html += f'    <td class="tire-cell"><span class="tire-text">{tire_r}</span></td>\n'
    table_rows_html += f'    <td>{to_th(r["mount_m21"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["device_m4"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["mount_m23"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["drift"])}</td>\n'
    table_rows_html += f'    <td>{to_th(r["remark"])}</td>\n'
    table_rows_html += "</tr>\n"

sig = blueprint["signature_block"]
sig_verify_html = f'<div class="sig-verify">{sig["verification_text"]}</div>' if sig.get("verification_text") else ''
sig_rank_html = f'<span class="sig-rank-anchor">{sig["rank"]}</span>' if sig.get("rank") else ''

body_content = f"""
        <div class="doc-header">
            <div class="doc-title">{blueprint["document_metadata"]["title_th"]}</div>
            <div class="doc-unit">{blueprint["document_metadata"]["unit_th"]}</div>
        </div>

        <table class="military-table">
            <thead>
{table_header_html}
            </thead>
            <tbody>
{table_rows_html}
            </tbody>
        </table>

        <div class="doc-footer-grid">
            <div class="sig-block">
                {sig_verify_html}
                <div class="sig-name-pos-group">
                    <div class="sig-name-wrapper">
                        {sig_rank_html}
                        <div class="sig-name">{sig["full_name"]}</div>
                    </div>
                    <div class="sig-pos">{sig["position"]}</div>
                </div>
            </div>
        </div>
"""

full_html = tpl_html.replace("{{title}}", blueprint["document_metadata"]["title_th"]).replace("{{content}}", body_content)
html_file_path = os.path.join(WORKDIR, "บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print("Saved HTML:", html_file_path)


# -------------------------------------------------------------
# 4. Excel Production-Grade Generation (.xlsx)
# -------------------------------------------------------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "รายละเอียด ปบค.95"

ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.fitToPage = True
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True

ws.page_margins.left = 0.35
ws.page_margins.right = 0.35
ws.page_margins.top = 0.4
ws.page_margins.bottom = 0.4

font_title = Font(name="TH Sarabun PSK", size=18, bold=True)
font_unit = Font(name="TH Sarabun PSK", size=16, bold=True)
font_th = Font(name="TH Sarabun PSK", size=14, bold=True)
font_td = Font(name="TH Sarabun PSK", size=13)
font_footer = Font(name="TH Sarabun PSK", size=16)

thin_border = Border(
    left=Side(style='thin', color='000000'),
    right=Side(style='thin', color='000000'),
    top=Side(style='thin', color='000000'),
    bottom=Side(style='thin', color='000000')
)

# Row 1: Title
ws.merge_cells("A1:L1")
ws["A1"] = blueprint["document_metadata"]["title_th"]
ws["A1"].font = font_title
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 28

# Row 2: Unit
ws.merge_cells("A2:L2")
ws["A2"] = blueprint["document_metadata"]["unit_th"]
ws["A2"].font = font_unit
ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[2].height = 24

# Row 3: Blank spacing (ห่าง 1 เคาะ)
ws.row_dimensions[3].height = 18

# Row 4: Header
ws.row_dimensions[4].height = 46
headers = [
    "ลำดับ",
    "หมายเลข\nปบค.๙๕",
    "ลำกล้อง\nปืน",
    "รถรองปืน\n(เปลปืน)",
    "เครื่องรับ\nแรงถอย",
    "ยางซ้าย",
    "ยางขวา",
    "ฐานกล้องเล็ง\nM.๒๑ A.๑",
    "เครื่องให้ระยิง\nM.๔ A.๑",
    "ฐานกล้อง\nข้อศอก M.๒๓",
    "ค่า ตร.",
    "หมายเหตุ"
]

for col_idx, h_text in enumerate(headers, start=1):
    c = ws.cell(row=4, column=col_idx)
    c.value = h_text
    c.font = font_th
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border

col_widths_xl = [6.5, 12, 10, 11, 11, 26, 26, 12, 12, 14, 9, 11]
for i, w in enumerate(col_widths_xl, start=1):
    col_letter = get_column_letter(i)
    ws.column_dimensions[col_letter].width = w

# Data rows (Row 5 - 10)
excel_row = 5
for r_data in blueprint["rows"]:
    ws.row_dimensions[excel_row].height = 36
    
    ws.cell(row=excel_row, column=1, value=to_th(r_data["seq"]))
    ws.cell(row=excel_row, column=2, value=to_th(r_data["gun_no"]))
    ws.cell(row=excel_row, column=3, value=to_th(r_data["barrel"]))
    ws.cell(row=excel_row, column=4, value=to_th(r_data["carriage"]))
    ws.cell(row=excel_row, column=5, value=to_th(r_data["recoil"]))
    ws.cell(row=excel_row, column=6, value=to_th(r_data["tire_left"]))
    ws.cell(row=excel_row, column=7, value=to_th(r_data["tire_right"]))
    ws.cell(row=excel_row, column=8, value=to_th(r_data["mount_m21"]))
    ws.cell(row=excel_row, column=9, value=to_th(r_data["device_m4"]))
    ws.cell(row=excel_row, column=10, value=to_th(r_data["mount_m23"]))
    ws.cell(row=excel_row, column=11, value=to_th(r_data["drift"]))
    ws.cell(row=excel_row, column=12, value=to_th(r_data["remark"]))

    for ci in range(1, 13):
        cell_item = ws.cell(row=excel_row, column=ci)
        cell_item.font = font_td
        cell_item.border = thin_border
        cell_item.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    excel_row += 1

# Footer Section
ws.row_dimensions[excel_row].height = 20
excel_row += 1

# ตรวจถูกต้อง
if sig.get("verification_text"):
    ws.row_dimensions[excel_row].height = 22
    ws.cell(row=excel_row, column=8, value=sig["verification_text"]).font = font_footer
    ws.cell(row=excel_row, column=8).alignment = Alignment(horizontal="left", vertical="center")
    excel_row += 1

# ยศ จ.ส.อ. -> จุด . ชนแนวซ้าย Col I
if sig.get("rank"):
    ws.row_dimensions[excel_row].height = 22
    ws.cell(row=excel_row, column=8, value=sig["rank"]).font = font_footer
    ws.cell(row=excel_row, column=8).alignment = Alignment(horizontal="right", vertical="center")

# Space for signature
excel_row += 1
ws.row_dimensions[excel_row].height = 26

# ชื่อ & ตำแหน่ง จัดกึ่งกลางร่วมกัน (Cols I-K)
ws.row_dimensions[excel_row].height = 22
ws.merge_cells(f"I{excel_row}:K{excel_row}")
cell_sig_name = ws.cell(row=excel_row, column=9, value=sig["full_name"])
cell_sig_name.font = font_footer
cell_sig_name.alignment = Alignment(horizontal="center", vertical="center")

excel_row += 1
ws.row_dimensions[excel_row].height = 22
ws.merge_cells(f"I{excel_row}:K{excel_row}")
cell_sig_pos = ws.cell(row=excel_row, column=9, value=sig["position"])
cell_sig_pos.font = font_footer
cell_sig_pos.alignment = Alignment(horizontal="center", vertical="center")

xlsx_file_path = os.path.join(WORKDIR, "บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.xlsx")
wb.save(xlsx_file_path)
print("Saved XLSX:", xlsx_file_path)


# -------------------------------------------------------------
# 5. Word Document Generation (.docx)
# -------------------------------------------------------------
doc = docx.Document()

section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(11.69)
section.page_height = Inches(8.27)
section.left_margin = Inches(0.4)
section.right_margin = Inches(0.4)
section.top_margin = Inches(0.45)
section.bottom_margin = Inches(0.45)

def format_run(run, font_name="TH Sarabun PSK", size_pt=16, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:eastAsia="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)

# Title Paragraph
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(2)
run_title = p_title.add_run(blueprint["document_metadata"]["title_th"])
format_run(run_title, size_pt=18, bold=True)

# Unit Paragraph (Space after = 18 pt = 1 เคาะ)
p_unit = doc.add_paragraph()
p_unit.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_unit.paragraph_format.space_before = Pt(0)
p_unit.paragraph_format.space_after = Pt(18)
run_unit = p_unit.add_run(blueprint["document_metadata"]["unit_th"])
format_run(run_unit, size_pt=16, bold=True)

# Table
table = doc.add_table(rows=1 + len(blueprint["rows"]), cols=12)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

total_table_inches = 10.85
col_widths_inches = [(c["width_percent"] / 100.0) * total_table_inches for c in blueprint["columns"]]

def set_cell_margins_and_border(cell, top=60, bottom=60, left=40, right=40):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)
    
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)

# Header Cells
hdr_cells = table.rows[0].cells
for idx, col_def in enumerate(blueprint["columns"]):
    cell = hdr_cells[idx]
    cell.width = Inches(col_widths_inches[idx])
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_margins_and_border(cell, top=70, bottom=70)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    
    lines = to_th(col_def["header_th"]).split("\n")
    for l_idx, line in enumerate(lines):
        if l_idx > 0:
            p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
        r = p.add_run(line)
        format_run(r, size_pt=14, bold=True)

# Data Cells
for row_idx, r_data in enumerate(blueprint["rows"], start=1):
    row_cells = table.rows[row_idx].cells
    row_values = [
        to_th(r_data["seq"]),
        to_th(r_data["gun_no"]),
        to_th(r_data["barrel"]),
        to_th(r_data["carriage"]),
        to_th(r_data["recoil"]),
        to_th(r_data["tire_left"]),
        to_th(r_data["tire_right"]),
        to_th(r_data["mount_m21"]),
        to_th(r_data["device_m4"]),
        to_th(r_data["mount_m23"]),
        to_th(r_data["drift"]),
        to_th(r_data["remark"])
    ]
    for col_idx, val in enumerate(row_values):
        cell = row_cells[col_idx]
        cell.width = Inches(col_widths_inches[col_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins_and_border(cell, top=65, bottom=65)
        
        lines = val.split("\n")
        for l_idx, line in enumerate(lines):
            if l_idx == 0:
                p = cell.paragraphs[0]
            else:
                p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(line)
            sz = 12.5 if col_idx in (5, 6) else 13.5
            format_run(r, size_pt=sz, bold=False)

# Footer Paragraphs
p_foot = doc.add_paragraph()
p_foot.paragraph_format.space_before = Pt(16)
p_foot.paragraph_format.space_after = Pt(0)

# Right-aligned signature table
foot_table = doc.add_table(rows=1, cols=2)
foot_table.alignment = WD_TABLE_ALIGNMENT.CENTER
foot_table.autofit = False

cell_f_left = foot_table.rows[0].cells[0]
cell_f_left.width = Inches(6.0)
p_l = cell_f_left.paragraphs[0]
p_l.paragraph_format.space_before = Pt(0)
p_l.paragraph_format.space_after = Pt(0)

cell_f_right = foot_table.rows[0].cells[1]
cell_f_right.width = Inches(4.8)

# 1. Verification text (ตรวจถูกต้อง)
if sig.get("verification_text"):
    p_v = cell_f_right.paragraphs[0]
    p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_v.paragraph_format.space_before = Pt(0)
    p_v.paragraph_format.space_after = Pt(7.5)
    p_v.paragraph_format.line_spacing = 1.0
    r_v = p_v.add_run(sig["verification_text"])
    format_run(r_v, size_pt=16)

# แกนเส้นสีแดงใน Word DOCX
axis_red_line = Inches(1.40)

# 2. Rank (จ.ส.อ.) -> Right Tab ชนเส้น axis_red_line (จุด . แตะแกน)
if sig.get("rank"):
    p_rk = cell_f_right.add_paragraph()
    p_rk.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_rk.paragraph_format.space_before = Pt(0)
    p_rk.paragraph_format.space_after = Pt(24) # เว้นลงลายมือชื่อ
    p_rk.paragraph_format.line_spacing = 1.0
    p_rk.paragraph_format.tab_stops.add_tab_stop(axis_red_line, WD_TAB_ALIGNMENT.RIGHT)
    r_rk = p_rk.add_run("\t" + sig["rank"])
    format_run(r_rk, size_pt=16)

# 3. Full Name (ณัฐชัย   รักษาวงษ์) -> Left Tab ชนเส้น axis_red_line (วงเล็บเปิด ( แตะแกน)
p_nm = cell_f_right.add_paragraph()
p_nm.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_nm.paragraph_format.space_before = Pt(0)
p_nm.paragraph_format.space_after = Pt(0)
p_nm.paragraph_format.line_spacing = 1.0
p_nm.paragraph_format.tab_stops.add_tab_stop(axis_red_line, WD_TAB_ALIGNMENT.LEFT)
r_nm = p_nm.add_run("\t" + sig["full_name"])
format_run(r_nm, size_pt=16)

# 4. Position (ส.หน.สย. ป.๔ พัน.๔ ร้อย.๒) -> จัดกึ่งกลางร่วมกับชื่อ
p_pos = cell_f_right.add_paragraph()
p_pos.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_pos.paragraph_format.space_before = Pt(0)
p_pos.paragraph_format.space_after = Pt(0)
p_pos.paragraph_format.line_spacing = 1.0
pos_axis = Inches(1.20)
p_pos.paragraph_format.tab_stops.add_tab_stop(pos_axis, WD_TAB_ALIGNMENT.LEFT)
r_pos = p_pos.add_run("\t" + sig["position"])
format_run(r_pos, size_pt=16)

docx_file_path = os.path.join(WORKDIR, "บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.docx")
doc.save(docx_file_path)
print("Saved DOCX:", docx_file_path)

print("\n--- ALL SUPERCLONE ARTIFACTS RE-GENERATED SUCCESSFULLY ---")
