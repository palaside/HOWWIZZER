# -*- coding: utf-8 -*-
"""
Superclone Production-Grade Engine for ทบ.๔๐๐-๐๑๒ (REF-TB-400-012-V1)
Form: ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์
Specifications:
- 2-Page Legal Landscape (14" x 8.5" / 1008 x 612 pt)
- Dual-Axis Signature Block Engine (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1)
- 100% Thai Numeral Compliance (ยกเว้นรหัสสากล NATO Stock Number)
- Strict Typography Hierarchy: หัวข้อ = ตัวหนา (13.5-14pt), ตัวแปร = ตัวปกติ (12pt)
- Exact Column Line Alignment between Header Master Table and Data Table (61.5% grid line)
- ผู้สั่งการสำรวจ: ชื่อ นามสกุล อยู่บรรทัดเดียวกัน
- อนุมัติ: วันที่กึ่งกลางร่วมกับชื่อ นามสกุล
- Outputs: .json, .html, .xlsx, .docx
"""

import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import CellRichText, TextBlock
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

WORKDIR = r"d:\Project\WEPAPP"

# Helper function for converting Arabic digits to Thai digits
def to_th(val):
    if val is None or val == "":
        return ""
    s = str(val)
    mapping = {
        '0': '๐', '1': '๑', '2': '๒', '3': '๓', '4': '๔',
        '5': '๕', '6': '๖', '7': '๗', '8': '๘', '9': '๙'
    }
    return "".join(mapping.get(c, c) for c in s)

# Blueprint Data Model (SSOT)
blueprint = {
    "metadata": {
        "form_id": "ทบ.๔๐๐ - ๐๑๒",
        "form_name": "ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์",
        "regulation": "( พิมพ์ตามระเบียบกองทัพบก ว่าด้วย การส่งกำลังสิ่งอุปกรณ์ประเภท ๒ และ ๔ พ.ศ.๒๕๓๔ )",
        "unit_name": "ป.๔ พัน.๔",
        "unit_location": "๘๐๗ ม.๒ ค่ายจิรประวัติ ต.นครสวรรค์ออก อ.เมือง จ.นครสวรรค์",
        "report_date": "พ.ย.๖๖",
        "survey_unit": "ป.๔ พัน.๔ ร้อย.๒",
        "order_authority": {
            "title": "ผู้สั่งการสำรวจ",
            "name": "พ.ท. พรชัย  มากเทพพงษ์",
            "position": "ผบ.ป.๔ พัน.๔"
        },
        "cert_text": "ขอรับรองว่าผลเปรียบเทียบการตรวจสอบ\nตามยอดต่อไปนี้ คือยอดแตกต่างระหว่าง\nยอดในบัญชีคุม และยอดที่ตรวจนับได้จริง",
        "cert_date": "๑๗ / พ.ย. / ๖๖",
        "counters": {
            "title": "ผู้ตรวจนับ",
            "ranks": ["ร.ท.", "จ.ส.อ.", "จ.ส.อ."],
            "date": "๑๗ / พ.ย. / ๖๖"
        },
        "inspector": {
            "title": "ผู้ตรวจสอบ",
            "rank": "พ.ท.",
            "name": "(พรชัย   มากเทพพงษ์)",
            "date": "๑๗ / พ.ย. / ๖๖"
        },
        "approver": {
            "title": "อนุมัติ",
            "rank": "พ.ท.",
            "name": "( พรชัย   มากเทพพงษ์ )",
            "date": "๑๗ / พ.ย. / ๖๔"
        },
        "admin_data": {
            "control_branch": "สายงานที่ควบคุม   สาย สพ.",
            "survey_reg": "ทะเบียน ใบสำรวจสิ่งอุปกรณ์ ที่ ๑ - ๒๓",
            "report_evidence": "หลักฐานการรายงาน คำสั่ง ป.๔ พัน.๔ ที่ ๑๕๐/๒๕๖๖ ลง ๑๗ พ.ย. ๖๖",
            "storage_loc": "ที่เก็บหลักฐานการตรวจสอบ ป.๔ พัน.๔ ร้อย.๒"
        },
        "total_pages": 2
    },
    "page_1_rows": [
        {
            "seq": 1, "survey_no": "๑/๖๖", "item_code": "1015-00-722-9752",
            "item_name": "ปบค.๙๕ ขนาด ๑๐๕ มม.", "unit": "กระบอก", "type": "๒",
            "count_actual": 6, "count_ledger": 6, "diff_short": "-", "diff_over": "-",
            "unit_price": 332712.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 2, "survey_no": "๒/๖๖", "item_code": "5180-00-757-7727",
            "item_name": "เครื่องชุดช่างซ่อมปืนใหญ่", "unit": "ชุด", "type": "๒",
            "count_actual": 3, "count_ledger": 3, "diff_short": "-", "diff_over": "-",
            "unit_price": 17496.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 3, "survey_no": "๓/๖๖", "item_code": "66885-00-3444613",
            "item_name": "เครื่องวัดอุณหภูมิส่วนบรรจุ", "unit": "ชุด", "type": "๒",
            "count_actual": 4, "count_ledger": 4, "diff_short": "-", "diff_over": "-",
            "unit_price": 1694.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 4, "survey_no": "๔/๖๖", "item_code": "1230-35-165-0005",
            "item_name": "กล้องพาโนรามิค", "unit": "ตัว", "type": "๔",
            "count_actual": 9, "count_ledger": 9, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 5, "survey_no": "๕/๖๖", "item_code": "-",
            "item_name": "กล้องข้อศอก", "unit": "ตัว", "type": "๔",
            "count_actual": 7, "count_ledger": 7, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 6, "survey_no": "๖/๖๖", "item_code": "-",
            "item_name": "เครื่องตั้งมุมยิงประณีต", "unit": "ตัว", "type": "๔",
            "count_actual": 6, "count_ledger": 6, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 7, "survey_no": "๗/๖๖", "item_code": "6685-xx-165-1315",
            "item_name": "เครื่องวัดอุณหภูมิดินส่ง แบบดิจิตอล", "unit": "ตัว", "type": "๔",
            "count_actual": 3, "count_ledger": 3, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 8, "survey_no": "๘/๖๖", "item_code": "-",
            "item_name": "ฐานกล้องเล็ง", "unit": "ตัว", "type": "๔",
            "count_actual": 6, "count_ledger": 6, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 9, "survey_no": "๙/๖๖", "item_code": "1240-006-6065",
            "item_name": "กล้องคอลลิเมเตอร์", "unit": "ตัว", "type": "๔",
            "count_actual": 5, "count_ledger": 5, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 10, "survey_no": "๑๐/๖๖", "item_code": "1015-00-712-0207",
            "item_name": "เครื่องอะไหล่บำรุงขั้น ๒", "unit": "ชุด", "type": "๔",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 11, "survey_no": "๑๑/๖๖", "item_code": "-",
            "item_name": "ชุดตรวจและเติมแก๊ส", "unit": "ชุด", "type": "๔",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": 1944.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 12, "survey_no": "๑๒/๖๖", "item_code": "-",
            "item_name": "ลำกล้องปืนเครื่องประกอบ", "unit": "ชุด", "type": "๔",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        }
    ],
    "page_2_rows": [
        {
            "seq": 13, "survey_no": "๑๓/๖๖", "item_code": "6240-155-7864",
            "item_name": "LAMP M.19 หลอดไฟหลักเล็ง", "unit": "ชิ้น", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 14, "survey_no": "๑๔/๖๖", "item_code": "6240-635-9800",
            "item_name": "LAMP M.14 หลอดไฟกล้องเล็ง", "unit": "ชิ้น", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 15, "survey_no": "๑๕/๖๖", "item_code": "1240-769-1521",
            "item_name": "CHEST,PACKING M.27 กล่องใส่กล้องเล็ง", "unit": "ชิ้น", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 16, "survey_no": "๑๖/๖๖", "item_code": "2610-262-6877",
            "item_name": "TIRE,PNEUMATIC 900-20 ยางนอก", "unit": "อัน", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 17, "survey_no": "๑๗/๖๖", "item_code": "26103500-944",
            "item_name": "INNER TUBE 900-20 ยางใน", "unit": "อัน", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 18, "survey_no": "๑๘/๖๖", "item_code": "2530-738-9618",
            "item_name": "WHEEL AND RIM กระทะล้อ", "unit": "อัน", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 19, "survey_no": "๑๙/๖๖", "item_code": "1015-615-7208",
            "item_name": "BRUSH,SECTION แปลงดอกแส้", "unit": "ชิ้น", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 20, "survey_no": "๒๐/๖๖", "item_code": "1290-824-7245",
            "item_name": "CASE,CARRYNG กล่องใส่เครื่องตั้งหัวชนวน", "unit": "อัน", "type": "๒",
            "count_actual": 1, "count_ledger": 1, "diff_short": "-", "diff_over": "-",
            "unit_price": None, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 21, "survey_no": "๒๑/๖๖", "item_code": "8340-35-229-0026",
            "item_name": "กระโจมประจำหมู่ปืน", "unit": "กระโจม", "type": "๒",
            "count_actual": 6, "count_ledger": 6, "diff_short": "-", "diff_over": "-",
            "unit_price": 17400.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 22, "survey_no": "๒๒/๖๖", "item_code": "8340-35-229-0025",
            "item_name": "กระโจมกระสุน", "unit": "กระโจม", "type": "๒",
            "count_actual": 4, "count_ledger": 4, "diff_short": "-", "diff_over": "-",
            "unit_price": 17480.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        },
        {
            "seq": 23, "survey_no": "๒๓/๖๖", "item_code": "8340-35-229-0058",
            "item_name": "กระโจมส่วนบรรจุ", "unit": "กระโจม", "type": "๒",
            "count_actual": 6, "count_ledger": 6, "diff_short": "-", "diff_over": "-",
            "unit_price": 1944.00, "total_short": "-", "total_over": "-", "currency": "บาท", "remark": "-"
        }
    ]
}

