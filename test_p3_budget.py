import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 1600})
    
    # Test Page 3: 16 rows + double signature
    p3_html = '''<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
<style>
@page { size: A4 portrait; margin: 0; }
body { margin: 0; padding: 0; font-family: 'Sarabun', sans-serif; }
.page { width: 210mm; height: 297mm; padding: 15mm 20mm; box-sizing: border-box; overflow: hidden; display: flex; flex-direction: column; }
table { width: 100%; border-collapse: collapse; font-size: FONT_SIZE; line-height: 1.18; }
th, td { border: 1px solid #000; padding: 0.8mm 1.5mm; }
</style>
</head>
<body>
<div class="page">
<table>
<thead><tr><th style="width: 14mm;">ลำดับ</th><th>หัวข้อการตรวจ</th><th style="width: 35mm;">ผลการตรวจ</th></tr></thead>
<tbody>
''' + ''.join([f'<tr><td style="text-align:center;">{i}</td><td>หัวข้อการตรวจทดสอบที่ {i} รายละเอียดของเนื้อหา</td><td style="text-align:center;">เรียบร้อย</td></tr>' for i in range(1, 17)]) + '''
</tbody>
</table>
<div style="margin-top: 8mm; margin-left: 100mm; font-size: 16pt;">
    <div style="margin-bottom: 7mm;">จ.ส.อ. ...... ผู้แก้ไข<br>(ณัฐชัย  รักษาวงษ์)<br>ส.หน.สย.ป.๔ พัน.๔ ร้อย.๒</div>
    <div>ร.อ. ...... ผู้ตรวจ<br>(กฤติน  นราพงษ์)<br>ผบ.ป.๔ พัน.๔ ร้อย.๒<br>มิ.ย. ๖๙</div>
</div>
</div>
</body>
</html>'''
    for fz in ['13.5pt', '14pt', '15pt', '16pt', '17pt']:
        c = p3_html.replace('FONT_SIZE', fz)
        page.set_content(c)
        sh = page.evaluate('document.querySelector(".page").scrollHeight')
        ch = page.evaluate('document.querySelector(".page").clientHeight')
        print(f'Page 3: font={fz} -> sh={sh}, ch={ch}, pass={sh <= ch}')

    browser.close()
