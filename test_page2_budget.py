import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

html_template = '''<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page { size: A4 portrait; margin: 0; }
body { margin: 0; padding: 0; font-family: 'Sarabun', sans-serif; }
.page { width: 210mm; height: 297mm; padding: 12mm 18mm 12mm 22mm; box-sizing: border-box; overflow: hidden; display: flex; flex-direction: column; }
table { width: 100%; border-collapse: collapse; font-size: FONT_SIZE; line-height: LINE_HEIGHT; }
th, td { border: 1px solid #000; padding: PADDING; }
</style>
</head>
<body>
<div class="page">
<div style="font-size: 16pt; font-weight: bold; text-align: center; margin-bottom: 2mm;">แบบรายงานผลการตรวจอาวุธ และสิ่งอุปกรณ์ประจำโรงเก็บปืนใหญ่</div>
<div style="font-size: 13.5pt; font-weight: bold; text-align: center; margin-bottom: 3mm;">หน่วย ป.๔ พัน.๔ ร้อย.๒<br>สัปดาห์ที่ ๓ ตั้งแต่วันที่ ๑๕ มิ.ย. – ๑๙ มิ.ย. ๖๙<br>(ตรวจในวันวันศุกร์ที่ ๑๙ มิ.ย. ๖๙  เวลา  ๑๓๐๐ – ๑๕๐๐ น.)</div>
<table>
<thead><tr><th style="width: 14mm;">ลำดับ</th><th>หัวข้อการตรวจ</th><th style="width: 35mm;">ผลการตรวจ</th></tr></thead>
<tbody>
''' + ''.join([f'<tr><td style="text-align:center;">{i}</td><td>หัวข้อการตรวจทดสอบที่ {i} รายละเอียดของเนื้อหา</td><td style="text-align:center;">เรียบร้อย</td></tr>' for i in range(1, 30)]) + '''
</tbody>
</table>
</div>
</body>
</html>'''

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 1600})
    for fz in ['10.5pt', '11pt', '11.5pt', '12pt', '12.5pt', '13pt', '14pt', '15pt', '16pt', '17pt']:
        for pad in ['0.8mm 1.5mm', '0.6mm 1.2mm', '0.4mm 1.0mm']:
            content = html_template.replace('FONT_SIZE', fz).replace('LINE_HEIGHT', '1.15').replace('PADDING', pad)
            page.set_content(content)
            sh = page.evaluate('document.querySelector(".page").scrollHeight')
            ch = page.evaluate('document.querySelector(".page").clientHeight')
            if sh <= ch:
                print(f'PASS: font={fz}, pad={pad} -> scrollHeight={sh} <= {ch}')
            else:
                print(f'OVERFLOW: font={fz}, pad={pad} -> scrollHeight={sh} > {ch}')
    browser.close()
