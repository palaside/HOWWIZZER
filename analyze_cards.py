import json

with open('tb400_005_extracted_raw.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

with open('cards_analysis.txt', 'w', encoding='utf-8') as out:
    for p in raw:
        txt = p['text']
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        has_header = any('บัญชีสิ่งอุปกรณ์ของหน่วย' in l for l in lines)
        has_back = any('รายการสถานที่อยู่ของสิ่งอุปกรณ์' in l for l in lines)
        has_toc = any('สารบัญ' in l for l in lines)
        
        item_name = ''
        nsn = ''
        for l in lines:
            if 'ชื่อสิ่งอุปกรณ์' in l:
                item_name = l
            if 'หมายเลขสิ่งอุปกรณ์' in l:
                nsn = l
                
        t_shapes = [f"{len(t)}r x {len(t[0]) if t else 0}c" for t in p['tables']]
        page_num = p['page']
        out.write(f"P{page_num:02d}: Head={has_header} Back={has_back} TOC={has_toc} | Tbls={t_shapes} | NSN={nsn} | Name={item_name}\n")

print('Wrote cards_analysis.txt')
