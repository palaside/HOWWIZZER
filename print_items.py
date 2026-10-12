import json

with open('d:/Project/WEPAPP/all_items_extracted.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('d:/Project/WEPAPP/items_summary.txt', 'w', encoding='utf-8') as out:
    for it in items:
        out.write(f"=== ITEM {it['item_no']} (Page {it['page']}) ===\n")
        out.write(it['text'] + "\n\n")

print("Done writing items_summary.txt")
