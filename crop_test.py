from PIL import Image

img = Image.open('C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14/.user_uploaded/media_1791587628825.png')
# Save crops to inspect
crop1 = img.crop((270, 0, 580, 75))
crop1.save('d:/Project/WEPAPP/crop_top_middle.png')

print("Cropped saved")
