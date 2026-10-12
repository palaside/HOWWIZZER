import os
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# Load Blueprint
blueprint_path = r"d:\Project\WEPAPP\table_layout_400_005.json"
with open(blueprint_path, "r", encoding="utf-8") as f:
    bp = json.load(f)

# Load Trans Map
with open(r"d:\Project\WEPAPP\extracted_transactions_by_page.json", "r", encoding="utf-8") as f:
    trans_map = json.load(f)

# Transactions mapping for cards
# Card 1: P1
# Card 2: P3
# Card 3: P5
# Card 4: P6 & P15
# Card 5: P18
# Card 6: P20
# Card 7: P22
# Card 8: P24
# Card 9: P25
# Card 10: P26
# Card 11: P30
# Card 12: P32
# Card 13: P34

card_trans = {
    1: [
        {"date": "29 ก.ค. 07", "doc": "ใบเบิกที่ 15 / 07\nลง 29 ก.ค. 07\nทะเบียนหน่วยจ่าย\nที่ 63 / 07\nลง 29 ก.ค. 07", "req": "2", "recv": "2", "ret": "-", "bal": "2", "sig": "จ.ส.อ."},
        {"date": "14 ธ.ค. 32", "doc": "ใบเบิกที่ 35 / 32\nลง 14 ธ.ค. 32\nทะเบียนหน่วยจ่าย\nที่ 113 / 32\nลง 14 ธ.ค. 32", "req": "2", "recv": "2", "ret": "-", "bal": "4", "sig": "จ.ส.อ."}
    ],
    2: [
        {"date": "3 พ.ย. 04", "doc": "ใบเบิกที่ 7 / 08\nลง 3 พ.ย. 04\nทะเบียนหน่วยจ่าย\nที่ 54 / 04\nลง 1 ส.ค. 04", "req": "1", "recv": "1", "ret": "-", "bal": "1", "sig": "จ.ส.อ."}
    ],
    3: [
        {"date": "29 เม.ย. 16", "doc": "ใบเบิกที่ 4 / 06\nลง 29 เม.ย. 06\nทะเบียนหน่วยจ่าย\nที่ 55 / 06\nลง 29 เม.ย. 06", "req": "1", "recv": "1", "ret": "-", "bal": "1", "sig": "จ.ส.อ."},
        {"date": "4 เม.ย. 28", "doc": "ใบเบิกที่ 4 / 28\nลง 4 เม.ย. 28\nทะเบียนหน่วยจ่าย\nที่ 28 / 28\nลง 4 เม.ย. 28", "req": "2", "recv": "2", "ret": "-", "bal": "3", "sig": "จ.ส.อ."}
    ],
    4: [
        {"date": "25 ส.ค. 04", "doc": "ใบเบิกที่ 168 / 04\nลง 25 ส.ค. 04\nทะเบียนหน่วยจ่าย\nที่ 75 / 04\nลง 25 ส.ค. 04", "req": "2", "recv": "2", "ret": "-", "bal": "2", "sig": "จ.ส.อ."},
        {"date": "16 มี.ค. 07", "doc": "ใบเบิกที่ 14 / 07\nลง 16 มี.ค. 07\nทะเบียนหน่วยจ่าย\nที่ 48 / 07\nลง 16 มี.ค. 07", "req": "2", "recv": "2", "ret": "-", "bal": "4", "sig": "จ.ส.อ."}
    ]
}

# ==========================================
# 1. GENERATE HTML (Pixel-Perfect A5 Portrait)
# ==========================================
html_out_path = r"d:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html"

