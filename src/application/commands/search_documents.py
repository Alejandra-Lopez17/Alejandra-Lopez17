from dataclasses import dataclass
from typing import List, Optional, Any
import numpy as np
from domain.entities import TechnicalDocument
from domain.services import IEmbeddingService
from domain.repositories import IDocumentRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SearchDocumentsCommand:
    document_repository: IDocumentRepository
    embedding_service: IEmbeddingService

    def execute(
        self, query: str, top_k: int = 5, **filters: Any
    ) -> List[TechnicalDocument]:
        try:
            processed_query = self._preprocess_query(query)
            query_embedding = self.embedding_service.generate_embedding(processed_query)
            if np.all(query_embedding == 0):
                raise ValueError("Failed to generate query embedding")
            results = self.document_repository.search_similar(
                query_embedding, top_k, **filters
            )
            if not results:
                logger.warning(f"No results found for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise

    def _preprocess_query(self, query: str) -> str:
        """Enhance query based on search intent"""
        query = query.lower()
        if "dependency" in query:
            terms = query.split()
            enhanced = [
                f"{term} dependencies:{term}" if i == 0 else term
                for i, term in enumerate(terms)
            ]
            return " ".join(enhanced)
        return query
