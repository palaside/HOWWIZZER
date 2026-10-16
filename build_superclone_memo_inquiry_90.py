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

import signature_engine

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

        # Table rows HTML (7 columns for 90 days)
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
        # Fill empty rows up to 7 rows (deleting bottom rows to fit exactly 7 rows on page)
        current_rows = len(tbl["rows"])
        for _ in range(max(0, 7 - current_rows)):
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

        # HTML Signature Blocks via signature_engine.py with font_size_pt=17
        sig_cdr_html = f"""
        <div class="sig-block" style="font-size: 17pt; line-height: 1.0;">
            <div style="height: 17pt; margin-bottom: 18pt; visibility: hidden;">&nbsp;</div>
            <div class="sig-name-pos-group" style="margin-left: 45px;">
                <div class="sig-name-wrapper" style="margin-top: 18pt;">
                    <span class="sig-rank-anchor" style="font-size: 17pt;">{sig_cdr['rank']}</span>
                    <div class="sig-name" style="font-size: 17pt;">({sig_cdr['name']})</div>
                </div>
                <div class="sig-pos" style="font-size: 17pt;">{sig_cdr['position']}</div>
                <div class="sig-date" style="margin-top: 4px; font-size: 17pt; text-align: center; white-space: nowrap;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{sig_cdr['date']}</div>
            </div>
        </div>
        """.strip()

        sig_insp_html = f"""
        <div class="sig-block" style="font-size: 17pt; line-height: 1.0;">
            <div class="sig-verify" style="font-weight: 600; margin-bottom: 18pt; font-size: 17pt; text-align: left;">{sig_insp.get('label', 'ผู้ตรวจสอบ')}</div>
            <div class="sig-name-pos-group" style="margin-left: 45px;">
                <div class="sig-name-wrapper" style="margin-top: 18pt;">
                    <span class="sig-rank-anchor" style="font-size: 17pt;">{sig_insp['rank']}</span>
                    <div class="sig-name" style="font-size: 17pt;">({sig_insp['name']})</div>
                </div>
                <div class="sig-pos" style="font-size: 17pt;">{sig_insp['position']}</div>
                <div class="sig-date" style="margin-top: 4px; font-size: 17pt; text-align: center; white-space: nowrap;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{sig_insp['date']}</div>
            </div>
        </div>
        """.strip()

        return f"""
        <div class="page-legal-landscape" id="{page_id}">
            <!-- Form Top Header -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2mm;">
                <div></div>
                <div style="font-size: 20pt; font-weight: 600; text-align: center; margin-left: 60mm;">
                    {p_data["title"]}
                </div>
                <div style="text-align: right; font-size: 14pt; line-height: 1.2;">
                    <div style="font-weight: 600;">{p_data["form_code"]}</div>
                    <div>{p_data["form_subcode"]}</div>
                </div>
            </div>

            <!-- Meta block -->
            <div style="margin-bottom: 3mm; font-size: 17pt; line-height: 1.35;">
                <div style="margin-bottom: 1mm;">{h["doc_number"]}</div>
                <div style="margin-bottom: 1mm;">{h["subject"]}</div>
                <div style="margin-bottom: 1mm;">
                    <span style="font-weight: 600; display: inline-block; width: 14mm;">{h["to_label"]}</span>
                    <span>{h["to_value"]}</span>
                </div>
                <div style="margin-bottom: 2mm;">
                    <span style="font-weight: 600; display: inline-block; width: 14mm;">{h["from_label"]}</span>
                    <span>{h["from_value"]}</span>
                </div>
                <div style="padding-left: 20mm; margin-top: 2mm; margin-bottom: 3mm;">
                    {h["instruction"]}
                </div>
            </div>

            <!-- Table (7 columns) -->
            <table class="grid-table">
                <thead>
                    <tr>
                        <th style="width: 4%;">ลำดับ</th>
                        <th style="width: 18%;">รายการ สป.</th>
                        <th style="width: 16%;">หมายเลข สป.</th>
                        <th style="width: 20%; white-space: nowrap;">ที่ใบเบิก ที่ทะเบียนหน่วยจ่าย</th>
                        <th style="width: 13%;">วันที่ส่งหรือวางใบเบิก</th>
                        <th style="width: 14%;">{tbl["columns"][5]["name"]}</th>
                        <th style="width: 15%;">หมายเหตุ  (บันทึกโดยหน่วยจ่าย)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>

            <!-- Double Signature Block (Universal Red Line Standard) -->
            <div style="display: flex; justify-content: space-between; margin-top: 6mm; padding: 0 20mm;">
                <!-- Left: Commander (ผบ.ร้อย / นยส.) -->
                <div style="width: 45%; display: flex; justify-content: center;">
                    {sig_cdr_html}
                </div>

                <!-- Right: Inspector (ผู้ตรวจสอบ) -->
                <div style="width: 45%; display: flex; justify-content: center;">
                    {sig_insp_html}
                </div>
            </div>

            <!-- Footer note (เลื่อนขึ้นมา 1 บรรทัด) -->
            <div style="text-align: center; margin-top: 4mm; font-size: 12pt;">
                {p_data["footer_note"]}
            </div>
        </div>
        """

    p2_html = render_tracking_page(p2, "page-2")
    p3_html = render_tracking_page(p3, "page-3")

    sig1_html = f"""
    <div class="sig-block" style="font-size: 17pt; line-height: 1.0;">
        <div class="sig-name-pos-group" style="margin-left: 45px;">
            <div class="sig-name-wrapper" style="margin-top: 22pt;">
                <span class="sig-rank-anchor" style="font-size: 17pt;">{sig1['rank']}</span>
                <div class="sig-name" style="font-size: 17pt;">({sig1['name']})</div>
            </div>
            <div class="sig-pos" style="font-size: 17pt;">{sig1['position']}</div>
        </div>
    </div>
    """.strip()

    # Admin footer on page 1 - RULE-STAFF-REVIEW-FOOTER-V1: exactly 5 Enter (22mm) under commander signature
    admin_footer_html = f"""
    <div class="memo-footer-staff">
        <div class="staff-grid">
            <div>{c1["admin_footer"][0]["rank"]}</div>
            <div>{c1["admin_footer"][0]["role"]}</div>
            <div style="text-align: right;"></div>
            <div style="padding-left: 2mm;">{c1["admin_footer"][0]["date"]}</div>

            <div>{c1["admin_footer"][1]["rank"]}</div>
            <div>{c1["admin_footer"][1]["role"]}</div>
            <div style="text-align: right;">{c1["admin_footer"][1]["day"]}</div>
            <div style="padding-left: 2mm;">{c1["admin_footer"][1]["date"]}</div>
        </div>
    </div>
    """

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{bp["document_title"]}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,600;0,700;1,100;1,300;1,400;1,700&display=swap" rel="stylesheet">
    <style>
        /* ======================================================== */
        /* OFFICIAL GOVERNMENT TH SARABUN PSK ENGINE (PRIMARY SSOT) */
        /* ======================================================== */
        @font-face {{
            font-family: 'TH Sarabun PSK';
            font-style: normal;
            font-weight: 400;
            src: local('TH Sarabun PSK'), local('THSarabunPSK'),
                 url('/fonts/THSarabunPSK.ttf') format('truetype'),
                 url('fonts/THSarabunPSK.ttf') format('truetype'),
                 url('../fonts/THSarabunPSK.ttf') format('truetype'),
                 url('../../fonts/THSarabunPSK.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'TH Sarabun PSK';
            font-style: normal;
            font-weight: 300;
            src: local('TH Sarabun PSK'), local('THSarabunPSK'),
                 url('/fonts/THSarabunPSK.ttf') format('truetype'),
                 url('fonts/THSarabunPSK.ttf') format('truetype'),
                 url('../fonts/THSarabunPSK.ttf') format('truetype'),
                 url('../../fonts/THSarabunPSK.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'TH Sarabun PSK';
            font-style: normal;
            font-weight: 600;
            src: local('TH Sarabun PSK Bold'), local('THSarabunPSK-Bold'),
                 url('/fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('../fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('../../fonts/THSarabunPSK-Bold.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'TH Sarabun PSK';
            font-style: normal;
            font-weight: 700;
            src: local('TH Sarabun PSK Bold'), local('THSarabunPSK-Bold'),
                 url('/fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('../fonts/THSarabunPSK-Bold.ttf') format('truetype'),
                 url('../../fonts/THSarabunPSK-Bold.ttf') format('truetype');
        }}

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
            font-family: 'TH Sarabun PSK', 'THSarabunPSK', 'TH Sarabun New', 'THSarabunNew', 'Sarabun', sans-serif;
        }}
        body {{
            margin: 0;
            padding: 20px 0;
            background-color: #525659;
            font-family: 'TH Sarabun PSK', 'THSarabunPSK', 'TH Sarabun New', 'THSarabunNew', 'Sarabun', sans-serif;
            font-size: 17pt;
            font-weight: normal;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
            color: #000000;
            line-height: 1.25;
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
            padding: 15mm 15mm 15mm 25mm; /* Top 1.5cm, Right 1.5cm, Bottom 1.5cm, Left 2.5cm */
            overflow: hidden;
            page-break-after: always;
            page: portrait-page;
            font-size: 17pt;
            line-height: 1.25;
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
            font-size: 17pt;
            line-height: 1.25;
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
        .font-bold {{ font-weight: 600; }}

        /* MEMO HEADER */
        .memo-copy-label {{
            text-align: center;
            font-size: 13pt;
            margin-bottom: 2mm;
        }}
        .memo-header-container {{
            position: relative;
            width: 100%;
            height: 30mm;
            margin-top: 0mm;
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
            font-size: 29pt;
            font-weight: 600;
            line-height: 1;
            font-family: 'TH Sarabun PSK', 'THSarabunNew', 'Sarabun', sans-serif;
        }}
        .memo-meta-label {{
            font-size: 20pt;
            font-weight: 600;
            line-height: 1.05;
            padding-bottom: 1.5px;
            white-space: nowrap;
        }}
        .memo-meta-dots {{
            border-bottom: 1px dotted #000;
            padding-left: 2mm;
            padding-bottom: 1.5px;
            font-size: 17pt;
            line-height: 1.05;
        }}
        .memo-content {{
            margin-top: 2mm;
            font-size: 17pt;
            line-height: 1.25;
        }}
        .memo-p {{
            text-indent: 2.5cm;
            margin: 0 0 1.5mm 0;
            text-align: justify;
            text-justify: inter-cluster; word-break: keep-all; overflow-wrap: break-word;
            line-height: 1.25;
            font-size: 17pt;
        }}

        /* UNIVERSAL SIGNATURE BLOCK (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .sig-block {{
            display: inline-flex;
            flex-direction: column;
            align-items: flex-start;
            position: relative;
            min-width: 220px;
            font-size: 17pt;
            line-height: 1.2;
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
            margin-top: 18pt;
        }}
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 18px);
            white-space: nowrap;
            font-size: 17pt;
            line-height: 1.2;
        }}
        .sig-name {{
            margin: 0;
            line-height: 1.2;
            text-align: center;
            white-space: nowrap;
            font-size: 17pt;
            display: block;
        }}
        .sig-pos {{
            margin: 0;
            line-height: 1.2;
            text-align: center;
            white-space: nowrap;
            font-size: 17pt;
            display: block;
        }}

        /* STAFF INITIALS FOOTER (RULE-STAFF-REVIEW-FOOTER-V1: Mandatory 4-Column Dual-Axis) */
        .memo-footer-staff {{
            margin-top: 22mm; /* อยู่ใต้ ผบ.ป.๔ พัน.๔ ร้อย.๒ ๕ เอนเตอร์ */
            display: flex;
            justify-content: flex-end;
        }}
        .staff-grid {{
            display: grid;
            grid-template-columns: 26mm 22mm 8mm 20mm;
            font-size: 13.5pt;
            font-weight: 300;
            line-height: 1.25;
            text-align: left;
        }}

        /* TABLE STYLES (LEGAL LANDSCAPE) - Scaled down 5% to prevent signature overflow */
        table.grid-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 16.15pt;
            margin-top: 2mm;
        }}
        table.grid-table th, table.grid-table td {{
            border: 1px solid #000000;
            padding: 1.1mm 1.5mm;
            vertical-align: middle;
        }}
        table.grid-table th {{
            text-align: center;
            font-weight: 600;
            font-size: 16.15pt;
            background-color: #ffffff;
        }}
        table.grid-table td {{
            font-size: 16.15pt;
        }}

        /* RULE 9: THIN FONT-WEIGHT STANDARD (font-weight: 300 for non-headings) */
        p, span, td, .memo-p, .memo-content, .memo-att-row, .memo-att-desc, .memo-att-qty,
        .sig-rank-anchor, .sig-name, .sig-pos, .staff-grid, .staff-grid div {{
            font-weight: 300;
        }}

        .memo-title, .memo-meta-label, th, table.grid-table th,
        .font-bold, b, strong, .sig-verify {{
            font-weight: 600;
        }}
    </style>
</head>
<body>

    <!-- PAGE 1: บันทึกข้อความ (A4 Portrait) -->
    <div class="page-portrait" id="page-1">
        <div class="memo-copy-label">( สำเนาคู่ฉบับ )</div>
        <div class="memo-header-container">
            <img class="memo-garuda" src="data:image/png;base64,{GARUDA_B64}" alt="ตราครุฑ">
            <div class="memo-title">{c1["title"]}</div>
        </div>

        <div style="margin-top: 2mm; font-size: 17pt; line-height: 1.25;">
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
            <!-- เรื่อง -->
            <div style="display: flex; align-items: baseline; margin-bottom: 1.5mm;">
                <span class="memo-meta-label" style="margin-right: 2mm;">{c1["subject_label"]}</span>
                <div class="memo-meta-dots" style="flex: 1;">{c1["subject_value"]}</div>
            </div>
        </div>

        <div class="memo-content">
            <div style="margin-bottom: 2mm; font-size: 17pt;">
                <span class="font-bold">{c1["recipient_label"]}</span>&nbsp;&nbsp;{c1["recipient_value"]}
            </div>
            <div style="margin-bottom: 2mm; font-size: 17pt;">
                <span class="font-bold">{c1["reference_label"]}</span>&nbsp;&nbsp;{c1["reference_value"]}
            </div>

            <div style="margin: 0 0 2.5mm 0; font-size: 17pt; line-height: 1.25;">
                <table style="width: 100%; border-collapse: collapse; font-size: 17pt; line-height: 1.25;">
                    <tr>
                        <td style="width: 32mm; vertical-align: top; white-space: nowrap;"><span class="font-bold">{c1["attachments_label"]}</span></td>
                        <td style="vertical-align: top; font-size: 17pt;">{c1["attachments"][0]["title"]}</td>
                        <td style="width: 35mm; vertical-align: top; text-align: right; white-space: nowrap; font-size: 17pt;">{c1["attachments"][0]["quantity"]}</td>
                    </tr>
                </table>
            </div>

            <p class="memo-p" style="font-size: 17pt; line-height: 1.25;">{c1["paragraphs"][0]}</p>
            <p class="memo-p" style="font-size: 17pt; line-height: 1.25;">{c1["paragraphs"][1]}</p>
        </div>

        <!-- SIGNATURE BLOCK (RULE: เคาะ 5 Enter จากบรรทัดสุดท้าย, พิกัดซ้าย 130 มม. - Margin ซ้าย 25 มม. = padding-left 105 มม.) -->
        <div style="margin-top: 55pt; padding-left: 105mm;">
            {sig1_html}
        </div>

        <!-- ADMIN FOOTER BLOCK -->
        {admin_footer_html}
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
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = parse_xml(r'<%s %s %s/>' % (tag, nsdecls('w'),
                ''.join(['w:{}="{}" '.format(k, v) for k, v in edge_data.items()])))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def set_run_font(run, font_name="TH Sarabun PSK", size_pt=16, bold=False, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run._r.get_or_add_rPr().append(
        parse_xml(r'<w:rFonts %s w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (nsdecls('w'), font_name, font_name, font_name))
    )

def generate_docx(output_path):
    doc = Document()

    # SECTION 1: A4 PORTRAIT (บันทึกข้อความ)
    sec1 = doc.sections[0]
    sec1.orientation = WD_ORIENTATION.PORTRAIT
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.top_margin = Inches(0.59)
    sec1.right_margin = Inches(0.59)
    sec1.bottom_margin = Inches(0.59)
    sec1.left_margin = Inches(0.98) # 2.5 cm

    p1 = bp["pages"][0]
    c1 = p1["content"]
    sig1 = c1["signature"]

    # Header Copy Label
    p_copy = doc.add_paragraph()
    p_copy.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_copy.paragraph_format.space_after = Pt(2)
    r_copy = p_copy.add_run("( สำเนาคู่ฉบับ )")
    set_run_font(r_copy, "TH Sarabun PSK", 13)

    # Garuda + Title Table
    t_hdr = doc.add_table(rows=1, cols=2)
    t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_img = t_hdr.cell(0, 0)
    c_title = t_hdr.cell(0, 1)
    c_img.width = Inches(1.2)
    c_title.width = Inches(5.5)

    p_img = c_img.paragraphs[0]
    p_img.paragraph_format.space_after = Pt(0)
    r_img = p_img.add_run()
    r_img.add_picture(GARUDA_PATH, width=Inches(1.18), height=Inches(1.18))

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
        p_m.paragraph_format.line_spacing = 1.25
        r_lbl = p_m.add_run(label + "  ")
        set_run_font(r_lbl, "TH Sarabun PSK", 17, bold=True)
        r_val = p_m.add_run(val)
        set_run_font(r_val, "TH Sarabun PSK", 17)

    # Attachments
    p_att = doc.add_paragraph()
    p_att.paragraph_format.space_after = Pt(2)
    p_att.paragraph_format.line_spacing = 1.25
    r_al = p_att.add_run(c1["attachments_label"] + "  ")
    set_run_font(r_al, "TH Sarabun PSK", 17, bold=True)
    r_av = p_att.add_run(f'{c1["attachments"][0]["title"]}     {c1["attachments"][0]["quantity"]}')
    set_run_font(r_av, "TH Sarabun PSK", 17)

    # Paragraphs
    for para in c1["paragraphs"]:
        p_p = doc.add_paragraph()
        p_p.paragraph_format.first_line_indent = Inches(0.98)
        p_p.paragraph_format.space_after = Pt(4)
        p_p.paragraph_format.line_spacing = 1.25
        p_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_p = p_p.add_run(para)
        set_run_font(r_p, "TH Sarabun PSK", 17)

    # Signature Block via signature_engine.py
    signature_engine.render_signature_docx(
        doc,
        sig1,
        axis_inch=4.13,
        font_name="TH Sarabun PSK",
        font_size=17,
        space_after_rank_pt=22,
        space_before_block_pt=55
    )

    # Admin Footer Block
    p_adm1 = doc.add_paragraph()
    p_adm1.paragraph_format.space_before = Pt(30)
    p_adm1.paragraph_format.space_after = Pt(0)
    p_adm1.paragraph_format.tab_stops.add_tab_stop(Inches(4.5), WD_TAB_ALIGNMENT.LEFT)
    p_adm1.paragraph_format.tab_stops.add_tab_stop(Inches(5.5), WD_TAB_ALIGNMENT.LEFT)
    p_adm1.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.LEFT)
    r_adm1 = p_adm1.add_run(f"\t{c1['admin_footer'][0]['rank']}\t{c1['admin_footer'][0]['role']}\t{c1['admin_footer'][0]['date']}")
    set_run_font(r_adm1, "TH Sarabun PSK", 13.5)

    p_adm2 = doc.add_paragraph()
    p_adm2.paragraph_format.space_before = Pt(0)
    p_adm2.paragraph_format.space_after = Pt(0)
    p_adm2.paragraph_format.tab_stops.add_tab_stop(Inches(4.5), WD_TAB_ALIGNMENT.LEFT)
    p_adm2.paragraph_format.tab_stops.add_tab_stop(Inches(5.5), WD_TAB_ALIGNMENT.LEFT)
    p_adm2.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.LEFT)
    r_adm2 = p_adm2.add_run(f"\t{c1['admin_footer'][1]['rank']}\t{c1['admin_footer'][1]['role']}\t{c1['admin_footer'][1]['date']}")
    set_run_font(r_adm2, "TH Sarabun PSK", 13.5)

    # FUNCTION TO RENDER LEGAL LANDSCAPE TRACKING FORM PAGES IN DOCX
    def add_docx_tracking_page(p_data):
        sec = doc.add_section(WD_SECTION.NEW_PAGE)
        sec.orientation = WD_ORIENTATION.LANDSCAPE
        sec.page_width = Inches(14.0) # US Legal
        sec.page_height = Inches(8.5)
        sec.top_margin = Inches(0.39)
        sec.right_margin = Inches(0.59)
        sec.bottom_margin = Inches(0.39)
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
        set_run_font(r_fc, "TH Sarabun PSK", 14, bold=True)

        p_th = doc.add_paragraph()
        p_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_th.paragraph_format.space_after = Pt(2)
        r_th = p_th.add_run(p_data["title"])
        set_run_font(r_th, "TH Sarabun PSK", 20, bold=True)

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
            set_run_font(r_it, "TH Sarabun PSK", 17)

        # Grid Table (7 columns for 90 days)
        cols_w = [Inches(0.5), Inches(2.3), Inches(2.0), Inches(2.5), Inches(1.8), Inches(1.8), Inches(1.9)]
        t_form = doc.add_table(rows=1, cols=7)
        t_form.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        headers = ["ลำดับ", "รายการ สป.", "หมายเลข สป.", "ที่ใบเบิก ที่ทะเบียนหน่วยจ่าย", "วันที่ส่งหรือวางใบเบิก", tbl_data["columns"][5]["name"], "หมายเหตุ (บันทึกโดยหน่วยจ่าย)"]
        for c_i, h_txt in enumerate(headers):
            cell = t_form.cell(0, c_i)
            cell.width = cols_w[c_i]
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_c.add_run(h_txt)
            set_run_font(r_c, "TH Sarabun PSK", 13.5, bold=True)
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
                set_run_font(r_c, "TH Sarabun PSK", 13.5)
                set_cell_border(cell, top={"val": "single", "sz": "4", "color": "000000"},
                                      bottom={"val": "single", "sz": "4", "color": "000000"},
                                      left={"val": "single", "sz": "4", "color": "000000"},
                                      right={"val": "single", "sz": "4", "color": "000000"})

        # Pad rows up to 7
        for _ in range(max(0, 7 - len(tbl_data["rows"]))):
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
        p_sp.paragraph_format.space_before = Pt(10)

        t_sig = doc.add_table(rows=1, cols=2)
        t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
        c_left = t_sig.cell(0, 0)
        c_right = t_sig.cell(0, 1)
        c_left.width = Inches(6.0)
        c_right.width = Inches(6.0)

        # Left: Commander (ผบ.ร้อย / นยส.) — via signature_engine.py
        sig_cdr_copy = dict(sig_cdr)
        sig_cdr_copy["add_top_spacer"] = True
        signature_engine.render_signature_docx(
            c_left,
            sig_cdr_copy,
            axis_inch=3.0,
            font_name="TH Sarabun PSK",
            font_size=16,
            space_after_rank_pt=18,
            space_before_block_pt=0
        )

        # Right: Inspector (ผู้ตรวจสอบ) — via signature_engine.py
        signature_engine.render_signature_docx(
            c_right,
            sig_insp,
            axis_inch=3.0,
            font_name="TH Sarabun PSK",
            font_size=16,
            space_after_rank_pt=18,
            space_before_block_pt=0
        )

        # Footer Note
        p_ft = doc.add_paragraph()
        p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ft.paragraph_format.space_before = Pt(8)
        r_ft = p_ft.add_run(p_data["footer_note"])
        set_run_font(r_ft, "TH Sarabun PSK", 12)

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

    p1 = bp["pages"][0]
    c1 = p1["content"]
    sig1 = c1["signature"]

    font_large_bold = Font(name="TH Sarabun PSK", size=24, bold=True)
    font_bold = Font(name="TH Sarabun PSK", size=16, bold=True)
    font_regular = Font(name="TH Sarabun PSK", size=16)
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")

    ws1["A1"] = "( สำเนาคู่ฉบับ )"
    ws1["A1"].font = Font(name="TH Sarabun PSK", size=13)
    ws1["A1"].alignment = align_center
    ws1.merge_cells("A1:E1")

    ws1["B3"] = c1["title"]
    ws1["B3"].font = font_large_bold
    ws1["B3"].alignment = align_center
    ws1.merge_cells("B3:D3")

    ws1["B5"] = c1["official_department"]
    ws1["B5"].font = font_bold
    ws1["C5"] = c1["department_value"]
    ws1["C5"].font = font_regular

    ws1["B6"] = c1["doc_number_label"]
    ws1["B6"].font = font_bold
    ws1["C6"] = c1["doc_number_value"]
    ws1["C6"].font = font_regular
    ws1["D6"] = c1["doc_date_label"]
    ws1["D6"].font = font_bold
    ws1["E6"] = c1["doc_date_month_year"]
    ws1["E6"].font = font_regular

    ws1["B7"] = c1["subject_label"]
    ws1["B7"].font = font_bold
    ws1["C7"] = c1["subject_value"]
    ws1["C7"].font = font_regular

    ws1["B8"] = c1["recipient_label"]
    ws1["B8"].font = font_bold
    ws1["C8"] = c1["recipient_value"]
    ws1["C8"].font = font_regular

    ws1["B9"] = c1["reference_label"]
    ws1["B9"].font = font_bold
    ws1["C9"] = c1["reference_value"]
    ws1["C9"].font = font_regular

    ws1["B10"] = c1["attachments_label"]
    ws1["B10"].font = font_bold
    ws1["C10"] = f"{c1['attachments'][0]['title']}   {c1['attachments'][0]['quantity']}"
    ws1["C10"].font = font_regular

    ws1["B12"] = c1["paragraphs"][0]
    ws1["B12"].font = font_regular
    ws1["B13"] = c1["paragraphs"][1]
    ws1["B13"].font = font_regular

    # Signature via signature_engine.py
    signature_engine.render_signature_xlsx(
        ws1,
        sig1,
        start_row=16,
        rank_col="D",
        name_col="E",
        font_name="TH Sarabun PSK",
        font_size=16
    )

    # Admin footer in Excel
    ws1["D22"] = c1["admin_footer"][0]["rank"]
    ws1["D22"].font = font_regular
    ws1["E22"] = f"{c1['admin_footer'][0]['role']}    {c1['admin_footer'][0]['date']}"
    ws1["E22"].font = font_regular

    ws1["D23"] = c1["admin_footer"][1]["rank"]
    ws1["D23"].font = font_regular
    ws1["E23"] = f"{c1['admin_footer'][1]['role']}  {c1['admin_footer'][1]['day']}    {c1['admin_footer'][1]['date']}"
    ws1["E23"].font = font_regular

    ws1.column_dimensions["A"].width = 5
    ws1.column_dimensions["B"].width = 18
    ws1.column_dimensions["C"].width = 50
    ws1.column_dimensions["D"].width = 25
    ws1.column_dimensions["E"].width = 30

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

        # Table Header (7 columns)
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

        start_sig_row = 11 + len(tbl["rows"]) + 2

        # Signatures via signature_engine.py
        # Left signature in B:C
        signature_engine.render_signature_xlsx(
            ws,
            sig_cdr,
            start_row=start_sig_row,
            rank_col="B",
            name_col="C",
            font_name="TH Sarabun PSK",
            font_size=16
        )

        # Right signature in F:G
        signature_engine.render_signature_xlsx(
            ws,
            sig_insp,
            start_row=start_sig_row,
            rank_col="F",
            name_col="G",
            font_name="TH Sarabun PSK",
            font_size=16
        )

        # Footer note (เลื่อนขึ้นมา 1 แถว)
        ws[f"B{start_sig_row + 4}"] = p_data["footer_note"]
        ws[f"B{start_sig_row + 4}"].font = Font(name="TH Sarabun PSK", size=10.5)
        ws[f"B{start_sig_row + 4}"].alignment = align_center
        ws.merge_cells(f"B{start_sig_row + 4}:G{start_sig_row + 4}")

        ws.column_dimensions["A"].width = 7
        ws.column_dimensions["B"].width = 24
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 28
        ws.column_dimensions["E"].width = 18
        ws.column_dimensions["F"].width = 20
        ws.column_dimensions["G"].width = 25

    add_xlsx_tracking_sheet(bp["pages"][1], "ใบติดตามใบเบิก_แผ่นที่1")
    add_xlsx_tracking_sheet(bp["pages"][2], "ใบติดตามใบเบิก_แผ่นที่2")

    wb.save(output_path)
    print(f"Generated XLSX: {output_path}")


if __name__ == "__main__":
    html_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html")
    docx_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.docx")
    xlsx_out = os.path.join(BASE_DIR, "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.xlsx")

    generate_html(html_out)
    generate_docx(docx_out)
    generate_xlsx(xlsx_out)
    print("All 90-day builds completed successfully!")
