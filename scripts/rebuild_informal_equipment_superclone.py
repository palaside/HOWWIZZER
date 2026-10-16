import sys
import os
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
import openpyxl
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from signature_engine import render_signature_docx, render_signature_xlsx

WORKSPACE = Path(__file__).resolve().parent.parent
XLSX_PATH = WORKSPACE / "บัญชีรายการและสิ่งอุปกรณ์.xlsx"
OUT_HTML = WORKSPACE / "บัญชีรายการและสิ่งอุปกรณ์_Rebuild_Thai.html"
OUT_DOCX = WORKSPACE / "บัญชีรายการและสิ่งอุปกรณ์_Rebuild_Thai.docx"

FRONTEND_DOCS = WORKSPACE / "frontend" / "static" / "docs"
STATIC_DOCS = WORKSPACE / "static" / "docs"

SIG_COMMANDER = {
    "rank": "ร.อ.",
    "name": "กฤติน  นราพงษ์",
    "position": "ผบ.ร้อย.ป.๒",
}

def fmt_val(v):
    if v is None or v == "" or v == 0:
        return ""
    # If formula, evaluate or return empty/clean
    if isinstance(v, str) and v.startswith("="):
        return ""
    return str(v)

def parse_excel_data():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb['Sheet1']
    
    # Page 1: R1 to R29 (Title + Items 1 to 15 of โรงเก็บปืนใหญ่) -> EXACT MATCH TO IMAGE 2!
    # Page 2: R30 to R63 (Items 16 to 43 of โรงเก็บปืนใหญ่)
    # Page 3: R71 to R105 (Items 1 to 25 of คลัง บก.โรงเก็บปืนใหญ่)
    # Page 4: R106 to R115 (Items 26 to 29 of คลัง บก.โรงเก็บปืนใหญ่)
    
    pages = [
        {
            "page_num": 1,
            "title_1": "บัญชียุทโธปกรณ์ ป.4 พัน.4 ร้อย.2",
            "title_2": "โรงเก็บปืนใหญ่",
            "start_row": 5,
            "end_row": 29
        },
        {
            "page_num": 2,
            "title_1": "บัญชียุทโธปกรณ์ ป.4 พัน.4 ร้อย.2",
            "title_2": "โรงเก็บปืนใหญ่ (ต่อ)",
            "start_row": 30, # wait, R30 to R35, R36 is header, R37 to R63
            "skip_rows": [36],
            "end_row": 63
        },
        {
            "page_num": 3,
            "title_1": "บัญชียุทโธปกรณ์ ป.4 พัน.4 ร้อย.2",
            "title_2": "คลัง บก.โรงเก็บปืนใหญ่",
            "start_row": 72,
            "end_row": 105
        },
        {
            "page_num": 4,
            "title_1": "บัญชียุทโธปกรณ์ ป.4 พัน.4 ร้อย.2",
            "title_2": "คลัง บก.โรงเก็บปืนใหญ่ (ต่อ)",
            "start_row": 107,
            "end_row": 115
        }
    ]
    
    parsed_pages = []
    
    for p in pages:
        p_data = {
            "page_num": p["page_num"],
            "title_1": p["title_1"],
            "title_2": p["title_2"],
            "rows": []
        }
        
        r = p["start_row"]
        skip_list = p.get("skip_rows", [])
        
        while r <= p["end_row"]:
            if r in skip_list:
                r += 1
                continue
            
            # Read row cells:
            seq_val = ws.cell(r, 1).value
            c2 = ws.cell(r, 2).value
            c3 = ws.cell(r, 3).value
            
            # Reconstruct item name
            # In Excel: if c2 == '-' or c2 == '- ' then sub-item name is c3
            is_sub = False
            item_name = ""
            if c2 in ['-', '- ']:
                is_sub = True
                item_name = f"- {c3}" if c3 else "-"
            elif c2 is not None:
                item_name = str(c2)
                if c3 is not None and str(c3).strip():
                    item_name += f" {c3}"
            
            ctrl = fmt_val(ws.cell(r, 6).value)
            curr = fmt_val(ws.cell(r, 7).value)
            short = fmt_val(ws.cell(r, 8).value)
            surp = fmt_val(ws.cell(r, 9).value)
            repair = fmt_val(ws.cell(r, 10).value)
            loan = fmt_val(ws.cell(r, 11).value)
            bal = fmt_val(ws.cell(r, 12).value)
            rem = fmt_val(ws.cell(r, 13).value)
            
            # For calculate deficit / balance if empty and has ctrl & curr
            if short == "" and ctrl != "" and curr != "":
                try:
                    c_i = int(ctrl)
                    u_i = int(curr)
                    if c_i > u_i:
                        short = str(c_i - u_i)
                except:
                    pass
            if bal == "" and curr != "":
                bal = curr
            
            # Look at Image 2 for exact blank cells:
            # Row 2 (แผ่นเป้าทดสอบ): 6 | 5 | (blank) | (blank) | (blank) | (blank) | 5 | (blank)
            # In Image 2, row 2 short is blank! Even though 6 - 5 = 1!
            if r == 10: # แผ่นเป้าทดสอบ
                short = "" # match image 2 exactly
            
            # Row 1 (เต็นท์ main row): numeric cells are completely empty!
            if r == 5:
                ctrl, curr, short, surp, repair, loan, bal, rem = [""] * 8
            # Row 5 (ป้าย main row): numeric cells completely empty!
            if r == 13:
                ctrl, curr, short, surp, repair, loan, bal, rem = [""] * 8
            # Row 6 (ฝาปิดหลุม main row): numeric cells completely empty!
            if r == 17:
                ctrl, curr, short, surp, repair, loan, bal, rem = [""] * 8
                
            p_data["rows"].append({
                "excel_row": r,
                "seq": seq_val,
                "is_sub": is_sub,
                "name": item_name,
                "ctrl": ctrl,
                "curr": curr,
                "short": short,
                "surp": surp,
                "repair": repair,
                "loan": loan,
                "bal": bal,
                "rem": rem
            })
            r += 1
            
        parsed_pages.append(p_data)
        
    return parsed_pages

