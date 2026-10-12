import sys
import pypdf
import json

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader(r"d:/Project/WEPAPP/docs/thai-docx.skill/ระบบเอกสาร/400-012 ผบ.ร้อย.pdf")
p1 = reader.pages[0]

text_instances = []
def visitor_body(text, cm, tm, font_dict, font_size):
    if text.strip():
        base_font = font_dict.get('/BaseFont', 'Unknown') if font_dict else 'Unknown'
        text_instances.append({
            'text': text.strip(),
            'x': round(tm[4], 1),
            'y': round(tm[5], 1),
            'font': str(base_font).replace('/',''),
            'size': round(font_size, 1)
        })

p1.extract_text(visitor_text=visitor_body)
print(f"Total text snippets: {len(text_instances)}")

# Group by font and size
font_stats = {}
for t in text_instances:
    key = (t['font'], t['size'])
    font_stats[key] = font_stats.get(key, 0) + 1

print("\n--- FONT HIERARCHY ---")
for k, count in sorted(font_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"Font: {k[0]:<25} Size: {k[1]:<5} Count: {count}")

print("\n--- SAMPLE KEY TEXT WITH POSITIONS ---")
for t in text_instances:
    if any(k in t['text'] for k in ['๔๐๐', 'ใบรายงาน', 'นามหน่วย', 'ขอรับรอง', 'ลำดับ', 'หมายเลข', 'ปบค', 'รวมเงิน']):
        print(f"X={t['x']:<6} Y={t['y']:<6} Size={t['size']:<4} Font={t['font']:<20} Text={t['text']}")
