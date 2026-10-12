import fitz
import os

pdf_path = r"d:\Project\WEPAPP\memo_inquiry_90_rendered.pdf"
doc = fitz.open(pdf_path)
out_dir = r"C:\Users\EVE\.gemini\antigravity-ide\brain\7ca9cd9b-6ae7-44b7-ab50-280c021eef14"

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_img = os.path.join(out_dir, f"memo_inquiry_90_rebuild_p{i+1}.png")
    pix.save(out_img)
    print(f"Saved rebuilt page {i+1}: {pix.width}x{pix.height} to {out_img}")

print("All rebuilt pages rendered successfully!")