def render_front_card(c, card_idx):
    transactions = card_trans.get(c['item_no'], [])
    
    # Table rows (12 rows for standard ledger)
    t_rows_html = ""
    for r_i in range(12):
        if r_i < len(transactions):
            tx = transactions[r_i]
            doc_lines = "<br>".join(tx['doc'].split("\n"))
            t_rows_html += f"""
            <tr class="tx-row">
                <td class="tx-date thai-numeral">{tx['date']}</td>
                <td class="tx-doc">{doc_lines}</td>
                <td class="tx-qty thai-numeral">{tx['req']}</td>
                <td class="tx-qty thai-numeral">{tx['recv']}</td>
                <td class="tx-qty thai-numeral">{tx['ret']}</td>
                <td class="tx-qty thai-numeral">{tx['bal']}</td>
                <td class="tx-sig">{tx['sig']}</td>
            </tr>
            """
        else:
            t_rows_html += """
            <tr class="tx-row empty-row">
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
            </tr>
            """

    html = f"""
    <!-- CARD {c['item_no']}: {c['item_name']} (FRONT) -->
    <div class="a5-sheet" id="card-{c['item_no']}-front">
        <div class="card-header-row">
            <span class="form-code thai-numeral">ทบ.๔๐๐ – ๐๐๕</span>
        </div>
        <div class="card-title">บัญชีสิ่งอุปกรณ์ของหน่วย</div>
        
        <div class="unit-info-block">
            <div class="unit-name-line">นามหน่วย <span>{bp['unit_info']['unit_name']}</span></div>
            <div class="unit-detail-line">
                <span>ที่ตั้ง</span> <span>{bp['unit_info']['station']}</span>
                <span style="margin-left: 15px;">อัตรายุทโธปกรณ์ที่</span> <span>{bp['unit_info']['toe']}</span>
            </div>
        </div>

        <table class="ledger-table">
            <thead>
                <tr>
                    <th rowspan="2" style="width: 17%;">ว.ด.ป.</th>
                    <th rowspan="2" style="width: 33%;">หลักฐาน</th>
                    <th colspan="4" style="width: 35%;">จำนวน</th>
                    <th rowspan="2" style="width: 15%;">ลงนาม</th>
                </tr>
                <tr>
                    <th style="width: 9%;">ขอ<br>เบิก</th>
                    <th style="width: 9%;">ได้รับ</th>
                    <th style="width: 8%;">ส่งคืน</th>
                    <th style="width: 9%;">คงมี</th>
                </tr>
            </thead>
            <tbody>
                {t_rows_html}
            </tbody>
        </table>

        <!-- FOOTER SPEC GRID -->
        <table class="footer-spec-table">
            <tr>
                <td style="width: 40%;" colspan="2">
                    <span class="f-lbl">สายงานที่ควบคุม</span><br>
                    <span class="f-val">{c['service']}</span>
                </td>
                <td style="width: 30%;">
                    <span class="f-lbl">จำนวนตามอัตราเต็ม</span><br>
                    <span class="f-val thai-numeral">{c['rate_full']}</span>
                </td>
                <td style="width: 30%;">
                    <span class="f-lbl">จำนวนตามอัตราลด</span><br>
                    <span class="f-val thai-numeral">{c['rate_reduced']}</span>
                </td>
            </tr>
            <tr>
                <td style="width: 25%;">
                    <span class="f-lbl">ประเภท</span><br>
                    <span class="f-val">{c['category']}</span>
                </td>
                <td style="width: 25%;">
                    <span class="f-lbl">หน่วยนับ</span><br>
                    <span class="f-val">{c['unit']}</span>
                </td>
                <td style="width: 25%;">
                    <span class="f-lbl">น้ำหนัก</span><br>
                    <span class="f-val thai-numeral">{c['weight']}</span>
                </td>
                <td style="width: 25%;">
                    <span class="f-lbl">ปริมาตร</span><br>
                    <span class="f-val thai-numeral">{c['volume']}</span>
                </td>
            </tr>
            <tr>
                <td colspan="4" class="f-span-row">
                    <span class="f-lbl">หมายเลขสิ่งอุปกรณ์</span> &nbsp; <span class="f-val thai-numeral">{c['nsn']}</span>
                </td>
            </tr>
            <tr>
                <td colspan="4" class="f-span-row">
                    <span class="f-lbl">ชื่อสิ่งอุปกรณ์</span> &nbsp; <span class="f-val">{c['item_name']}</span>
                </td>
            </tr>
            <tr>
                <td colspan="2" class="f-span-row">
                    <span class="f-lbl">หน่วยจ่าย</span> &nbsp; <span class="f-val">{c['issuing_unit']}</span>
                </td>
                <td colspan="2" class="f-span-row" style="text-align: right;">
                    <span class="f-lbl">ราคา</span> &nbsp; <span class="f-val thai-numeral">{c['price']}</span>
                </td>
            </tr>
        </table>
        
        <div class="regulation-note">
            (พิมพ์ตามระเบียบกองทัพบกว่าด้วยการส่งกำลังสิ่งอุปกรณ์ประเภท ๒ และ ๔ พ.ศ.๒๕๓๔)
        </div>
    </div>
    """
    return html

