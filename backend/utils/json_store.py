import json
from pathlib import Path
from typing import List
from ..models.custom_document import CustomDocument

# JSON file storing custom document metadata
DATA_FILE = Path(__file__).resolve().parents[2] / 'data' / 'custom_documents.json'

def load_custom_documents() -> List[CustomDocument]:
    """Load custom documents from the JSON store.
    Returns an empty list if the file does not exist or is empty.
    """
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open('r', encoding='utf-8') as f:
        raw = json.load(f)
    return [CustomDocument(**item) for item in raw]

def save_custom_documents(docs: List[CustomDocument]) -> None:
    """Write the list of CustomDocument objects back to the JSON store.
    The file is pretty‑printed for readability.
    """
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump([doc.dict() for doc in docs], f, ensure_ascii=False, indent=2)
