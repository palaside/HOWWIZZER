import fitz

doc = fitz.open(r"d:\Project\WEPAPP\memo_inquiry_90_p2.pdf")
print("Total pages:", len(doc))
for i, p in enumerate(doc):
    print(f"Page {i+1}: width={p.rect.width}, height={p.rect.height}")
    pix = p.get_pixmap(dpi=150)
    pix.save(f"C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14/test_tb400_012_p{i+1}.png")
print("Done saving test images!")
