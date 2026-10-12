# -*- coding: utf-8 -*-
"""
Superclone Production-Grade Engine for ประวัติการใช้อาวุธปืนใหญ่ (5.ประวัติการใช้อาวุธ ปืน.pdf)
Form: ประวัติการใช้อาวุธ ป.หมู่ ๒ ถึง ๖
Specifications:
- 5-Page A4 Portrait (210mm x 297mm)
- Master Grid: 4 Equal Columns (25% each)
  - Col 1: ส่วนประกอบ (25%) - Center
  - Col 2: หมายเลขแบบ (25%) - Center
  - Col 3: หมายเลข (25%) - Center
  - Col 4: หมายเหตุ (25%) - Center
- Spacing: Table top separated by 1 Enter from Title
- Bottom text: วัน เดือน ปี ที่ยิงครั้งสุดท้าย............/..................../..................../ จำนวนนัดที่ยิงมาแล้ว...................นัด
- Signer: Universal Red Line Standard
  - Certification: ตรวจถูกต้อง (top left of signature group)
  - Rank endpoint '.' aligns exactly with '(' of name (right: 100%)
  - Name and position centered together
  - Signer: ร.อ. (กฤติน  นราพงษ์) ผบ.ป.๔ พัน.๔ ร้อย.๒
"""

import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

WORKDIR = r"d:\Project\WEPAPP"

# Helper function for Thai digits
def to_th(val):
    if val is None or val == "":
        return ""
    s = str(val)
    mapping = {
        '0': '๐', '1': '๑', '2': '๒', '3': '๓', '4': '๔',
        '5': '๕', '6': '๖', '7': '๗', '8': '๘', '9': '๙'
    }
    return "".join(mapping.get(c, c) for c in s)

# Load extracted data
with open(os.path.join(WORKDIR, "gun_history_extracted.json"), "r", encoding="utf-8") as f:
    raw_pages = json.load(f)

# Build Blueprint SSOT Model
blueprint = {
    "metadata": {
        "form_name": "ประวัติการใช้อาวุธ",
        "category": "ทะเบียนประวัติการใช้อาวุธประจำหมู่ปืนใหญ่",
        "signer": {
            "cert": "ตรวจถูกต้อง",
            "rank": "ร.อ.",
            "name": "(กฤติน  นราพงษ์)",
            "position": "ผบ.ป.๔ พัน.๔ ร้อย.๒"
        },
        "firing_record": {
            "line1": "วัน เดือน ปี ที่ยิงครั้งสุดท้าย   ........./............../............../",
            "line2": "จำนวนนัดที่ยิงมาแล้ว ............  นัด"
        },
        "columns": [
            {"id": "part", "label": "ส่วนประกอบ", "width_pct": 30.0},
            {"id": "model", "label": "หมายเลขแบบ", "width_pct": 24.0},
            {"id": "serial", "label": "หมายเลข", "width_pct": 23.0},
            {"id": "remark", "label": "หมายเหตุ", "width_pct": 23.0}
        ]
    },
    "pages": []
}

for p in raw_pages:
    squad_th = to_th(p["squad_num"])
    page_obj = {
        "page_num": p["page_num"],
        "squad_num": p["squad_num"],
        "squad_th": squad_th,
        "title": f"ประวัติการใช้อาวุธ ป.หมู่ {squad_th}",
        "items": []
    }
    for item in p["items"]:
        # Convert serial numbers to Thai digits if purely numeric
        serial_val = item["serial"]
        if serial_val.isdigit():
            serial_display = to_th(serial_val)
        elif serial_val.startswith("-") and serial_val[1:].replace(".", "").isdigit():
            serial_display = f"-{to_th(serial_val[1:])}"
        else:
            serial_display = serial_val

        page_obj["items"].append({
            "part": item["part"],
            "model": item["model"],
            "serial": serial_display,
            "raw_serial": item["serial"],
            "remark": item["remark"]
        })
    blueprint["pages"].append(page_obj)

# Save SSOT Blueprint JSON
ssot_path = os.path.join(WORKDIR, "table_layout_gun_history.json")
with open(ssot_path, "w", encoding="utf-8") as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)
print("Saved SSOT Blueprint:", ssot_path)


