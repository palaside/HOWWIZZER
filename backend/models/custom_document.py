from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FilePaths(BaseModel):
    original: str
    html: Optional[str] = None
    docx: Optional[str] = None
    xlsx: Optional[str] = None
    pdf: Optional[str] = None

class CustomDocument(BaseModel):
    id: str = Field(..., description='Unique document identifier, e.g., doc-custom-<timestamp>')
    code: str = Field(..., description='Document code used for indexing')
    title: str = Field(..., description='Human readable title')
    category: str = Field(..., description='Category key, e.g., inventory, inspection, memo, general')
    category_label: str = Field(..., description='Label displayed in UI')
    desc: str = Field(..., description='Description of the document')
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, description='ISO timestamp of upload')
    uploader: str = Field(..., description='User who uploaded the document')
    original_filename: str = Field(..., description='Original uploaded file name')
    file_type: str = Field(..., description='File extension without dot, e.g., xlsx, docx, pdf')
    is_in_weekly_queue: bool = Field(default=False, description='Whether the doc participates in weekly queue')
    queue_desc: Optional[str] = Field(None, description='Description for weekly queue entry')
    files: FilePaths = Field(..., description='Paths to stored files')
