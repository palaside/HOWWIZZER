from playwright.sync_api import sync_playwright

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700&display=swap');
body {
    font-family: 'TH Sarabun PSK', 'TH Sarabun New', 'Sarabun', sans-serif;
    padding: 20px;
    background: #fff;
}
table {
    border-collapse: collapse;
    width: 600px;
    margin-bottom: 20px;
}
th, td {
    border: 1px solid #000;
    text-align: center;
    font-size: 11pt;
}

/* Option A: Current */
.opt-a th {
    padding: 2px 3px;
    height: 7mm;
    vertical-align: middle;
}

/* Option B: padding-top: 0px, padding-bottom: 4px */
.opt-b th {
    padding: 1px 3px 5px 3px;
    height: 7mm;
    vertical-align: middle;
    line-height: 1.0;
}

/* Option C: padding: 3px 3px 6px 3px, line-height: 1.0 */
.opt-c th {
    padding: 2px 3px 6px 3px;
    height: 8mm;
    vertical-align: middle;
    line-height: 1.0;
}

/* Option D: flex center */
.opt-d th {
    height: 8mm;
    vertical-align: middle;
    padding: 0 3px 4px 3px;
    line-height: 1.1;
}
</style>
</head>
<body>
<h3>Option A (Current)</h3>
<table class="opt-a">
<tr>
    <th style="width: 20%;">ว.ด.ป.</th>
    <th style="width: 15%;">จำนวน</th>
    <th style="width: 35%;">หน่วย / ที่ตั้ง</th>
    <th style="width: 30%;">รายการหลักฐาน</th>
</tr>
</table>

<h3>Option B (padding: 1px 3px 5px 3px)</h3>
<table class="opt-b">
<tr>
    <th style="width: 20%;">ว.ด.ป.</th>
    <th style="width: 15%;">จำนวน</th>
    <th style="width: 35%;">หน่วย / ที่ตั้ง</th>
    <th style="width: 30%;">รายการหลักฐาน</th>
</tr>
</table>

<h3>Option C (padding: 2px 3px 6px 3px)</h3>
<table class="opt-c">
<tr>
    <th style="width: 20%;">ว.ด.ป.</th>
    <th style="width: 15%;">จำนวน</th>
    <th style="width: 35%;">หน่วย / ที่ตั้ง</th>
    <th style="width: 30%;">รายการหลักฐาน</th>
</tr>
</table>

<h3>Option D (padding: 0 3px 4px 3px)</h3>
<table class="opt-d">
<tr>
    <th style="width: 20%;">ว.ด.ป.</th>
    <th style="width: 15%;">จำนวน</th>
    <th style="width: 35%;">หน่วย / ที่ตั้ง</th>
    <th style="width: 30%;">รายการหลักฐาน</th>
</tr>
</table>
</body>
</html>
"""

open(r'd:\Project\WEPAPP\test_vcenter.html', 'w', encoding='utf-8').write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 800, "height": 600}, device_scale_factor=2)
    page.goto(r'file:///d:/Project/WEPAPP/test_vcenter.html')
    page.screenshot(path=r'C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14\test_vcenter.png')
    browser.close()

print("Screenshot test_vcenter.png taken")
