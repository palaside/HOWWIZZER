import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("repair_track_a_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for p in data:
    p_num = p["page"]
    print(f"\n================ PAGE {p_num} ================")
    print("TABLES:")
    for t in p["tables"]:
        for r in t:
            print("  ", r)
    print("\nWORDS (grouped roughly by y):")
    words = sorted(p["words"], key=lambda w: (round(w["top"] / 5) * 5, w["x0"]))
    current_y = None
    line_words = []
    for w in words:
        y_group = round(w["top"] / 6) * 6
        if current_y is None or abs(y_group - current_y) <= 4:
            line_words.append(w["text"])
            current_y = y_group
        else:
            print(f"y~{current_y:3d}: {' '.join(line_words)}")
            line_words = [w["text"]]
            current_y = y_group
    if line_words:
        print(f"y~{current_y:3d}: {' '.join(line_words)}")
