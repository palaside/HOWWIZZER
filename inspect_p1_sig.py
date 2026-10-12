import json
import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("ใบติดตามใบส่งซ่อมแบบ_ก_ต้นฉบับ.pdf") as plum:
    p1 = plum.pages[0]
    # filter words below y > 400
    sig_words = [w for w in p1.extract_words() if w["top"] > 400]
    for w in sorted(sig_words, key=lambda x: (x["top"], x["x0"])):
        print(f"x0={w['x0']:6.1f}, top={w['top']:6.1f}, bottom={w['bottom']:6.1f}: {w['text']}")