def build_superclone_html(pages):
    html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>บัญชียุทโธปกรณ์ ป.4 พัน.4 ร้อย.2 โรงเก็บปืนใหญ่</title>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4 portrait;
            margin: 12mm 15mm 15mm 15mm;
        }
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        body {
            font-family: 'TH Sarabun PSK', 'THSarabunPSK', 'TH Sarabun New', 'Sarabun', sans-serif !important;
            margin: 0;
            padding: 20px;
            background-color: #525659;
            color: #000;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .page-sheet {
            background: #ffffff;
            width: 210mm;
            min-height: 297mm;
            padding: 16mm 15mm 15mm 15mm;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 25px;
            position: relative;
        }
        @media print {
            body {
                background: none;
                padding: 0;
            }
            .page-sheet {
                box-shadow: none;
                margin: 0;
                width: 100%;
                min-height: 100vh;
                page-break-after: always;
                padding: 12mm 15mm 15mm 15mm;
            }
        }
        .doc-title-1 {
            text-align: center;
            font-size: 18pt;
            font-weight: 600;
            line-height: 1.25;
            margin-bottom: 2px;
            color: #000;
        }
        .doc-title-2 {
            text-align: center;
            font-size: 16pt;
            font-weight: 600;
            line-height: 1.25;
            margin-bottom: 14px;
            color: #000;
        }
        table.equipment-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 17pt;
            line-height: 1.2;
            border: 1px solid #000;
        }
        table.equipment-table th, table.equipment-table td {
            border: 1px solid #000;
            padding: 3px 4px;
            height: 25px;
            color: #000;
        }
        table.equipment-table th {
            text-align: center;
            vertical-align: middle;
            font-weight: 600;
            background-color: #ffffff;
        }
        .col-seq { width: 44px; text-align: center; }
        .col-name { width: 220px; text-align: left; }
        .col-ctrl { width: 55px; text-align: center; }
        .col-curr { width: 55px; text-align: center; }
        .col-short { width: 45px; text-align: center; }
        .col-surp { width: 45px; text-align: center; }
        .col-repair { width: 50px; text-align: center; }
        .col-loan { width: 50px; text-align: center; }
        .col-bal { width: 55px; text-align: center; }
        .col-rem { width: 70px; text-align: left; }
        
        .sub-indent {
            padding-left: 20px !important;
        }

        /* SIGNATURE BLOCK (Universal Red Line Standard) */
        .sig-container {
            width: 100%;
            display: flex;
            justify-content: flex-end;
            padding-right: 25mm;
            margin-top: 18mm;
        }
        .sig-block {
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            font-size: 17pt;
            line-height: 1.0;
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
            margin-top: 24pt;
        }
        .sig-rank-anchor {
            position: absolute;
            right: 100%;
            bottom: calc(100% + 22px);
            white-space: nowrap;
            font-size: 17pt;
            line-height: 1.0;
            font-weight: 300;
        }
        .sig-name, .sig-pos {
            font-size: 17pt;
            white-space: nowrap;
            text-align: center;
            line-height: 1.25;
            font-weight: 300;
        }
    </style>
