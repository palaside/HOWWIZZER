import json, sys

with open('weekly_inspection_extracted.json', 'r', encoding='utf-8') as f:
    weekly = json.load(f)

with open('weekly_full_text.txt', 'w', encoding='utf-8') as out:
    for p in weekly:
        out.write(f"============================== PAGE {p['page']} ==============================\n")
        out.write(p['text'])
        out.write('\n\n')

print('Dumped to weekly_full_text.txt')
