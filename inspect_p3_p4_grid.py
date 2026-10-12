import fitz

doc = fitz.open('docs/thai-docx.skill/ระบบเอกสาร/11.ทบ468-360 ปรนนิบัติบำรุง.pdf')
p3 = doc[2]
p4 = doc[3]

p3_drawings = p3.get_drawings()
p4_drawings = p4.get_drawings()

print("P3 drawings rects y-range:")
y_coords_p3 = sorted(list(set([round(d['rect'].y0, 1) for d in p3_drawings if 'rect' in d])))
print("P3 unique y0:", y_coords_p3[:15], "...", y_coords_p3[-10:])

print("\nP4 drawings rects y-range:")
y_coords_p4 = sorted(list(set([round(d['rect'].y0, 1) for d in p4_drawings if 'rect' in d])))
print("P4 unique y0:", y_coords_p4)

# Let's inspect text on P3
print("\nP3 Text items:")
for b in p3.get_text('dict')['blocks']:
    if b.get('type') == 0:
        for l in b['lines']:
            for s in l['spans']:
                if s['text'].strip():
                    print(f"  y={s['bbox'][1]:.1f}: '{s['text']}'")
