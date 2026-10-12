import json

with open('tb400_005_extracted_raw.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

# Let's see what each page contains in raw
cards = []

# Let's inspect each page's text and table to extract:
for p in raw:
    p_num = p['page']
    txt = p['text']
    tbls = p['tables']
    
    # Save a text summary for each page
    with open(f"page_{p_num:02d}.txt", "w", encoding="utf-8") as pf:
        pf.write(f"=== PAGE {p_num} ===\n")
        pf.write(txt)
        pf.write("\n\n--- TABLES ---\n")
        for t_idx, t in enumerate(tbls):
            pf.write(f"\nTable {t_idx} ({len(t)}x{len(t[0]) if t else 0}):\n")
            for r in t:
                pf.write(str(r) + "\n")

print("Dumped 35 pages text and tables to individual files")
