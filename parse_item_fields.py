import json
import re

with open("d:/Project/WEPAPP/all_items_extracted.json", "r", encoding="utf-8") as f:
    items = json.load(f)

parsed_records = []

for it in items:
    txt = it["text"]
    no = it["item_no"]
    
    # NSN pattern
    # e.g. 1015 – 00 – 722 - 9752 or 5180 – 00 – 757 - 7727 or 66885 – 00 – 344 – 4613 or - or 1015-615-7208
    # Search between "รำยกำร" / "รายการ" and the unit/location or next text
    
    parsed_records.append({
        "item_no": no,
        "survey_no": f"{no}/66",
        "raw_snippet": txt[:300]
    })

for p in parsed_records[:10]:
    print(f"[{p['survey_no']}] {p['raw_snippet']}\n")
