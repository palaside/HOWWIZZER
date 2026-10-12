import json

# Let's inspect pages in groups to reconstruct the items
with open('tb400_005_all_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Let's write an analysis of all cards
with open('cards_detail.txt', 'w', encoding='utf-8') as out:
    for p in pages:
        p_num = p['page']
        out.write(f"\n==================== PAGE {p_num} ====================\n")
        out.write(p['full_text'])
        out.write("\n")

print("Wrote cards_detail.txt")