def render_back_card(c):
    # Back table with 20 rows
    b_rows = ""
    for _ in range(20):
        b_rows += """
        <tr class="back-row">
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        """
        
    html = f"""
    <!-- CARD {c['item_no']}: {c['item_name']} (BACK) -->
    <div class="a5-sheet" id="card-{c['item_no']}-back">
        <div class="back-title">
            รายการสถานที่อยู่ของสิ่งอุปกรณ์<br>พร้อมทั้งรายการหลักฐาน
        </div>
        
        <table class="back-table">
            <thead>
                <tr>
                    <th style="width: 20%;">ว.ด.ป.</th>
                    <th style="width: 15%;">จำนวน</th>
                    <th style="width: 35%;">หน่วย / ที่ตั้ง</th>
                    <th style="width: 30%;">รายการหลักฐาน</th>
                </tr>
            </thead>
            <tbody>
                {b_rows}
            </tbody>
        </table>
    </div>
    """
    return html

# Generate TOC & Certification Page
toc_rows_html = ""
for t_item in bp['toc']:
    section_hdr = ""
    if "section" in t_item:
        section_hdr = f"""
        <tr class="toc-sec-row">
            <td colspan="3" class="toc-sec-title">{t_item['section']}</td>
        </tr>
        """
    toc_rows_html += f"""
    {section_hdr}
    <tr class="toc-row">
        <td class="toc-no thai-numeral">{t_item['no']}</td>
        <td class="toc-name">{t_item['name']}</td>
        <td class="toc-page thai-numeral">{t_item['page']}</td>
    </tr>
    """

