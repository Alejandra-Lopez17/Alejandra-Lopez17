from typing import Dict
from pathlib import Path
from domain.entities import TechnicalDocument, DocumentType
from datetime import datetime
import uuid


class TextHandler:
    def __init__(self, source: str = "unknown"):
        self.source = source

    def parse(self, file_path: str) -> TechnicalDocument:
        """Parse a plain text file"""
        path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return TechnicalDocument(
            id=f"txt-{uuid.uuid4().hex}",
            content=content,
            title=path.stem,
            file_path=str(file_path),
            document_type=DocumentType.PLAIN_TEXT,
            last_updated=datetime.fromtimestamp(path.stat().st_mtime),
            metadata={},
            version=None,
            dependencies=[],
            api_references=[],
            source=self.source,
        )
