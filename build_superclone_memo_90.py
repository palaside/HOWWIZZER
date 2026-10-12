import os
import sys
import json
import base64

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# -----------------------------------------------------------------------------
# PATH DEFINITIONS
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_PATH = os.path.join(BASE_DIR, "table_layout_memo_90.json")
GARUDA_PATH = os.path.join(BASE_DIR, "garuda_vector_official.png")

with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    bp = json.load(f)

with open(GARUDA_PATH, "rb") as f:
    GARUDA_B64 = base64.b64encode(f.read()).decode("utf-8")

# -----------------------------------------------------------------------------
# 1. GENERATE HTML (Pixel-Perfect A4 Portrait with Governance Standards)
# -----------------------------------------------------------------------------
def generate_html(output_path):
    c = bp["content"]
    sig = c["signature"]
    
    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp["document_title"]}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
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
            padding: 20px 0;
            background-color: #525659;
            font-family: 'Sarabun', 'TH Sarabun PSK', 'THSarabunNew', sans-serif;
            font-size: 12pt;
            font-weight: 300; /* Light / Thin standard */
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
            color: #000000;
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .page-portrait {{
            width: 210mm;
            height: 297mm;
            background-color: #ffffff;
            margin-bottom: 20mm;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
            position: relative;
            padding: 20mm 15mm 15mm 25mm; /* Top 2cm, Right 1.5cm, Bottom 1.5cm, Left 2.5cm */
            overflow: hidden;
        }}
        @media print {{
            body {{
                background-color: #ffffff;
                padding: 0;
            }}
            .page-portrait {{
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

        /* MEMO HEADER */
        .memo-copy-label {{
            position: absolute;
            top: 7mm;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 12pt;
            line-height: 1.5;
        }}
        .memo-header-container {{
            position: relative;
            width: 100%;
            height: 30mm;
            margin-top: -2mm;
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
        .memo-meta-label {{
            font-size: 14pt;
            font-weight: bold;
            white-space: nowrap;
        }}
        .memo-meta-dots {{
            border-bottom: 1px dotted #000;
            padding-left: 2mm;
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

        /* UNIVERSAL SIGNATURE BLOCK (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            position: relative;
            min-width: 220px;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            margin-left: 0;
        }}
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 18pt; /* สำหรับลงลายมือชื่อจริง */
        }}
        .sig-rank-anchor {{
            position: absolute;
            right: 100%; /* จุด . ท้ายยศ แตะแนวเส้นดิ่งเดียวกับ ( พอดีเป๊ะ 100% */
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

        /* ROUTING FOOTER */
        .memo-footer-routing {{
            position: absolute;
            bottom: 20mm;
            right: 20mm;
            font-size: 12pt;
            line-height: 1.5;
        }}
    </style>
</head>
<body>

    <div class="page-portrait" id="page-1">
        <div class="memo-header-container">
            <img class="memo-garuda" src="data:image/png;base64,{GARUDA_B64}" alt="ครุฑ">
            <div class="memo-title">{c["title"]}</div>
        </div>

        <div style="margin-top: 2mm; font-size: 12pt; line-height: 1.5;">
            <!-- ส่วนราชการ -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <span class="memo-meta-label" style="margin-right: 2mm;">{c["official_department"]}</span>
                <div class="memo-meta-dots" style="flex: 1;">{c["department_value"]}</div>
            </div>
            <!-- ที่ และ วันที่ -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <div style="display: flex; align-items: baseline; flex: 1.2; margin-right: 6mm;">
                    <span class="memo-meta-label" style="margin-right: 2mm;">{c["doc_number_label"]}</span>
                    <div class="memo-meta-dots" style="flex: 1;">{c["doc_number_value"]}</div>
                </div>
                <div style="display: flex; align-items: baseline; flex: 1;">
                    <span class="memo-meta-label" style="margin-right: 2mm;">{c["doc_date_label"]}</span>
                    <div class="memo-meta-dots" style="flex: 1;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{c["doc_date_month_year"]}</div>
                </div>
            </div>
            <!-- เรื่อง (บรรทัดเดียว ไม่มีเส้นไข่ปลา) -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <span class="memo-meta-label" style="margin-right: 2mm;">{c["subject_label"]}</span>
                <div style="flex: 1; padding-left: 2mm;">{c["subject_value"]}</div>
            </div>
        </div>

        <div class="memo-content">
            <div style="margin-bottom: 2mm;">
                <span class="font-bold">{c["recipient_label"]}</span>&nbsp;&nbsp;{c["recipient_value"]}
            </div>
            <div style="margin-bottom: 2mm;">
                <span class="font-bold">{c["reference_label"]}</span>&nbsp;&nbsp;{c["reference_value"]}
            </div>

            <div style="margin: 0 0 2.5mm 0; font-size: 12pt; line-height: 1.5;">
                <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
                    <tr>
                        <td style="width: 28mm; vertical-align: top; white-space: nowrap;"><span class="font-bold">{c["attachments_label"]}</span></td>
                        <td style="vertical-align: top;">{c["attachments"][0]["title"]}</td>
                        <td style="width: 28mm; vertical-align: top; text-align: right; white-space: nowrap;">{c["attachments"][0]["quantity"]}</td>
                    </tr>
                </table>
            </div>

            <p class="memo-p">{c["paragraphs"][0]}</p>
            <p class="memo-p">{c["paragraphs"][1]}</p>
        </div>

        <!-- SIGNATURE BLOCK (RULE: เคาะ 5 Enter จากบรรทัดสุดท้าย, พิกัดซ้าย 130 มม. - Margin ซ้าย 25 มม. = padding-left 105 มม.) -->
        <div style="margin-top: 55pt; padding-left: 105mm;">
            <div class="sig-block" style="margin-right: 0;">
                <div class="sig-name-pos-group">
                    <div class="sig-name-wrapper">
                        <span class="sig-rank-anchor">{sig["rank"]}</span>
                        <div class="sig-name">({sig["name"]})</div>
                    </div>
                    <div class="sig-pos">{sig["position"]}</div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML: {output_path}")


# -----------------------------------------------------------------------------
# 2. GENERATE DOCX
# -----------------------------------------------------------------------------
def set_cell_margins(cell, top=100, bottom=100, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            b = OxmlElement(f'w:{edge}')
            b.set(qn('w:val'), edge_data.get('val', 'single'))
            b.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), edge_data.get('color', '000000'))
            tcBorders.append(b)
        else:
            b = OxmlElement(f'w:{edge}')
            b.set(qn('w:val'), 'none')
            tcBorders.append(b)
    tcPr.append(tcBorders)

def set_run_font(run, font_name="TH Sarabun PSK", size_pt=12, bold=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rPr.append(rFonts)

def generate_docx(output_path):
    c = bp["content"]
    sig = c["signature"]
    doc = Document()

    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(0.98)    # 2.5 cm
    sec.bottom_margin = Inches(0.79) # 2.0 cm
    sec.left_margin = Inches(0.98)   # 2.5 cm
    sec.right_margin = Inches(0.79)  # 2.0 cm

    # Copy label
    p_copy = doc.add_paragraph()
    p_copy.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_copy = p_copy.add_run(c["copy_type"])
    set_run_font(r_copy, "TH Sarabun PSK", 12)

    # Header with Garuda
    tbl_head = doc.add_table(rows=1, cols=2)
    tbl_head.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_head.autofit = False
    c_img = tbl_head.cell(0, 0)
    c_img.width = Inches(1.5)
    p_img = c_img.paragraphs[0]
    p_img.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists(GARUDA_PATH):
        p_img.add_run().add_picture(GARUDA_PATH, width=Inches(1.2))

    c_title = tbl_head.cell(0, 1)
    c_title.width = Inches(5.0)
    p_title = c_title.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    r_title = p_title.add_run(c["title"])
    set_run_font(r_title, "TH Sarabun PSK", 24, bold=True)

    set_cell_border(c_img)
    set_cell_border(c_title)

    # Meta Lines
    meta_lines = [
        (c["official_department"], c["department_value"]),
        (f'{c["doc_number_label"]}  {c["doc_number_value"]}', f'{c["doc_date_label"]}            {c["doc_date_month_year"]}'),
        (c["subject_label"], c["subject_value"]),
        (c["recipient_label"], c["recipient_value"]),
        (c["reference_label"], c["reference_value"])
    ]

    for label, val in meta_lines:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_after = Pt(2)
        p_m.paragraph_format.line_spacing = 1.5
        r_lbl = p_m.add_run(label + "  ")
        set_run_font(r_lbl, "TH Sarabun PSK", 14, bold=True)
        r_val = p_m.add_run(val)
        set_run_font(r_val, "TH Sarabun PSK", 12)

    # Attachments
    p_att = doc.add_paragraph()
    p_att.paragraph_format.space_after = Pt(2)
    p_att.paragraph_format.line_spacing = 1.5
    r_al = p_att.add_run(c["attachments_label"] + "  ")
    set_run_font(r_al, "TH Sarabun PSK", 14, bold=True)
    r_av = p_att.add_run(f'{c["attachments"][0]["title"]}     {c["attachments"][0]["quantity"]}')
    set_run_font(r_av, "TH Sarabun PSK", 12)

    # Paragraphs
    for para in c["paragraphs"]:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.first_line_indent = Inches(0.98)
        p_p.paragraph_format.space_after = Pt(4)
        p_p.paragraph_format.line_spacing = 1.5
        p_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_p = p_p.add_run(para)
        set_run_font(r_p, "TH Sarabun PSK", 12)

    # RULE: เคาะ 5 Enter จากข้อความสุดท้าย + พิกัด 130 มม.
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(55) # ~ 5 Enters
    p_sig.paragraph_format.left_indent = Inches(4.13) # 105 mm from left margin (total 130 mm from page edge)
    r_s = p_sig.add_run(f'{sig["rank"]}\n({sig["name"]})\n{sig["position"]}')
    set_run_font(r_s, "TH Sarabun PSK", 12)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")


# -----------------------------------------------------------------------------
# 3. GENERATE XLSX
# -----------------------------------------------------------------------------
def generate_xlsx(output_path):
    c = bp["content"]
    sig = c["signature"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "บันทึกข้อความ"
    ws.views.sheetView[0].showGridLines = True

    font_regular = Font(name="TH Sarabun PSK", size=12)
    font_bold = Font(name="TH Sarabun PSK", size=12, bold=True)
    font_large_bold = Font(name="TH Sarabun PSK", size=18, bold=True)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws["C4"] = c["title"]
    ws["C4"].font = font_large_bold
    ws["C4"].alignment = align_center

    memo_rows = [
        ("ส่วนราชการ", c["department_value"]),
        ("ที่", f'{c["doc_number_value"]}       วันที่            {c["doc_date_month_year"]}'),
        ("เรื่อง", c["subject_value"]),
        ("เรียน", c["recipient_value"]),
        ("อ้างถึง", c["reference_value"]),
        ("สิ่งที่ส่งมาด้วย", f'{c["attachments"][0]["title"]}   {c["attachments"][0]["quantity"]}'),
        ("", c["paragraphs"][0]),
        ("", c["paragraphs"][1])
    ]

    for idx, (lbl, val) in enumerate(memo_rows, start=6):
        ws[f"B{idx}"] = lbl
        ws[f"B{idx}"].font = font_bold
        ws[f"C{idx}"] = val
        ws[f"C{idx}"].font = font_regular
        ws.row_dimensions[idx].height = 28

    # Signature at 5 Enters down
    ws["E18"] = f'{sig["rank"]}\n({sig["name"]})\n{sig["position"]}'
    ws["E18"].font = font_regular
    ws["E18"].alignment = align_center

    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 50
    ws.column_dimensions["D"].width = 30
    ws.column_dimensions["E"].width = 25

    wb.save(output_path)
    print(f"Generated XLSX: {output_path}")


# -----------------------------------------------------------------------------
# MAIN COMPILER
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    html_out = os.path.join(BASE_DIR, "บันทึกข้อความ_90_วัน_Rebuild_Thai.html")
    docx_out = os.path.join(BASE_DIR, "บันทึกข้อความ_90_วัน_Rebuild_Thai.docx")
    xlsx_out = os.path.join(BASE_DIR, "บันทึกข้อความ_90_วัน_Rebuild_Thai.xlsx")

    generate_html(html_out)
    generate_docx(docx_out)
    generate_xlsx(xlsx_out)
    print("Compiled all formats successfully!")
