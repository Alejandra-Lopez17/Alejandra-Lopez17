from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime


from domain.entities import TechnicalDocument, DocumentType
from domain.repositories import IDocumentRepository
from domain.services import IEmbeddingService
from application.commands import ProcessDocumentsCommand
from infrastructure.file_handlers import (
    MarkdownHandler,
    RSTHandler,
    PDFHandler,
    TextHandler,
)
from api.core.dependencies import get_db, get_embedding_service

router = APIRouter(prefix="/documents", tags=["documents"])

HANDLERS = {
    DocumentType.MARKDOWN.value: MarkdownHandler,
    DocumentType.RST.value: RSTHandler,
    DocumentType.PDF.value: PDFHandler,
    DocumentType.PLAIN_TEXT.value: TextHandler,
}


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


@router.post("/process-file", response_model=DocumentResponse)
async def process_uploaded_file(
    file: UploadFile = File(...),
    source: str = "upload",
    repo: IDocumentRepository = Depends(get_db),
    embedding_service: IEmbeddingService = Depends(get_embedding_service),
) -> DocumentResponse:
    """Process a single uploaded file"""
    try:
        if file.filename is None:
            raise HTTPException(400, detail="Filename is required")

        file_ext = os.path.splitext(file.filename)[1].lower().lstrip(".")
        if file_ext not in HANDLERS:
            raise HTTPException(400, detail="Unsupported file type")
        handler_class = HANDLERS[file_ext]

        handler = handler_class(source=source)

        if not hasattr(handler, "parse"):
            raise HTTPException(
                500, detail=f"Handler {handler_class.__name__} has no 'parse' method"
            )

        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file.file.read())
        document = handler.parse(temp_path)
        os.remove(temp_path)
        command = ProcessDocumentsCommand(repo, embedding_service)
        doc_id = command.execute([document])[0]

        return DocumentResponse(
            id=doc_id,
            title=document.title,
            type=document.document_type.value,
            source=document.source,
            version=document.version,
            file_path=document.file_path,
            last_updated=(
                document.last_updated.isoformat() if document.last_updated else None
            ),
        )
    except Exception as e:
        raise HTTPException(500, detail=str(e))
