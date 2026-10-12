import pdfplumber
import json

with pdfplumber.open('docs/thai-docx.skill/ระบบเอกสาร/400-012 ผบ.ร้อย.pdf') as pdf:
    p = pdf.pages[0]
    print(f"Page size: {p.width} x {p.height}")
    
    # Extract lines / rects
    lines = p.lines
    print(f"Total lines: {len(lines)}")
    
    # Find all vertical lines in header (top < 250)
    v_lines = sorted([l['x0'] for l in lines if abs(l['x0'] - l['x1']) < 2 and l['top'] < 200])
    print(f"Header vertical line X coords: {sorted(list(set([round(x, 1) for x in v_lines])))}")
    
    # Extract text with bounding boxes in header
    words = p.extract_words()
    header_words = [w for w in words if w['top'] < 160]
    for w in sorted(header_words, key=lambda x: (round(x['top']/5)*5, x['x0'])):
        print(f"y={w['top']:5.1f}, x={w['x0']:5.1f}-{w['x1']:5.1f}: {w['text']}")
