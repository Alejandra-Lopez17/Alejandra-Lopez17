from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, List


class DocumentType(str, Enum):
    RST = "rst"
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"
    PLAIN_TEXT = "txt"


@dataclass
class TechnicalDocument:
    id: str
    content: str
    title: str
    file_path: str
    document_type: DocumentType
    last_updated: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: Optional[str] = None
    dependencies: Optional[List[str]] = None
    api_references: Optional[List[str]] = None
    source: Optional[str] = None

    def __post_init__(self) -> None:
        self.metadata = self.metadata or {}
        self.dependencies = self.dependencies or []
        self.api_references = self.api_references or []

    def get_technical_context(self) -> str:
        """Genera contexto técnico para embeddings"""
        context = f"Title: {self.title}\n"
        context += f"Content: {self.content[:5000]}\n"
        if self.api_references:
            context += f"API References: {', '.join(self.api_references)}\n"
        if self.dependencies:
            context += f"Dependencies: {', '.join(self.dependencies)}\n"
        return context
