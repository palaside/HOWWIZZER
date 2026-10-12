import re
import json

with open("d:/Project/WEPAPP/parsed_all_23_items.json", "r", encoding="utf-8") as f:
    items_raw = json.load(f)

extracted = []

for item in items_raw:
    snip = item["snippet"]
    lines = [l.strip() for l in snip.split("\n") if l.strip()]
    
    extracted.append({
        "item_no": item["item_no"],
        "target": item["target"],
        "lines": lines
    })

with open("d:/Project/WEPAPP/detailed_items_lines.json", "w", encoding="utf-8") as f:
    json.dump(extracted, f, ensure_ascii=False, indent=2)

print("Saved detailed_items_lines.json")
