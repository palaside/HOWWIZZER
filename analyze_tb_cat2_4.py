import json
import sys

with open(r'd:\Project\WEPAPP\tb_cat2_4_pages_info.json', encoding='utf-8') as f:
    pages = json.load(f)

out_lines = []
out_lines.append(f"Total pages: {len(pages)}")
out_lines.append("\n--- FIRST 15 PAGES ---")
for p in pages[:15]:
    out_lines.append(f"=== PAGE {p['page']} ===")
    lines = [line.strip() for line in p['text'].split('\n') if line.strip()]
    for line in lines[:10]:
        out_lines.append(f"   {line}")

out_lines.append("\n--- LAST 6 PAGES ---")
for p in pages[-6:]:
    out_lines.append(f"=== PAGE {p['page']} ===")
    lines = [line.strip() for line in p['text'].split('\n') if line.strip()]
    for line in lines[:10]:
        out_lines.append(f"   {line}")

with open(r'd:\Project\WEPAPP\analysis_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print("Analysis written to analysis_output.txt")
