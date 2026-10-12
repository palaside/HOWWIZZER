import json
import os
import base64
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load Blueprint
with open(r'd:\Project\WEPAPP\table_layout_cat2_4.json', encoding='utf-8') as f:
    bp = json.load(f)

emblem_path = r'd:\Project\WEPAPP\tiger_artillery_emblem.jpg'
with open(emblem_path, 'rb') as f:
    emblem_b64 = base64.b64encode(f.read()).decode('utf-8')

# Output paths
html_path = r'd:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.html'
docx_path = r'd:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.docx'
xlsx_path = r'd:\Project\WEPAPP\บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.xlsx'

# -------------------------------------------------------------
# 1. HTML GENERATOR
# -------------------------------------------------------------
def generate_html():
    cards_html = []
    
    # Render all 87 cards
    for idx, c in enumerate(bp['cards'], start=1):
        # Front card
        t_rows_html = ""
        tx_list = c.get('transactions', [])
        for r_i in range(12):
            if r_i < len(tx_list):
                tx = tx_list[r_i]
                t_rows_html += f"""
                <tr class="tx-row">
                    <td class="tx-date thai-numeral">{tx['date']}</td>
                    <td class="tx-doc">{tx['doc']}</td>
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
                
        front_card = f"""
        <!-- CARD {c['item_no']}: {c['item_name']} (FRONT) -->
        <div class="a5-sheet" id="card-{c['item_no']}-front">
            <div class="card-header-row">
                <span class="form-code thai-numeral">{bp['form_code']}</span>
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
                        <span class="f-val thai-numeral">{c['category']}</span>
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
        cards_html.append(front_card)
        
        # Back card (location record)
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
        back_card = f"""
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
        cards_html.append(back_card)

    cert = bp['commander_certification']
    html_content = f"""<!DOCTYPE html>
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
        
        /* COVER PAGE */
        .cover-sheet {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 15mm 10mm;
        }}
        
        .cover-code {{
            position: absolute;
            top: 8mm;
            right: 8mm;
            font-size: 14pt;
            font-weight: bold;
            color: #0b3b60;
        }}
        
        .cover-emblem {{
            width: 75mm;
            height: auto;
            margin-bottom: 8mm;
            filter: drop-shadow(0 2px 5px rgba(0,0,0,0.2));
        }}
        
        .cover-title {{
            font-size: 20pt;
            font-weight: bold;
            color: #0b3b60;
            line-height: 1.25;
            margin-bottom: 4mm;
        }}
        
        .cover-service {{
            font-size: 18pt;
            font-weight: bold;
            color: #0b3b60;
            margin-bottom: 3mm;
        }}
        
        .cover-store {{
            font-size: 16pt;
            font-weight: bold;
            color: #0b3b60;
            margin-bottom: 8mm;
        }}
        
        .cover-unit-full {{
            font-size: 13pt;
            color: #333;
            margin-top: auto;
        }}
        
        /* CERTIFICATION PAGE */
        .cert-sheet {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 20mm 15mm;
        }}
        
        .cert-hdr-title {{
            font-size: 16pt;
            font-weight: bold;
            color: #0b3b60;
            margin-bottom: 4mm;
        }}
        
        .cert-unit-title {{
            font-size: 16pt;
            font-weight: bold;
            color: #0b3b60;
            margin-bottom: 12mm;
        }}
        
        .cert-quote-box {{
            font-size: 15pt;
            font-weight: bold;
            color: #0b3b60;
            line-height: 1.4;
            margin-bottom: 15mm;
            max-width: 110mm;
        }}
        
        /* SIGNATURE BLOCK (Universal Red Line Standard) */
        .sig-container {{
            width: 100%;
            display: flex;
            justify-content: flex-end;
            margin-top: 5mm;
        }}
        
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 12pt;
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
            margin-top: 8mm;
        }}
        
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 2mm);
            white-space: nowrap;
            font-size: 12pt;
            line-height: 1.0;
        }}
        
        .sig-name, .sig-pos {{
            font-size: 12pt;
            white-space: nowrap;
        }}
        
        /* WARNING & INSPECTION PAGE */
        .warning-box {{
            border: 2px solid #000;
            padding: 3mm 4mm;
            font-size: 11pt;
            font-weight: bold;
            line-height: 1.25;
            margin-bottom: 6mm;
            background-color: #fcfcfc;
        }}
        
        .insp-title {{
            text-align: center;
            font-size: 15pt;
            font-weight: bold;
            margin-bottom: 3mm;
        }}
        
        .insp-table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #000;
        }}
        
        .insp-table th {{
            border: 1px solid #000;
            padding: 1px 3px 5px 3px;
            font-size: 11pt;
            text-align: center;
            vertical-align: middle;
            line-height: 1.0;
            height: 7.5mm;
        }}
        
        .insp-table td {{
            border: 1px solid #000;
            padding: 2.5px 3px;
            font-size: 11pt;
            text-align: center;
            vertical-align: middle;
        }}
        
        .insp-row td {{
            height: 7.5mm;
        }}
        
        /* CARD SPECIFIC */
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
            vertical-align: middle;
        }}
        
        .ledger-table th {{
            font-weight: normal;
            background-color: #fcfcfc;
            padding: 1px 2px 4px 2px;
            line-height: 1.0;
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
        
        .back-table th {{
            border: 1px solid #000;
            padding: 1px 3px 5px 3px;
            font-size: 11pt;
            text-align: center;
            vertical-align: middle;
            line-height: 1.0;
            height: 7.5mm;
        }}
        
        .back-table td {{
            border: 1px solid #000;
            padding: 2px 3px;
            font-size: 11pt;
            text-align: center;
            vertical-align: middle;
        }}
        
        .back-row td {{
            height: 7.5mm;
        }}
    </style>
</head>
<body>

<!-- PAGE 1: COVER PAGE -->
<div class="a5-sheet cover-sheet" id="page-cover">
    <div class="cover-code thai-numeral">ทบ.400 - 005</div>
    <img src="data:image/jpeg;base64,{emblem_b64}" class="cover-emblem" alt="Artillery Emblem">
    <div class="cover-title">บัญชีสิ่งอุปกรณ์ประเภท 2 และ 4</div>
    <div class="cover-service">สาย สพ.</div>
    <div class="cover-store">(คลังโรงปืน)</div>
    <div class="cover-unit-full">{bp['unit_info']['battalion_full']}</div>
</div>

<!-- PAGE 2: CERTIFICATION PAGE -->
<div class="a5-sheet cert-sheet" id="page-cert">
    <div class="cert-hdr-title">{cert['toe_ref']}</div>
    <div class="cert-unit-title">{cert['unit']}</div>
    <div class="cert-quote-box">{cert['statement']}</div>
    
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

<!-- PAGE 3: INSPECTION & WARNING PAGE -->
<div class="a5-sheet" id="page-inspection">
    <div class="warning-box">
        {bp['warning_text']}
    </div>
    
    <div class="insp-title">บันทึกผลการตรวจของผู้บังคับบัญชา</div>
    <table class="insp-table">
        <thead>
            <tr>
                <th style="width: 25%;">ว.ด.ป.</th>
                <th style="width: 50%;">หัวข้อการตรวจ</th>
                <th style="width: 25%;">ลงนามผู้ตรวจ</th>
            </tr>
        </thead>
        <tbody>
            {''.join(['<tr class="insp-row"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>' for _ in range(16)])}
        </tbody>
    </table>
</div>

<!-- PAGE 4: LOCATION RECORD PAGE -->
<div class="a5-sheet" id="page-location-intro">
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
            {''.join(['<tr class="back-row"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>' for _ in range(20)])}
        </tbody>
    </table>
</div>

<!-- 87 STOCK CARDS (FRONT & BACK) -->
{''.join(cards_html)}

</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated HTML successfully!")

# -------------------------------------------------------------
# 2. DOCX GENERATOR
# -------------------------------------------------------------
def generate_docx():
    doc = Document()
    
    # Page setup A5 Portrait
    for sec in doc.sections:
        sec.page_width = Inches(5.83)   # 148 mm
        sec.page_height = Inches(8.27)  # 210 mm
        sec.top_margin = Inches(0.25)
        sec.bottom_margin = Inches(0.25)
        sec.left_margin = Inches(0.3)
        sec.right_margin = Inches(0.3)
        
    def format_cell(cell, font_size=9.5, bold=False, color="000000", align=WD_ALIGN_PARAGRAPH.CENTER):
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = align
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            for r in p.runs:
                r.font.name = "TH Sarabun PSK"
                r.font.size = Pt(font_size)
                r.bold = bold
                r.font.color.rgb = RGBColor.from_string(color)

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

    # 1. Cover Page
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_c = p_code.add_run("ทบ.400 - 005")
    r_c.font.name = "TH Sarabun PSK"
    r_c.font.size = Pt(13)
    r_c.bold = True
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(emblem_path, width=Inches(2.5))
    
    p_ct = doc.add_paragraph()
    p_ct.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ct.paragraph_format.space_before = Pt(12)
    p_ct.paragraph_format.space_after = Pt(4)
    r_ct = p_ct.add_run("บัญชีสิ่งอุปกรณ์ประเภท 2 และ 4\nสาย สพ.\n(คลังโรงปืน)")
    r_ct.font.name = "TH Sarabun PSK"
    r_ct.font.size = Pt(18)
    r_ct.bold = True
    r_ct.font.color.rgb = RGBColor(11, 59, 96)
    
    p_cu = doc.add_paragraph()
    p_cu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cu.paragraph_format.space_before = Pt(24)
    r_cu = p_cu.add_run(bp['unit_info']['battalion_full'])
    r_cu.font.name = "TH Sarabun PSK"
    r_cu.font.size = Pt(13)
    
    # 2. Certification Page
    doc.add_page_break()
    cert = bp['commander_certification']
    p_cert_hdr = doc.add_paragraph()
    p_cert_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_hdr.paragraph_format.space_before = Pt(36)
    p_cert_hdr.paragraph_format.space_after = Pt(6)
    r_ch = p_cert_hdr.add_run(f"{cert['toe_ref']}\n{cert['unit']}")
    r_ch.font.name = "TH Sarabun PSK"
    r_ch.font.size = Pt(16)
    r_ch.bold = True
    r_ch.font.color.rgb = RGBColor(11, 59, 96)
    
    p_cert_q = doc.add_paragraph()
    p_cert_q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_q.paragraph_format.space_before = Pt(24)
    p_cert_q.paragraph_format.space_after = Pt(24)
    r_cq = p_cert_q.add_run(cert['statement'])
    r_cq.font.name = "TH Sarabun PSK"
    r_cq.font.size = Pt(15)
    r_cq.bold = True
    r_cq.font.color.rgb = RGBColor(11, 59, 96)
    
    # Signature block
    p_sig1 = doc.add_paragraph()
    p_sig1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig1.paragraph_format.space_after = Pt(18)
    r_s1 = p_sig1.add_run(f"{cert['commander_rank']}\t\t")
    r_s1.font.name = "TH Sarabun PSK"
    r_s1.font.size = Pt(12)
    
    p_sig2 = doc.add_paragraph()
    p_sig2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig2.paragraph_format.space_after = Pt(0)
    r_s2 = p_sig2.add_run(f"{cert['commander_name']}\n{cert['commander_position']}\t")
    r_s2.font.name = "TH Sarabun PSK"
    r_s2.font.size = Pt(12)
    
    # 3. 87 Cards in DOCX
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
        
        # Ledger Table
        tbl = doc.add_table(rows=14, cols=7)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        col_w = [Inches(0.9), Inches(1.8), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.6)]
        for ci, w in enumerate(col_w):
            tbl.columns[ci].width = w
            
        r0 = tbl.rows[0].cells
        r1 = tbl.rows[1].cells
        r0[0].merge(r1[0]).paragraphs[0].add_run("ว.ด.ป.")
        r0[1].merge(r1[1]).paragraphs[0].add_run("หลักฐาน")
        r0[2].merge(r0[5]).paragraphs[0].add_run("จำนวน")
        r1[2].paragraphs[0].add_run("ขอเบิก")
        r1[3].paragraphs[0].add_run("ได้รับ")
        r1[4].paragraphs[0].add_run("ส่งคืน")
        r1[5].paragraphs[0].add_run("คงมี")
        r0[6].merge(r1[6]).paragraphs[0].add_run("ลงนาม")
        
        for ri in range(2):
            for cell in tbl.rows[ri].cells:
                format_cell(cell, font_size=9, bold=True)
                set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
                
        # Data rows
        tx_list = c.get('transactions', [])
        for ri in range(2, 14):
            data_cells = tbl.rows[ri].cells
            tx_idx = ri - 2
            if tx_idx < len(tx_list):
                tx = tx_list[tx_idx]
                data_cells[0].paragraphs[0].add_run(tx['date'])
                data_cells[1].paragraphs[0].add_run(tx['doc'])
                data_cells[2].paragraphs[0].add_run(tx['req'])
                data_cells[3].paragraphs[0].add_run(tx['recv'])
                data_cells[4].paragraphs[0].add_run(tx['ret'])
                data_cells[5].paragraphs[0].add_run(tx['bal'])
                data_cells[6].paragraphs[0].add_run(tx['sig'])
                format_cell(data_cells[1], font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for cell in data_cells:
                format_cell(cell, font_size=9)
                set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
                
        # Footer spec table
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(2)
        p_sp.paragraph_format.space_after = Pt(0)
        
        t_spec = doc.add_table(rows=5, cols=4)
        t_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_spec.autofit = False
        s_col_w = [Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.4)]
        for ci, w in enumerate(s_col_w):
            t_spec.columns[ci].width = w
            
        sr0 = t_spec.rows[0].cells
        sr0[0].merge(sr0[1]).paragraphs[0].add_run(f"สายงานที่ควบคุม: {c['service']}")
        sr0[2].paragraphs[0].add_run(f"อัตราเต็ม: {c['rate_full']}")
        sr0[3].paragraphs[0].add_run(f"อัตราลด: {c['rate_reduced']}")
        
        sr1 = t_spec.rows[1].cells
        sr1[0].paragraphs[0].add_run(f"ประเภท: {c['category']}")
        sr1[1].paragraphs[0].add_run(f"หน่วยนับ: {c['unit']}")
        sr1[2].paragraphs[0].add_run(f"น้ำหนัก: {c['weight']}")
        sr1[3].paragraphs[0].add_run(f"ปริมาตร: {c['volume']}")
        
        sr2 = t_spec.rows[2].cells
        sr2[0].merge(sr2[3]).paragraphs[0].add_run(f"หมายเลขสิ่งอุปกรณ์: {c['nsn']}")
        
        sr3 = t_spec.rows[3].cells
        sr3[0].merge(sr3[3]).paragraphs[0].add_run(f"ชื่อสิ่งอุปกรณ์: {c['item_name']}")
        
        sr4 = t_spec.rows[4].cells
        sr4[0].merge(sr4[1]).paragraphs[0].add_run(f"หน่วยจ่าย: {c['issuing_unit']}")
        sr4[2].merge(sr4[3]).paragraphs[0].add_run(f"ราคา: {c['price']}")
        
        for r in t_spec.rows:
            for cell in r.cells:
                format_cell(cell, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
                set_cell_border(cell, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})

    doc.save(docx_path)
    print("Generated DOCX successfully!")

# -------------------------------------------------------------
# 3. XLSX GENERATOR
# -------------------------------------------------------------
def generate_xlsx():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    font_th = Font(name="TH Sarabun PSK", size=11)
    font_th_bold = Font(name="TH Sarabun PSK", size=11, bold=True)
    font_title = Font(name="TH Sarabun PSK", size=14, bold=True)
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center")
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    fill_header = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    # Sheet 1: สารบัญ & คำรับรอง
    ws_toc = wb.create_sheet(title="สารบัญ")
    ws_toc.views.sheetView[0].showGridLines = True
    
    ws_toc.cell(row=1, column=1, value="บัญชีสิ่งอุปกรณ์ประเภท 2 และ 4 สาย สพ. (คลังโรงปืน)").font = font_title
    ws_toc.cell(row=2, column=1, value=f"นามหน่วย: {bp['unit_info']['unit_name']}  {bp['unit_info']['battalion_full']}").font = font_th_bold
    
    ws_toc.cell(row=4, column=1, value="ลำดับ").font = font_th_bold
    ws_toc.cell(row=4, column=2, value="ชื่อสิ่งอุปกรณ์").font = font_th_bold
    ws_toc.cell(row=4, column=3, value="หมายเลขสิ่งอุปกรณ์ (NSN)").font = font_th_bold
    ws_toc.cell(row=4, column=4, value="หน่วยนับ").font = font_th_bold
    ws_toc.cell(row=4, column=5, value="อัตราเต็ม").font = font_th_bold
    ws_toc.cell(row=4, column=6, value="ราคา").font = font_th_bold
    
    for c_i in range(1, 7):
        cell = ws_toc.cell(row=4, column=c_i)
        cell.alignment = align_center
        cell.fill = fill_header
        cell.border = thin_border
        
    for r_idx, itm in enumerate(bp['cards'], start=5):
        ws_toc.cell(row=r_idx, column=1, value=itm['item_no']).alignment = align_center
        ws_toc.cell(row=r_idx, column=2, value=itm['item_name']).alignment = align_left
        ws_toc.cell(row=r_idx, column=3, value=itm['nsn']).alignment = align_center
        ws_toc.cell(row=r_idx, column=4, value=itm['unit']).alignment = align_center
        ws_toc.cell(row=r_idx, column=5, value=itm['rate_full']).alignment = align_center
        ws_toc.cell(row=r_idx, column=6, value=itm['price']).alignment = align_right
        
        for c_i in range(1, 7):
            cell = ws_toc.cell(row=r_idx, column=c_i)
            cell.font = font_th
            cell.border = thin_border
            
    ws_toc.column_dimensions['A'].width = 8
    ws_toc.column_dimensions['B'].width = 42
    ws_toc.column_dimensions['C'].width = 24
    ws_toc.column_dimensions['D'].width = 10
    ws_toc.column_dimensions['E'].width = 12
    ws_toc.column_dimensions['F'].width = 15

    # Cards sheets (Generate up to all cards or clean individual tabs)
    # Excel limits sheets count to reasonable numbers, 87 sheets is fully supported
    for c in bp['cards']:
        sh_name = f"สป.{c['item_no']}"
        ws = wb.create_sheet(title=sh_name)
        ws.views.sheetView[0].showGridLines = True
        
        ws.cell(row=1, column=7, value="ทบ.๔๐๐ – ๐๐๕").font = font_th_bold
        ws.cell(row=1, column=7).alignment = align_right
        
        ws.cell(row=2, column=1, value="บัญชีสิ่งอุปกรณ์ของหน่วย").font = font_title
        ws.merge_cells("A2:G2")
        ws.cell(row=2, column=1).alignment = align_center
        
        ws.cell(row=3, column=1, value=f"นามหน่วย {bp['unit_info']['unit_name']}    ที่ตั้ง {bp['unit_info']['station']}    อัตรายุทโธปกรณ์ที่ {bp['unit_info']['toe']}").font = font_th
        ws.merge_cells("A3:G3")
        
        # Headers
        ws.cell(row=5, column=1, value="ว.ด.ป.").font = font_th_bold
        ws.merge_cells("A5:A6")
        ws.cell(row=5, column=2, value="หลักฐาน").font = font_th_bold
        ws.merge_cells("B5:B6")
        ws.cell(row=5, column=3, value="จำนวน").font = font_th_bold
        ws.merge_cells("C5:F5")
        ws.cell(row=6, column=3, value="ขอเบิก").font = font_th_bold
        ws.cell(row=6, column=4, value="ได้รับ").font = font_th_bold
        ws.cell(row=6, column=5, value="ส่งคืน").font = font_th_bold
        ws.cell(row=6, column=6, value="คงมี").font = font_th_bold
        ws.cell(row=5, column=7, value="ลงนาม").font = font_th_bold
        ws.merge_cells("G5:G6")
        
        for r_i in range(5, 7):
            for c_i in range(1, 8):
                cell = ws.cell(row=r_i, column=c_i)
                cell.alignment = align_center
                cell.fill = fill_header
                cell.border = thin_border

        # 12 Data rows
        tx_list = c.get('transactions', [])
        for r_i in range(7, 19):
            tx_idx = r_i - 7
            if tx_idx < len(tx_list):
                tx = tx_list[tx_idx]
                ws.cell(row=r_i, column=1, value=tx['date']).alignment = align_center
                ws.cell(row=r_i, column=2, value=tx['doc']).alignment = align_left
                ws.cell(row=r_i, column=3, value=int(tx['req']) if tx['req'].isdigit() else tx['req']).alignment = align_center
                ws.cell(row=r_i, column=4, value=int(tx['recv']) if tx['recv'].isdigit() else tx['recv']).alignment = align_center
                ws.cell(row=r_i, column=5, value=tx['ret']).alignment = align_center
                ws.cell(row=r_i, column=6, value=int(tx['bal']) if tx['bal'].isdigit() else tx['bal']).alignment = align_center
                ws.cell(row=r_i, column=7, value=tx['sig']).alignment = align_center
            for c_i in range(1, 8):
                cell = ws.cell(row=r_i, column=c_i)
                cell.font = font_th
                cell.border = thin_border
                
        # Footer Spec Grid
        r_f = 20
        ws.cell(row=r_f, column=1, value=f"สายงานที่ควบคุม: {c['service']}").font = font_th_bold
        ws.merge_cells(start_row=r_f, start_column=1, end_row=r_f, end_column=3)
        ws.cell(row=r_f, column=4, value=f"อัตราเต็ม: {c['rate_full']}").font = font_th_bold
        ws.merge_cells(start_row=r_f, start_column=4, end_row=r_f, end_column=5)
        ws.cell(row=r_f, column=6, value=f"อัตราลด: {c['rate_reduced']}").font = font_th_bold
        ws.merge_cells(start_row=r_f, start_column=6, end_row=r_f, end_column=7)
        
        ws.cell(row=r_f+1, column=1, value=f"ประเภท: {c['category']}").font = font_th
        ws.merge_cells(start_row=r_f+1, start_column=1, end_row=r_f+1, end_column=2)
        ws.cell(row=r_f+1, column=3, value=f"หน่วยนับ: {c['unit']}").font = font_th
        ws.merge_cells(start_row=r_f+1, start_column=3, end_row=r_f+1, end_column=4)
        ws.cell(row=r_f+1, column=5, value=f"น้ำหนัก: {c['weight']}").font = font_th
        ws.cell(row=r_f+1, column=6, value=f"ปริมาตร: {c['volume']}").font = font_th
        ws.merge_cells(start_row=r_f+1, start_column=6, end_row=r_f+1, end_column=7)
        
        ws.cell(row=r_f+2, column=1, value=f"หมายเลขสิ่งอุปกรณ์: {c['nsn']}").font = font_th_bold
        ws.merge_cells(start_row=r_f+2, start_column=1, end_row=r_f+2, end_column=7)
        
        ws.cell(row=r_f+3, column=1, value=f"ชื่อสิ่งอุปกรณ์: {c['item_name']}").font = font_th_bold
        ws.merge_cells(start_row=r_f+3, start_column=1, end_row=r_f+3, end_column=7)
        
        ws.cell(row=r_f+4, column=1, value=f"หน่วยจ่าย: {c['issuing_unit']}").font = font_th
        ws.merge_cells(start_row=r_f+4, start_column=1, end_row=r_f+4, end_column=4)
        ws.cell(row=r_f+4, column=5, value=f"ราคา: {c['price']}").font = font_th
        ws.merge_cells(start_row=r_f+4, start_column=5, end_row=r_f+4, end_column=7)
        
        for r_sub in range(r_f, r_f+5):
            for c_sub in range(1, 8):
                ws.cell(row=r_sub, column=c_sub).border = thin_border
                
        # Set column widths
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 28
        ws.column_dimensions['C'].width = 9
        ws.column_dimensions['D'].width = 9
        ws.column_dimensions['E'].width = 9
        ws.column_dimensions['F'].width = 9
        ws.column_dimensions['G'].width = 12

    wb.save(xlsx_path)
    print("Generated XLSX successfully!")

if __name__ == "__main__":
    generate_html()
    generate_docx()
    generate_xlsx()
    print("ALL 3 PRODUCTION FORMATS GENERATED SUCCESSFULLY!")
