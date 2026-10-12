from PIL import Image

img = Image.open('d:/Project/WEPAPP/current_render.png')
print(f"Rendered size: {img.size}")

# Let's crop around the header-data junction
# The page starts somewhere around top 100-300
crop = img.crop((500, 150, 1300, 450))
crop.save('d:/Project/WEPAPP/crop_current_render.png')
print("Saved crop_current_render.png")
