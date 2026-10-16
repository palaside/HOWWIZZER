import os
import shutil
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
FRONTEND_STATIC_DOCS = WORKSPACE / "frontend" / "static" / "docs"
FRONTEND_STATIC = WORKSPACE / "frontend" / "static"
STATIC_DOCS = WORKSPACE / "static" / "docs"
STATIC_ROOT = WORKSPACE / "static"

FRONTEND_STATIC_DOCS.mkdir(parents=True, exist_ok=True)
STATIC_DOCS.mkdir(parents=True, exist_ok=True)

# List of files to relocate/copy
doc_patterns = [
    "*Rebuild_Thai*.html",
    "*Rebuild_Thai*.docx",
    "*Rebuild_Thai*.xlsx",
    "weekly_report*.pdf",
    "บัญชีรายการและสิ่งอุปกรณ์.*"
]

copied_files = []

for pattern in doc_patterns:
    for f in WORKSPACE.glob(pattern):
        if f.is_file():
            # Copy to frontend/static/docs
            dest1 = FRONTEND_STATIC_DOCS / f.name
            shutil.copy2(f, dest1)
            # Copy to static/docs
            dest2 = STATIC_DOCS / f.name
            shutil.copy2(f, dest2)
            copied_files.append(f.name)

# Also ensure PDFs are directly in frontend/static and static
for pdf_name in ["weekly_report.pdf", "weekly_report_next.pdf"]:
    src = STATIC_ROOT / pdf_name
    if src.exists():
        shutil.copy2(src, FRONTEND_STATIC / pdf_name)
        shutil.copy2(src, FRONTEND_STATIC_DOCS / pdf_name)
        shutil.copy2(src, STATIC_DOCS / pdf_name)
        copied_files.append(pdf_name)

print(f"Successfully copied/relocated {len(set(copied_files))} unique files into frontend/static/docs and static/docs.")
