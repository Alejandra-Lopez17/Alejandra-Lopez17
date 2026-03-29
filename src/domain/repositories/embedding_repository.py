from abc import ABC, abstractmethod
from domain.entities import DocumentEmbedding


class IEmbeddingRepository(ABC):
    @abstractmethod
    def store(self, embedding: DocumentEmbedding) -> None:
        pass

    @abstractmethod
    def get(self, document_id: str) -> DocumentEmbedding:
        pass
