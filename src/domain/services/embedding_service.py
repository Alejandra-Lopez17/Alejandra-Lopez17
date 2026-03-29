from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from typing import List
from sentence_transformers import SentenceTransformer
from domain.entities import TechnicalDocument
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IEmbeddingService(ABC):
    model: SentenceTransformer
    embedding_dim: int

    @abstractmethod
    def generate_embedding(self, text: str) -> NDArray[np.float32]:
        """Generate embedding for a text string"""
        pass

    @abstractmethod
    def generate_document_embedding(
        self, document: TechnicalDocument
    ) -> NDArray[np.float32]:
        """Generate embedding for a document"""
        pass

    @abstractmethod
    def generate_batch_embeddings(
        self, documents: List[TechnicalDocument]
    ) -> List[NDArray[np.float32]]:
        """Generate embeddings for a batch of documents"""
        pass

    @abstractmethod
    def _create_document_context(self, document: TechnicalDocument) -> str:
        """Create unified context for document embedding"""
        pass


class TechnicalDocEmbeddingService(IEmbeddingService):
    def __init__(
        self, model_name: str = "sentence-transformers/all-mpnet-base-v2"
    ) -> None:
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_embedding(self, text: str) -> NDArray[np.float32]:
        try:
            embedding = self.model.encode(
                text, convert_to_numpy=True, show_progress_bar=False
            )
            return np.array(embedding, dtype=np.float32)
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return np.zeros(self.embedding_dim, dtype=np.float32)

    def generate_document_embedding(
        self, document: TechnicalDocument
    ) -> NDArray[np.float32]:
        context = self._create_document_context(document)
        return self.generate_embedding(context)

    def generate_batch_embeddings(
        self, documents: List[TechnicalDocument]
    ) -> List[NDArray[np.float32]]:
        try:
            contexts = [self._create_document_context(doc) for doc in documents]
            embeddings = self.model.encode(
                contexts, batch_size=32, show_progress_bar=True, convert_to_numpy=True
            )
            return [np.array(emb, dtype=np.float32) for emb in embeddings]
        except Exception as e:
            logger.error(f"Batch embedding error: {str(e)}")
            return [np.zeros(self.embedding_dim, dtype=np.float32) for _ in documents]

    def _create_document_context(self, document: TechnicalDocument) -> str:
        """Crea contexto unificado para embeddings de documentos"""
        context_parts = [
            f"Title: {document.title}",
            f"Content: {document.content[:5000]}",
        ]
        if document.dependencies:
            context_parts.append(f"Dependencies: {' '.join(document.dependencies)}")
        if document.version:
            context_parts.append(f"Version: {document.version}")
        if document.api_references:
            context_parts.append(f"API References: {' '.join(document.api_references)}")
        return "\n".join(context_parts)
