import os
import json
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load Blueprint
blueprint_path = r"d:\Project\WEPAPP\table_layout_survey_sp.json"
with open(blueprint_path, "r", encoding="utf-8") as f:
    bp = json.load(f)

meta = bp["metadata"]
items = bp["items"]
sig_defaults = bp["signature_defaults"]

# ==========================================
# 1. GENERATE HTML
# ==========================================
html_out_path = r"d:\Project\WEPAPP\ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html"

# Group items into pairs for 12 pages (2 items per page)
pages_items = []
for i in range(0, len(items), 2):
    pair = [items[i]]
    if i + 1 < len(items):
        pair.append(items[i+1])
    else:
        # 24th card is blank template
        pair.append({
            "item_no": "",
            "survey_no": "",
            "nsn": "",
            "item_name": "",
            "storage_location": "โรงเก็บปืนใหญ่",
            "unit": "ป.4 พัน.4 ร้อย.2",
            "survey_date": "พ.ย. 66",
            "qty_record": "",
            "qty_counted": "",
            "qty_short": "",
            "qty_over": "",
            "price_short": "",
            "price_over": ""
        })
    pages_items.append(pair)

def render_slip(item, slip_idx, is_top_card):
    sig_key = f"slip_{slip_idx}"
    sigs = sig_defaults[sig_key]
    
    # Check rank override for slip 3
    c_rank = sigs["checker"]["rank"]
    t_rank = sigs["team_lead"]["rank"]
    a_rank = sigs["account_officer"]["rank"]
    
    nsn_display = item["nsn"] if item["nsn"] else "&nbsp;"
    name_display = item["item_name"] if item["item_name"] else "&nbsp;"
    survey_no_display = item["survey_no"] if item["survey_no"] else "&nbsp;"
    
    html = f"""
    <div class="survey-slip slip-{slip_idx}">
        <div class="slip-header-row">
            <div class="slip-title">ใบสำรวจสิ่งอุปกรณ์</div>
        </div>
        
        <div class="item-nsn-row">
            <div class="nsn-label">หมายเลขสิ่งอุปกรณ์และ<br>รายการ</div>
            <div class="nsn-val thai-numeral">{nsn_display}</div>
        </div>
        
        <div class="item-name-row">
            <div class="item-name-val">{name_display}</div>
        </div>
        
        <table class="meta-box-table">
            <tr>
                <td style="width: 44%;">
                    <div class="meta-lbl">ที่เก็บ</div>
                    <div class="meta-val">โรงเก็บปืนใหญ่</div>
                    <div class="meta-val">ป.4 พัน.4 ร้อย.2</div>
                </td>
                <td style="width: 28%;">
                    <div class="meta-lbl">ที่ใบสำรวจ</div>
                    <div class="meta-val thai-numeral">{survey_no_display}</div>
                </td>
                <td style="width: 28%;">
                    <div class="meta-lbl">วันสำรวจ</div>
                    <div class="meta-val meta-date thai-numeral">พ.ย. 66</div>
                </td>
            </tr>
        </table>
        
        <table class="record-grid-table">
            <thead>
                <tr>
                    <th colspan="6" class="grid-title">บันทึกการสำรวจ</th>
                </tr>
                <tr>
                    <th colspan="2" style="width: 33.33%;">จำนวน</th>
                    <th colspan="2" style="width: 33.33%;">ผลสรุปจำนวน</th>
                    <th colspan="2" style="width: 33.34%;">ผลสรุปราคา</th>
                </tr>
                <tr>
                    <th style="width: 16.66%;">ตามบัญชี</th>
                    <th style="width: 16.67%;">ที่นับได้</th>
                    <th style="width: 16.66%;">ขาด</th>
                    <th style="width: 16.67%;">เกิน</th>
                    <th style="width: 16.67%;">ขาด</th>
                    <th style="width: 16.67%;">เกิน</th>
                </tr>
            </thead>
            <tbody>
                <tr class="data-row">
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
            </tbody>
        </table>
        
        <table class="sig-box-table">
            <tr>
                <td style="width: 33.33%;">
                    <div class="sig-cell-content">
                        <div class="sig-rank">{c_rank}</div>
                        <div class="sig-bottom-group">
                            <div class="sig-date thai-numeral">พ.ย. 66</div>
                            <div class="sig-role">ผู้ตรวจนับ</div>
                        </div>
                    </div>
                </td>
                <td style="width: 33.33%;">
                    <div class="sig-cell-content">
                        <div class="sig-rank">{t_rank}</div>
                        <div class="sig-bottom-group">
                            <div class="sig-date thai-numeral">พ.ย. 66</div>
                            <div class="sig-role">หัวหน้าชุด</div>
                        </div>
                    </div>
                </td>
                <td style="width: 33.34%;">
                    <div class="sig-cell-content">
                        <div class="sig-rank">{a_rank}</div>
                        <div class="sig-bottom-group">
                            <div class="sig-date thai-numeral">พ.ย. 66</div>
                            <div class="sig-role">เจ้าหน้าที่บัญชีคุม</div>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </div>
    """
    return html

