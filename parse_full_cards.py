import json
import re

with open('tb400_005_all_pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Let's write an intelligent extractor that parses each card
# Let's inspect pages and match cards
print(f"Loaded {len(pages)} pages")
