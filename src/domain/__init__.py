"""Módulo principal del dominio para gestión de documentación técnica"""

from .entities import TechnicalDocument, DocumentType
from .services import IEmbeddingService, TechnicalTextProcessor
from .repositories import IDocumentRepository

__all__ = [
    "TechnicalDocument",
    "DocumentType",
    "IEmbeddingService",
    "TechnicalTextProcessor",
    "IDocumentRepository",
]
