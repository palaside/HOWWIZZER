import fitz
import json

doc = fitz.open('docs/thai-docx.skill/ระบบเอกสาร/11.ทบ468-360 ปรนนิบัติบำรุง.pdf')
report = {}

for p_no, page in enumerate(doc):
    blocks = page.get_text('dict')['blocks']
    page_data = {
        'rect': [page.rect.x0, page.rect.y0, page.rect.x1, page.rect.y1],
        'text_blocks': [],
        'drawings_count': len(page.get_drawings())
    }
    for b in blocks:
        if b.get('type') == 0: # text
            for line in b.get('lines', []):
                for span in line.get('spans', []):
                    txt = span.get('text', '').strip()
                    if txt:
                        page_data['text_blocks'].append({
                            'text': txt,
                            'font': span.get('font'),
                            'size': span.get('size'),
                            'flags': span.get('flags'),
                            'bbox': [round(x, 2) for x in span.get('bbox')]
                        })
    report[f'page_{p_no+1}'] = page_data

with open('deep_analysis_468_360.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Deep analysis finished.")