cert = bp['commander_certification']
cert_page_html = f"""
<!-- PAGE 1: TOC & UNIT CERTIFICATION -->
<div class="a5-sheet" id="page-toc">
    <div class="card-title" style="margin-top: 2mm; margin-bottom: 3mm;">
        สารบัญ<br>
        <span style="font-size: 13pt; font-weight: normal;">บัญชีสิ่งอุปกรณ์ สป.๒-๔ สาย สพ. อจย.๖-๒๗ (๒ พ.ค.๒๙)</span>
    </div>
    
    <table class="toc-table">
        <thead>
            <tr>
                <th style="width: 18%;">ลำดับ</th>
                <th style="width: 66%;">รายการ</th>
                <th style="width: 16%;">หน้า</th>
            </tr>
        </thead>
        <tbody>
            {toc_rows_html}
        </tbody>
    </table>
    
    <div class="cert-box">
        <div class="cert-title">{cert['title']}</div>
        <div class="cert-date-result">
            <span>{cert['inspection_date']}</span> &nbsp; <span>{cert['inspection_result']}</span>
        </div>
        <div class="cert-statement">{cert['statement']}</div>
        
        <!-- SIGNATURE BLOCK (Universal Red Line Standard) -->
        <div class="sig-container">
            <div class="sig-block">
                <div class="sig-name-pos-group">
                    <div class="sig-name-wrapper">
                        <span class="sig-rank-anchor">{cert['commander_rank']}</span>
                        <div class="sig-name">{cert['commander_name']}</div>
                    </div>
                    <div class="sig-pos">{cert['commander_position']}</div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Assemble all cards
all_cards_html = ""
for idx, c in enumerate(bp['cards']):
    all_cards_html += render_front_card(c, idx)
    # Add back card for key items
    if c['item_no'] in [1, 2, 4]:
        all_cards_html += render_back_card(c)

html_full = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp['form_name']} - SUPERCLONE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');
        
        @page {{
            size: 148mm 210mm; /* A5 Portrait */
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
            font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', sans-serif;
            font-size: 12pt;
            line-height: 1.15;
            color: #000;
        }}
        
        .thai-numeral {{
            font-variant-numeric: tabular-nums;
            font-feature-settings: "locl" 1, "numr" 1;
        }}
        
        .a5-sheet {{
            width: 148mm;
            height: 210mm;
            background: #ffffff;
            margin: 15px auto;
            padding: 6mm 7mm 5mm 7mm;
            position: relative;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            overflow: hidden;
        }}
        
        @media print {{
            body {{
                background-color: transparent;
            }}
            .a5-sheet {{
                margin: 0;
                box-shadow: none;
                width: 148mm;
                height: 210mm;
            }}
        }}
        
        .card-header-row {{
            text-align: right;
            font-size: 13pt;
            line-height: 1.0;
            margin-bottom: 1mm;
        }}
        
        .card-title {{
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            line-height: 1.1;
            margin-bottom: 2mm;
        }}
        
        .unit-info-block {{
            font-size: 11pt;
            line-height: 1.15;
            margin-bottom: 1.5mm;
            border-bottom: 1px solid #000;
            padding-bottom: 1mm;
        }}
        
        .unit-name-line {{
            font-weight: normal;
        }}
        
        .unit-detail-line {{
            display: flex;
            justify-content: flex-start;
            font-size: 10.5pt;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .ledger-table {{
            border: 1px solid #000;
            margin-bottom: 1.5mm;
        }}
        
        .ledger-table th, .ledger-table td {{
            border: 1px solid #000;
            padding: 1px 2px;
            font-size: 10.5pt;
            line-height: 1.05;
            text-align: center;
        }}
        
        .ledger-table th {{
            font-weight: normal;
            background-color: #fcfcfc;
        }}
        
        .tx-row td {{
            height: 4.8mm;
        }}
        
        .tx-date {{
            white-space: nowrap;
            font-size: 10pt;
        }}
        
        .tx-doc {{
            text-align: left !important;
            padding-left: 3px !important;
            font-size: 9.5pt !important;
            line-height: 1.0;
        }}
        
        .tx-qty {{
            font-size: 10.5pt;
        }}
        
        .tx-sig {{
            font-size: 10pt;
        }}
        
        .footer-spec-table {{
            border: 1px solid #000;
            margin-bottom: 1.5mm;
        }}
        
        .footer-spec-table td {{
            border: 1px solid #000;
            padding: 1.5px 3px;
            font-size: 10.5pt;
            line-height: 1.1;
        }}
        
        .f-lbl {{
            font-size: 10pt;
            color: #333;
        }}
        
        .f-val {{
            font-size: 11pt;
            font-weight: bold;
        }}
        
        .f-span-row {{
            padding: 1px 3px;
        }}
        
        .regulation-note {{
            font-size: 8.5pt;
            text-align: center;
            color: #444;
            margin-top: auto;
        }}
        
        /* BACK CARD */
        .back-title {{
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            line-height: 1.2;
            margin-top: 3mm;
            margin-bottom: 4mm;
        }}
        
        .back-table {{
            border: 1px solid #000;
            margin-top: 2mm;
        }}
        
        .back-table th, .back-table td {{
            border: 1px solid #000;
            padding: 2px 3px;
            font-size: 11pt;
            text-align: center;
        }}
        
        .back-row td {{
            height: 7.5mm;
        }}
        
        /* TOC TABLE */
        .toc-table {{
            border: 1px solid #000;
            margin-bottom: 3mm;
        }}
        
        .toc-table th, .toc-table td {{
            border: 1px solid #000;
            padding: 1.5px 3px;
            font-size: 10.5pt;
            text-align: center;
        }}
        
        .toc-name {{
            text-align: left !important;
            padding-left: 5px !important;
        }}
        
        .toc-sec-title {{
            background: #eee;
            font-weight: bold;
            text-align: center;
            font-size: 10.5pt;
        }}
        
        .cert-box {{
            border: 1px solid #000;
            padding: 3mm;
            font-size: 10.5pt;
            line-height: 1.2;
        }}
        
        .cert-title {{
            font-weight: bold;
            text-align: center;
            margin-bottom: 1mm;
        }}
        
        .cert-statement {{
            text-indent: 10mm;
            text-align: justify;
            margin: 2mm 0;
            font-size: 10pt;
        }}
        
        .sig-container {{
            width: 100%;
            display: flex;
            justify-content: flex-end;
            margin-top: 3mm;
        }}
        
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 11pt;
            line-height: 1.1;
        }}
        
        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            margin-left: 20px;
        }}
        
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 6mm;
        }}
        
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 2mm);
            white-space: nowrap;
            font-size: 11pt;
            line-height: 1.0;
        }}
        
        .sig-name, .sig-pos {{
            font-size: 11pt;
            white-space: nowrap;
        }}
    </style>
</head>
<body>
    {cert_page_html}
    {all_cards_html}
</body>
</html>
"""