html_pages_str = ""
for p_idx, page_pair in enumerate(pages_items):
    top_item = page_pair[0]
    bot_item = page_pair[1]
    
    html_pages_str += f"""
    <!-- PAGE {p_idx+1} of {len(pages_items)} -->
    <div class="sheet-container" id="page-{p_idx+1}">
        <div class="form-doc-header">
            <span class="thai-numeral">ทบ. ๔๐๐ - ๐๑๑</span>
        </div>
        
        <!-- TOP CARD -->
        <div class="card-container top-card">
            {render_slip(top_item, 1, True)}
            {render_slip(top_item, 2, True)}
            {render_slip(top_item, 3, True)}
        </div>
        
        <div class="cut-line-h"></div>
        
        <!-- BOTTOM CARD -->
        <div class="card-container bottom-card">
            {render_slip(bot_item, 1, False)}
            {render_slip(bot_item, 2, False)}
            {render_slip(bot_item, 3, False)}
        </div>
    </div>
    """

html_full = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ใบสำรวจสิ่งอุปกรณ์ สาย สพ. (ทบ. ๔๐๐ - ๐๑๑) - SUPERCLONE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');
        
        @page {{
            size: 355.6mm 215.9mm; /* US Legal Landscape */
            margin: 0;
        }}
        
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            font-weight: normal !important;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            background-color: #525659;
            font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', sans-serif;
            font-size: 14pt;
            line-height: 1.15;
            color: #000;
        }}
        
        .thai-numeral {{
            font-variant-numeric: tabular-nums;
            font-feature-settings: "locl" 1, "numr" 1;
        }}
        
        .sheet-container {{
            width: 355.6mm;
            height: 215.9mm;
            background-color: #ffffff;
            margin: 15px auto;
            padding: 5mm 9mm 6mm 9mm;
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
            .sheet-container {{
                margin: 0;
                box-shadow: none;
                width: 355.6mm;
                height: 215.9mm;
            }}
        }}
        
        .form-doc-header {{
            text-align: right;
            font-size: 14pt;
            font-weight: normal;
            height: 6mm;
            padding-right: 2mm;
            margin-bottom: 1mm;
        }}
        
        .card-container {{
            display: flex;
            width: 100%;
            height: 96mm;
            justify-content: space-between;
        }}
        
        .survey-slip {{
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 0 4.5mm;
            position: relative;
        }}
        
        .survey-slip:not(:last-child) {{
            border-right: 1px dashed #777;
        }}
        
        .cut-line-h {{
            width: 100%;
            height: 1px;
            border-bottom: 1px dashed #777;
            margin: 2mm 0;
        }}
        
        .slip-header-row {{
            margin-bottom: 1mm;
        }}
        
        .slip-title {{
            font-size: 15pt;
            font-weight: normal;
            text-align: left;
        }}
        
        .item-nsn-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-height: 8mm;
            margin-bottom: 1mm;
        }}
        
        .nsn-label {{
            font-size: 13pt;
            line-height: 1.1;
            width: 45%;
        }}
        
        .nsn-val {{
            font-size: 14pt;
            font-weight: normal;
            width: 55%;
            text-align: center;
            letter-spacing: 0.5px;
        }}
        
        .item-name-row {{
            min-height: 7mm;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5mm;
        }}
        
        .item-name-val {{
            font-size: 14pt;
            font-weight: normal;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .meta-box-table {{
            border: 1px solid #000;
            margin-bottom: 2mm;
        }}
        
        .meta-box-table td {{
            border: 1px solid #000;
            padding: 1.5px 3px;
            vertical-align: top;
            text-align: center;
            height: 14mm;
        }}
        
        .meta-lbl {{
            font-size: 12.5pt;
            line-height: 1.1;
        }}
        
        .meta-val {{
            font-size: 13pt;
            font-weight: normal;
            line-height: 1.15;
        }}
        
        .meta-date {{
            display: inline-block;
            position: relative;
            left: 18px; /* เลื่อนไปทางขวา 4 เคาะ */
        }}
        
        .record-grid-table {{
            border: 1px solid #000;
            margin-bottom: 2mm;
        }}
        
        .record-grid-table th, .record-grid-table td {{
            border: 1px solid #000;
            text-align: center;
            padding: 1px 2px;
            font-weight: normal;
            font-size: 12.5pt;
            line-height: 1.1;
        }}
        
        .grid-title {{
            font-size: 13pt !important;
            padding: 2px !important;
        }}
        
        .data-row td {{
            height: 6mm;
        }}
        
        .sig-box-table {{
            border: 1px solid #000;
            height: 24mm;
        }}
        
        .sig-box-table td {{
            border: 1px solid #000;
            padding: 0;
            vertical-align: top;
        }}
        
        .sig-cell-content {{
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 3px 5px 3px 5px;
        }}
        
        .sig-rank {{
            font-size: 13.5pt;
            font-weight: normal;
            text-align: left;
            line-height: 1.1;
            padding-left: 2px;
        }}
        
        .sig-bottom-group {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            margin-bottom: 2px;
        }}
        
        .sig-date {{
            font-size: 13.5pt;
            line-height: 1.1;
            text-align: center;
            margin-left: 20px; /* เลื่อนไปทางขวา 4 เคาะตามที่อนุมัติ */
            margin-bottom: 8px; /* เลื่อนลงมาใกล้ตำแหน่ง */
        }}
        
        .sig-role {{
            font-size: 13pt;
            line-height: 1.1;
            text-align: center;
        }}
    </style>
</head>
<body>
    {html_pages_str}
</body>
</html>
"""

with open(html_out_path, "w", encoding="utf-8") as f:
    f.write(html_full)

print("Generated HTML successfully!")

# ==========================================
# 2. GENERATE EXCEL (XLSX)
# ==========================================
xlsx_out_path = r"d:\Project\WEPAPP\ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "ใบสำรวจสิ่งอุปกรณ์ สาย สพ"

# Enable gridlines
ws.views.sheetView[0].showGridLines = True

font_normal = Font(name="TH Sarabun PSK", size=14)
font_bold = Font(name="TH Sarabun PSK", size=14, bold=False)
font_title = Font(name="TH Sarabun PSK", size=15, bold=False)
font_header = Font(name="TH Sarabun PSK", size=14)

thin_border = Border(
    left=Side(style='thin', color='000000'),
    right=Side(style='thin', color='000000'),
    top=Side(style='thin', color='000000'),
    bottom=Side(style='thin', color='000000')
)

dash_right_border = Border(
    right=Side(style='dashed', color='777777')
)

# Number format with Thai locale preserving data integrity
TH_NUM_FMT = '[$-th-TH,26]#,##0'

# Layout: Each slip takes 6 columns. Card = 3 slips = 18 columns.
# Slip 1: Cols A-F (1-6)
# Slip 2: Cols G-L (7-12)
# Slip 3: Cols M-R (13-18)

# Set column widths
col_widths = [8, 8, 8, 8, 8, 8] * 3
for c_idx, w in enumerate(col_widths, start=1):
    ws.column_dimensions[get_column_letter(c_idx)].width = w

current_row = 1

for p_idx, pair in enumerate(pages_items):
    # Form header at top of page
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=18)
    h_cell = ws.cell(row=current_row, column=1, value="ทบ. ๔๐๐ - ๐๑๑")
    h_cell.font = font_normal
    h_cell.alignment = Alignment(horizontal="right")
    current_row += 1
    
    for card_idx, item in enumerate(pair):
        card_start_row = current_row
        
        for slip_num in [1, 2, 3]:
            col_offset = (slip_num - 1) * 6
            c_start = col_offset + 1
            c_end = col_offset + 6
            
            sig_key = f"slip_{slip_num}"
            sigs = sig_defaults[sig_key]
            
            # Row 1: ใบสำรวจสิ่งอุปกรณ์
            ws.cell(row=card_start_row, column=c_start, value="ใบสำรวจสิ่งอุปกรณ์").font = font_title
            
            # Row 2: หมายเลขสิ่งอุปกรณ์และรายการ + NSN
            ws.merge_cells(start_row=card_start_row+1, start_column=c_start, end_row=card_start_row+1, end_column=c_start+2)
            lbl_c = ws.cell(row=card_start_row+1, column=c_start, value="หมายเลขสิ่งอุปกรณ์และรายการ")
            lbl_c.font = font_normal
            lbl_c.alignment = Alignment(horizontal="left", vertical="center")
            
            ws.merge_cells(start_row=card_start_row+1, start_column=c_start+3, end_row=card_start_row+1, end_column=c_end)
            nsn_c = ws.cell(row=card_start_row+1, column=c_start+3, value=item["nsn"])
            nsn_c.font = font_bold
            nsn_c.alignment = Alignment(horizontal="center", vertical="center")
            
            # Row 3: ชื่อรายการ
            ws.merge_cells(start_row=card_start_row+2, start_column=c_start, end_row=card_start_row+2, end_column=c_end)
            name_c = ws.cell(row=card_start_row+2, column=c_start, value=item["item_name"])
            name_c.font = font_bold
            name_c.alignment = Alignment(horizontal="center", vertical="center")
            
            # Row 4-5: Meta Box (ที่เก็บ, ที่ใบสำรวจ, วันสำรวจ)
            ws.merge_cells(start_row=card_start_row+3, start_column=c_start, end_row=card_start_row+4, end_column=c_start+2)
            m1 = ws.cell(row=card_start_row+3, column=c_start, value="ที่เก็บ โรงเก็บปืนใหญ่\nป.4 พัน.4 ร้อย.2")
            m1.font = font_normal
            m1.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
            ws.merge_cells(start_row=card_start_row+3, start_column=c_start+3, end_row=card_start_row+4, end_column=c_start+4)
            m2 = ws.cell(row=card_start_row+3, column=c_start+3, value=f"ที่ใบสำรวจ\n{item['survey_no']}")
            m2.font = font_normal
            m2.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
            ws.merge_cells(start_row=card_start_row+3, start_column=c_start+5, end_row=card_start_row+4, end_column=c_end)
            m3 = ws.cell(row=card_start_row+3, column=c_start+5, value="วันสำรวจ\n    พ.ย. 66")
            m3.font = font_normal
            m3.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
            # Borders for meta box
            for r in range(card_start_row+3, card_start_row+5):
                for c in range(c_start, c_end+1):
                    ws.cell(row=r, column=c).border = thin_border
                    
            # Row 6: บันทึกการสำรวจ
            ws.merge_cells(start_row=card_start_row+5, start_column=c_start, end_row=card_start_row+5, end_column=c_end)
            t_title = ws.cell(row=card_start_row+5, column=c_start, value="บันทึกการสำรวจ")
            t_title.font = font_bold
            t_title.alignment = Alignment(horizontal="center", vertical="center")
            for c in range(c_start, c_end+1):
                ws.cell(row=card_start_row+5, column=c).border = thin_border
                
            # Row 7: จำนวน | ผลสรุปจำนวน | ผลสรุปราคา
            ws.merge_cells(start_row=card_start_row+6, start_column=c_start, end_row=card_start_row+6, end_column=c_start+1)
            ws.cell(row=card_start_row+6, column=c_start, value="จำนวน").alignment = Alignment(horizontal="center")
            
            ws.merge_cells(start_row=card_start_row+6, start_column=c_start+2, end_row=card_start_row+6, end_column=c_start+3)
            ws.cell(row=card_start_row+6, column=c_start+2, value="ผลสรุปจำนวน").alignment = Alignment(horizontal="center")
            
            ws.merge_cells(start_row=card_start_row+6, start_column=c_start+4, end_row=card_start_row+6, end_column=c_end)
            ws.cell(row=card_start_row+6, column=c_start+4, value="ผลสรุปราคา").alignment = Alignment(horizontal="center")
            for c in range(c_start, c_end+1):
                ws.cell(row=card_start_row+6, column=c).font = font_normal
                ws.cell(row=card_start_row+6, column=c).border = thin_border
                
            # Row 8: ตามบัญชี | ที่นับได้ | ขาด | เกิน | ขาด | เกิน
            sub_hdrs = ["ตามบัญชี", "ที่นับได้", "ขาด", "เกิน", "ขาด", "เกิน"]
            for i_sh, sh_val in enumerate(sub_hdrs):
                c_cell = ws.cell(row=card_start_row+7, column=c_start+i_sh, value=sh_val)
                c_cell.font = font_normal
                c_cell.alignment = Alignment(horizontal="center")
                c_cell.border = thin_border
                
            # Row 9: Data Row
            for i_sh in range(6):
                c_cell = ws.cell(row=card_start_row+8, column=c_start+i_sh, value="")
                c_cell.border = thin_border
                c_cell.number_format = TH_NUM_FMT
                
            # Row 10-12: Signatures box
            sig_officers = [
                (sigs['checker']['rank'], "ผู้ตรวจนับ"),
                (sigs['team_lead']['rank'], "หัวหน้าชุด"),
                (sigs['account_officer']['rank'], "เจ้าหน้าที่บัญชีคุม")
            ]
            for s_idx, (r_rank, r_role) in enumerate(sig_officers):
                c_sub_start = c_start + (s_idx * 2)
                c_sub_end = c_sub_start + 1
                
                # Row 10: Rank (aligned left)
                ws.merge_cells(start_row=card_start_row+9, start_column=c_sub_start, end_row=card_start_row+9, end_column=c_sub_end)
                rk_c = ws.cell(row=card_start_row+9, column=c_sub_start, value=f" {r_rank}")
                rk_c.font = font_normal
                rk_c.alignment = Alignment(horizontal="left", vertical="top")
                
                # Row 11: Date (aligned center, shifted)
                ws.merge_cells(start_row=card_start_row+10, start_column=c_sub_start, end_row=card_start_row+10, end_column=c_sub_end)
                dt_c = ws.cell(row=card_start_row+10, column=c_sub_start, value="    พ.ย. 66")
                dt_c.font = font_normal
                dt_c.alignment = Alignment(horizontal="center", vertical="bottom")
                
                # Row 12: Role (aligned center)
                ws.merge_cells(start_row=card_start_row+11, start_column=c_sub_start, end_row=card_start_row+11, end_column=c_sub_end)
                ro_c = ws.cell(row=card_start_row+11, column=c_sub_start, value=r_role)
                ro_c.font = font_normal
                ro_c.alignment = Alignment(horizontal="center", vertical="bottom")
                
            for r in range(card_start_row+9, card_start_row+12):
                for c in range(c_start, c_end+1):
                    ws.cell(row=r, column=c).border = thin_border

        current_row += 13
    
    # Page separator in Excel
    current_row += 2

wb.save(xlsx_out_path)
print("Generated XLSX successfully!")

# ==========================================
# 3. GENERATE WORD (DOCX)
# ==========================================
docx_out_path = r"d:\Project\WEPAPP\ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.docx"
doc = Document()

# Set US Legal Landscape
section = doc.sections[0]
section.page_width = Inches(14.0)
section.page_height = Inches(8.5)
section.top_margin = Inches(0.2)
section.bottom_margin = Inches(0.2)
section.left_margin = Inches(0.35)
section.right_margin = Inches(0.35)

def format_cell(cell, font_size=11, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
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
    """
    kwargs: top, bottom, left, right
    values: {"val": "single", "sz": "4", "color": "000000"}
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), edge_data.get('sz', '4'))
            element.set(qn('w:color'), edge_data.get('color', '000000'))
            tcBorders.append(element)
    tcPr.append(tcBorders)

