from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from domain.entities import TechnicalDocument
import numpy as np
from numpy.typing import NDArray


class IDocumentRepository(ABC):
    @abstractmethod
    def add_document(
        self, document: TechnicalDocument, embedding: NDArray[np.float32]
    ) -> str:
        pass

    @abstractmethod
    def search_similar(
        self, embedding: NDArray[np.float32], top_k: int = 5, **filters: Dict[str, Any]
    ) -> List[TechnicalDocument]:
        pass

    @abstractmethod
    def get_by_id(self, document_id: str) -> Optional[TechnicalDocument]:
        pass
