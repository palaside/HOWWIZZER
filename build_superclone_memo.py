import os
import json
import base64
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

# Load SSOT Blueprint
blueprint_path = r"d:\Project\WEPAPP\table_layout_memo.json"
with open(blueprint_path, "r", encoding="utf-8") as f:
    bp = json.load(f)

# Encode Garuda image to base64 for standalone HTML rendering
garuda_path = r"d:\Project\WEPAPP\garuda_memo.png"
with open(garuda_path, "rb") as f:
    garuda_b64 = base64.b64encode(f.read()).decode("utf-8")

# ==========================================
# 1. GENERATE HTML (Pixel-Perfect A4 Portrait)
# ==========================================
html_out_path = r"d:\Project\WEPAPP\บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html"

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp['document_title']} - SUPERCLONE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');

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
            font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', sans-serif;
            font-size: 16pt;
            line-height: 1.25;
            color: #000;
        }}

        .thai-numeral {{
            font-variant-numeric: tabular-nums;
            font-feature-settings: "locl" 1, "numr" 1;
        }}

        .page-sheet {{
            width: 210mm;
            min-height: 297mm;
            height: 297mm;
            background: #ffffff;
            margin: 20px auto;
            padding: 25mm 20mm 20mm 30mm; /* บน 2.5 ซม, ขวา 2 ซม, ล่าง 2 ซม, ซ้าย 3 ซม */
            position: relative;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}

        @media print {{
            body {{
                background-color: transparent;
            }}
            .page-sheet {{
                margin: 0;
                box-shadow: none;
                width: 210mm;
                height: 297mm;
                page-break-after: avoid;
            }}
        }}

        /* HEADER SECTION */
        .header-container {{
            position: relative;
            width: 100%;
            height: 25mm;
            margin-bottom: 2mm;
        }}

        .garuda-img {{
            position: absolute;
            left: 0;
            top: 0;
            height: 15mm;
            width: auto;
        }}

        .doc-title {{
            font-size: 29pt;
            font-weight: bold;
            text-align: center;
            line-height: 1.1;
            padding-top: 3mm;
            letter-spacing: 0.5px;
        }}

        /* METADATA ROWS */
        .meta-section {{
            width: 100%;
            margin-bottom: 4mm;
        }}

        .meta-row {{
            display: flex;
            align-items: flex-end;
            margin-bottom: 3.5mm;
            font-size: 16pt;
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
            font-size: 16pt;
            line-height: 1.1;
        }}

        .meta-half-col {{
            flex: 1;
            display: flex;
            align-items: flex-end;
        }}

        /* RECIPIENT & ATTACHMENTS */
        .salutation-row {{
            margin-top: 3mm;
            margin-bottom: 3.5mm;
            font-size: 16pt;
        }}

        .attachment-row {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4mm;
            font-size: 16pt;
        }}

        .attachment-item {{
            flex: 1;
        }}

        .attachment-qty {{
            white-space: nowrap;
            margin-left: 10mm;
        }}

        /* CONTENT PARAGRAPHS */
        .content-para {{
            text-indent: 25mm; /* กั้นหน้าย่อหน้า 2.5 ซม. */
            text-align: justify;
            text-justify: inter-cluster;
            line-height: 1.35;
            margin-bottom: 3.5mm;
            font-size: 16pt;
        }}

        /* UNIVERSAL SIGNATURE BLOCK (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .signature-container {{
            width: 100%;
            margin-top: 18mm;
            display: flex;
            justify-content: flex-end;
        }}

        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 16pt;
            line-height: 1.15;
            min-width: 75mm;
        }}

        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center; /* ชื่อและตำแหน่งจัดกึ่งกลางร่วมกัน */
            position: relative;
            margin-left: 12mm;
        }}

        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 14mm; /* พื้นที่ว่างสำหรับลงลายมือชื่อจริง 2 Enter */
        }}

        /* Red Line Anchor: จุด . ท้ายสุดของยศ ตรงกับแนวเส้นดิ่งวงเล็บเปิด ( พอดีเป๊ะ 100% */
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 3.5mm); /* ลดลงมา 1 เอนเตอร์ */
            white-space: nowrap;
            font-size: 16pt;
            line-height: 1.0;
        }}

        .sig-name {{
            font-size: 16pt;
            line-height: 1.15;
            white-space: nowrap;
        }}

        .sig-pos {{
            font-size: 16pt;
            line-height: 1.15;
            white-space: nowrap;
            margin-top: 0; /* 1 Enter, Space After 0 pt */
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="page-sheet" id="memo-page-1">
        <!-- HEADER -->
        <div class="header-container">
            <img src="data:image/png;base64,{garuda_b64}" alt="Garuda" class="garuda-img">
            <div class="doc-title">{bp['header']['title']}</div>
        </div>

        <!-- METADATA ROWS -->
        <div class="meta-section">
            <!-- Row 1: ส่วนราชการ -->
            <div class="meta-row">
                <span class="meta-label">ส่วนราชการ</span>
                <div class="meta-fill-dotted">{bp['metadata_fields'][0]['value']}</div>
            </div>

            <!-- Row 2: ที่ & วันที่ -->
            <div class="meta-row">
                <div class="meta-half-col" style="margin-right: 4mm;">
                    <span class="meta-label">ที่</span>
                    <div class="meta-fill-dotted">{bp['metadata_fields'][1]['row'][0]['value']}</div>
                </div>
                <div class="meta-half-col">
                    <span class="meta-label">วันที่</span>
                    <div class="meta-fill-dotted" style="padding-left: 20mm;">{bp['metadata_fields'][1]['row'][1]['value']}</div>
                </div>
            </div>

            <!-- Row 3: เรื่อง -->
            <div class="meta-row">
                <span class="meta-label">เรื่อง</span>
                <div class="meta-fill-dotted">{bp['metadata_fields'][2]['value']}</div>
            </div>
        </div>

        <!-- SALUTATION -->
        <div class="salutation-row">{bp['salutation']}</div>

        <!-- ATTACHMENTS -->
        <div class="attachment-row">
            <div class="attachment-item">สิ่งที่ส่งมาด้วย  {bp['attachments'][0]['item']}</div>
            <div class="attachment-qty">จำนวน  {bp['attachments'][0]['quantity']}</div>
        </div>

        <!-- BODY PARAGRAPHS -->
        <div class="content-para">{bp['content_paragraphs'][0]}</div>
        <div class="content-para">{bp['content_paragraphs'][1]}</div>

        <!-- UNIVERSAL SIGNATURE BLOCK -->
        <div class="signature-container">
            <div class="sig-block">
                <div class="sig-name-pos-group">
                    <div class="sig-name-wrapper">
                        <span class="sig-rank-anchor">{bp['signature_block']['rank']}</span>
                        <div class="sig-name">{bp['signature_block']['name']}</div>
                    </div>
                    <div class="sig-pos">{bp['signature_block']['position']}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

with open(html_out_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Generated HTML successfully!")

# ==========================================
# 2. GENERATE WORD (DOCX)
# ==========================================
docx_out_path = r"d:\Project\WEPAPP\บันทึกข้อความล่าสุดสุด_Rebuild_Thai.docx"
doc = Document()

# Page Setup: A4 Portrait
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.98)    # 25mm
section.bottom_margin = Inches(0.79) # 20mm
section.left_margin = Inches(1.18)   # 30mm
section.right_margin = Inches(0.79)  # 20mm

def format_run(run, font_name="TH Sarabun PSK", size_pt=16, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold

# Header: Garuda on left, Title "บันทึกข้อความ" center
hdr_tbl = doc.add_table(rows=1, cols=2)
hdr_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_tbl.autofit = False
hdr_tbl.columns[0].width = Inches(1.5)
hdr_tbl.columns[1].width = Inches(4.8)

# Add Garuda to col 0
p_garuda = hdr_tbl.rows[0].cells[0].paragraphs[0]
p_garuda.paragraph_format.space_before = Pt(0)
p_garuda.paragraph_format.space_after = Pt(0)
p_garuda.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_garuda.add_run().add_picture(garuda_path, height=Inches(0.59)) # 1.5 cm

# Add Title to col 1
p_title = hdr_tbl.rows[0].cells[1].paragraphs[0]
p_title.paragraph_format.space_before = Pt(6)
p_title.paragraph_format.space_after = Pt(0)
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = p_title.add_run(bp['header']['title'])
format_run(r_title, size_pt=29, bold=True)

# Spacing after header
p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(4)
p_space.paragraph_format.space_after = Pt(2)

# Row 1: ส่วนราชการ
p_dept = doc.add_paragraph()
p_dept.paragraph_format.space_before = Pt(0)
p_dept.paragraph_format.space_after = Pt(2)
r_dept_lbl = p_dept.add_run("ส่วนราชการ  ")
format_run(r_dept_lbl, size_pt=20, bold=True)
r_dept_val = p_dept.add_run(bp['metadata_fields'][0]['value'])
format_run(r_dept_val, size_pt=16, bold=False)

# Row 2: ที่ & วันที่
p_ref = doc.add_paragraph()
p_ref.paragraph_format.space_before = Pt(0)
p_ref.paragraph_format.space_after = Pt(2)
# Add tab stops for วันที่
p_ref.paragraph_format.tab_stops.add_tab_stop(Inches(3.2), WD_TAB_ALIGNMENT.LEFT)
r_ref_lbl = p_ref.add_run("ที่  ")
format_run(r_ref_lbl, size_pt=20, bold=True)
r_ref_val = p_ref.add_run(bp['metadata_fields'][1]['row'][0]['value'] + "\t")
format_run(r_ref_val, size_pt=16, bold=False)
r_date_lbl = p_ref.add_run("วันที่  ")
format_run(r_date_lbl, size_pt=20, bold=True)
r_date_val = p_ref.add_run("          " + bp['metadata_fields'][1]['row'][1]['value'])
format_run(r_date_val, size_pt=16, bold=False)

# Row 3: เรื่อง
p_subj = doc.add_paragraph()
p_subj.paragraph_format.space_before = Pt(0)
p_subj.paragraph_format.space_after = Pt(6)
r_subj_lbl = p_subj.add_run("เรื่อง  ")
format_run(r_subj_lbl, size_pt=20, bold=True)
r_subj_val = p_subj.add_run(bp['metadata_fields'][2]['value'])
format_run(r_subj_val, size_pt=16, bold=False)

# Salutation
p_sal = doc.add_paragraph()
p_sal.paragraph_format.space_before = Pt(4)
p_sal.paragraph_format.space_after = Pt(4)
r_sal = p_sal.add_run(bp['salutation'])
format_run(r_sal, size_pt=16, bold=False)

# Attachments
p_att = doc.add_paragraph()
p_att.paragraph_format.space_before = Pt(0)
p_att.paragraph_format.space_after = Pt(6)
p_att.paragraph_format.tab_stops.add_tab_stop(Inches(5.0), WD_TAB_ALIGNMENT.LEFT)
r_att_lbl = p_att.add_run("สิ่งที่ส่งมาด้วย  ")
format_run(r_att_lbl, size_pt=16, bold=False)
r_att_item = p_att.add_run(bp['attachments'][0]['item'] + "\t")
format_run(r_att_item, size_pt=16, bold=False)
r_att_qty = p_att.add_run("จำนวน  " + bp['attachments'][0]['quantity'])
format_run(r_att_qty, size_pt=16, bold=False)

# Body Paragraph 1
p_b1 = doc.add_paragraph()
p_b1.paragraph_format.space_before = Pt(4)
p_b1.paragraph_format.space_after = Pt(4)
p_b1.paragraph_format.first_line_indent = Inches(1.0) # 2.5 cm
p_b1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r_b1 = p_b1.add_run(bp['content_paragraphs'][0])
format_run(r_b1, size_pt=16, bold=False)

# Body Paragraph 2
p_b2 = doc.add_paragraph()
p_b2.paragraph_format.space_before = Pt(4)
p_b2.paragraph_format.space_after = Pt(16)
p_b2.paragraph_format.first_line_indent = Inches(1.0)
r_b2 = p_b2.add_run(bp['content_paragraphs'][1])
format_run(r_b2, size_pt=16, bold=False)

# Signature Block (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1)
sig_tbl = doc.add_table(rows=3, cols=2)
sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
sig_tbl.autofit = False
sig_tbl.columns[0].width = Inches(3.2)
sig_tbl.columns[1].width = Inches(3.1)

# Row 0: Rank (aligned left in right column)
p_s0 = sig_tbl.rows[0].cells[1].paragraphs[0]
p_s0.paragraph_format.space_before = Pt(36) # ลดบรรทัดลงมา 1 เอนเตอร์
p_s0.paragraph_format.space_after = Pt(4)
p_s0.alignment = WD_ALIGN_PARAGRAPH.LEFT
r_s0 = p_s0.add_run(bp['signature_block']['rank'])
format_run(r_s0, size_pt=16, bold=False)

# Row 1: Name (centered in right column)
p_s1 = sig_tbl.rows[1].cells[1].paragraphs[0]
p_s1.paragraph_format.space_before = Pt(0)
p_s1.paragraph_format.space_after = Pt(0)
p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_s1 = p_s1.add_run(bp['signature_block']['name'])
format_run(r_s1, size_pt=16, bold=False)

# Row 2: Position (centered in right column)
p_s2 = sig_tbl.rows[2].cells[1].paragraphs[0]
p_s2.paragraph_format.space_before = Pt(0)
p_s2.paragraph_format.space_after = Pt(0)
p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_s2 = p_s2.add_run(bp['signature_block']['position'])
format_run(r_s2, size_pt=16, bold=False)

doc.save(docx_out_path)
print("Generated DOCX successfully!")

# ==========================================
# 3. GENERATE EXCEL (XLSX)
# ==========================================
xlsx_out_path = r"d:\Project\WEPAPP\บันทึกข้อความล่าสุดสุด_Rebuild_Thai.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "บันทึกข้อความ"

# Page setup for printing A4 Portrait
ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.views.sheetView[0].showGridLines = True

font_title = Font(name="TH Sarabun PSK", size=24, bold=True)
font_label = Font(name="TH Sarabun PSK", size=16, bold=True)
font_normal = Font(name="TH Sarabun PSK", size=16, bold=False)

# Set 10 columns
for c in range(1, 11):
    ws.column_dimensions[get_column_letter(c)].width = 9

# Row 2: Garuda indicator & Title
ws.merge_cells("A2:B4")
ws["A2"] = "[ตราครุฑ]"
ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws["A2"].font = Font(name="TH Sarabun PSK", size=14, italic=True)

ws.merge_cells("C2:I3")
ws["C2"] = bp['header']['title']
ws["C2"].font = font_title
ws["C2"].alignment = Alignment(horizontal="center", vertical="center")

# Row 5: ส่วนราชการ
ws["A5"] = "ส่วนราชการ"
ws["A5"].font = font_label
ws.merge_cells("B5:J5")
ws["B5"] = bp['metadata_fields'][0]['value']
ws["B5"].font = font_normal

# Row 6: ที่ & วันที่
ws["A6"] = "ที่"
ws["A6"].font = font_label
ws.merge_cells("B6:E6")
ws["B6"] = bp['metadata_fields'][1]['row'][0]['value']
ws["B6"].font = font_normal

ws["F6"] = "วันที่"
ws["F6"].font = font_label
ws.merge_cells("G6:J6")
ws["G6"] = "          " + bp['metadata_fields'][1]['row'][1]['value']
ws["G6"].font = font_normal

# Row 7: เรื่อง
ws["A7"] = "เรื่อง"
ws["A7"].font = font_label
ws.merge_cells("B7:J7")
ws["B7"] = bp['metadata_fields'][2]['value']
ws["B7"].font = font_normal

# Row 9: Salutation
ws.merge_cells("A9:J9")
ws["A9"] = bp['salutation']
ws["A9"].font = font_normal

# Row 11: Attachments
ws.merge_cells("A11:G11")
ws["A11"] = "สิ่งที่ส่งมาด้วย  " + bp['attachments'][0]['item']
ws["A11"].font = font_normal

ws.merge_cells("H11:J11")
ws["H11"] = "จำนวน  " + bp['attachments'][0]['quantity']
ws["H11"].font = font_normal
ws["H11"].alignment = Alignment(horizontal="right")

# Row 13-14: Paragraph 1
ws.merge_cells("A13:J14")
ws["A13"] = "          " + bp['content_paragraphs'][0]
ws["A13"].font = font_normal
ws["A13"].alignment = Alignment(wrap_text=True, vertical="top")

# Row 16: Paragraph 2
ws.merge_cells("A16:J16")
ws["A16"] = "          " + bp['content_paragraphs'][1]
ws["A16"].font = font_normal

# Row 20: Rank (ลดลงมา 1 เอนเตอร์ จากแถว 19 มาเป็นแถว 20)
ws.merge_cells("F20:J20")
ws["F20"] = "     " + bp['signature_block']['rank']
ws["F20"].font = font_normal

# Row 22: Name
ws.merge_cells("F22:J22")
ws["F22"] = bp['signature_block']['name']
ws["F22"].font = font_normal
ws["F22"].alignment = Alignment(horizontal="center")

# Row 23: Position
ws.merge_cells("F23:J23")
ws["F23"] = bp['signature_block']['position']
ws["F23"].font = font_normal
ws["F23"].alignment = Alignment(horizontal="center")

wb.save(xlsx_out_path)
print("Generated XLSX successfully!")
