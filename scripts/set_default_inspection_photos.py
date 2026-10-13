import base64
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    src_img = r"D:\Project\DOCS HOWWIZ\IMG_1283.JPG"
    if not os.path.exists(src_img):
        src_img = r"backend/data/default_inspection_photo.jpg"
    
    with open(src_img, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64}"

    target_files = [
        "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html",
        "page1_sd1_template.html",
        "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html",
        os.path.join("references", "approved_sd1_weekly_report", "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html"),
        os.path.join("references", "approved_weekly_inspection", "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html")
    ]

    for fp in target_files:
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()

            count = [0]
            def repl(m):
                count[0] += 1
                if count[0] <= 4:
                    card_html = m.group(0)
                    new_card = re.sub(r'src="data:image/[^"]+"', f'src="{data_uri}"', card_html)
                    return new_card
                return m.group(0)

            new_content = re.sub(r'<div class="photo-card">[\s\S]*?</div>', repl, content)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {fp}: replaced {count[0]} cards with IMG_1283")

if __name__ == "__main__":
    main()
