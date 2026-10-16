import re

with open("frontend/static/dashboard.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace file paths in MASTER_DOC_INVENTORY
new_content = re.sub(r"htmlFile:\s*'/(?!static/docs/)", "htmlFile: '/static/docs/", content)
new_content = re.sub(r"docxFile:\s*'/(?!static/docs/)", "docxFile: '/static/docs/", new_content)
new_content = re.sub(r"xlsxFile:\s*'/(?!static/docs/)", "xlsxFile: '/static/docs/", new_content)

with open("frontend/static/dashboard.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated frontend/static/dashboard.js with /static/docs/ paths successfully!")
