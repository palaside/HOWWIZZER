import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
import urllib.parse
from backend.app import app

# Test both root and /static/docs/
doc_stems = [
    "แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai",
    "บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai",
    "ขอส่งใบติดตามทวงถาม_45_วัน_Rebuild_Thai",
    "ขอส่งใบติดตามทวงถาม_90_วัน_Rebuild_Thai",
    "บันทึกข้อความล่าสุดสุด_Rebuild_Thai",
    "บันทึกข้อความ_90_วัน_Rebuild_Thai",
    "ใบติดตามใบส่งซ่อมแบบ_ก_Rebuild_Thai",
    "ใบติดตามใบส่งซ่อมแบบ_ข_Rebuild_Thai",
    "รายงานผลการตรวจสอบ_ไตรมาส_Rebuild_Thai",
    "ทบ_400_012_Rebuild_Thai",
    "บันทึกผลการตรวจกิจการทั่วไป_ชุดตรวจที่_2_Rebuild_Thai",
    "ทบ_468_360_ปรนนิบัติบำรุง_Rebuild_Thai",
    "ใบสำรวจสิ่งอุปกรณ์_สาย_สพ_Rebuild_Thai",
    "สมุดประวัติการใช้ปืนใหญ่_Rebuild_Thai",
    "ประวัติการใช้อาวุธ_Rebuild_Thai",
    "บัญชีรายละเอียดหมายเลข_ปบค_Rebuild_Thai",
    "ทบ_468_204_Rebuild_Thai",
    "บัญชีคุมสิ่งอุปกรณ์ของหน่วยทบ400_005_Rebuild_Thai",
    "บัญชีคุมสิ่งอุปกรณ์ประเภท_2_และ_4_Rebuild_Thai",
]

test_urls = ["/", "/index.html", "/static/weekly_report.pdf", "/static/weekly_report_next.pdf"]

for stem in doc_stems:
    test_urls.append(f"/static/docs/{stem}.html")
    test_urls.append(f"/static/docs/{stem}.docx")
    test_urls.append(f"/static/docs/{stem}.xlsx")
    # Also test direct root fallback URLs
    test_urls.append(f"/{stem}.html")

async def request_asgi(path: str):
    response_headers = {}
    response_body = []
    status_code = None

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        nonlocal status_code
        if message["type"] == "http.response.start":
            status_code = message["status"]
            for k, v in message.get("headers", []):
                response_headers[k.decode("latin1")] = v.decode("latin1")
        elif message["type"] == "http.response.body":
            response_body.append(message.get("body", b""))

    # Unquoted path goes into ASGI path, quoted path into raw_path
    quoted_path = urllib.parse.quote(path)
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": path,
        "raw_path": quoted_path.encode("latin1"),
        "query_string": b"",
        "headers": [
            (b"host", b"127.0.0.1:8000"),
            (b"user-agent", b"test-runner"),
        ],
        "client": ("127.0.0.1", 12345),
        "server": ("127.0.0.1", 8000),
    }

    await app(scope, receive, send)
    body = b"".join(response_body)
    return status_code, response_headers, body

async def main():
    failures = []
    print(f"Testing {len(test_urls)} total document endpoints (HTML, DOCX, XLSX, PDF)...")
    for url in test_urls:
        status, headers, body = await request_asgi(url)
        if status != 200:
            failures.append((url, status))
            print(f"FAILED [{status}]: {url}")
        else:
            ct = headers.get("content-type", "unknown")

    if failures:
        print(f"\nCompleted with {len(failures)} failures.")
        sys.exit(1)
    else:
        print(f"\nSUCCESS: All {len(test_urls)} URLs passed with 200 OK! กดทุกครั้งคือเห็นเอกสาร ๑๐๐%")

if __name__ == "__main__":
    asyncio.run(main())