with open(html_out_path, "w", encoding="utf-8") as f:
    f.write(html_full)

print("Generated HTML successfully!")

# ==========================================
# 2. GENERATE WORD (DOCX)
# ==========================================
docx_out_path = r"d:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.docx"
doc = Document()

# Set A5 Portrait
section = doc.sections[0]
section.page_width = Inches(5.83)
section.page_height = Inches(8.27)
section.top_margin = Inches(0.2)
section.bottom_margin = Inches(0.2)
section.left_margin = Inches(0.25)
section.right_margin = Inches(0.25)

def format_cell(cell, font_size=9.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for run in p.runs:
        run.font.name = "TH Sarabun PSK"
        run.font.size = Pt(font_size)
        run.bold = bold

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), edge_data.get('sz', '4'))
            element.set(qn('w:color'), edge_data.get('color', '000000'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

# Page 1: TOC in DOCX
p_th = doc.add_paragraph()
p_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_th.paragraph_format.space_before = Pt(0)
p_th.paragraph_format.space_after = Pt(2)
r_th = p_th.add_run("สารบัญ\nบัญชีสิ่งอุปกรณ์ สป.๒-๔ สาย สพ. อจย.๖-๒๗ (๒ พ.ค.๒๙)")
r_th.font.name = "TH Sarabun PSK"
r_th.font.size = Pt(13)
r_th.bold = True

t_toc = doc.add_table(rows=len(bp['toc']) + 1, cols=3)
t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
t_toc.autofit = False
t_toc.columns[0].width = Inches(0.8)
t_toc.columns[1].width = Inches(3.7)
t_toc.columns[2].width = Inches(0.8)

# Headers
headers = ["ลำดับ", "รายการ", "หน้า"]
for i_h, h_txt in enumerate(headers):
    c = t_toc.rows[0].cells[i_h]
    c.paragraphs[0].add_run(h_txt)
    format_cell(c, font_size=10, bold=True)
    set_cell_border(c, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})

for idx, itm in enumerate(bp['toc'], start=1):
    row_c = t_toc.rows[idx].cells
    row_c[0].paragraphs[0].add_run(itm['no'])
    row_c[1].paragraphs[0].add_run(itm['name'])
    row_c[2].paragraphs[0].add_run(itm['page'])
    format_cell(row_c[0], font_size=9.5)
    format_cell(row_c[1], font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT)
    format_cell(row_c[2], font_size=9.5)
    for rc in row_c:
        set_cell_border(rc, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})

