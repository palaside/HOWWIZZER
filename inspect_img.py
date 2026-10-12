from PIL import Image

img = Image.open('C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14/.user_uploaded/media_1791587628825.png')
w, h = img.size
print(f"Image dimensions: {w}x{h}")

# Find black lines along a horizontal line in top half (y=50) and table header (y=150)
for y in [20, 50, 80, 115, 140, 180]:
    black_xs = []
    for x in range(w):
        r, g, b = img.getpixel((x, y))[:3]
        if r < 100 and g < 100 and b < 100:
            black_xs.append(x)
    print(f"y={y}: black x positions: {black_xs[:20]}")