</head>
<body>
"""

    for p in pages:
        p_num = p["page_num"]
        t1 = p["title_1"]
        t2 = p["title_2"]
        rows = p["rows"]
        
        html += f"""
    <!-- PAGE {p_num} -->
    <div class="page-sheet">
        <div class="doc-title-1">{t1}</div>
        <div class="doc-title-2">{t2}</div>
        
        <table class="equipment-table">
            <thead>
                <tr>
                    <th class="col-seq">ลำดับ</th>
                    <th class="col-name">รายการ</th>
                    <th class="col-ctrl">ยอดบัญชีคุม</th>
                    <th class="col-curr">ยอดที่มี</th>
                    <th class="col-short">ขาด</th>
                    <th class="col-surp">เกิน</th>
                    <th class="col-repair">ส่งซ่อม</th>
                    <th class="col-loan">เบิกยืม</th>
                    <th class="col-bal">คงเหลือ</th>
                    <th class="col-rem">หมายเหตุ</th>
                </tr>
            </thead>
            <tbody>
"""
        # We need to handle rowspans for column 1 (ลำดับ)
        # Scan rows to find groups where seq is set, followed by sub-rows with seq == None
        i = 0
        n = len(rows)
        while i < n:
            curr_row = rows[i]
            seq_val = curr_row["seq"]
            
            # Count how many subsequent rows belong to this item
            rowspan = 1
            if seq_val is not None:
                j = i + 1
                while j < n and rows[j]["seq"] is None and rows[j]["is_sub"]:
                    rowspan += 1
                    j += 1
            
            # Render first row of the group
            html += "                <tr>\n"
            if seq_val is not None:
                if rowspan > 1:
                    html += f'                    <td class="col-seq" rowspan="{rowspan}" style="vertical-align: middle;">{seq_val}</td>\n'
                else:
                    html += f'                    <td class="col-seq">{seq_val}</td>\n'
            
            name_cls = "col-name sub-indent" if curr_row["is_sub"] else "col-name"
            html += f'                    <td class="{name_cls}">{curr_row["name"]}</td>\n'
            html += f'                    <td class="col-ctrl">{curr_row["ctrl"]}</td>\n'
            html += f'                    <td class="col-curr">{curr_row["curr"]}</td>\n'
            html += f'                    <td class="col-short">{curr_row["short"]}</td>\n'
            html += f'                    <td class="col-surp">{curr_row["surp"]}</td>\n'
            html += f'                    <td class="col-repair">{curr_row["repair"]}</td>\n'
            html += f'                    <td class="col-loan">{curr_row["loan"]}</td>\n'
            html += f'                    <td class="col-bal">{curr_row["bal"]}</td>\n'
            html += f'                    <td class="col-rem">{curr_row["rem"]}</td>\n'
            html += "                </tr>\n"
            
            # If there are sub-rows in this group:
            for k in range(1, rowspan):
                sub_r = rows[i + k]
                html += "                <tr>\n"
                # col-seq is covered by rowspan!
                html += f'                    <td class="col-name sub-indent">{sub_r["name"]}</td>\n'
                html += f'                    <td class="col-ctrl">{sub_r["ctrl"]}</td>\n'
                html += f'                    <td class="col-curr">{sub_r["curr"]}</td>\n'
                html += f'                    <td class="col-short">{sub_r["short"]}</td>\n'
                html += f'                    <td class="col-surp">{sub_r["surp"]}</td>\n'
                html += f'                    <td class="col-repair">{sub_r["repair"]}</td>\n'
                html += f'                    <td class="col-loan">{sub_r["loan"]}</td>\n'
                html += f'                    <td class="col-bal">{sub_r["bal"]}</td>\n'
                html += f'                    <td class="col-rem">{sub_r["rem"]}</td>\n'
                html += "                </tr>\n"
            
            i += rowspan
            
        html += """            </tbody>
        </table>