# Render Cards in DOCX
for idx, c in enumerate(bp['cards']):
    doc.add_page_break()
    
    # Header
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(0)
    r_h = p_hdr.add_run("ทบ.๔๐๐ – ๐๐๕")
    r_h.font.name = "TH Sarabun PSK"
    r_h.font.size = Pt(11)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("บัญชีสิ่งอุปกรณ์ของหน่วย")
    r_t.font.name = "TH Sarabun PSK"
    r_t.font.size = Pt(13)
    r_t.bold = True
    
    p_unit = doc.add_paragraph()
    p_unit.paragraph_format.space_before = Pt(0)
    p_unit.paragraph_format.space_after = Pt(2)
    r_u = p_unit.add_run(f"นามหน่วย {bp['unit_info']['unit_name']}\nที่ตั้ง {bp['unit_info']['station']}  อัตรายุทโธปกรณ์ที่ {bp['unit_info']['toe']}")
    r_u.font.name = "TH Sarabun PSK"
    r_u.font.size = Pt(9.5)
    
    # Ledger Table (7 cols)
    transactions = card_trans.get(c['item_no'], [])
    t_rows = 14
    tbl = doc.add_table(rows=t_rows + 2, cols=7)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    col_w = [Inches(0.9), Inches(1.8), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.6)]
    for ci, w in enumerate(col_w):
        tbl.columns[ci].width = w
        
    # Header row 0 & 1
    r0 = tbl.rows[0].cells
    r1 = tbl.rows[1].cells
    r0[0].merge(r1[0]).paragraphs[0].add_run("ว.ด.ป.")
    r0[1].merge(r1[1]).paragraphs[0].add_run("หลักฐาน")
    
    # Merge quantity
    q_merged = r0[2].merge(r0[5])
    q_merged.paragraphs[0].add_run("จำนวน")
    r1[2].paragraphs[0].add_run("ขอเบิก")
    r1[3].paragraphs[0].add_run("ได้รับ")
    r1[4].paragraphs[0].add_run("ส่งคืน")
    r1[5].paragraphs[0].add_run("คงมี")
    
    r0[6].merge(r1[6]).paragraphs[0].add_run("ลงนาม")
    
    for r in tbl.rows[:2]:
        for cell in r.cells:
            format_cell(cell, font_size=9, bold=True)
            set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
            
    # Transaction rows
    for r_i in range(t_rows):
        cells = tbl.rows[r_i + 2].cells
        if r_i < len(transactions):
            tx = transactions[r_i]
            cells[0].paragraphs[0].add_run(tx['date'])
            cells[1].paragraphs[0].add_run(tx['doc'])
            cells[2].paragraphs[0].add_run(tx['req'])
            cells[3].paragraphs[0].add_run(tx['recv'])
            cells[4].paragraphs[0].add_run(tx['ret'])
            cells[5].paragraphs[0].add_run(tx['bal'])
            cells[6].paragraphs[0].add_run(tx['sig'])
        for cell_idx, cell in enumerate(cells):
            format_cell(cell, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT if cell_idx==1 else WD_ALIGN_PARAGRAPH.CENTER)
            set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
            
    # Footer Spec Table (4 cols)
    f_tbl = doc.add_table(rows=5, cols=4)
    f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_tbl.autofit = False
    
    # Row 0: สายงาน (2) | เต็ม | ลด
    f0 = f_tbl.rows[0].cells
    f0[0].merge(f0[1]).paragraphs[0].add_run(f"สายงานที่ควบคุม: {c['service']}")
    f0[2].paragraphs[0].add_run(f"อัตราเต็ม: {c['rate_full']}")
    f0[3].paragraphs[0].add_run(f"อัตราลด: {c['rate_reduced']}")
    
    # Row 1: ประเภท | หน่วยนับ | น้ำหนัก | ปริมาตร
    f1 = f_tbl.rows[1].cells
    f1[0].paragraphs[0].add_run(f"ประเภท: {c['category']}")
    f1[1].paragraphs[0].add_run(f"หน่วยนับ: {c['unit']}")
    f1[2].paragraphs[0].add_run(f"น้ำหนัก: {c['weight']}")
    f1[3].paragraphs[0].add_run(f"ปริมาตร: {c['volume']}")
    
    # Row 2: NSN
    f2 = f_tbl.rows[2].cells
    f2[0].merge(f2[3]).paragraphs[0].add_run(f"หมายเลขสิ่งอุปกรณ์: {c['nsn']}")
    
    # Row 3: Name
    f3 = f_tbl.rows[3].cells
    f3[0].merge(f3[3]).paragraphs[0].add_run(f"ชื่อสิ่งอุปกรณ์: {c['item_name']}")
    
    # Row 4: หน่วยจ่าย | ราคา
    f4 = f_tbl.rows[4].cells
    f4[0].merge(f4[1]).paragraphs[0].add_run(f"หน่วยจ่าย: {c['issuing_unit']}")
    f4[2].merge(f4[3]).paragraphs[0].add_run(f"ราคา: {c['price']}")
    
    for row in f_tbl.rows:
        for cell in row.cells:
            format_cell(cell, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})

