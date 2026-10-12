import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('table_layout_sd1.json', 'r', encoding='utf-8') as f:
    bp = json.load(f)

with open('weekly_full_text.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

print("=== CHECKING SECTIONS ===")
s1 = bp['inspection_form_sd1']['section_1']['items']
print(f"Section 1 items: {len(s1)}")
for it in s1:
    print(f"  {it['code']} {it['text'][:25]} -> {it['result']}")

s2 = bp['inspection_form_sd1']['section_2']['subsections']
for sub in s2:
    print(f"Section 2: {sub.get('id')} {sub.get('title') or sub.get('subtitle') or sub.get('name')} ({len(sub['items'])} items)")
    for it in sub['items']:
        print(f"    - {it.get('text', '')[:35]} -> {it.get('result')}")

s3 = bp['inspection_form_sd1']['section_3']['items']
print(f"Section 3 items: {len(s3)}")
for it in s3:
    print(f"  {it['code']} {it['text'][:25]} -> {it['result']}")

s4 = bp['inspection_form_sd1']['section_4']['items']
print(f"Section 4 items: {len(s4)}")
for it in s4:
    print(f"  {it['code']} {it['text'][:25]} -> {it['result']}")

s5 = bp['inspection_form_sd1']['section_5']['items']
print(f"Section 5 items: {len(s5)}")
for it in s5:
    print(f"  {it['code']} {it['text'][:25]} -> {it['result']}")