"""
        # If this is the last page (Page 4), add Commander Signature Block
        if p_num == 4:
            html += f"""
        <!-- SIGNATURE BLOCK (Universal Red Line Standard for ผบ.ร้อย) -->
        <div class="sig-container">
            <div class="sig-block">
                <div class="sig-name-pos-group">
                    <div class="sig-name-wrapper">
                        <span class="sig-rank-anchor">{SIG_COMMANDER['rank']}</span>
                        <div class="sig-name">({SIG_COMMANDER['name']})</div>
                    </div>
                    <div class="sig-pos">{SIG_COMMANDER['position']}</div>
                </div>
            </div>
        </div>
"""
        html += """    </div>\n"""

    html += """
</body>
</html>
"""
    return html

def build_superclone_docx(pages):
    doc = Document()
    
    # Set Margins A4 Portrait
    for s in doc.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(1.2)
        s.bottom_margin = Cm(1.2)
        s.left_margin = Cm(1.5)
        s.right_margin = Cm(1.5)
        
    def add_page_content(p, is_first=False):
        if not is_first:
            doc.add_page_break()
            
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(p["title_1"])
        r1.font.name = "TH Sarabun PSK"
        r1.font.size = Pt(18)
        r1.font.bold = True
        
        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(8)
        r2 = p2.add_run(p["title_2"])
        r2.font.name = "TH Sarabun PSK"
        r2.font.size = Pt(16)
        r2.font.bold = True
        
        # Add table
        headers = ["ลำดับ", "รายการ", "ยอดบัญชีคุม", "ยอดที่มี", "ขาด", "เกิน", "ส่งซ่อม", "เบิกยืม", "คงเหลือ", "หมายเหตุ"]
        col_widths = [Cm(1.1), Cm(5.6), Cm(1.4), Cm(1.4), Cm(1.1), Cm(1.1), Cm(1.2), Cm(1.2), Cm(1.4), Cm(1.7)]
        
        rows = p["rows"]
        tbl = doc.add_table(rows=1, cols=10)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        
        # Border XML
        tblPr = tbl._tbl.tblPr
        borders_xml = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
            f'  <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
            f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>\n'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
            f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
            f'</w:tblBorders>'
        )
        tblPr.append(borders_xml)
        
        hdr_cells = tbl.rows[0].cells
        for idx, title in enumerate(headers):
            hdr_cells[idx].text = title
            hdr_cells[idx].width = col_widths[idx]
            hdr_cells[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            hdr_cells[idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for run in hdr_cells[idx].paragraphs[0].runs:
                run.font.name = "TH Sarabun PSK"
                run.font.size = Pt(14)
                run.font.bold = True
                
        # Populate rows
        i = 0
        n = len(rows)
        while i < n:
            curr_row = rows[i]
            seq_val = curr_row["seq"]
            
            rowspan = 1
            if seq_val is not None:
                j = i + 1
                while j < n and rows[j]["seq"] is None and rows[j]["is_sub"]:
                    rowspan += 1
                    j += 1
                    
            r_idx_start = len(tbl.rows)
            for k in range(rowspan):
                r_item = rows[i + k]
                row_cells = tbl.add_row().cells
                for ci, w in enumerate(col_widths):
                    row_cells[ci].width = w
                    row_cells[ci].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    
                # Fill text
                row_cells[0].text = str(r_item["seq"]) if r_item["seq"] is not None else ""
                row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                name_prefix = "   " if r_item["is_sub"] else ""
                row_cells[1].text = name_prefix + str(r_item["name"])
                row_cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                row_cells[2].text = str(r_item["ctrl"])
                row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[3].text = str(r_item["curr"])
                row_cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[4].text = str(r_item["short"])
                row_cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[5].text = str(r_item["surp"])
                row_cells[5].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[6].text = str(r_item["repair"])
                row_cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[7].text = str(r_item["loan"])
                row_cells[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[8].text = str(r_item["bal"])
                row_cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                row_cells[9].text = str(r_item["rem"])
                row_cells[9].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                for cell in row_cells:
                    for run in cell.paragraphs[0].runs:
                        run.font.name = "TH Sarabun PSK"
                        run.font.size = Pt(13)
                        run.font.bold = False
                        
            # Merge col 0 if rowspan > 1
            if rowspan > 1:
                start_cell = tbl.rows[r_idx_start].cells[0]
                end_cell = tbl.rows[r_idx_start + rowspan - 1].cells[0]
                start_cell.merge(end_cell)
                start_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                start_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                
            i += rowspan

        # If this is the last page (Page 4), add Commander Signature Block
        if p["page_num"] == 4:
            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_before = Pt(24)
            p_sp.paragraph_format.space_after = Pt(0)
            render_signature_docx(
                doc,
                SIG_COMMANDER,
                axis_inch=4.8,
                font_name="TH Sarabun PSK",
                font_size=15,
                space_after_rank_pt=24
            )

    for idx, p in enumerate(pages):
        add_page_content(p, is_first=(idx == 0))
        
    doc.save(str(OUT_DOCX))
    print(f"Generated DOCX: {OUT_DOCX}")

def update_superclone_xlsx():
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb['Sheet1']
    for r in range(116, 126):
        for c in range(1, 15):
            ws.cell(r, c).value = None
            
    render_signature_xlsx(
        ws,
        SIG_COMMANDER,
        start_row=118,
        rank_col="G",
        name_col="H",
        font_name="TH Sarabun PSK",
        font_size=14
    )
    try:
        wb.save(str(XLSX_PATH))
        print(f"Updated XLSX with signature block: {XLSX_PATH}")
    except PermissionError:
        print(f"Notice: {XLSX_PATH.name} is currently open in Excel. Saving to Rebuild_Thai.xlsx instead.")
        alt_xlsx = WORKSPACE / "บัญชีรายการและสิ่งอุปกรณ์_Rebuild_Thai.xlsx"
        wb.save(str(alt_xlsx))
        print(f"Saved alternate XLSX: {alt_xlsx}")

def main():
    pages = parse_excel_data()
    print(f"Parsed {len(pages)} pages from Excel data.")
    
    html_content = build_superclone_html(pages)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML: {OUT_HTML}")
    
    build_superclone_docx(pages)
    update_superclone_xlsx()
    
    # Sync to static docs
    for dest in [FRONTEND_DOCS, STATIC_DOCS]:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUT_HTML, dest / OUT_HTML.name)
        shutil.copy2(OUT_DOCX, dest / OUT_DOCX.name)
        try:
            shutil.copy2(XLSX_PATH, dest / XLSX_PATH.name)
        except Exception as e:
            print(f"Could not copy {XLSX_PATH.name}: {e}")
        alt_xlsx = WORKSPACE / "บัญชีรายการและสิ่งอุปกรณ์_Rebuild_Thai.xlsx"
        if alt_xlsx.exists():
            shutil.copy2(alt_xlsx, dest / alt_xlsx.name)
        print(f"Synced files to: {dest}")

if __name__ == "__main__":
    main()

