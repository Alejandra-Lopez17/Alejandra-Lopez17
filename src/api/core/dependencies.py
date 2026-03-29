from typing import Generator, Any
from infrastructure.persistence import ChromaDocumentRepository
from api.core.config import settings
from domain.services import TechnicalDocEmbeddingService


def get_db() -> Generator[ChromaDocumentRepository, None, None]:
    db = ChromaDocumentRepository(settings.CHROMA_DB_PATH)
    try:
        yield db
    finally:
        pass


def get_embedding_service() -> Generator[TechnicalDocEmbeddingService, None, None]:
    service = TechnicalDocEmbeddingService(settings.EMBEDDING_MODEL)
    try:
        yield service
    finally:
        pass
