import fitz, json, sys

pdf_path = r'd:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\7.ขอส่งใบติดตามทวงถาม 45 วัน.pdf'
doc = fitz.open(pdf_path)

data = []
for pno in range(len(doc)):
    page = doc[pno]
    p_data = {'page': pno + 1, 'width': page.rect.width, 'height': page.rect.height, 'spans': []}
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    p_data['spans'].append({
                        'text': s['text'],
                        'bbox': [round(x, 1) for x in s['bbox']],
                        'size': round(s['size'], 1),
                        'font': s['font']
                    })
    data.append(p_data)

with open('memo_inquiry_45_spans.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved memo_inquiry_45_spans.json')
for p in data:
    print(f"Page {p['page']}: {len(p['spans'])} spans")