# 1. Save SSOT Blueprint JSON
json_path = os.path.join(WORKDIR, "table_layout_400_012.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(blueprint, f, ensure_ascii=False, indent=2)
print("Saved SSOT Blueprint:", json_path)


# ----------------------------------------------------------------------
# 2. HTML Generation (Aligned Grid + 12pt Variables + Shared Axis Date)
# ----------------------------------------------------------------------
def generate_page_html(page_num, total_pages, rows):
    rows_html = ""
    for r in rows:
        price_str = to_th(f"{r['unit_price']:,.2f}") if r['unit_price'] is not None else "-"
        # Format item name & NATO Stock Number
        code_part = f"<span class='item-code'>{r['item_code']}</span> " if r['item_code'] != '-' else ""
        item_full = f"{code_part}<span class='item-desc'>{r['item_name']}</span>"
        
        rows_html += f"""
        <tr>
            <td class="text-center">{to_th(r['seq'])}</td>
            <td class="text-center">{r['survey_no']}</td>
            <td class="text-left">{item_full}</td>
            <td class="text-center">{r['unit']}</td>
            <td class="text-center">{r['type']}</td>
            <td class="text-center">{to_th(r['count_actual'])}</td>
            <td class="text-center">{to_th(r['count_ledger'])}</td>
            <td class="text-center">{r['diff_short']}</td>
            <td class="text-center">{r['diff_over']}</td>
            <td class="text-right">{price_str}</td>
            <td class="text-center">{r['total_short']}</td>
            <td class="text-center">{r['total_over']}</td>
            <td class="text-center">{r['currency']}</td>
            <td class="text-center">{r['remark']}</td>
        </tr>"""

    page_th = to_th(page_num)
    total_pages_th = to_th(total_pages)

    return f"""
    <div class="sheet-container">
        <!-- รหัสแบบฟอร์มมุมบนขวา -->
        <div class="top-form-id font-bold">{blueprint['metadata']['form_id']}</div>

        <!-- กล่องหัวเอกสารและคณะกรรมการตรวจสอบ (Header Master Table: Grid Aligned to 61.5%) -->
        <table class="header-master-table">
            <colgroup>
                <col style="width: 26.0%;">
                <col style="width: 19.0%;">
                <col style="width: 16.5%;">
                <col style="width: 18.5%;">
                <col style="width: 20.0%;">
            </colgroup>
            <!-- แถวที่ 1: ชื่อรายงาน, นามหน่วย/ที่ตั้ง, วันที่, แผ่นที่ -->
            <tr>
                <td class="hdr-title text-center font-bold">
                    {blueprint['metadata']['form_name']}
                </td>
                <td class="hdr-unit-info">
                    <div><span class="lbl font-bold">นามหน่วย</span> &nbsp; <span class="val">{blueprint['metadata']['unit_name']}</span></div>
                    <div><span class="lbl font-bold">ที่ตั้ง</span> &nbsp; <span class="val">{blueprint['metadata']['unit_location']}</span></div>
                </td>
                <td class="hdr-date text-center">
                    <div><span class="lbl font-bold">วันที่รายงาน</span></div>
                    <div class="val">{blueprint['metadata']['report_date']}</div>
                </td>
                <td colspan="2" class="hdr-page text-center">
                    <span class="lbl font-bold">แผ่นที่</span> &nbsp; <span class="val">{page_th}</span> &nbsp; <span class="lbl font-bold">ในจำนวน</span> &nbsp; <span class="val">{total_pages_th}</span> &nbsp; <span class="lbl font-bold">แผ่น</span>
                </td>
            </tr>

            <!-- แถวที่ 2: เนื้อหาคณะกรรมการ และผู้มีอำนาจลงนาม -->
            <tr>
                <!-- คอลัมน์ 1: หน่วยสำรวจ + ผู้สั่งการสำรวจ (ชื่อ นามสกุล อยู่บรรทัดเดียวกัน) -->
                <td class="hdr-col-surveyor">
                    <div class="survey-unit-box">
                        <span class="lbl font-bold">หน่วยสำรวจ</span> &nbsp; <span class="val">{blueprint['metadata']['survey_unit']}</span>
                    </div>
                    <div class="order-box">
                        <div class="order-title">
                            <span class="lbl font-bold">ผู้สั่งการสำรวจ</span> &nbsp; <span class="val">{blueprint['metadata']['order_authority']['name']}</span>
                        </div>
                        <div class="order-pos-sig">
                            <div class="sig-space-small"></div>
                            <div class="text-center val">{blueprint['metadata']['order_authority']['position']}</div>
                        </div>
                    </div>
                </td>

                <!-- คอลัมน์ 2: คำรับรองผลเปรียบเทียบ -->
                <td class="hdr-col-cert">
                    <div class="cert-inner">
                        <div class="cert-body val">
                            ขอรับรองว่าผลเปรียบเทียบการตรวจสอบ<br>
                            ตามยอดต่อไปนี้ คือยอดแตกต่างระหว่าง<br>
                            ยอดในบัญชีคุม และยอดที่ตรวจนับได้จริง
                        </div>
                        <div class="cert-date-row">
                            <span class="lbl font-bold">เมื่อ</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span class="val">{blueprint['metadata']['cert_date']}</span>
                        </div>
                    </div>
                </td>

                <!-- คอลัมน์ 3: ผู้ตรวจนับ & ผู้ตรวจสอบ (Universal Signature Engine) -->
                <td class="hdr-col-inspectors">
                    <!-- ส่วนผู้ตรวจนับ -->
                    <div class="box-counters">
                        <div class="box-tag font-bold">ผู้ตรวจนับ</div>
                        <div class="counter-ranks val">
                            <div>ร.ท.</div>
                            <div>จ.ส.อ.</div>
                            <div>จ.ส.อ.</div>
                        </div>
                        <div class="box-date-line val">{blueprint['metadata']['counters']['date']}</div>
                    </div>
                    <!-- ส่วนผู้ตรวจสอบ (Universal Red Line Standard) -->
                    <div class="box-verifier">
                        <div class="box-tag font-bold">ผู้ตรวจสอบ</div>
                        <div class="sig-name-pos-group">
                            <div class="sig-name-wrapper">
                                <span class="sig-rank-anchor val">{blueprint['metadata']['inspector']['rank']}</span>
                                <div class="sig-name val">{blueprint['metadata']['inspector']['name']}</div>
                            </div>
                            <div class="box-date-line val">{blueprint['metadata']['inspector']['date']}</div>
                        </div>
                    </div>
                </td>

                <!-- คอลัมน์ 4: อนุมัติ (Universal Red Line Standard + Shared Axis Date) -->
                <td class="hdr-col-approve">
                    <div class="approve-tag font-bold">อนุมัติ</div>
                    <div class="approve-sig-area">
                        <div class="sig-space-large"></div>
                        <div class="sig-name-pos-group">
                            <div class="sig-name-wrapper">
                                <span class="sig-rank-anchor val">{blueprint['metadata']['approver']['rank']}</span>
                                <div class="sig-name val">{blueprint['metadata']['approver']['name']}</div>
                            </div>
                            <div class="approve-date-line val">{blueprint['metadata']['approver']['date']}</div>
                        </div>
                    </div>
                </td>

                <!-- คอลัมน์ 5: ข้อมูลทะเบียนและหลักฐานการรายงาน -->
                <td class="hdr-col-admin">
                    <div class="admin-row border-b"><span class="lbl font-bold">สายงานที่ควบคุม</span> &nbsp; <span class="val">สาย สพ.</span></div>
                    <div class="admin-row border-b"><span class="lbl font-bold">ทะเบียน</span> &nbsp; <span class="val">{blueprint['metadata']['admin_data']['survey_reg'].replace('ทะเบียน ', '')}</span></div>
                    <div class="admin-row border-b"><div class="lbl font-bold">หลักฐานการรายงาน</div><div class="val" style="margin-top: 2px;">{blueprint['metadata']['admin_data']['report_evidence'].replace('หลักฐานการรายงาน ', '')}</div></div>
                    <div class="admin-row"><div class="lbl font-bold">ที่เก็บหลักฐานการตรวจสอบ</div><div class="val" style="margin-top: 14px;">{blueprint['metadata']['admin_data']['storage_loc'].replace('ที่เก็บหลักฐานการตรวจสอบ ', '')}</div></div>
                </td>
            </tr>
        </table>

        <!-- ตารางข้อมูลหลัก 14 คอลัมน์ (Data Grid: เส้นตรงแนวเดียวกับกล่องบน 100%) -->
        <table class="military-data-table">
            <colgroup>
                <col style="width: 4.0%;">  <!-- ลำดับ -->
                <col style="width: 5.5%;">  <!-- ใบสำรวจที่ -->
                <col style="width: 35.0%;"> <!-- หมายเลขสิ่งอุปกรณ์ -->
                <col style="width: 4.5%;">  <!-- หน่วยนับ (รวม 4 คอลัมน์แรก = 49.0%) -->
                <col style="width: 4.3%;">  <!-- ประเภทสิ่งอุปกรณ์ -->
                <col style="width: 4.1%;">  <!-- นับได้ -->
                <col style="width: 4.1%;">  <!-- บัญชีคุม (รวมสะสม 61.5% ตรงแนวผู้ตรวจสอบ/อนุมัติ เป๊ะ!) -->
                <col style="width: 4.5%;">  <!-- เปรียบเทียบ ขาด -->
                <col style="width: 4.5%;">  <!-- เปรียบเทียบ เกิน -->
                <col style="width: 9.5%;">  <!-- ราคาหน่วยละ (รวมสะสม 80.0% ตรงแนวอนุมัติ/สายงาน เป๊ะ!) -->
                <col style="width: 5.0%;">  <!-- เปรียบเทียบราคารวม ขาด -->
                <col style="width: 5.0%;">  <!-- เปรียบเทียบราคารวม เกิน -->
                <col style="width: 4.5%;">  <!-- ประเภทเงิน -->
                <col style="width: 5.5%;">  <!-- หมายเหตุ (รวมสะสม 100.0%) -->
            </colgroup>
            <thead>
                <tr>
                    <th rowspan="2">ลำดับ</th>
                    <th rowspan="2">ใบสำรวจที่</th>
                    <th rowspan="2">หมายเลขสิ่งอุปกรณ์และรายการ</th>
                    <th rowspan="2">หน่วย<br>นับ</th>
                    <th rowspan="2">ประเภท<br>สิ่งอุปกรณ์</th>
                    <th colspan="2">จำนวนสิ่งอุปกรณ์</th>
                    <th colspan="2">เปรียบเทียบ</th>
                    <th rowspan="2">ราคา<br>หน่วยละ</th>
                    <th colspan="2">เปรียบเทียบราคารวม</th>
                    <th rowspan="2">ประเภท<br>เงิน</th>
                    <th rowspan="2">หมายเหตุ</th>
                </tr>
                <tr>
                    <th>นับได้</th>
                    <th>บัญชีคุม</th>
                    <th>ขาด</th>
                    <th>เกิน</th>
                    <th>ขาด</th>
                    <th>เกิน</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
                <!-- แถวรวมเงิน -->
                <tr class="total-row font-bold">
                    <td colspan="3" class="text-center font-bold">รวมเงิน</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-right font-bold"></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>

        <!-- ข้อความกำกับระเบียบด้านล่าง -->
        <div class="doc-reg-footer val">
            {blueprint['metadata']['regulation']}
        </div>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทบ.๔๐๐-๐๑๒ ใบรายงานผลเปรียบเทียบการตรวจสอบสิ่งอุปกรณ์</title>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: legal landscape;
            margin: 6mm 8mm;
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
            font-size: 14pt;
            line-height: 1.15;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            font-feature-settings: "locl" 1, "numr" 1;
            font-variant-numeric: tabular-nums;
        }}

        .sheet-container {{
            width: 340mm;
            min-height: 205mm;
            margin: 0 auto 30px auto;
            background: #fff;
            padding: 8mm 10mm;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: relative;
            page-break-after: always;
        }}

        .top-form-id {{
            text-align: right;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 2px;
            padding-right: 2px;
        }}

        /* Master Header Table */
        .header-master-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            border: 1.5px solid #000;
            margin-bottom: 0;
            font-size: 13.5pt;
        }}
        .header-master-table td {{
            border: 1px solid #000;
            padding: 4px 6px;
            vertical-align: top;
        }}
        .hdr-title {{
            font-weight: bold;
            font-size: 13.5pt;
            line-height: 1.2;
            vertical-align: middle !important;
            padding: 4px 6px;
        }}
        .lbl {{ 
            font-weight: bold; 
            font-size: 13pt;
        }}
        .val {{ 
            font-weight: normal; 
            font-size: 12pt;
        }}
        .font-bold {{ font-weight: bold; }}
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}

        /* Left Column (Surveyor & Order) */
        .hdr-col-surveyor {{
            padding: 0 !important;
            vertical-align: top;
        }}
        .survey-unit-box {{
            padding: 5px 6px;
            border-bottom: 1px solid #000;
            min-height: 48px;
        }}
        .order-box {{
            padding: 5px 6px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 102px;
        }}
        .order-title {{
            white-space: nowrap;
            line-height: 1.3;
        }}
        .order-title .val {{
            font-size: 12pt;
            white-space: nowrap;
        }}
        .order-pos-sig .val {{
            font-size: 12pt;
        }}
        .sig-space-small {{ height: 26px; }}
        .sig-space-large {{ height: 35px; }}

        /* Cert Column */
        .hdr-col-cert {{
            padding: 6px 8px !important;
            vertical-align: top;
        }}
        .cert-inner {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 148px;
        }}
        .cert-body {{
            line-height: 1.25;
            font-size: 12pt;
        }}
        .cert-date-row {{
            margin-top: 18px;
        }}
        .cert-date-row .val {{
            font-size: 12pt;
        }}

        /* Inspectors Column */
        .hdr-col-inspectors {{
            padding: 0 !important;
            vertical-align: top;
        }}
        .box-counters {{
            border-bottom: 1px solid #000;
            padding: 4px 6px;
            min-height: 78px;
            position: relative;
        }}
        .box-tag {{
            font-size: 13.5pt;
            margin-bottom: 2px;
        }}
        .counter-ranks {{
            padding-left: 28px;
            line-height: 1.15;
            font-size: 12pt;
        }}
        .box-date-line {{
            text-align: right;
            padding-right: 6px;
            font-size: 12pt;
            margin-top: 4px;
        }}
        .box-verifier {{
            padding: 4px 6px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 85px;
        }}
        .box-verifier .sig-name-pos-group {{
            margin-top: 12px;
            margin-left: 36px;
        }}
        .box-verifier .sig-name-wrapper {{
            margin-top: 16px;
        }}
        .box-verifier .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 6px);
            white-space: nowrap;
            font-size: 12pt;
            line-height: 1.0;
        }}
        .box-verifier .box-date-line {{
            margin-top: 4px;
            text-align: center;
        }}

        /* Approve Column */
        .hdr-col-approve {{
            padding: 6px 8px !important;
            vertical-align: top;
        }}
        .approve-tag {{
            font-size: 13.5pt;
        }}
        .approve-sig-area {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            min-height: 125px;
        }}
        .approve-sig-area .sig-name-pos-group {{
            margin-left: 36px;
            margin-bottom: 4px;
        }}
        .approve-date-line {{
            font-size: 12pt;
            margin-top: 6px;
            text-align: center;
            white-space: nowrap;
        }}

        /* Universal Signature Engine (RULE-UNIVERSAL-SIGNATURE-BLOCK-V1) */
        .sig-name-pos-group {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            margin-left: 45px;
        }}
        .sig-name-wrapper {{
            position: relative;
            display: inline-block;
            white-space: nowrap;
            margin-top: 24px;
        }}
        .sig-rank-anchor {{
            position: absolute;
            right: 100%;
            bottom: calc(100% + 14px);
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

        /* Admin Info Column */
        .hdr-col-admin {{
            padding: 0 !important;
            font-size: 11pt;
            line-height: 1.15;
        }}
        .admin-row {{
            padding: 5px 6px 4px 6px;
            font-size: 11pt;
        }}
        .admin-row .lbl {{
            font-size: 11pt;
            padding-top: 2px;
        }}
        .admin-row .val {{
            font-size: 10.5pt;
        }}
        .border-b {{
            border-bottom: 1px solid #000;
        }}

        /* Main Data Table */
        .military-data-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            border: 1.5px solid #000;
            border-top: none;
            font-size: 11.5pt;
        }}
        .military-data-table th, .military-data-table td {{
            border: 1px solid #000;
            padding: 4px 2px 2px 2px;
            vertical-align: middle;
            line-height: 1.1;
        }}
        .military-data-table thead th {{
            background-color: #fafafa;
            font-weight: normal;
            font-size: 11pt;
            text-align: center;
            padding: 4px 1px 2px 1px;
            line-height: 1.1;
        }}
        .military-data-table tbody td {{
            height: 24px;
            font-size: 11.5pt;
            font-weight: normal;
        }}
        .item-code {{
            font-family: 'TH Sarabun PSK', Sarabun, monospace;
            display: inline-block;
            margin-right: 4px;
            font-feature-settings: "locl" 0, "numr" 0;
            font-size: 11.5pt;
            font-weight: normal;
        }}
        .item-desc {{
            display: inline-block;
            font-size: 11.5pt;
            font-weight: normal;
        }}
        .total-row td {{
            font-weight: bold;
            font-size: 13pt;
            height: 26px;
        }}

        .doc-reg-footer {{
            text-align: center;
            margin-top: 8px;
            font-size: 12pt;
        }}

        @media print {{
            body {{ background: transparent; padding: 0; }}
            .sheet-container {{
                box-shadow: none;
                margin: 0;
                padding: 4mm 6mm;
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    {generate_page_html(1, 2, blueprint['page_1_rows'])}
    {generate_page_html(2, 2, blueprint['page_2_rows'])}
</body>
</html>
"""

html_out_path = os.path.join(WORKDIR, "ทบ_400_012_Rebuild_Thai.html")
with open(html_out_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print("Saved HTML:", html_out_path)


# ----------------------------------------------------------------------
# 3. Excel Spreadsheet Generation (.xlsx) (Data Integrity & 12pt RichText)
# ----------------------------------------------------------------------
wb = openpyxl.Workbook()
wb.remove(wb.active)

ifont_regular = InlineFont(rFont="TH Sarabun PSK", sz=12, b=False)
ifont_bold = InlineFont(rFont="TH Sarabun PSK", sz=13, b=True)
ifont_small = InlineFont(rFont="TH Sarabun PSK", sz=11.5, b=False)
ifont_small_bold = InlineFont(rFont="TH Sarabun PSK", sz=12, b=True)

font_regular = Font(name="TH Sarabun PSK", size=12, bold=False)
font_bold = Font(name="TH Sarabun PSK", size=13, bold=True)
font_title = Font(name="TH Sarabun PSK", size=14, bold=True)
font_small = Font(name="TH Sarabun PSK", size=11.5, bold=False)
font_small_bold = Font(name="TH Sarabun PSK", size=12, bold=True)

thin_side = Side(border_style="thin", color="000000")
medium_side = Side(border_style="medium", color="000000")
box_border = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")

def build_excel_sheet(ws, sheet_title, rows, page_num):
    ws.views.sheetView[0].showGridLines = True
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_LEGAL
    ws.page_margins.left = 0.35
    ws.page_margins.right = 0.35
    ws.page_margins.top = 0.35
    ws.page_margins.bottom = 0.35

    # Column widths (14 cols)
    col_widths = {
        'A': 6,   # ลำดับ
        'B': 8,   # ใบสำรวจที่
        'C': 34,  # หมายเลขและรายการ
        'D': 8,   # หน่วยนับ
        'E': 7,   # ประเภท
        'F': 7,   # นับได้
        'G': 7,   # บัญชีคุม
        'H': 6,   # ขาด
        'I': 6,   # เกิน
        'J': 13,  # ราคาหน่วยละ
        'K': 8,   # รวมขาด
        'L': 8,   # รวมเกิน
        'M': 8,   # ประเภทเงิน
        'N': 8    # หมายเหตุ
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Row 1: Form ID
    ws.merge_cells("L1:N1")
    ws["L1"] = blueprint['metadata']['form_id']
    ws["L1"].font = font_bold
    ws["L1"].alignment = Alignment(horizontal="right", vertical="center")

    # Header Master Grid
    ws.row_dimensions[2].height = 28
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 20
    ws.row_dimensions[5].height = 20
    ws.row_dimensions[6].height = 20
    ws.row_dimensions[7].height = 20

    # A2:C2: Title
    ws.merge_cells("A2:C2")
    ws["A2"] = blueprint['metadata']['form_name']
    ws["A2"].font = font_title
    ws["A2"].alignment = align_center

    # D2:H2: Unit info with RichText (Labels = Bold, Values = 12pt Regular)
    ws.merge_cells("D2:H2")
    ws["D2"] = CellRichText(
        TextBlock(ifont_small_bold, "นามหน่วย  "),
        TextBlock(ifont_small, f"{blueprint['metadata']['unit_name']}   "),
        TextBlock(ifont_small_bold, "ที่ตั้ง  "),
        TextBlock(ifont_small, f"{blueprint['metadata']['unit_location']}")
    )
    ws["D2"].alignment = align_left

    # I2:J2: Report Date
    ws.merge_cells("I2:J2")
    ws["I2"] = CellRichText(
        TextBlock(ifont_bold, "วันที่รายงาน\n"),
        TextBlock(ifont_regular, f"{blueprint['metadata']['report_date']}")
    )
    ws["I2"].alignment = align_center

    # K2:N2: Page count
    page_th = to_th(page_num)
    ws.merge_cells("K2:N2")
    ws["K2"] = CellRichText(
        TextBlock(ifont_bold, "แผ่นที่  "),
        TextBlock(ifont_regular, f"{page_th}"),
        TextBlock(ifont_bold, "  ในจำนวน  "),
        TextBlock(ifont_regular, "๒"),
        TextBlock(ifont_bold, "  แผ่น")
    )
    ws["K2"].alignment = align_center

    # Row 3 to 7: Committee & Signatures
    # A3:C4: หน่วยสำรวจ
    ws.merge_cells("A3:C4")
    ws["A3"] = CellRichText(
        TextBlock(ifont_bold, "หน่วยสำรวจ  "),
        TextBlock(ifont_regular, f"{blueprint['metadata']['survey_unit']}")
    )
    ws["A3"].alignment = Alignment(horizontal="left", vertical="top")

    # A5:C7: ผู้สั่งการสำรวจ (ชื่อ นามสกุล บรรทัดเดียวกัน)
    ws.merge_cells("A5:C7")
    ws["A5"] = CellRichText(
        TextBlock(ifont_bold, "ผู้สั่งการสำรวจ  "),
        TextBlock(ifont_regular, f"{blueprint['metadata']['order_authority']['name']}\n\n{blueprint['metadata']['order_authority']['position']}")
    )
    ws["A5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # D3:F7: คำรับรอง
    ws.merge_cells("D3:F7")
    ws["D3"] = CellRichText(
        TextBlock(ifont_regular, f"{blueprint['metadata']['cert_text']}\n\n"),
        TextBlock(ifont_bold, "เมื่อ            "),
        TextBlock(ifont_regular, f"{blueprint['metadata']['cert_date']}")
    )
    ws["D3"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # G3:I5: ผู้ตรวจนับ
    ws.merge_cells("G3:I5")
    ws["G3"] = CellRichText(
        TextBlock(ifont_bold, "ผู้ตรวจนับ\n"),
        TextBlock(ifont_regular, f"    ร.ท.\n    จ.ส.อ.\n    จ.ส.อ.\n              {blueprint['metadata']['counters']['date']}")
    )
    ws["G3"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # G6:I7: ผู้ตรวจสอบ
    ws.merge_cells("G6:I7")
    ws["G6"] = CellRichText(
        TextBlock(ifont_bold, "ผู้ตรวจสอบ\n"),
        TextBlock(ifont_regular, f"      {blueprint['metadata']['inspector']['rank']}\n      {blueprint['metadata']['inspector']['name']}\n              {blueprint['metadata']['inspector']['date']}")
    )
    ws["G6"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # J3:K7: อนุมัติ (วันที่กึ่งกลางร่วมกับชื่อ)
    ws.merge_cells("J3:K7")
    ws["J3"] = CellRichText(
        TextBlock(ifont_bold, "อนุมัติ\n\n\n"),
        TextBlock(ifont_regular, f"      {blueprint['metadata']['approver']['rank']}\n      {blueprint['metadata']['approver']['name']}\n              {blueprint['metadata']['approver']['date']}")
    )
    ws["J3"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # L3:N7: ทะเบียน & หลักฐาน (RichText)
    ws.merge_cells("L3:N3")
    ws["L3"] = CellRichText(
        TextBlock(ifont_small_bold, "สายงานที่ควบคุม   "),
        TextBlock(ifont_small, "สาย สพ.")
    )
    ws["L3"].alignment = align_left

    ws.merge_cells("L4:N4")
    ws["L4"] = CellRichText(
        TextBlock(ifont_small_bold, "ทะเบียน   "),
        TextBlock(ifont_small, f"{blueprint['metadata']['admin_data']['survey_reg'].replace('ทะเบียน ', '')}")
    )
    ws["L4"].alignment = align_left

    ws.merge_cells("L5:N6")
    ws["L5"] = CellRichText(
        TextBlock(ifont_small_bold, "หลักฐานการรายงาน   "),
        TextBlock(ifont_small, f"{blueprint['metadata']['admin_data']['report_evidence'].replace('หลักฐานการรายงาน ', '')}")
    )
    ws["L5"].alignment = align_left

    ws.merge_cells("L7:N7")
    ws["L7"] = CellRichText(
        TextBlock(ifont_small_bold, "ที่เก็บหลักฐานการตรวจสอบ   "),
        TextBlock(ifont_small, f"{blueprint['metadata']['admin_data']['storage_loc'].replace('ที่เก็บหลักฐานการตรวจสอบ ', '')}")
    )
    ws["L7"].alignment = align_left

    # Apply borders to Header Grid (Rows 2 to 7)
    for r in range(2, 8):
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = box_border

    # Data Table Headers (Rows 8 & 9)
    ws.row_dimensions[8].height = 24
    ws.row_dimensions[9].height = 20

    headers_row8 = [
        ("A8:A9", "ลำดับ"), ("B8:B9", "ใบสำรวจที่"), ("C8:C9", "หมายเลขสิ่งอุปกรณ์และรายการ"),
        ("D8:D9", "หน่วยนับ"), ("E8:E9", "ประเภท\nสิ่งอุปกรณ์"),
        ("F8:G8", "จำนวนสิ่งอุปกรณ์"), ("H8:I8", "เปรียบเทียบ"),
        ("J8:J9", "ราคา\nหน่วยละ"), ("K8:L8", "เปรียบเทียบราคารวม"),
        ("M8:M9", "ประเภท\nเงิน"), ("N8:N9", "หมายเหตุ")
    ]
    for rng, txt in headers_row8:
        if ":" in rng:
            ws.merge_cells(rng)
        first_cell = ws[rng.split(":")[0]]
        first_cell.value = txt
        first_cell.font = font_regular
        first_cell.alignment = align_center

    ws["F9"] = "นับได้"; ws["F9"].font = font_regular; ws["F9"].alignment = align_center
    ws["G9"] = "บัญชีคุม"; ws["G9"].font = font_regular; ws["G9"].alignment = align_center
    ws["H9"] = "ขาด"; ws["H9"].font = font_regular; ws["H9"].alignment = align_center
    ws["I9"] = "เกิน"; ws["I9"].font = font_regular; ws["I9"].alignment = align_center
    ws["K9"] = "ขาด"; ws["K9"].font = font_regular; ws["K9"].alignment = align_center
    ws["L9"] = "เกิน"; ws["L9"].font = font_regular; ws["L9"].alignment = align_center

    for r in [8, 9]:
        for c in range(1, 15):
            ws.cell(row=r, column=c).border = box_border
            ws.cell(row=r, column=c).fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")

    # Data Rows (Font 12pt)
    current_r = 10
    start_data_row = current_r
    for item in rows:
        ws.row_dimensions[current_r].height = 20
        # A: ลำดับ (Pure Thai)
        c_seq = ws.cell(row=current_r, column=1, value=to_th(item["seq"]))
        c_seq.alignment = align_center; c_seq.font = font_regular
        # B: ใบสำรวจที่
        c_surv = ws.cell(row=current_r, column=2, value=item["survey_no"])
        c_surv.alignment = align_center; c_surv.font = font_regular
        # C: หมายเลขและรายการ
        code_txt = f"{item['item_code']}  " if item['item_code'] != '-' else ""
        c_desc = ws.cell(row=current_r, column=3, value=f"{code_txt}{item['item_name']}")
        c_desc.alignment = align_left; c_desc.font = font_regular
        # D: หน่วยนับ
        c_unit = ws.cell(row=current_r, column=4, value=item["unit"])
        c_unit.alignment = align_center; c_unit.font = font_regular
        # E: ประเภท
        c_typ = ws.cell(row=current_r, column=5, value=item["type"])
        c_typ.alignment = align_center; c_typ.font = font_regular
        # F: นับได้
        c_act = ws.cell(row=current_r, column=6, value=item["count_actual"])
        c_act.number_format = '[$-th-TH,26]#,##0'
        c_act.alignment = align_center; c_act.font = font_regular
        # G: บัญชีคุม
        c_led = ws.cell(row=current_r, column=7, value=item["count_ledger"])
        c_led.number_format = '[$-th-TH,26]#,##0'
        c_led.alignment = align_center; c_led.font = font_regular
        # H: ขาด
        c_dsh = ws.cell(row=current_r, column=8, value=item["diff_short"])
        c_dsh.alignment = align_center; c_dsh.font = font_regular
        # I: เกิน
        c_dov = ws.cell(row=current_r, column=9, value=item["diff_over"])
        c_dov.alignment = align_center; c_dov.font = font_regular
        # J: ราคาหน่วยละ
        if item["unit_price"] is not None:
            c_prc = ws.cell(row=current_r, column=10, value=float(item["unit_price"]))
            c_prc.number_format = '[$-th-TH,26]#,##0.00'
        else:
            c_prc = ws.cell(row=current_r, column=10, value="-")
        c_prc.alignment = align_right; c_prc.font = font_regular
        # K: เปรียบเทียบราคารวม ขาด
        c_tsh = ws.cell(row=current_r, column=11, value=item["total_short"])
        c_tsh.alignment = align_center; c_tsh.font = font_regular
        # L: เปรียบเทียบราคารวม เกิน
        c_tov = ws.cell(row=current_r, column=12, value=item["total_over"])
        c_tov.alignment = align_center; c_tov.font = font_regular
        # M: ประเภทเงิน
        c_cur = ws.cell(row=current_r, column=13, value=item["currency"])
        c_cur.alignment = align_center; c_cur.font = font_regular
        # N: หมายเหตุ
        c_rem = ws.cell(row=current_r, column=14, value=item["remark"])
        c_rem.alignment = align_center; c_rem.font = font_regular

        for c in range(1, 15):
            ws.cell(row=current_r, column=c).border = box_border
        current_r += 1

    # Total Row (รวมเงิน)
    ws.merge_cells(f"A{current_r}:C{current_r}")
    c_tot = ws.cell(row=current_r, column=1, value="รวมเงิน")
    c_tot.alignment = align_center; c_tot.font = font_bold
    
    # Formula for Total Price in J
    c_sum = ws.cell(row=current_r, column=10, value=f"=SUM(J{start_data_row}:J{current_r-1})")
    c_sum.number_format = '[$-th-TH,26]#,##0.00'
    c_sum.alignment = align_right; c_sum.font = font_bold

    for c in range(1, 15):
        cell_tot = ws.cell(row=current_r, column=c)
        cell_tot.border = box_border
        if c not in [1, 2, 3, 10]:
            cell_tot.value = ""
    current_r += 1

    # Bottom regulation
    current_r += 1
    ws.merge_cells(f"A{current_r}:N{current_r}")
    c_reg = ws.cell(row=current_r, column=1, value=blueprint['metadata']['regulation'])
    c_reg.alignment = align_center
    c_reg.font = font_regular

ws1 = wb.create_sheet(title="แผ่นที่ ๑")
build_excel_sheet(ws1, "แผ่นที่ ๑", blueprint['page_1_rows'], 1)

ws2 = wb.create_sheet(title="แผ่นที่ ๒")
build_excel_sheet(ws2, "แผ่นที่ ๒", blueprint['page_2_rows'], 2)

xlsx_out_path = os.path.join(WORKDIR, "ทบ_400_012_Rebuild_Thai.xlsx")
wb.save(xlsx_out_path)
print("Saved XLSX:", xlsx_out_path)


# ----------------------------------------------------------------------
# 4. Word Document Generation (.docx) (Legal Landscape & Tab Red Line)
# ----------------------------------------------------------------------
doc = docx.Document()
section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(14.0)
section.page_height = Inches(8.5)
section.left_margin = Inches(0.4)
section.right_margin = Inches(0.4)
section.top_margin = Inches(0.35)
section.bottom_margin = Inches(0.35)

def format_docx_run(run, font_name="TH Sarabun PSK", size_pt=12, bold=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:eastAsia="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/><w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>')
    tcPr.append(borders)

def build_docx_page(doc, page_num, rows):
    # Form ID top right
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_top.paragraph_format.space_before = Pt(0)
    p_top.paragraph_format.space_after = Pt(2)
    r_top = p_top.add_run(blueprint['metadata']['form_id'])
    format_docx_run(r_top, size_pt=14, bold=True)

    # Master Header Table (2 rows, 5 cols) - Aligned widths: 23.5%, 21.5%, 16.5%, 18.5%, 20.0%
    hdr_table = doc.add_table(rows=2, cols=5)
    hdr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_table.autofit = False

    col_widths_inches = [Inches(3.1), Inches(2.8), Inches(2.2), Inches(2.5), Inches(2.6)]
    for row in hdr_table.rows:
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths_inches[c_idx]
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            set_cell_borders(cell)

    # Row 0: Title, Unit, Date, Page
    c00 = hdr_table.cell(0, 0)
    p00 = c00.paragraphs[0]; p00.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r00 = p00.add_run(blueprint['metadata']['form_name'])
    format_docx_run(r00, size_pt=13.5, bold=True)

    c01 = hdr_table.cell(0, 1)
    p01 = c01.paragraphs[0]
    r01_1 = p01.add_run("นามหน่วย  "); format_docx_run(r01_1, size_pt=13, bold=True)
    r01_2 = p01.add_run(f"{blueprint['metadata']['unit_name']}\n"); format_docx_run(r01_2, size_pt=12, bold=False)
    r01_3 = p01.add_run("ที่ตั้ง  "); format_docx_run(r01_3, size_pt=12, bold=True)
    r01_4 = p01.add_run(f"{blueprint['metadata']['unit_location']}"); format_docx_run(r01_4, size_pt=12, bold=False)

    c02 = hdr_table.cell(0, 2)
    p02 = c02.paragraphs[0]; p02.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r02_1 = p02.add_run("วันที่รายงาน\n"); format_docx_run(r02_1, size_pt=13, bold=True)
    r02_2 = p02.add_run(f"{blueprint['metadata']['report_date']}"); format_docx_run(r02_2, size_pt=12, bold=False)

    # Merge cols 3 and 4 for Page count
    c03 = hdr_table.cell(0, 3)
    c04 = hdr_table.cell(0, 4)
    c03.merge(c04)
    p03 = c03.paragraphs[0]; p03.alignment = WD_ALIGN_PARAGRAPH.CENTER
    page_th = to_th(page_num)
    r03_1 = p03.add_run("แผ่นที่  "); format_docx_run(r03_1, size_pt=13.5, bold=True)
    r03_2 = p03.add_run(f"{page_th}"); format_docx_run(r03_2, size_pt=12, bold=False)
    r03_3 = p03.add_run("  ในจำนวน  "); format_docx_run(r03_3, size_pt=13.5, bold=True)
    r03_4 = p03.add_run("๒"); format_docx_run(r03_4, size_pt=12, bold=False)
    r03_5 = p03.add_run("  แผ่น"); format_docx_run(r03_5, size_pt=13.5, bold=True)

    # Row 1: Content
    # Cell 1,0: หน่วยสำรวจ & ผู้สั่งการสำรวจ (ชื่อ นามสกุล บรรทัดเดียวกัน)
    c10 = hdr_table.cell(1, 0)
    p10_1 = c10.paragraphs[0]
    r10_1 = p10_1.add_run("หน่วยสำรวจ  "); format_docx_run(r10_1, size_pt=13, bold=True)
    r10_2 = p10_1.add_run(f"{blueprint['metadata']['survey_unit']}\n\n"); format_docx_run(r10_2, size_pt=12, bold=False)
    r10_3 = p10_1.add_run("ผู้สั่งการสำรวจ  "); format_docx_run(r10_3, size_pt=12.5, bold=True)
    r10_4 = p10_1.add_run(f"{blueprint['metadata']['order_authority']['name']}\n\n"); format_docx_run(r10_4, size_pt=12, bold=False)
    r10_5 = p10_1.add_run(f"          {blueprint['metadata']['order_authority']['position']}"); format_docx_run(r10_5, size_pt=12, bold=False)

    # Cell 1,1: คำรับรอง
    c11 = hdr_table.cell(1, 1)
    p11 = c11.paragraphs[0]
    r11_1 = p11.add_run("ขอรับรองว่าผลเปรียบเทียบการตรวจสอบ\nตามยอดต่อไปนี้ คือยอดแตกต่างระหว่าง\nยอดในบัญชีคุม และยอดที่ตรวจนับได้จริง\n\n")
    format_docx_run(r11_1, size_pt=12, bold=False)
    r11_lbl = p11.add_run("เมื่อ"); format_docx_run(r11_lbl, size_pt=12.5, bold=True)
    r11_dt = p11.add_run(f"               {blueprint['metadata']['cert_date']}"); format_docx_run(r11_dt, size_pt=12, bold=False)

    # Cell 1,2: ผู้ตรวจนับ & ผู้ตรวจสอบ (Universal Signature Red Line Standard)
    c12 = hdr_table.cell(1, 2)
    p12_1 = c12.paragraphs[0]
    r12_tag1 = p12_1.add_run("ผู้ตรวจนับ\n"); format_docx_run(r12_tag1, size_pt=12.5, bold=True)
    r12_ranks = p12_1.add_run(f"    ร.ท.\n    จ.ส.อ.\n    จ.ส.อ.\n      {blueprint['metadata']['counters']['date']}\n\n")
    format_docx_run(r12_ranks, size_pt=12, bold=False)
    r12_tag2 = p12_1.add_run("ผู้ตรวจสอบ\n"); format_docx_run(r12_tag2, size_pt=12.5, bold=True)
    
    axis_insp = Inches(0.65)
    p_insp_rk = c12.add_paragraph()
    p_insp_rk.paragraph_format.tab_stops.add_tab_stop(axis_insp, WD_TAB_ALIGNMENT.RIGHT)
    p_insp_rk.paragraph_format.space_after = Pt(14)
    r_irk = p_insp_rk.add_run(f"\t{blueprint['metadata']['inspector']['rank']}")
    format_docx_run(r_irk, size_pt=12, bold=False)
    
    p_insp_nm = c12.add_paragraph()
    p_insp_nm.paragraph_format.tab_stops.add_tab_stop(axis_insp, WD_TAB_ALIGNMENT.LEFT)
    p_insp_nm.paragraph_format.space_after = Pt(0)
    r_inm = p_insp_nm.add_run(f"\t{blueprint['metadata']['inspector']['name']}")
    format_docx_run(r_inm, size_pt=12, bold=False)

    p_insp_dt = c12.add_paragraph()
    p_insp_dt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_idt = p_insp_dt.add_run(blueprint['metadata']['inspector']['date'])
    format_docx_run(r_idt, size_pt=12, bold=False)

    # Cell 1,3: อนุมัติ (Universal Signature Red Line Standard + Shared Axis Date)
    c13 = hdr_table.cell(1, 3)
    p13_tag = c13.paragraphs[0]
    r13_tag = p13_tag.add_run("อนุมัติ\n\n"); format_docx_run(r13_tag, size_pt=13, bold=True)

    axis_appr = Inches(0.80)
    p_app_rk = c13.add_paragraph()
    p_app_rk.paragraph_format.tab_stops.add_tab_stop(axis_appr, WD_TAB_ALIGNMENT.RIGHT)
    p_app_rk.paragraph_format.space_after = Pt(22)
    r_ark = p_app_rk.add_run(f"\t{blueprint['metadata']['approver']['rank']}")
    format_docx_run(r_ark, size_pt=12, bold=False)

    p_app_nm = c13.add_paragraph()
    p_app_nm.paragraph_format.tab_stops.add_tab_stop(axis_appr, WD_TAB_ALIGNMENT.LEFT)
    p_app_nm.paragraph_format.space_after = Pt(2)
    r_anm = p_app_nm.add_run(f"\t{blueprint['metadata']['approver']['name']}")
    format_docx_run(r_anm, size_pt=12, bold=False)

    p_app_dt = c13.add_paragraph()
    p_app_dt.paragraph_format.tab_stops.add_tab_stop(axis_appr, WD_TAB_ALIGNMENT.LEFT)
    p_app_dt.paragraph_format.space_after = Pt(0)
    r_adt = p_app_dt.add_run(f"\t  {blueprint['metadata']['approver']['date']}")
    format_docx_run(r_adt, size_pt=12, bold=False)

    # Cell 1,4: ทะเบียน และหลักฐาน
    c14 = hdr_table.cell(1, 4)
    p14 = c14.paragraphs[0]
    r14_1_lbl = p14.add_run("สายงานที่ควบคุม  "); format_docx_run(r14_1_lbl, size_pt=12, bold=True)
    r14_1_val = p14.add_run("สาย สพ.\n\n"); format_docx_run(r14_1_val, size_pt=12, bold=False)
    r14_2_lbl = p14.add_run("ทะเบียน  "); format_docx_run(r14_2_lbl, size_pt=12, bold=True)
    r14_2_val = p14.add_run(f"{blueprint['metadata']['admin_data']['survey_reg'].replace('ทะเบียน ', '')}\n\n"); format_docx_run(r14_2_val, size_pt=12, bold=False)
    r14_3_lbl = p14.add_run("หลักฐานการรายงาน  "); format_docx_run(r14_3_lbl, size_pt=12, bold=True)
    r14_3_val = p14.add_run(f"{blueprint['metadata']['admin_data']['report_evidence'].replace('หลักฐานการรายงาน ', '')}\n\n"); format_docx_run(r14_3_val, size_pt=12, bold=False)
    r14_4_lbl = p14.add_run("ที่เก็บหลักฐานการตรวจสอบ  "); format_docx_run(r14_4_lbl, size_pt=12, bold=True)
    r14_4_val = p14.add_run(f"{blueprint['metadata']['admin_data']['storage_loc'].replace('ที่เก็บหลักฐานการตรวจสอบ ', '')}"); format_docx_run(r14_4_val, size_pt=12, bold=False)

    # Data Table (14 columns)
    num_data_rows = len(rows) + 3 # 2 header rows + data + 1 total row
    data_table = doc.add_table(rows=num_data_rows, cols=14)
    data_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    data_table.autofit = False

    # Proportional column widths in inches matching exactly 45.0%, 16.5%, 18.5%, 20.0%
    dt_widths = [
        Inches(0.53), Inches(0.73), Inches(4.68), Inches(0.53), Inches(0.59),
        Inches(0.53), Inches(0.53), Inches(0.59), Inches(0.59), Inches(1.25),
        Inches(0.66), Inches(0.66), Inches(0.59), Inches(0.73)
    ]

    for r_idx in range(num_data_rows):
        for c_idx in range(14):
            c = data_table.cell(r_idx, c_idx)
            c.width = dt_widths[c_idx]
            set_cell_margins(c, top=20, bottom=20, left=30, right=30)
            set_cell_borders(c)

    # Headers setup
    h_titles = [
        (0, 0, "ลำดับ"), (0, 1, "ใบสำรวจที่"), (0, 2, "หมายเลขสิ่งอุปกรณ์และรายการ"),
        (0, 3, "หน่วย\nนับ"), (0, 4, "ประเภท\nสิ่งอุปกรณ์"),
        (0, 5, "จำนวนสิ่งอุปกรณ์"), (0, 7, "เปรียบเทียบ"),
        (0, 9, "ราคา\nหน่วยละ"), (0, 10, "เปรียบเทียบราคารวม"),
        (0, 12, "ประเภท\nเงิน"), (0, 13, "หมายเหตุ")
    ]
    for c in [0, 1, 2, 3, 4, 9, 12, 13]:
        data_table.cell(0, c).merge(data_table.cell(1, c))
    data_table.cell(0, 5).merge(data_table.cell(0, 6))
    data_table.cell(0, 7).merge(data_table.cell(0, 8))
    data_table.cell(0, 10).merge(data_table.cell(0, 11))

    for r_i, c_i, txt in h_titles:
        cell = data_table.cell(r_i, c_i)
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt)
        format_docx_run(run, size_pt=11, bold=False)

    sub_headers = [(1, 5, "นับได้"), (1, 6, "บัญชีคุม"), (1, 7, "ขาด"), (1, 8, "เกิน"), (1, 10, "ขาด"), (1, 11, "เกิน")]
    for r_i, c_i, txt in sub_headers:
        cell = data_table.cell(r_i, c_i)
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(txt)
        format_docx_run(run, size_pt=11, bold=False)

    # Fill data rows with 12pt regular runs
    row_offset = 2
    for idx, item in enumerate(rows):
        r_num = row_offset + idx
        values = [
            (0, to_th(item["seq"]), WD_ALIGN_PARAGRAPH.CENTER),
            (1, item["survey_no"], WD_ALIGN_PARAGRAPH.CENTER),
            (2, f"{item['item_code']}  {item['item_name']}" if item['item_code'] != '-' else item['item_name'], WD_ALIGN_PARAGRAPH.LEFT),
            (3, item["unit"], WD_ALIGN_PARAGRAPH.CENTER),
            (4, item["type"], WD_ALIGN_PARAGRAPH.CENTER),
            (5, to_th(item["count_actual"]), WD_ALIGN_PARAGRAPH.CENTER),
            (6, to_th(item["count_ledger"]), WD_ALIGN_PARAGRAPH.CENTER),
            (7, item["diff_short"], WD_ALIGN_PARAGRAPH.CENTER),
            (8, item["diff_over"], WD_ALIGN_PARAGRAPH.CENTER),
            (9, to_th(f"{item['unit_price']:,.2f}") if item["unit_price"] else "-", WD_ALIGN_PARAGRAPH.RIGHT),
            (10, item["total_short"], WD_ALIGN_PARAGRAPH.CENTER),
            (11, item["total_over"], WD_ALIGN_PARAGRAPH.CENTER),
            (12, item["currency"], WD_ALIGN_PARAGRAPH.CENTER),
            (13, item["remark"], WD_ALIGN_PARAGRAPH.CENTER),
        ]
        for col_idx, val, align in values:
            cell = data_table.cell(r_num, col_idx)
            p = cell.paragraphs[0]; p.alignment = align
            run = p.add_run(val)
            format_docx_run(run, size_pt=12, bold=False)

    # Total Row
    tot_row_idx = row_offset + len(rows)
    data_table.cell(tot_row_idx, 0).merge(data_table.cell(tot_row_idx, 2))
    p_tot = data_table.cell(tot_row_idx, 0).paragraphs[0]; p_tot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tot = p_tot.add_run("รวมเงิน")
    format_docx_run(r_tot, size_pt=12.5, bold=True)

    # Footer paragraph
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(6)
    p_foot.paragraph_format.space_after = Pt(0)
    r_foot = p_foot.add_run(blueprint['metadata']['regulation'])
    format_docx_run(r_foot, size_pt=12, bold=False)

# Build Page 1
build_docx_page(doc, 1, blueprint['page_1_rows'])
# Build Page 2
doc.add_page_break()
build_docx_page(doc, 2, blueprint['page_2_rows'])

docx_out_path = os.path.join(WORKDIR, "ทบ_400_012_Rebuild_Thai.docx")
doc.save(docx_out_path)
print("Saved DOCX:", docx_out_path)
