import fitz
import json
import re

doc = fitz.open(r"d:\Project\WEPAPP\docs\thai-docx.skill\ระบบเอกสาร\4.ใบสำรวจสิ่งอุปกรณ์ สาย สพ ผบ.ร้อย.pdf")

cards_data = []

for page_idx in range(len(doc)):
    page = doc[page_idx]
    mid_y = 306.0
    
    # We will inspect words with bbox
    words = page.get_text("words") # (x0, y0, x1, y1, word, block_no, line_no, word_no)
    
    top_words = [w for w in words if (w[1] + w[3])/2 < mid_y]
    bot_words = [w for w in words if (w[1] + w[3])/2 >= mid_y]
    
    for section_name, sec_words in [("top", top_words), ("bottom", bot_words)]:
        if not sec_words:
            continue
            
        full_text = " ".join([w[4] for w in sec_words])
        if "ใบส" not in full_text and "ที่ใบส" not in full_text and "1015" not in full_text:
            continue
            
        cards_data.append({
            "page": page_idx + 1,
            "section": section_name,
            "words_count": len(sec_words),
            "text": full_text
        })

print(f"Total valid card sections found: {len(cards_data)}")
for c in cards_data:
    # Look for survey number
    m_no = re.search(r"(\d+/66)", c["text"])
    no_str = m_no.group(1) if m_no else "N/A"
    print(f"Page {c['page']} ({c['section']}): Survey No = {no_str}")
