import fitz

doc = fitz.open(r"d:\Project\WEPAPP\memo_90_rendered.pdf")
page = doc[0]
pix = page.get_pixmap(dpi=150)
out_path = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14\memo_90_rebuild.png"
pix.save(out_path)
print(f"Rendered successfully: {pix.width}x{pix.height} to {out_path}")
