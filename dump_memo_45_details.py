import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('memo_inquiry_45_spans.json', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    print(f"\n{'='*20} PAGE {p['page']} ({p['width']} x {p['height']}) {'='*20}")
    # group by y-approx
    lines = {}
    for s in p['spans']:
        t = s['text'].strip()
        if not t:
            continue
        y = round(s['bbox'][1] / 5.0) * 5
        lines.setdefault(y, []).append(s)
    
    for y in sorted(lines.keys()):
        items = sorted(lines[y], key=lambda x: x['bbox'][0])
        line_str = " | ".join([f"x={it['bbox'][0]:.1f}: {it['text'].strip()}" for it in items])
        print(f"y~{y}: {line_str}")
