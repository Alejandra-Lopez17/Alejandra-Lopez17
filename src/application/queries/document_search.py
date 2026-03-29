import numpy as np
from dataclasses import dataclass
from numpy.typing import NDArray
from typing import List, Optional

from domain.entities import TechnicalDocument
from domain.repositories import IDocumentRepository


@dataclass
class DocumentSearchQuery:
    repository: IDocumentRepository

    def __init__(self, repository: IDocumentRepository):
        self.repository = repository

    def get_document(self, document_id: str) -> Optional[TechnicalDocument]:
        return self.repository.get_by_id(document_id)

    def get_all_documents(self, limit: int = 100) -> List[TechnicalDocument]:
        dummy_embedding = np.zeros(384, dtype=np.float32)
        return self.repository.search_similar(dummy_embedding, limit)
