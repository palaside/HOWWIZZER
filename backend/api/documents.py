from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pathlib import Path
import uuid
from datetime import datetime

from ..utils.json_store import load_custom_documents, save_custom_documents
from ..models.custom_document import CustomDocument, FilePaths
from ..document_intake_engine import process_upload

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_ROOT = Path(__file__).resolve().parents[2] / "frontend" / "static" / "docs" / "uploads"
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

@router.get("/custom")
def get_custom_documents():
    return load_custom_documents()

@router.post("/register")
async def register_document(
    file: UploadFile = File(...),
    code: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    desc: str = Form(...),
    is_in_weekly_queue: bool = Form(False),
    queue_desc: str | None = Form(None),
    uploader: str = Form(...)
):
    # Save original file
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    doc_id = f"doc-custom-{timestamp}"
    original_path = UPLOAD_ROOT / f"{doc_id}_{file.filename}"
    with original_path.open('wb') as out_file:
        content = await file.read()
        out_file.write(content)
    # Process file to generate previews
    doc_meta = {
        "id": doc_id,
        "code": code,
        "title": title,
        "category": category,
        "category_label": category,  # simplistic mapping
        "desc": desc,
        "uploaded_at": datetime.utcnow().isoformat(),
        "uploader": uploader,
        "original_filename": file.filename,
        "file_type": original_path.suffix.lstrip('.'),
        "is_in_weekly_queue": is_in_weekly_queue,
        "queue_desc": queue_desc,
    }
    custom_doc = process_upload(original_path, doc_meta)
    # Persist
    docs = load_custom_documents()
    docs.append(custom_doc)
    save_custom_documents(docs)
    return custom_doc

@router.delete("/custom/{doc_id}")
def delete_document(doc_id: str):
    docs = load_custom_documents()
    doc = next((d for d in docs if d.id == doc_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    # Delete files
    for path in doc.files.dict().values():
        if path:
            try:
                p = Path(path)
                if p.is_file():
                    p.unlink()
            except Exception:
                pass
    docs = [d for d in docs if d.id != doc_id]
    save_custom_documents(docs)
    return {"status": "deleted"}

@router.patch("/custom/{doc_id}/toggle-queue")
def toggle_queue(
    doc_id: str,
    is_in_weekly_queue: bool = Form(...),
    queue_desc: str | None = Form(None)
) -> CustomDocument:
    docs = load_custom_documents()
    for doc in docs:
        if doc.id == doc_id:
            doc.is_in_weekly_queue = is_in_weekly_queue
            doc.queue_desc = queue_desc
            save_custom_documents(docs)
            return doc
    raise HTTPException(status_code=404, detail="Document not found")
