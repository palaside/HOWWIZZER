import json
import re

with open(r'd:\Project\WEPAPP\tb_cat2_4_pages_info.json', encoding='utf-8') as f:
    pages = json.load(f)

print(f"Total pages: {len(pages)}")

# Let's inspect page 7 to 179
cards = []
i = 6 # Page index for page 7 (0-based)
while i < len(pages) - 2:
    p_top = pages[i]
    p_bot = pages[i+1] if i + 1 < len(pages) else None
    
    # Check if p_top is card top
    if "ทบ.๔๐๐" in p_top['text'] or "บัญชีสิ่งอุปกรณ์ของหน่วย" in p_top['text']:
        card_text_top = p_top['text']
        card_text_bot = p_bot['text'] if p_bot else ""
        
        # Try to find item name, nsn, unit, etc.
        combined = card_text_top + "\n" + card_text_bot
        
        # Extract NSN
        nsn_m = re.search(r'หม[ำา]ยเลขสิ่งอุปกรณ์\s*([0-9A-Za-z\-\s]+)', combined)
        nsn = nsn_m.group(1).strip() if nsn_m else "-"
        
        # Extract Item Name
        name_m = re.search(r'ชื่อสิ่งอุปกรณ์\s*([^\n\r]+)', combined)
        name = name_m.group(1).strip() if name_m else "-"
        
        # Extract Unit
        unit_m = re.search(r'(อัน|ชุด|เครื่อง|กล้อง|กระบอก|ท่อน|เล่ม|ซอง|ชิ้น|กล่อง|ผืน|หลัง)', combined)
        unit = unit_m.group(1) if unit_m else "-"
        
        # Extract Price
        price_m = re.search(r'ร[ำา]ค[ำา]\s*([0-9\,\.\s]+บ[ำา]ท|[0-9\,\.]+)', combined)
        price = price_m.group(1).strip() if price_m else "-"

        cards.append({
            'card_idx': len(cards) + 1,
            'page_top': p_top['page'],
            'page_bot': p_bot['page'] if p_bot else None,
            'name': name,
            'nsn': nsn,
            'unit': unit,
            'price': price
        })
        i += 2
    else:
        i += 1

print(f"Total cards found: {len(cards)}")

with open(r'd:\Project\WEPAPP\extracted_cat2_4_cards.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, ensure_ascii=False, indent=2)

print("Saved extracted_cat2_4_cards.json")
for c in cards[:10]:
    print(f"Card {c['card_idx']}: {c['name']} | NSN: {c['nsn']} | Unit: {c['unit']} | Price: {c['price']}")
if len(cards) > 10:
    print("...")
    for c in cards[-5:]:
        print(f"Card {c['card_idx']}: {c['name']} | NSN: {c['nsn']} | Unit: {c['unit']} | Price: {c['price']}")
