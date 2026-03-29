from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, cast
from domain.entities import TechnicalDocument
from domain.repositories import IDocumentRepository
from domain.services import IEmbeddingService
from api.core.dependencies import get_db, get_embedding_service
from application.commands import SearchDocumentsCommand

router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    id: str
    title: str
    content_preview: str
    similarity: float
    type: str
    source: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    source: Optional[str] = None
    doc_type: Optional[str] = None


@router.post("/", response_model=List[SearchResult])
async def search_documents(
    request: SearchRequest,
    repo: IDocumentRepository = Depends(get_db),
    embedding_service: IEmbeddingService = Depends(get_embedding_service),
) -> List[SearchResult]:
    """Search for similar technical documents"""
    try:
        command = SearchDocumentsCommand(repo, embedding_service)
        filters = {}
        if request.source:
            filters["source"] = request.source
        if request.doc_type:
            filters["type"] = request.doc_type

        results = command.execute(request.query, request.top_k, **filters)

        return [
            SearchResult(
                id=doc.id,
                title=doc.title,
                content_preview=doc.content[:200] + "...",
                similarity=1 - float(doc.metadata.get("distance", 0)),
                type=doc.document_type.value,
                source=doc.source,
            )
            for doc in results
        ]
    except Exception as e:
        raise HTTPException(500, detail=str(e))
