import os
import sys
import json
import base64

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION, WD_ORIENTATION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_PATH = os.path.join(BASE_DIR, "table_layout_memo_inquiry_90.json")
GARUDA_PATH = os.path.join(BASE_DIR, "garuda_vector_official.png")

with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
    bp = json.load(f)

with open(GARUDA_PATH, "rb") as f:
    GARUDA_B64 = base64.b64encode(f.read()).decode("utf-8")

# -----------------------------------------------------------------------------
# 1. GENERATE HTML
# -----------------------------------------------------------------------------
def generate_html(output_path):
    p1 = bp["pages"][0]
    c1 = p1["content"]
    sig1 = c1["signature"]
    
    p2 = bp["pages"][1]
    p3 = bp["pages"][2]

    def render_tracking_page(p_data, page_id):
        h = p_data["header"]
        tbl = p_data["table"]
        sigs = p_data["signatures"]
        sig_cdr = next(s for s in sigs if s["role_key"] == "commander")
        sig_insp = next(s for s in sigs if s["role_key"] == "inspector")

        # Table rows HTML
        rows_html = ""
        for r in tbl["rows"]:
            rows_html += f"""
                <tr>
                    <td class="text-center">{r["no"]}</td>
                    <td class="text-left" style="padding-left: 3mm;">{r["item_name"]}</td>
                    <td class="text-center">{r["stock_no"]}</td>
                    <td class="text-center">{r["voucher_no"]}</td>
                    <td class="text-center">{r["submitted_date"]}</td>
                    <td class="text-center">{r["tracked_date"]}</td>
                    <td class="text-left">{r["note"]}</td>
                </tr>
            """
        # Fill empty rows up to 10 rows for clean government format
        current_rows = len(tbl["rows"])
        for _ in range(max(0, 10 - current_rows)):
            rows_html += """
                <tr>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                    <td>&nbsp;</td>
                </tr>
            """

        return f"""
        <div class="page-legal-landscape" id="{page_id}">
            <!-- Form Top Header -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2mm;">
                <div></div>
                <div style="font-size: 18pt; font-weight: bold; text-align: center; margin-left: 60mm;">
                    {p_data["title"]}
                </div>
                <div style="text-align: right; font-size: 12pt; line-height: 1.2;">
                    <div style="font-weight: bold;">{p_data["form_code"]}</div>
                    <div>{p_data["form_subcode"]}</div>
                </div>
            </div>

            <!-- Meta block -->
            <div style="margin-bottom: 3mm; font-size: 12pt; line-height: 1.5;">
                <div style="margin-bottom: 1mm;">{h["doc_number"]}</div>
                <div style="margin-bottom: 1mm;">{h["subject"]}</div>
                <div style="margin-bottom: 1mm;">
                    <span style="font-weight: bold; display: inline-block; width: 12mm;">{h["to_label"]}</span>
                    <span>{h["to_value"]}</span>
                </div>
                <div style="margin-bottom: 2mm;">
                    <span style="font-weight: bold; display: inline-block; width: 12mm;">{h["from_label"]}</span>
                    <span>{h["from_value"]}</span>
                </div>
                <div style="padding-left: 20mm; margin-top: 2mm; margin-bottom: 3mm;">
                    {h["instruction"]}
                </div>
            </div>

            <!-- Table -->
            <table class="grid-table">
                <thead>
                    <tr>
                        <th style="width: 5%;">ลำดับ</th>
                        <th style="width: 22%;">รายการ สป.</th>
                        <th style="width: 19%;">หมายเลข สป.</th>
                        <th style="width: 14%;">ที่ใบเบิก ที่ทะเบียนหน่วย<br>จ่าย</th>
                        <th style="width: 12%;">วันที่ส่งหรือวางใบเบิก</th>
                        <th style="width: 13%;">{tbl["columns"][5]["name"]}</th>
                        <th style="width: 15%;">หมายเหตุ (บันทึกโดยหน่วยจ่าย)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>

            <!-- Double Signature Block Area (Signature Block Engine v1.0) -->
            <div style="display: flex; justify-content: space-between; margin-top: 10mm; padding: 0 20mm;">
                <!-- ฝั่งซ้าย: ผบ.ร้อย -->
                <div style="min-width: 80mm; display: flex; flex-direction: column; align-items: center;">
                    <div class="sig-block" style="font-size: 12pt; line-height: 1.0;">
                        <div style="height: 12pt; margin-bottom: 24pt;">&nbsp;</div>
                        <div class="sig-name-pos-group" style="margin-left: 45px;">
                            <div class="sig-name-wrapper" style="margin-top: 22pt;">
                                <span class="sig-rank-anchor">{sig_cdr["rank"]}</span>
                                <div class="sig-name">({sig_cdr["name"]})</div>
                            </div>
                            <div class="sig-pos">{sig_cdr["position"]}</div>
                            <div style="margin-top: 4px; font-size: 12pt; text-align: center; white-space: nowrap;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{sig_cdr["date"]}</div>
                        </div>
                    </div>
                </div>

                <!-- ฝั่งขวา: ผู้ตรวจสอบ -->
                <div style="min-width: 80mm; display: flex; flex-direction: column; align-items: center;">
                    <div class="sig-block" style="font-size: 12pt; line-height: 1.0;">
                        <div style="font-weight: bold; margin-bottom: 24pt; font-size: 12pt; text-align: left;">{sig_insp["label"]}</div>
                        <div class="sig-name-pos-group" style="margin-left: 55px;">
                            <div class="sig-name-wrapper" style="margin-top: 22pt;">
                                <span class="sig-rank-anchor">{sig_insp["rank"]}</span>
                                <div class="sig-name">({sig_insp["name"]})</div>
                            </div>
                            <div class="sig-pos">{sig_insp["position"]}</div>
                            <div style="margin-top: 4px; font-size: 12pt; text-align: center; white-space: nowrap;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{sig_insp["date"]}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer Note -->
            <div style="position: absolute; bottom: 8mm; left: 0; right: 0; text-align: center; font-size: 10.5pt;">
                {p_data["footer_note"]}
            </div>
        </div>
        """

    p2_html = render_tracking_page(p2, "page-2")
    p3_html = render_tracking_page(p3, "page-3")

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
        @page portrait-page {{
            size: A4 portrait;
            margin: 0;
        }}
        @page landscape-page {{
            size: 355.6mm 215.9mm; /* Legal Landscape */
            margin: 0;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            font-family: 'TH Sarabun PSK', 'THSarabunNew', 'Sarabun', sans-serif;
        }}
        body {{
            margin: 0;
            padding: 20px 0;
            background-color: #525659;
            font-family: 'TH Sarabun PSK', 'THSarabunNew', 'Sarabun', sans-serif;
            font-size: 14pt;
            font-weight: normal;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
            color: #000000;
            line-height: 1.15;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        /* PAGE 1: A4 PORTRAIT */
        .page-portrait {{
            width: 210mm;
            height: 297mm;
            background-color: #ffffff;
            margin-bottom: 20mm;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
            position: relative;
            padding: 20mm 15mm 15mm 25mm; /* Top 2cm, Right 1.5cm, Bottom 1.5cm, Left 2.5cm */
            overflow: hidden;
            page-break-after: always;
            page: portrait-page;
            font-size: 12pt;
            line-height: 1.5;
        }}

        /* PAGE 2 & 3: LEGAL LANDSCAPE */
        .page-legal-landscape {{
            width: 355.6mm;
            height: 215.9mm;
            background-color: #ffffff;
            margin-bottom: 20mm;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
            position: relative;
            padding: 10mm 15mm 10mm 15mm;
            overflow: hidden;
            page-break-after: always;
            page: landscape-page;
        }}

        @media print {{
            body {{
                background-color: #ffffff;
                padding: 0;
            }}
            .page-portrait {{
                margin: 0;
                box-shadow: none;
                page: portrait-page;
            }}
            .page-legal-landscape {{
                margin: 0;
                box-shadow: none;
                page: landscape-page;
            }}
        }}

        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        .font-bold {{ font-weight: bold; }}

        /* MEMO HEADER */
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

        /* TABLE GRID */
        table.grid-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12pt;
            line-height: 1.25;
        }}
        table.grid-table th, table.grid-table td {{
            border: 1px solid #000;
            padding: 5px 4px;
            vertical-align: middle;
        }}
        table.grid-table th {{
            text-align: center;
            font-weight: bold;
            background-color: #ffffff;
        }}
    </style>
