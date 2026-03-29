from dataclasses import dataclass
from typing import List
from domain.entities import TechnicalDocument
from domain.services import IEmbeddingService
from domain.repositories import IDocumentRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProcessDocumentsCommand:
    document_repository: IDocumentRepository
    embedding_service: IEmbeddingService

    def execute(self, documents: List[TechnicalDocument]) -> List[str]:
        processed_ids = []
        try:
            embeddings = self.embedding_service.generate_batch_embeddings(documents)

            for doc, emb in zip(documents, embeddings):
                try:
                    doc_id = self.document_repository.add_document(doc, emb)
                    processed_ids.append(doc_id)
                except Exception as e:
                    logger.error(f"Failed to store document {doc.id}: {str(e)}")

            logger.info(f"Processed {len(processed_ids)}/{len(documents)} documents")
            return processed_ids
        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            raise

    def execute_batch(
        self, documents: List[TechnicalDocument], batch_size: int = 32
    ) -> List[str]:
        all_processed = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            processed = self.execute(batch)
            all_processed.extend(processed)
        return all_processed
