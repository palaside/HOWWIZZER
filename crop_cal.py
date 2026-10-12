from PIL import Image

im = Image.open('C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14/tb468_360_page_3_calendar.png')
# Crop top-left of calendar
crop_im = im.crop((50, 100, 450, 300))
crop_file = 'C:/Users/EVE/.gemini/antigravity-ide/brain/7ca9cd9b-6ae7-44b7-ab50-280c021eef14/tb468_360_cal_topleft_crop.png'
crop_im.save(crop_file)
print("Crop saved:", crop_file)
