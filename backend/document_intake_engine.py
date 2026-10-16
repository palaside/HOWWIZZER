import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict

from .models.custom_document import CustomDocument, FilePaths

# Simple placeholder processors – in a real system these would generate HTML/PDF with proper styling.

def _process_excel(file_path: Path, meta: Dict) -> FilePaths:
    # For demo, just copy original and create an empty HTML preview.
    html_path = file_path.with_suffix('.html')
    html_path.write_text(f"<html><head><title>{meta.get('title', 'Document')}</title></head><body><h1>{meta.get('title')}</h1><p>Excel preview placeholder.</p></body></html>", encoding='utf-8')
    pdf_path = file_path.with_suffix('.pdf')
    # Create a simple PDF placeholder using text (requires reportlab, but we'll just copy the original for now).
    shutil.copyfile(file_path, pdf_path)
    return FilePaths(original=str(file_path), html=str(html_path), pdf=str(pdf_path))

def _process_docx(file_path: Path, meta: Dict) -> FilePaths:
    html_path = file_path.with_suffix('.html')
    html_path.write_text(f"<html><head><title>{meta.get('title', 'Document')}</title></head><body><h1>{meta.get('title')}</h1><p>DOCX preview placeholder.</p></body></html>", encoding='utf-8')
    pdf_path = file_path.with_suffix('.pdf')
    shutil.copyfile(file_path, pdf_path)
    return FilePaths(original=str(file_path), html=str(html_path), pdf=str(pdf_path))

def _process_pdf(file_path: Path, meta: Dict) -> FilePaths:
    # For PDF we keep the original and also generate an HTML wrapper that embeds the PDF.
    html_path = file_path.with_suffix('.html')
    html_path.write_text(f"<html><head><title>{meta.get('title', 'Document')}</title></head><body><embed src='{file_path.name}' type='application/pdf' width='100%' height='800px'></embed></body></html>", encoding='utf-8')
    return FilePaths(original=str(file_path), html=str(html_path), pdf=str(file_path))

def process_upload(file_path: Path, meta: Dict) -> CustomDocument:
    """Process an uploaded file and return a populated CustomDocument model.
    This function dispatches to format‑specific processors and assembles the
    resulting file paths into a CustomDocument instance.
    """
    file_type = file_path.suffix.lstrip('.').lower()
    if file_type == 'xlsx':
        files = _process_excel(file_path, meta)
    elif file_type == 'docx':
        files = _process_docx(file_path, meta)
    elif file_type == 'pdf':
        files = _process_pdf(file_path, meta)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    # Build CustomDocument model
    return CustomDocument(
        id=meta['id'],
        code=meta['code'],
        title=meta['title'],
        category=meta['category'],
        category_label=meta.get('category_label', meta['category']),
        desc=meta['desc'],
        uploaded_at=datetime.fromisoformat(meta['uploaded_at']),
        uploader=meta['uploader'],
        original_filename=meta['original_filename'],
        file_type=file_type,
        is_in_weekly_queue=meta.get('is_in_weekly_queue', False),
        queue_desc=meta.get('queue_desc'),
        files=files,
    )