</head>
<body>

    <!-- PAGE 1: บันทึกข้อความ (A4 Portrait) -->
    <div class="page-portrait" id="page-1">
        <div class="memo-header-container">
            <img class="memo-garuda" src="data:image/png;base64,{GARUDA_B64}" alt="ครุฑ">
            <div class="memo-title">{c1["title"]}</div>
        </div>

        <div style="margin-top: 2mm; font-size: 12pt; line-height: 1.5;">
            <!-- ส่วนราชการ -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <span class="memo-meta-label" style="margin-right: 2mm;">{c1["official_department"]}</span>
                <div class="memo-meta-dots" style="flex: 1;">{c1["department_value"]}</div>
            </div>
            <!-- ที่ และ วันที่ -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <div style="display: flex; align-items: baseline; flex: 1.2; margin-right: 6mm;">
                    <span class="memo-meta-label" style="margin-right: 2mm;">{c1["doc_number_label"]}</span>
                    <div class="memo-meta-dots" style="flex: 1;">{c1["doc_number_value"]}</div>
                </div>
                <div style="display: flex; align-items: baseline; flex: 1;">
                    <span class="memo-meta-label" style="margin-right: 2mm;">{c1["doc_date_label"]}</span>
                    <div class="memo-meta-dots" style="flex: 1;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{c1["doc_date_month_year"]}</div>
                </div>
            </div>
            <!-- เรื่อง (บรรทัดเดียว ไม่มีเส้นไข่ปลา) -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <span class="memo-meta-label" style="margin-right: 2mm;">{c1["subject_label"]}</span>
                <div style="flex: 1; padding-left: 2mm;">{c1["subject_value"]}</div>
            </div>
        </div>

        <div class="memo-content">
            <div style="margin-bottom: 2mm;">
                <span class="font-bold">{c1["recipient_label"]}</span>&nbsp;&nbsp;{c1["recipient_value"]}
            </div>
            <div style="margin-bottom: 2mm;">
                <span class="font-bold">{c1["reference_label"]}</span>&nbsp;&nbsp;{c1["reference_value"]}
            </div>

            <div style="margin: 0 0 2.5mm 0; font-size: 12pt; line-height: 1.5;">
                <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
                    <tr>
                        <td style="width: 28mm; vertical-align: top; white-space: nowrap;"><span class="font-bold">{c1["attachments_label"]}</span></td>
                        <td style="vertical-align: top;">{c1["attachments"][0]["title"]}</td>
                        <td style="width: 28mm; vertical-align: top; text-align: right; white-space: nowrap;">{c1["attachments"][0]["quantity"]}</td>
                    </tr>
                </table>
            </div>

            <p class="memo-p">{c1["paragraphs"][0]}</p>
            <p class="memo-p">{c1["paragraphs"][1]}</p>
        </div>

        <!-- SIGNATURE BLOCK (RULE: เคาะ 5 Enter จากบรรทัดสุดท้าย, พิกัดซ้าย 130 มม. - Margin ซ้าย 25 มม. = padding-left 105 มม.) -->
        <div style="margin-top: 55pt; padding-left: 105mm;">
            <div class="sig-block" style="margin-right: 0;">
                <div class="sig-name-pos-group" style="margin-left: 45px;">
                    <div class="sig-name-wrapper" style="margin-top: 22pt;">
                        <span class="sig-rank-anchor">{sig1["rank"]}</span>
                        <div class="sig-name">({sig1["name"]})</div>
                    </div>
                    <div class="sig-pos">{sig1["position"]}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- PAGE 2: ใบติดตามใบเบิก แผ่นที่ ๑ (Legal Landscape) -->
    {p2_html}

    <!-- PAGE 3: ใบติดตามใบเบิก แผ่นที่ ๒ (Legal Landscape) -->
    {p3_html}