# ----------------------------------------------------------------------
# 2. HTML Generation (A4 Portrait, 4 Columns: 25% each)
# ----------------------------------------------------------------------
def generate_html():
    pages_html = ""
    for p in blueprint["pages"]:
        rows_tr = ""
        for it in p["items"]:
            rows_tr += f"""
            <tr class="data-row">
                <td class="col-part text-center">{it['part']}</td>
                <td class="col-model text-center">{it['model']}</td>
                <td class="col-serial text-center">{it['serial']}</td>
                <td class="col-remark text-center">{it['remark']}</td>
            </tr>"""

        pages_html += f"""
        <div class="sheet-container">
            <!-- หัวเรื่อง: ประวัติการใช้อาวุธ ป.หมู่ X -->
            <div class="form-title font-bold text-center">
                {p['title']}
            </div>

            <!-- ตารางหลัก 4 คอลัมน์: เว้น 1 Enter จากหัวเรื่อง -->
            <table class="gun-history-table">
                <colgroup>
                    <col style="width: 30%;">
                    <col style="width: 24%;">
                    <col style="width: 23%;">
                    <col style="width: 23%;">
                </colgroup>
                <thead>
                    <tr>
                        <th class="col-part">ส่วนประกอบ</th>
                        <th class="col-model">หมายเลขแบบ</th>
                        <th class="col-serial">หมายเลข</th>
                        <th class="col-remark">หมายเหตุ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_tr}
                </tbody>
            </table>

            <!-- ข้อมูลการยิงครั้งสุดท้าย: 2 บรรทัด เคาะ 1 Enter -->
            <div class="firing-record-container">
                <div class="firing-line">{blueprint['metadata']['firing_record']['line1']}</div>
                <div class="firing-line firing-line-2">{blueprint['metadata']['firing_record']['line2']}</div>
            </div>

            <!-- Signature Block Engine v1.0 — approved_pbk_95 Gold Standard -->
            <div class="doc-footer-grid">
                <div class="sig-block">
                    <div class="sig-verify">{blueprint['metadata']['signer']['cert']}</div>
                    <div class="sig-name-pos-group">
                        <div class="sig-name-wrapper">
                            <span class="sig-rank-anchor">{blueprint['metadata']['signer']['rank']}</span>
                            <div class="sig-name">{blueprint['metadata']['signer']['name']}</div>
                        </div>
                        <div class="sig-pos">{blueprint['metadata']['signer']['position']}</div>
                    </div>
                </div>
            </div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ประวัติการใช้อาวุธ ป.หมู่ ๒ ถึง ๖</title>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 15mm 15mm;
        }}
        * {{
            box-sizing: border-box;
            font-family: 'TH Sarabun PSK', Sarabun, sans-serif;
        }}
        body {{
            margin: 0;
            padding: 20px;
            background: #e2e8f0;
            color: #000;
            font-size: 16pt;
            line-height: 1.15;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
        }}

        .sheet-container {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto 30px auto;
            background: #fff;
            padding: 20mm 15mm 20mm 15mm;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: relative;
            page-break-after: always;
        }}

        /* Center Title */
        .form-title {{
            text-align: center;
            font-size: 20pt;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 24px; /* เว้น 1 Enter อย่างชัดเจน */
        }}

        /* Main 4-Column Table */
        .gun-history-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            border: 1px solid #000;
            font-size: 16pt;
        }}
        .gun-history-table th, .gun-history-table td {{
            border: 1px solid #000;
            padding: 4px 4px;
            vertical-align: middle;
            line-height: 1.2;
            white-space: nowrap;
        }}
        .gun-history-table thead th {{
            font-weight: normal; /* ตัวปกติ ตามมาตรฐาน */
            font-size: 16pt;
            text-align: center;
            padding: 6px 4px;
            background: #fbfbfb;
        }}

        /* Data Rows */
        .data-row td {{
            height: 28px;
        }}

        /* Firing record info */
        .firing-record-container {{
            margin-top: 36px;
            font-size: 16pt;
            line-height: 1.25;
            white-space: nowrap;
        }}
        .firing-line-2 {{
            margin-top: 14px; /* เคาะลงมา 1 Enter */
        }}

        /* ========================================================= */
        /* SIGNATURE BLOCK ENGINE v1.0 — TRUE RED LINE ALIGNMENT     */
        /* อ้างอิงแม่แบบ บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html */
        /* ========================================================= */
        .doc-footer-grid {{
            display: flex;
            justify-content: flex-end;
            margin-top: 36px;
            padding: 0 45px 0 0;
        }}
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 16pt;
            line-height: 1.0;
        }}
        .sig-verify {{
            margin-bottom: 32px; /* เคาะ 1 Enter แบบมีระยะห่างหลังย่อหน้า ก่อนถึงบรรทัดยศ */
            font-size: 16pt;
            line-height: 1.0;
        }}
        
        /* กล่องชื่อและตำแหน่ง */
        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            margin-left: 95px;
        }}

        /* กรอบชื่อ: ตัวยึดแนววงเล็บเปิด ( */
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 30px; /* พื้นที่สำหรับลงลายมือชื่อจริง */
        }}

        /* บรรทัดยศ: จุด . ท้ายยศ ชนขอบซ้ายของกรอบชื่อ ซึ่งคือ ( พอดีเป๊ะ 100% */
        .sig-rank-anchor {{
            position: absolute;
            right: 100%; /* ชนแนวเส้นดิ่งเดียวกับ ( พอดีเป๊ะ */
            bottom: calc(100% + 20px);
            white-space: nowrap;
            font-size: 16pt;
            line-height: 1.0;
        }}

        /* ชื่อและตำแหน่ง: จัดกึ่งกลางร่วมกัน 1 enter ไม่มีระยะย่อหน้า */
        .sig-name {{
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 16pt;
            display: block;
        }}
        .sig-pos {{
            margin: 0;
            line-height: 1.15;
            text-align: center;
            white-space: nowrap;
            font-size: 16pt;
            display: block;
        }}

        .font-bold {{ font-weight: bold; }}
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}

        @media print {{
            body {{ background: transparent; padding: 0; }}
            .sheet-container {{
                box-shadow: none;
                margin: 0;
                padding: 15mm 15mm;
                width: 100%;
                min-height: auto;
            }}
        }}
    </style>
</head>
<body>
    {pages_html}
</body>
</html>
    """

    html_path = os.path.join(WORKDIR, "ประวัติการใช้อาวุธ_Rebuild_Thai.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print("Saved HTML:", html_path)
    return html_path

generate_html()


# ----------------------------------------------------------------------
# 3. Microsoft Excel Generation (.xlsx)
# ----------------------------------------------------------------------
def generate_excel():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    font_regular = Font(name="TH Sarabun PSK", size=16, bold=False)
    font_bold = Font(name="TH Sarabun PSK", size=18, bold=True)
    thin_side = Side(border_style="thin", color="000000")
    thin_border = Border(top=thin_side, bottom=thin_side, left=thin_side, right=thin_side)
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    for p in blueprint["pages"]:
        ws = wb.create_sheet(title=f"ป.หมู่ {p['squad_th']}")
        ws.views.sheetView[0].showGridLines = True
        ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_margins.left = 0.6
        ws.page_margins.right = 0.6
        ws.page_margins.top = 0.6
        ws.page_margins.bottom = 0.6

        # Column widths: 4 columns (30%, 24%, 23%, 23%)
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 24
        ws.column_dimensions['C'].width = 23
        ws.column_dimensions['D'].width = 23

        # Row 2: Title (Merged across A2:D2)
        ws.merge_cells("A2:D2")
        ws["A2"] = p['title']
        ws["A2"].font = font_bold
        ws["A2"].alignment = align_center

        # Row 3: 1 Enter Gap
        # Row 4: Table Header
        headers = ["ส่วนประกอบ", "หมายเลขแบบ", "หมายเลข", "หมายเหตุ"]
        for idx, col in enumerate(['A', 'B', 'C', 'D']):
            c = ws[f"{col}4"]
            c.value = headers[idx]
            c.font = font_regular
            c.alignment = align_center
            c.border = thin_border
            c.fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")

        # Data rows
        curr_r = 5
        for it in p["items"]:
            ws[f"A{curr_r}"].value = it['part']; ws[f"A{curr_r}"].font = font_regular; ws[f"A{curr_r}"].alignment = align_center
            ws[f"B{curr_r}"].value = it['model']; ws[f"B{curr_r}"].font = font_regular; ws[f"B{curr_r}"].alignment = align_center
            ws[f"C{curr_r}"].value = it['serial']; ws[f"C{curr_r}"].font = font_regular; ws[f"C{curr_r}"].alignment = align_center
            ws[f"D{curr_r}"].value = it['remark']; ws[f"D{curr_r}"].font = font_regular; ws[f"D{curr_r}"].alignment = align_center
            for col in ['A', 'B', 'C', 'D']:
                ws[f"{col}{curr_r}"].border = thin_border
            curr_r += 1

        # Gap rows
        curr_r += 1

        # Firing record line 1
        ws.merge_cells(f"A{curr_r}:D{curr_r}")
        ws[f"A{curr_r}"] = blueprint['metadata']['firing_record']['line1']
        ws[f"A{curr_r}"].font = font_regular
        ws[f"A{curr_r}"].alignment = align_left
        curr_r += 1

        # Firing record line 2 (1 Enter)
        ws.merge_cells(f"A{curr_r}:D{curr_r}")
        ws[f"A{curr_r}"] = blueprint['metadata']['firing_record']['line2']
        ws[f"A{curr_r}"].font = font_regular
        ws[f"A{curr_r}"].alignment = align_left
        curr_r += 2

        # Certification row: ตรวจถูกต้อง in Col C
        ws[f"C{curr_r}"] = blueprint['metadata']['signer']['cert']
        ws[f"C{curr_r}"].font = font_regular
        ws[f"C{curr_r}"].alignment = align_center
        curr_r += 2 # 1 Enter blank row between ตรวจถูกต้อง and ยศ

        # Rank row
        ws[f"C{curr_r}"] = f"   {blueprint['metadata']['signer']['rank']}"
        ws[f"C{curr_r}"].font = font_regular
        ws[f"C{curr_r}"].alignment = align_center
        curr_r += 2 # Space for signature

        # Name row
        ws[f"C{curr_r}"] = blueprint['metadata']['signer']['name']
        ws[f"C{curr_r}"].font = font_regular
        ws[f"C{curr_r}"].alignment = align_center
        curr_r += 1

        # Position row
        ws[f"C{curr_r}"] = blueprint['metadata']['signer']['position']
        ws[f"C{curr_r}"].font = font_regular
        ws[f"C{curr_r}"].alignment = align_center

    xlsx_path = os.path.join(WORKDIR, "ประวัติการใช้อาวุธ_Rebuild_Thai.xlsx")
    wb.save(xlsx_path)
    print("Saved XLSX:", xlsx_path)

generate_excel()


# ----------------------------------------------------------------------
# 4. Microsoft Word Generation (.docx)
# ----------------------------------------------------------------------
def format_docx_run(run, font_name="TH Sarabun PSK", size_pt=16, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}" w:eastAsia="{font_name}"/>')
    rPr.append(rFonts)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, top="single", bottom="single", left="single", right="single", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="000000"/><w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="000000"/><w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="000000"/><w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="000000"/></w:tcBorders>')
    tcPr.append(borders)

def generate_word():
    doc = docx.Document()
    
    # Configure A4 Portrait (8.27" x 11.69")
    for section in doc.sections:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)

    for p_idx, p in enumerate(blueprint["pages"]):
        if p_idx > 0:
            doc.add_page_break()

        # Title Center
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.paragraph_format.space_before = Pt(6)
        p_title.paragraph_format.space_after = Pt(24) # 1 Enter gap
        r_t = p_title.add_run(p['title'])
        format_docx_run(r_t, size_pt=20, bold=True)

        # Table 4 columns (30%, 24%, 23%, 23%): total width = 6.87 inches
        tbl_widths = [Inches(2.06), Inches(1.65), Inches(1.58), Inches(1.58)]
        
        num_rows = 1 + len(p['items'])
        table = doc.add_table(rows=num_rows, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Set column widths & header
        headers = ["ส่วนประกอบ", "หมายเลขแบบ", "หมายเลข", "หมายเหตุ"]
        for c_idx in range(4):
            cell = table.cell(0, c_idx)
            cell.width = tbl_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single")
            p_c = cell.paragraphs[0]; p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_after = Pt(0)
            r_c = p_c.add_run(headers[c_idx])
            format_docx_run(r_c, size_pt=16, bold=False)

        # Data rows
        for it_idx, it in enumerate(p['items']):
            row_idx = 1 + it_idx
            vals = [it['part'], it['model'], it['serial'], it['remark']]
            for c_idx in range(4):
                cell = table.cell(row_idx, c_idx)
                cell.width = tbl_widths[c_idx]
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
                set_cell_borders(cell, top="single", bottom="single", left="single", right="single")
                p_cell = cell.paragraphs[0]; p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cell.paragraph_format.space_after = Pt(0)
                r_cell = p_cell.add_run(vals[c_idx])
                format_docx_run(r_cell, size_pt=16, bold=False)

        # Firing info paragraphs (2 lines with 1 Enter)
        p_fire1 = doc.add_paragraph()
        p_fire1.paragraph_format.space_before = Pt(28)
        p_fire1.paragraph_format.space_after = Pt(0)
        r_fire1 = p_fire1.add_run(blueprint['metadata']['firing_record']['line1'])
        format_docx_run(r_fire1, size_pt=16, bold=False)

        p_fire2 = doc.add_paragraph()
        p_fire2.paragraph_format.space_before = Pt(0)
        p_fire2.paragraph_format.space_after = Pt(20) # 1 Enter gap
        r_fire2 = p_fire2.add_run(blueprint['metadata']['firing_record']['line2'])
        format_docx_run(r_fire2, size_pt=16, bold=False)

        # Universal Signature Block in DOCX
        axis_tab = Inches(5.2) # Right-side anchor axis
        cert_tab = Inches(4.2)

        p_cert = doc.add_paragraph()
        p_cert.paragraph_format.tab_stops.add_tab_stop(cert_tab, WD_TAB_ALIGNMENT.LEFT)
        p_cert.paragraph_format.space_after = Pt(22) # 1 Enter gap with space after
        r_cert = p_cert.add_run(f"\t{blueprint['metadata']['signer']['cert']}")
        format_docx_run(r_cert, size_pt=16, bold=False)

        p_rk = doc.add_paragraph()
        p_rk.paragraph_format.tab_stops.add_tab_stop(axis_tab, WD_TAB_ALIGNMENT.RIGHT)
        p_rk.paragraph_format.space_after = Pt(14)
        r_rk = p_rk.add_run(f"\t{blueprint['metadata']['signer']['rank']}")
        format_docx_run(r_rk, size_pt=16, bold=False)

        p_nm = doc.add_paragraph()
        p_nm.paragraph_format.tab_stops.add_tab_stop(axis_tab, WD_TAB_ALIGNMENT.LEFT)
        p_nm.paragraph_format.space_after = Pt(0)
        r_nm = p_nm.add_run(f"\t{blueprint['metadata']['signer']['name']}")
        format_docx_run(r_nm, size_pt=16, bold=False)

        p_pos = doc.add_paragraph()
        p_pos.paragraph_format.tab_stops.add_tab_stop(axis_tab, WD_TAB_ALIGNMENT.CENTER)
        p_pos.paragraph_format.space_after = Pt(0)
        r_pos = p_pos.add_run(f"\t{blueprint['metadata']['signer']['position']}")
        format_docx_run(r_pos, size_pt=16, bold=False)

    docx_path = os.path.join(WORKDIR, "ประวัติการใช้อาวุธ_Rebuild_Thai.docx")
    doc.save(docx_path)
    print("Saved DOCX:", docx_path)

generate_word()
