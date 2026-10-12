import pdfplumber
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open("ใบติดตามใบส่งซ่อมแบบ_ก_ต้นฉบับ.pdf") as plum:
    p1 = plum.pages[0]
    tables = p1.find_tables()
    for t in tables:
        print("Table bbox:", t.bbox)
        for row in t.rows:
            print("Row bbox:", row.bbox)
            for cell in row.cells:
                print("   Cell:", cell)