for p_idx, pair in enumerate(pages_items):
    # Form Code at top right
    p_hdr = doc.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(2)
    r_hdr = p_hdr.add_run("ทบ. ๔๐๐ - ๐๑๑")
    r_hdr.font.name = "TH Sarabun PSK"
    r_hdr.font.size = Pt(13)
    
    for card_idx, item in enumerate(pair):
        # 3 slips side-by-side using a master 1-row, 3-column table
        master_tbl = doc.add_table(rows=1, cols=3)
        master_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        master_tbl.autofit = False
        
        # Total printable width is 13.3 inches -> 4.43 inches per slip
        slip_w = Inches(4.43)
        for c in master_tbl.columns:
            c.width = slip_w
            
        row_cells = master_tbl.rows[0].cells
        
        for slip_num in [1, 2, 3]:
            s_cell = row_cells[slip_num - 1]
            s_cell.width = slip_w
            
            sig_key = f"slip_{slip_num}"
            sigs = sig_defaults[sig_key]
            
            # Add dashed border on right for slip 1 and 2
            if slip_num < 3:
                set_cell_border(s_cell, right={"val": "dashed", "sz": "6", "color": "777777"})
                
            p_st = s_cell.paragraphs[0]
            p_st.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_st.paragraph_format.space_before = Pt(0)
            p_st.paragraph_format.space_after = Pt(1)
            r_st = p_st.add_run("ใบสำรวจสิ่งอุปกรณ์")
            r_st.font.name = "TH Sarabun PSK"
            r_st.font.size = Pt(13)
            r_st.bold = False
            
            # NSN row
            p_nsn = s_cell.add_paragraph()
            p_nsn.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_nsn.paragraph_format.space_before = Pt(0)
            p_nsn.paragraph_format.space_after = Pt(1)
            r_nl = p_nsn.add_run("หมายเลขสิ่งอุปกรณ์และรายการ     ")
            r_nl.font.name = "TH Sarabun PSK"
            r_nl.font.size = Pt(11)
            r_nv = p_nsn.add_run(item["nsn"])
            r_nv.font.name = "TH Sarabun PSK"
            r_nv.font.size = Pt(12)
            r_nv.bold = False
            
            # Name row
            p_nm = s_cell.add_paragraph()
            p_nm.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_nm.paragraph_format.space_before = Pt(0)
            p_nm.paragraph_format.space_after = Pt(2)
            r_nm = p_nm.add_run(item["item_name"])
            r_nm.font.name = "TH Sarabun PSK"
            r_nm.font.size = Pt(12)
            r_nm.bold = False
            
            # Meta table (3 cols)
            meta_tbl = s_cell.add_table(rows=1, cols=3)
            meta_tbl.autofit = False
            m_cells = meta_tbl.rows[0].cells
            m_cells[0].width = Inches(1.9)
            m_cells[1].width = Inches(1.25)
            m_cells[2].width = Inches(1.28)
            
            p_m0 = m_cells[0].paragraphs[0]
            p_m0.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_m0.add_run("ที่เก็บ โรงเก็บปืนใหญ่\nป.4 พัน.4 ร้อย.2").font.name = "TH Sarabun PSK"
            
            p_m1 = m_cells[1].paragraphs[0]
            p_m1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_m1.add_run(f"ที่ใบสำรวจ\n{item['survey_no']}").font.name = "TH Sarabun PSK"
            
            p_m2 = m_cells[2].paragraphs[0]
            p_m2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_m2.add_run("วันสำรวจ\n    พ.ย. 66").font.name = "TH Sarabun PSK"
            
            for mc in m_cells:
                format_cell(mc, font_size=10.5)
                set_cell_border(mc, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
                
            # Record table (6 cols)
            rec_tbl = s_cell.add_table(rows=4, cols=6)
            rec_tbl.autofit = False
            rec_w = Inches(4.43 / 6)
            for rc_col in rec_tbl.columns:
                rc_col.width = rec_w
                
            # Row 0: บันทึกการสำรวจ (merge 6)
            r0_cells = rec_tbl.rows[0].cells
            r0_merged = r0_cells[0].merge(r0_cells[5])
            p_r0 = r0_merged.paragraphs[0]
            p_r0.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_r0 = p_r0.add_run("บันทึกการสำรวจ")
            r_r0.font.name = "TH Sarabun PSK"
            r_r0.font.size = Pt(11)
            r_r0.bold = False
            
            # Row 1: จำนวน (2) | ผลสรุปจำนวน (2) | ผลสรุปราคา (2)
            r1_cells = rec_tbl.rows[1].cells
            r1_m0 = r1_cells[0].merge(r1_cells[1])
            r1_m0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            r1_m0.paragraphs[0].add_run("จำนวน").font.name = "TH Sarabun PSK"
            
            r1_m1 = r1_cells[2].merge(r1_cells[3])
            r1_m1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            r1_m1.paragraphs[0].add_run("ผลสรุปจำนวน").font.name = "TH Sarabun PSK"
            
            r1_m2 = r1_cells[4].merge(r1_cells[5])
            r1_m2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            r1_m2.paragraphs[0].add_run("ผลสรุปราคา").font.name = "TH Sarabun PSK"
            
            # Row 2: ตามบัญชี | ที่นับได้ | ขาด | เกิน | ขาด | เกิน
            sub_h = ["ตามบัญชี", "ที่นับได้", "ขาด", "เกิน", "ขาด", "เกิน"]
            r2_cells = rec_tbl.rows[2].cells
            for i_sh, sh_t in enumerate(sub_h):
                r2_cells[i_sh].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                r2_cells[i_sh].paragraphs[0].add_run(sh_t).font.name = "TH Sarabun PSK"
                
            # Format rec table borders & font
            for row in rec_tbl.rows:
                for rc in row.cells:
                    format_cell(rc, font_size=10)
                    set_cell_border(rc, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
                    
            # Row 3 (Data row) height
            rec_tbl.rows[3].height = Pt(14)
            
            # Signatures table (3 cols)
            sig_tbl = s_cell.add_table(rows=1, cols=3)
            sig_tbl.autofit = False
            sig_w = Inches(4.43 / 3)
            for sc_col in sig_tbl.columns:
                sc_col.width = sig_w
                
            sig_officers = [
                (sigs['checker']['rank'], "ผู้ตรวจนับ"),
                (sigs['team_lead']['rank'], "หัวหน้าชุด"),
                (sigs['account_officer']['rank'], "เจ้าหน้าที่บัญชีคุม")
            ]
            for s_idx, (r_rank, r_role) in enumerate(sig_officers):
                sc = sig_tbl.rows[0].cells[s_idx]
                p0 = sc.paragraphs[0]
                p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p0.paragraph_format.space_before = Pt(0)
                p0.paragraph_format.space_after = Pt(2)
                r0 = p0.add_run(f" {r_rank}")
                r0.font.name = "TH Sarabun PSK"
                r0.font.size = Pt(11)
                
                p1 = sc.add_paragraph()
                p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p1.paragraph_format.space_before = Pt(0)
                p1.paragraph_format.space_after = Pt(5)
                # 4 spaces shift
                r1 = p1.add_run("        พ.ย. 66")
                r1.font.name = "TH Sarabun PSK"
                r1.font.size = Pt(11)
                
                p2 = sc.add_paragraph()
                p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p2.paragraph_format.space_before = Pt(0)
                p2.paragraph_format.space_after = Pt(2)
                r2 = p2.add_run(r_role)
                r2.font.name = "TH Sarabun PSK"
                r2.font.size = Pt(11)
                
                set_cell_border(sc, top={"val": "single"}, bottom={"val": "single"}, left={"val": "single"}, right={"val": "single"})
                
        if card_idx == 0:
            # Spacer between top and bottom cards
            p_space = doc.add_paragraph()
            p_space.paragraph_format.space_before = Pt(3)
            p_space.paragraph_format.space_after = Pt(3)
            # Add dashed line representation
            r_sp = p_space.add_run("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            r_sp.font.color.rgb = RGBColor(128, 128, 128)
            r_sp.font.size = Pt(8)
            
    # Page break after each page except last
    if p_idx < len(pages_items) - 1:
        doc.add_page_break()

doc.save(docx_out_path)
print("Generated DOCX successfully!")
