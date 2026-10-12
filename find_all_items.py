import re
import json

with open("d:/Project/WEPAPP/all_survey_stream.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find each item occurrence
# Patterns:
# "ที่ใบสำรวจ" or "ที่ใบส ำรวจ" followed by "X/66"
items = []

# Let's inspect where "1/66", "2/66", ... "23/66" appear
for i in range(1, 24):
    target = f"{i}/66"
    pos = content.find(target)
    if pos != -1:
        # Extract snippet around this position
        start = max(0, pos - 400)
        end = min(len(content), pos + 600)
        snippet = content[start:end]
        items.append({
            "item_no": i,
            "target": target,
            "pos": pos,
            "snippet": snippet
        })
    else:
        print(f"WARNING: Item {target} NOT found!")

print(f"Found {len(items)} items.")

with open("d:/Project/WEPAPP/parsed_all_23_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("Saved parsed_all_23_items.json")
