import fitz, sys
sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open(r'docs/thai-docx.skill/ระบบเอกสาร/5.ประวัติการใช้อาวุธ ปืน.pdf')
page = doc[0]
for b in page.get_text('dict')['blocks']:
    if 'lines' in b:
        for l in b['lines']:
            for s in l['spans']:
                if s['bbox'][1] > 550:
                    print(f"bbox: ({s['bbox'][0]:.1f}, {s['bbox'][1]:.1f}, {s['bbox'][2]:.1f}, {s['bbox'][3]:.1f}) | font: {s['font']} | size: {s['size']:.1f} | text: '{s['text']}'")