</body>
</html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML: {output_path}")


# -----------------------------------------------------------------------------
# 2. GENERATE DOCX
# -----------------------------------------------------------------------------
def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["val", "color", "sz", "space"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

def set_run_font(run, font_name="TH Sarabun PSK", size_pt=12, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:cs'), font_name)

def generate_docx(output_path):
    doc = Document()

    # SECTION 1: Page 1 A4 Portrait
    sec1 = doc.sections[0]
    sec1.orientation = WD_ORIENTATION.PORTRAIT
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.top_margin = Inches(0.79) # 2 cm
    sec1.right_margin = Inches(0.59) # 1.5 cm
    sec1.bottom_margin = Inches(0.59) # 1.5 cm
    sec1.left_margin = Inches(0.98) # 2.5 cm

    c1 = bp["pages"][0]["content"]
    sig1 = c1["signature"]

    # Header Table
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_img = tbl_h.cell(0, 0)
    c_img.width = Inches(1.3)
    p_img = c_img.paragraphs[0]
    p_img.paragraph_format.space_after = Pt(0)
    r_img = p_img.add_run()
    r_img.add_picture(GARUDA_PATH, width=Inches(1.18))

    c_title = tbl_h.cell(0, 1)
    c_title.width = Inches(5.4)
    p_t = c_title.paragraphs[0]
    p_t.paragraph_format.space_before = Pt(14)
    p_t.paragraph_format.space_after = Pt(0)
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_t.add_run(c1["title"])
    set_run_font(r_t, "TH Sarabun PSK", 24, bold=True)

    set_cell_border(c_img)
    set_cell_border(c_title)

    # Meta Lines
    meta_lines = [
        (c1["official_department"], c1["department_value"]),
        (f'{c1["doc_number_label"]}  {c1["doc_number_value"]}', f'{c1["doc_date_label"]}            {c1["doc_date_month_year"]}'),
        (c1["subject_label"], c1["subject_value"]),
        (c1["recipient_label"], c1["recipient_value"]),
        (c1["reference_label"], c1["reference_value"])
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
    r_al = p_att.add_run(c1["attachments_label"] + "  ")
    set_run_font(r_al, "TH Sarabun PSK", 14, bold=True)
    r_av = p_att.add_run(f'{c1["attachments"][0]["title"]}     {c1["attachments"][0]["quantity"]}')
    set_run_font(r_av, "TH Sarabun PSK", 12)

    # Paragraphs
    for para in c1["paragraphs"]:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.first_line_indent = Inches(0.98)
        p_p.paragraph_format.space_after = Pt(4)
        p_p.paragraph_format.line_spacing = 1.5
        p_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_p = p_p.add_run(para)
        set_run_font(r_p, "TH Sarabun PSK", 12)

    # RULE-UNIVERSAL-SIGNATURE-BLOCK-V1: 5 Enters + 130mm from page left edge (4.13 inches from left margin)
    # Tab Stop Red Line Standard: Rank . ends at axis, Name ( starts at axis
    axis_memo = Inches(4.13)
    
    p_sig_rk = doc.add_paragraph()
    p_sig_rk.paragraph_format.space_before = Pt(55) # ~ 5 Enters
    p_sig_rk.paragraph_format.space_after = Pt(22)  # Space for signature
    p_sig_rk.paragraph_format.tab_stops.add_tab_stop(axis_memo, WD_TAB_ALIGNMENT.RIGHT)
    r_rk = p_sig_rk.add_run(f"\t{sig1['rank']}")
    set_run_font(r_rk, "TH Sarabun PSK", 16)
    
    p_sig_nm = doc.add_paragraph()
    p_sig_nm.paragraph_format.space_before = Pt(0)
    p_sig_nm.paragraph_format.space_after = Pt(0)
    p_sig_nm.paragraph_format.tab_stops.add_tab_stop(axis_memo, WD_TAB_ALIGNMENT.LEFT)
    r_nm = p_sig_nm.add_run(f"\t({sig1['name']})")
    set_run_font(r_nm, "TH Sarabun PSK", 16)
    
    # Position: Centered under Name (space after 0)
    p_sig_pos = doc.add_paragraph()
    p_sig_pos.paragraph_format.space_before = Pt(0)
    p_sig_pos.paragraph_format.space_after = Pt(0)
    p_sig_pos.paragraph_format.tab_stops.add_tab_stop(axis_memo + Inches(0.92), WD_TAB_ALIGNMENT.CENTER)
    r_pos = p_sig_pos.add_run(f"\t{sig1['position']}")
    set_run_font(r_pos, "TH Sarabun PSK", 16)

    # FUNCTION TO RENDER LEGAL LANDSCAPE TRACKING FORM PAGES IN DOCX
    def add_docx_tracking_page(p_data):
        sec = doc.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENTATION.LANDSCAPE
        sec.page_width = Inches(14.0) # US Legal
        sec.page_height = Inches(8.5)
        sec.top_margin = Inches(0.59)
        sec.right_margin = Inches(0.59)
        sec.bottom_margin = Inches(0.5)
        sec.left_margin = Inches(0.59)

        h = p_data["header"]
        tbl_data = p_data["table"]
        sigs = p_data["signatures"]
        sig_cdr = next(s for s in sigs if s["role_key"] == "commander")
        sig_insp = next(s for s in sigs if s["role_key"] == "inspector")

        # Top header
        p_top = doc.add_paragraph()
        p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_fc = p_top.add_run(f'{p_data["form_code"]}\n{p_data["form_subcode"]}')
        set_run_font(r_fc, "TH Sarabun PSK", 12, bold=True)

        p_th = doc.add_paragraph()
        p_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_th.paragraph_format.space_after = Pt(2)
        r_th = p_th.add_run(p_data["title"])
        set_run_font(r_th, "TH Sarabun PSK", 18, bold=True)

        # Meta
        meta_items = [
            h["doc_number"],
            h["subject"],
            f'{h["to_label"]}   {h["to_value"]}',
            f'{h["from_label"]}   {h["from_value"]}',
            f'        {h["instruction"]}'
        ]
        for itm in meta_items:
            p_it = doc.add_paragraph()
            p_it.paragraph_format.space_after = Pt(1)
            p_it.paragraph_format.line_spacing = 1.15
            r_it = p_it.add_run(itm)
            set_run_font(r_it, "TH Sarabun PSK", 12)

        # Grid Table
        cols_w = [Inches(0.6), Inches(2.8), Inches(2.4), Inches(1.8), Inches(1.5), Inches(1.6), Inches(2.0)]
        t_form = doc.add_table(rows=1, cols=7)
        t_form.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        headers = ["ลำดับ", "รายการ สป.", "หมายเลข สป.", "ที่ใบเบิก ที่ทะเบียนหน่วย\nจ่าย", "วันที่ส่งหรือวางใบเบิก", tbl_data["columns"][5]["name"], "หมายเหตุ (บันทึกโดยหน่วยจ่าย)"]
        for c_i, h_txt in enumerate(headers):
            cell = t_form.cell(0, c_i)
            cell.width = cols_w[c_i]
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_c.add_run(h_txt)
            set_run_font(r_c, "TH Sarabun PSK", 11, bold=True)
            set_cell_border(cell, top={"val": "single", "sz": "4", "color": "000000"},
                                  bottom={"val": "single", "sz": "4", "color": "000000"},
                                  left={"val": "single", "sz": "4", "color": "000000"},
                                  right={"val": "single", "sz": "4", "color": "000000"})

        # Data Rows
        for r_data in tbl_data["rows"]:
            row = t_form.add_row()
            vals = [r_data["no"], r_data["item_name"], r_data["stock_no"], r_data["voucher_no"], r_data["submitted_date"], r_data["tracked_date"], r_data["note"]]
            aligns = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
            for c_i, val in enumerate(vals):
                cell = row.cells[c_i]
                cell.width = cols_w[c_i]
                p_c = cell.paragraphs[0]
                p_c.alignment = aligns[c_i]
                r_c = p_c.add_run(val)
                set_run_font(r_c, "TH Sarabun PSK", 11)
                set_cell_border(cell, top={"val": "single", "sz": "4", "color": "000000"},
                                      bottom={"val": "single", "sz": "4", "color": "000000"},
                                      left={"val": "single", "sz": "4", "color": "000000"},
                                      right={"val": "single", "sz": "4", "color": "000000"})

        # Pad rows
        for _ in range(max(0, 10 - len(tbl_data["rows"]))):
            row = t_form.add_row()
            for c_i in range(7):
                cell = row.cells[c_i]
                cell.width = cols_w[c_i]
                set_cell_border(cell, top={"val": "single", "sz": "4", "color": "000000"},
                                      bottom={"val": "single", "sz": "4", "color": "000000"},
                                      left={"val": "single", "sz": "4", "color": "000000"},
                                      right={"val": "single", "sz": "4", "color": "000000"})

        # Signatures 2 columns table
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(14)

        t_sig = doc.add_table(rows=1, cols=2)
        t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_left = t_sig.cell(0, 0)
        c_right = t_sig.cell(0, 1)
        c_left.width = Inches(6.0)
        c_right.width = Inches(6.0)

        # Left: Commander (ผบ.ร้อย) — Universal Signature Block Red Line Standard
        axis_cdr = Inches(3.0)
        
        p_l_top = c_left.paragraphs[0]
        p_l_top.paragraph_format.space_after = Pt(16)
        p_l_top.add_run("") # spacer matching inspector label height
        
        p_l_rk = c_left.add_paragraph()
        p_l_rk.paragraph_format.tab_stops.add_tab_stop(axis_cdr, WD_TAB_ALIGNMENT.RIGHT)
        p_l_rk.paragraph_format.space_before = Pt(0)
        p_l_rk.paragraph_format.space_after = Pt(22) # space for signature
        r_l_rk = p_l_rk.add_run(f"\t{sig_cdr['rank']}")
        set_run_font(r_l_rk, "TH Sarabun PSK", 12)

        p_l_nm = c_left.add_paragraph()
        p_l_nm.paragraph_format.tab_stops.add_tab_stop(axis_cdr, WD_TAB_ALIGNMENT.LEFT)
        p_l_nm.paragraph_format.space_before = Pt(0)
        p_l_nm.paragraph_format.space_after = Pt(0)
        r_l_nm = p_l_nm.add_run(f"\t({sig_cdr['name']})")
        set_run_font(r_l_nm, "TH Sarabun PSK", 12)

        cdr_center = axis_cdr + Inches(0.70)
        p_l_pos = c_left.add_paragraph()
        p_l_pos.paragraph_format.tab_stops.add_tab_stop(cdr_center, WD_TAB_ALIGNMENT.CENTER)
        p_l_pos.paragraph_format.space_before = Pt(0)
        p_l_pos.paragraph_format.space_after = Pt(0)
        r_l_pos = p_l_pos.add_run(f"\t{sig_cdr['position']}")
        set_run_font(r_l_pos, "TH Sarabun PSK", 12)

        p_l_dt = c_left.add_paragraph()
        p_l_dt.paragraph_format.tab_stops.add_tab_stop(cdr_center, WD_TAB_ALIGNMENT.CENTER)
        p_l_dt.paragraph_format.space_before = Pt(0)
        p_l_dt.paragraph_format.space_after = Pt(0)
        r_l_dt = p_l_dt.add_run(f"\t{sig_cdr['date']}")
        set_run_font(r_l_dt, "TH Sarabun PSK", 12)

        # Right: Inspector (ผู้ตรวจสอบ) — Universal Signature Block Red Line Standard
        axis_insp = Inches(3.0)

        p_r_lbl = c_right.paragraphs[0]
        p_r_lbl.paragraph_format.tab_stops.add_tab_stop(axis_insp - Inches(0.8), WD_TAB_ALIGNMENT.LEFT)
        p_r_lbl.paragraph_format.space_after = Pt(16)
        r_r_lbl = p_r_lbl.add_run(f"\t{sig_insp['label']}")
        set_run_font(r_r_lbl, "TH Sarabun PSK", 12, bold=True)

        p_r_rk = c_right.add_paragraph()
        p_r_rk.paragraph_format.tab_stops.add_tab_stop(axis_insp, WD_TAB_ALIGNMENT.RIGHT)
        p_r_rk.paragraph_format.space_before = Pt(0)
        p_r_rk.paragraph_format.space_after = Pt(22) # space for signature
        r_r_rk = p_r_rk.add_run(f"\t{sig_insp['rank']}")
        set_run_font(r_r_rk, "TH Sarabun PSK", 12)

        p_r_nm = c_right.add_paragraph()
        p_r_nm.paragraph_format.tab_stops.add_tab_stop(axis_insp, WD_TAB_ALIGNMENT.LEFT)
        p_r_nm.paragraph_format.space_before = Pt(0)
        p_r_nm.paragraph_format.space_after = Pt(0)
        r_r_nm = p_r_nm.add_run(f"\t({sig_insp['name']})")
        set_run_font(r_r_nm, "TH Sarabun PSK", 12)

        insp_center = axis_insp + Inches(0.67)
        p_r_pos = c_right.add_paragraph()
        p_r_pos.paragraph_format.tab_stops.add_tab_stop(insp_center, WD_TAB_ALIGNMENT.CENTER)
        p_r_pos.paragraph_format.space_before = Pt(0)
        p_r_pos.paragraph_format.space_after = Pt(0)
        r_r_pos = p_r_pos.add_run(f"\t{sig_insp['position']}")
        set_run_font(r_r_pos, "TH Sarabun PSK", 12)

        p_r_dt = c_right.add_paragraph()
        p_r_dt.paragraph_format.tab_stops.add_tab_stop(insp_center, WD_TAB_ALIGNMENT.CENTER)
        p_r_dt.paragraph_format.space_before = Pt(0)
        p_r_dt.paragraph_format.space_after = Pt(0)
        r_r_dt = p_r_dt.add_run(f"\t{sig_insp['date']}")
        set_run_font(r_r_dt, "TH Sarabun PSK", 12)

        set_cell_border(c_left)
        set_cell_border(c_right)

        # Footer Note
        p_fn = doc.add_paragraph()
        p_fn.paragraph_format.space_before = Pt(18)
        p_fn.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_fn = p_fn.add_run(p_data["footer_note"])
        set_run_font(r_fn, "TH Sarabun PSK", 10.5)

    add_docx_tracking_page(bp["pages"][1])
    add_docx_tracking_page(bp["pages"][2])

    doc.save(output_path)
    print(f"Generated DOCX: {output_path}")


# -----------------------------------------------------------------------------
# 3. GENERATE XLSX
# -----------------------------------------------------------------------------
def generate_xlsx(output_path):
    wb = openpyxl.Workbook()
    # Sheet 1: บันทึกข้อความ
    ws1 = wb.active
    ws1.title = "บันทึกข้อความ"
    ws1.views.sheetView[0].showGridLines = True

    c1 = bp["pages"][0]["content"]
    sig1 = c1["signature"]

    font_regular = Font(name="TH Sarabun PSK", size=12)
    font_bold = Font(name="TH Sarabun PSK", size=12, bold=True)
    font_large_bold = Font(name="TH Sarabun PSK", size=18, bold=True)
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws1["C4"] = c1["title"]
    ws1["C4"].font = font_large_bold
    ws1["C4"].alignment = align_center

    memo_rows = [
        ("ส่วนราชการ", c1["department_value"]),
        ("ที่", f'{c1["doc_number_value"]}       วันที่            {c1["doc_date_month_year"]}'),
        ("เรื่อง", c1["subject_value"]),
        ("เรียน", c1["recipient_value"]),
        ("อ้างถึง", c1["reference_value"]),
        ("สิ่งที่ส่งมาด้วย", f'{c1["attachments"][0]["title"]}   {c1["attachments"][0]["quantity"]}'),
        ("", c1["paragraphs"][0]),
        ("", c1["paragraphs"][1])
    ]

    for idx, (lbl, val) in enumerate(memo_rows, start=6):
        ws1[f"B{idx}"] = lbl
        ws1[f"B{idx}"].font = font_bold
        ws1[f"C{idx}"] = val
        ws1[f"C{idx}"].font = font_regular
        ws1.row_dimensions[idx].height = 28

    ws1["D18"] = sig1["rank"]
    ws1["D18"].font = font_regular
    ws1["D18"].alignment = Alignment(horizontal="right", vertical="center")

    ws1["E18"] = f'({sig1["name"]})'
    ws1["E18"].font = font_regular
    ws1["E18"].alignment = Alignment(horizontal="left", vertical="center")

    ws1["D19"] = sig1["position"]
    ws1["D19"].font = font_regular
    ws1["D19"].alignment = align_center
    ws1.merge_cells("D19:E19")

    ws1.column_dimensions["A"].width = 5
    ws1.column_dimensions["B"].width = 18
    ws1.column_dimensions["C"].width = 50
    ws1.column_dimensions["D"].width = 30
    ws1.column_dimensions["E"].width = 25

    # Sheet 2 & 3: ใบติดตามใบเบิก
    def add_xlsx_tracking_sheet(p_data, sheet_title):
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        h = p_data["header"]
        tbl = p_data["table"]
        sigs = p_data["signatures"]
        sig_cdr = next(s for s in sigs if s["role_key"] == "commander")
        sig_insp = next(s for s in sigs if s["role_key"] == "inspector")

        thin = Side(style='thin', color='000000')
        border_all = Border(left=thin, right=thin, top=thin, bottom=thin)

        # Header
        ws["D2"] = p_data["title"]
        ws["D2"].font = font_large_bold
        ws["D2"].alignment = align_center

        ws["G2"] = f'{p_data["form_code"]}\n{p_data["form_subcode"]}'
        ws["G2"].font = font_bold
        ws["G2"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)

        ws["B4"] = h["doc_number"]
        ws["B4"].font = font_regular
        ws["B5"] = h["subject"]
        ws["B5"].font = font_regular
        ws["B6"] = f'{h["to_label"]}   {h["to_value"]}'
        ws["B6"].font = font_regular
        ws["B7"] = f'{h["from_label"]}   {h["from_value"]}'
        ws["B7"].font = font_regular
        ws["B8"] = f'        {h["instruction"]}'
        ws["B8"].font = font_regular

        # Table Header
        headers = ["ลำดับ", "รายการ สป.", "หมายเลข สป.", "ที่ใบเบิก ที่ทะเบียนหน่วยจ่าย", "วันที่ส่งหรือวางใบเบิก", tbl["columns"][5]["name"], "หมายเหตุ (บันทึกโดยหน่วยจ่าย)"]
        cols = ["A", "B", "C", "D", "E", "F", "G"]
        for col_letter, h_txt in zip(cols, headers):
            cell = ws[f"{col_letter}10"]
            cell.value = h_txt
            cell.font = font_bold
            cell.alignment = align_center
            cell.border = border_all
        ws.row_dimensions[10].height = 28

        # Table Data
        for r_idx, r_data in enumerate(tbl["rows"], start=11):
            vals = [r_data["no"], r_data["item_name"], r_data["stock_no"], r_data["voucher_no"], r_data["submitted_date"], r_data["tracked_date"], r_data["note"]]
            for c_idx, (col_letter, val) in enumerate(zip(cols, vals)):
                cell = ws[f"{col_letter}{r_idx}"]
                cell.value = val
                cell.font = font_regular
                cell.border = border_all
                if c_idx in [0, 2, 3, 4, 5]:
                    cell.alignment = align_center
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center")
            ws.row_dimensions[r_idx].height = 22

        # Signatures (Universal Signature Block Red Line Standard in XLSX)
        last_r = 11 + len(tbl["rows"]) + 2

        # Left: Commander
        ws[f"B{last_r}"] = sig_cdr["rank"]
        ws[f"B{last_r}"].font = font_regular
        ws[f"B{last_r}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"C{last_r}"] = f'({sig_cdr["name"]})'
        ws[f"C{last_r}"].font = font_regular
        ws[f"C{last_r}"].alignment = Alignment(horizontal="left", vertical="center")

        ws[f"B{last_r+1}"] = sig_cdr["position"]
        ws[f"B{last_r+1}"].font = font_regular
        ws[f"B{last_r+1}"].alignment = align_center
        ws.merge_cells(f"B{last_r+1}:C{last_r+1}")

        ws[f"B{last_r+2}"] = sig_cdr["date"]
        ws[f"B{last_r+2}"].font = font_regular
        ws[f"B{last_r+2}"].alignment = align_center
        ws.merge_cells(f"B{last_r+2}:C{last_r+2}")

        # Right: Inspector
        ws[f"E{last_r-1}"] = sig_insp["label"]
        ws[f"E{last_r-1}"].font = font_bold
        ws[f"E{last_r-1}"].alignment = Alignment(horizontal="left", vertical="center")

        ws[f"E{last_r}"] = sig_insp["rank"]
        ws[f"E{last_r}"].font = font_regular
        ws[f"E{last_r}"].alignment = Alignment(horizontal="right", vertical="center")

        ws[f"F{last_r}"] = f'({sig_insp["name"]})'
        ws[f"F{last_r}"].font = font_regular
        ws[f"F{last_r}"].alignment = Alignment(horizontal="left", vertical="center")

        ws[f"E{last_r+1}"] = sig_insp["position"]
        ws[f"E{last_r+1}"].font = font_regular
        ws[f"E{last_r+1}"].alignment = align_center
        ws.merge_cells(f"E{last_r+1}:F{last_r+1}")

        ws[f"E{last_r+2}"] = sig_insp["date"]
        ws[f"E{last_r+2}"].font = font_regular
        ws[f"E{last_r+2}"].alignment = align_center
        ws.merge_cells(f"E{last_r+2}:F{last_r+2}")

        ws.column_dimensions["A"].width = 8
        ws.column_dimensions["B"].width = 32
        ws.column_dimensions["C"].width = 28
        ws.column_dimensions["D"].width = 24
        ws.column_dimensions["E"].width = 20
        ws.column_dimensions["F"].width = 22
        ws.column_dimensions["G"].width = 25

    add_xlsx_tracking_sheet(bp["pages"][1], "ใบติดตามใบเบิก แผ่น 1")
    add_xlsx_tracking_sheet(bp["pages"][2], "ใบติดตามใบเบิก แผ่น 2")

    wb.save(output_path)
    print(f"Generated XLSX: {output_path}")


# -----------------------------------------------------------------------------
# MAIN COMPILER
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    html_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html")
    docx_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx")
    xlsx_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx")

    generate_html(html_out)
    generate_docx(docx_out)
    generate_xlsx(xlsx_out)
    print("Compiled all formats successfully!")
