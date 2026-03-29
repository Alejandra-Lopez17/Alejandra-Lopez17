import chromadb
import numpy as np
from numpy.typing import NDArray
from typing import List, Optional, Dict, Any, cast, Sequence
from chromadb.config import Settings
from chromadb.api.types import QueryResult, GetResult, Where
from domain.entities import TechnicalDocument, DocumentType
from domain.repositories import IDocumentRepository
from datetime import datetime
from chromadb.api.models import Collection


class ChromaDocumentRepository(IDocumentRepository):
    def __init__(self, db_path: str, collection_name: str = "tech_docs") -> None:
        self.client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=None,
        )

    def add_document(
        self, document: TechnicalDocument, embedding: NDArray[np.float32]
    ) -> str:
        metadata = self._create_metadata(document)

        if embedding.ndim != 1:
            embedding = embedding.reshape(-1)
        embedding_list: List[float] = cast(
            List[float], embedding.astype(float).tolist()
        )
        embedding_sequence: Sequence[float] = embedding_list

        try:
            self.collection.add(
                ids=[document.id],
                embeddings=[embedding_sequence],
                documents=[document.content],
                metadatas=[metadata],
            )
            return document.id
        except Exception as e:
            raise RuntimeError(f"Failed to add document: {str(e)}")

    def search_similar(
        self, embedding: NDArray[np.float32], top_k: int = 5, **filters: Any
    ) -> List[TechnicalDocument]:
        try:
            where_clause: Optional[Where] = None
            if filters:
                where_dict: Dict[str, Dict[str, str]] = {
                    k: {"$eq": str(v)} for k, v in filters.items()
                }
                where_clause = cast(Where, where_dict)

            if embedding.ndim != 1:
                embedding = embedding.reshape(-1)
            embedding_list: List[float] = cast(
                List[float], embedding.astype(float).tolist()
            )
            embedding_sequence: Sequence[float] = embedding_list

            results = self.collection.query(
                query_embeddings=[embedding_sequence],
                n_results=top_k,
                where=where_clause,
            )
            return self._convert_results_to_documents(results)
        except Exception as e:
            raise RuntimeError(f"Search failed: {str(e)}")

    def get_by_id(self, document_id: str) -> Optional[TechnicalDocument]:
        try:
            result = self.collection.get(ids=[document_id])
            if not result["ids"]:
                return None
            return self._convert_get_result_to_document(result)
        except Exception as e:
            raise RuntimeError(f"Failed to get document: {str(e)}")

    def _create_metadata(self, document: TechnicalDocument) -> Dict[str, str]:
        return {
            "title": document.title,
            "type": document.document_type.value,
            "version": document.version or "",
            "dependencies": (
                ",".join(document.dependencies) if document.dependencies else ""
            ),
            "api_refs": (
                ",".join(document.api_references) if document.api_references else ""
            ),
            "source": document.source or "",
            "file_path": document.file_path,
            "last_updated": (
                document.last_updated.isoformat()
                if document.last_updated and hasattr(document.last_updated, "isoformat")
                else ""
            ),
        }

    def _convert_results_to_documents(
        self, results: QueryResult
    ) -> List[TechnicalDocument]:
        documents: List[TechnicalDocument] = []
        if not results["ids"] or len(results["ids"]) == 0:
            return documents

        for i in range(len(results["ids"][0])):
            if not results["metadatas"] or len(results["metadatas"]) == 0:
                continue
            metadata = results["metadatas"][0][i]
            try:
                last_updated = None
                if metadata.get("last_updated") and isinstance(
                    metadata["last_updated"], str
                ):
                    last_updated = datetime.fromisoformat(metadata["last_updated"])
            except (ValueError, AttributeError):
                last_updated = None

            if (
                not results["documents"]
                or len(results["documents"]) == 0
                or not results["ids"]
                or len(results["ids"]) == 0
            ):
                continue

            documents.append(
                TechnicalDocument(
                    id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    title=str(metadata.get("title", "")),
                    file_path=str(metadata.get("file_path", "")),
                    document_type=DocumentType(str(metadata.get("type", "markdown"))),
                    last_updated=last_updated,
                    metadata=dict(metadata),
                    version=(
                        str(metadata.get("version", ""))
                        if metadata.get("version")
                        else None
                    ),
                    dependencies=(
                        str(metadata.get("dependencies", "")).split(",")
                        if metadata.get("dependencies")
                        and isinstance(metadata.get("dependencies"), str)
                        else []
                    ),
                    api_references=(
                        str(metadata.get("api_refs", "")).split(",")
                        if metadata.get("api_refs")
                        and isinstance(metadata.get("api_refs"), str)
                        else []
                    ),
                    source=(
                        str(metadata.get("source", ""))
                        if metadata.get("source")
                        else None
                    ),
                )
            )
        return documents

    def _convert_get_result_to_document(self, result: GetResult) -> TechnicalDocument:
        if not result["metadatas"] or not result["ids"] or not result["documents"]:
            raise ValueError("Invalid result structure")

        metadata = result["metadatas"][0]
        last_updated = None
        if metadata.get("last_updated") and isinstance(metadata["last_updated"], str):
            try:
                last_updated = datetime.fromisoformat(metadata["last_updated"])
            except ValueError:
                last_updated = None

        return TechnicalDocument(
            id=result["ids"][0],
            content=result["documents"][0],
            title=str(metadata.get("title", "")),
            file_path=str(metadata.get("file_path", "")),
            document_type=DocumentType(str(metadata.get("type", "markdown"))),
            last_updated=last_updated,
            metadata=dict(metadata),
            version=(
                str(metadata.get("version", "")) if metadata.get("version") else None
            ),
            dependencies=(
                str(metadata["dependencies"]).split(",")
                if metadata.get("dependencies")
                and isinstance(metadata["dependencies"], str)
                else []
            ),
            api_references=(
                str(metadata["api_refs"]).split(",")
                if metadata.get("api_refs") and isinstance(metadata["api_refs"], str)
                else []
            ),
            source=str(metadata.get("source", "")) if metadata.get("source") else None,
        )
