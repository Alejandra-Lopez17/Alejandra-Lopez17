from pydantic import BaseModel
from typing import Optional
from typing import List, Optional


class DocumentResponse(BaseModel):
    id: str
    title: str
    type: str
    source: Optional[str]
    version: Optional[str]
    file_path: str
    last_updated: Optional[str]


class ProcessDocumentsResponse(BaseModel):
    processed_ids: List[str]
    total_count: int
