from domain.services.embedding_service import TechnicalDocEmbeddingService
from domain.entities import TechnicalDocument, DocumentType
import numpy as np


def test_generate_embedding() -> None:
    service = TechnicalDocEmbeddingService()
    embedding = service.generate_embedding("test text")
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] > 0


def test_generate_document_embedding() -> None:
    service = TechnicalDocEmbeddingService()
    doc = TechnicalDocument(
        id="test",
        content="test content",
        title="test",
        file_path="test.txt",
        document_type=DocumentType.PLAIN_TEXT,
    )
    embedding = service.generate_document_embedding(doc)
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[0] > 0