doc.save(docx_out_path)
print("Generated DOCX successfully!")

# ==========================================
# 3. GENERATE EXCEL (XLSX)
# ==========================================
xlsx_out_path = r"d:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.xlsx"
wb = openpyxl.Workbook()

# Sheet 1: สารบัญ
ws_toc = wb.active
ws_toc.title = "สารบัญ"
ws_toc.views.sheetView[0].showGridLines = True

font_title = Font(name="TH Sarabun PSK", size=16, bold=True)
font_bold = Font(name="TH Sarabun PSK", size=13, bold=True)
font_norm = Font(name="TH Sarabun PSK", size=13)
thin_b = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

ws_toc.merge_cells("A1:C1")
ws_toc["A1"] = "สารบัญ บัญชีสิ่งอุปกรณ์ สป.๒-๔ สาย สพ. อจย.๖-๒๗ (๒ พ.ค.๒๙)"
ws_toc["A1"].font = font_title
ws_toc["A1"].alignment = Alignment(horizontal="center")

headers = ["ลำดับ", "รายการ", "หน้า"]
for ci, h in enumerate(headers, 1):
    c = ws_toc.cell(row=3, column=ci, value=h)
    c.font = font_bold
    c.border = thin_b
    c.alignment = Alignment(horizontal="center")

for r_i, itm in enumerate(bp['toc'], 4):
    c1 = ws_toc.cell(row=r_i, column=1, value=itm['no'])
    c2 = ws_toc.cell(row=r_i, column=2, value=itm['name'])
    c3 = ws_toc.cell(row=r_i, column=3, value=itm['page'])
    for cell in [c1, c2, c3]:
        cell.font = font_norm
        cell.border = thin_b
    c1.alignment = Alignment(horizontal="center")
    c3.alignment = Alignment(horizontal="center")

ws_toc.column_dimensions["A"].width = 8
ws_toc.column_dimensions["B"].width = 45
ws_toc.column_dimensions["C"].width = 8

