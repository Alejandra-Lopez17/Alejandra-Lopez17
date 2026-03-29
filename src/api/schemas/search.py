from pydantic import BaseModel
from typing import List, Optional


class SearchResult(BaseModel):
    id: str
    title: str
    content_preview: str
    similarity: float
    type: str
    source: Optional[str]


class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    source: Optional[str] = None
    doc_type: Optional[str] = None
