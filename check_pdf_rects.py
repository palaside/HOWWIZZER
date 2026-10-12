import fitz

doc = fitz.open(r"d:\Project\WEPAPP\memo_inquiry_90_rendered.pdf")
print("Total pages in rendered PDF:", len(doc))
for i, p in enumerate(doc):
    print(f"Page {i+1} rect: {p.rect.width} x {p.rect.height} pt (approx {p.rect.width/72*25.4:.1f} x {p.rect.height/72*25.4:.1f} mm)")