# Create worksheet for each Card
for c_item in bp['cards']:
    sheet_title = f"บัตร {c_item['item_no']}"
    ws = wb.create_sheet(title=sheet_title)
    ws.views.sheetView[0].showGridLines = True
    
    # Form header
    ws.merge_cells("A1:G1")
    ws["A1"] = "ทบ.๔๐๐ – ๐๐๕"
    ws["A1"].alignment = Alignment(horizontal="right")
    ws["A1"].font = font_norm
    
    ws.merge_cells("A2:G2")
    ws["A2"] = "บัญชีสิ่งอุปกรณ์ของหน่วย"
    ws["A2"].alignment = Alignment(horizontal="center")
    ws["A2"].font = font_title
    
    ws.merge_cells("A3:G3")
    ws["A3"] = f"นามหน่วย {bp['unit_info']['unit_name']}  ที่ตั้ง {bp['unit_info']['station']}  อัตรายุทโธปกรณ์ที่ {bp['unit_info']['toe']}"
    ws["A3"].font = font_norm
    
    # Ledger Table Headers
    ws.merge_cells("A4:A5")
    ws["A4"] = "ว.ด.ป."
    ws.merge_cells("B4:B5")
    ws["B4"] = "หลักฐาน"
    ws.merge_cells("C4:F4")
    ws["C4"] = "จำนวน"
    ws["C5"] = "ขอเบิก"
    ws["D5"] = "ได้รับ"
    ws["E5"] = "ส่งคืน"
    ws["F5"] = "คงมี"
    ws.merge_cells("G4:G5")
    ws["G4"] = "ลงนาม"
    
    for r in range(4, 6):
        for col in range(1, 8):
            cell = ws.cell(row=r, column=col)
            cell.font = font_bold
            cell.border = thin_b
            cell.alignment = Alignment(horizontal="center", vertical="center")
            
    # Transactions
    txs = card_trans.get(c_item['item_no'], [])
    for r_idx in range(6, 18):
        tx_i = r_idx - 6
        if tx_i < len(txs):
            tx = txs[tx_i]
            ws.cell(row=r_idx, column=1, value=tx['date']).alignment = Alignment(horizontal="center")
            ws.cell(row=r_idx, column=2, value=tx['doc']).alignment = Alignment(horizontal="left", wrap_text=True)
            ws.cell(row=r_idx, column=3, value=tx['req']).alignment = Alignment(horizontal="center")
            ws.cell(row=r_idx, column=4, value=tx['recv']).alignment = Alignment(horizontal="center")
            ws.cell(row=r_idx, column=5, value=tx['ret']).alignment = Alignment(horizontal="center")
            ws.cell(row=r_idx, column=6, value=tx['bal']).alignment = Alignment(horizontal="center")
            ws.cell(row=r_idx, column=7, value=tx['sig']).alignment = Alignment(horizontal="center")
        for col in range(1, 8):
            cell = ws.cell(row=r_idx, column=col)
            cell.font = font_norm
            cell.border = thin_b
            
    # Footer Spec Grid
    ws.merge_cells("A19:B19")
    ws["A19"] = f"สายงานที่ควบคุม: {c_item['service']}"
    ws.merge_cells("C19:E19")
    ws["C19"] = f"จำนวนตามอัตราเต็ม: {c_item['rate_full']}"
    ws.merge_cells("F19:G19")
    ws["F19"] = f"จำนวนตามอัตราลด: {c_item['rate_reduced']}"
    
    ws.merge_cells("A20:B20")
    ws["A20"] = f"ประเภท: {c_item['category']}"
    ws.cell(row=20, column=3, value=f"หน่วยนับ: {c_item['unit']}")
    ws.merge_cells("D20:E20")
    ws["D20"] = f"น้ำหนัก: {c_item['weight']}"
    ws.merge_cells("F20:G20")
    ws["F20"] = f"ปริมาตร: {c_item['volume']}"
    
    ws.merge_cells("A21:G21")
    ws["A21"] = f"หมายเลขสิ่งอุปกรณ์: {c_item['nsn']}"
    
    ws.merge_cells("A22:G22")
    ws["A22"] = f"ชื่อสิ่งอุปกรณ์: {c_item['item_name']}"
    
    ws.merge_cells("A23:D23")
    ws["A23"] = f"หน่วยจ่าย: {c_item['issuing_unit']}"
    ws.merge_cells("E23:G23")
    ws["E23"] = f"ราคา: {c_item['price']}"
    
    for r in range(19, 24):
        for col in range(1, 8):
            cell = ws.cell(row=r, column=col)
            cell.font = font_norm
            cell.border = thin_b
            
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 8
    ws.column_dimensions["D"].width = 8
    ws.column_dimensions["E"].width = 8
    ws.column_dimensions["F"].width = 8
    ws.column_dimensions["G"].width = 10

wb.save(xlsx_out_path)
print("Generated XLSX successfully!")
