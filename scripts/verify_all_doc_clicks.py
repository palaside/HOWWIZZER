import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import urllib.parse
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

test_docs = [
    "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html",
    "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.docx",
    "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.xlsx",
    "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html",
    "ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai.html",
    "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai.html",
    "บันทึกข้อความล่าสุดสุด_Rebuild_Thai.html",
    "บันทึกข้อความ_90_วัน_Rebuild_Thai.html",
    "ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai.html",
    "ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai.html",
    "รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai.html",
    "ทบ_400_012_Rebuild_Thai.html",
    "บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai.html",
    "ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai.html",
    "ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai.html",
    "สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai.html",
    "ประวัติการใช้อาวุธ_Rebuild_Thai.html",
    "บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai.html",
    "ทบ_468_204_Rebuild_Thai.html",
    "บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai.html",
    "บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai.html",
]

failures = []

print("=== 1. Testing Direct Root URL (e.g. /filename) ===")
for doc in test_docs:
    # URL encoded request
    encoded_url = "/" + urllib.parse.quote(doc)
    res = client.get(encoded_url)
    if res.status_code != 200:
        failures.append(f"Root URL failed for {doc}: status {res.status_code}")
    else:
        print(f"PASS: {encoded_url[:40]}... -> 200 OK ({len(res.content)} bytes)")

print("\n=== 2. Testing Static Docs URL (e.g. /static/docs/filename) ===")
for doc in test_docs:
    encoded_url = "/static/docs/" + urllib.parse.quote(doc)
    res = client.get(encoded_url)
    if res.status_code != 200:
        failures.append(f"Static docs URL failed for {doc}: status {res.status_code}")
    else:
        print(f"PASS: {encoded_url[:40]}... -> 200 OK ({len(res.content)} bytes)")

print("\n=== 3. Testing PDFs ===")
for pdf in ["weekly_report.pdf", "weekly_report_next.pdf"]:
    res1 = client.get(f"/static/{pdf}")
    res2 = client.get(f"/{pdf}")
    if res1.status_code != 200 or res2.status_code != 200:
        failures.append(f"PDF failed for {pdf}")
    else:
        print(f"PASS: /static/{pdf} and /{pdf} -> 200 OK")

if failures:
    print(f"\nFAILED with {len(failures)} errors:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
else:
    print("\nALL DOCUMENTS AND URLS PASSED WITH 200 OK! กดทุกครั้งคือเห็นเอกสาร ๑๐๐%")
