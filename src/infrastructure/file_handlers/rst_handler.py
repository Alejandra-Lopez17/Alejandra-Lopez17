from typing import Dict, Any
from pathlib import Path
from domain.entities import TechnicalDocument, DocumentType
from datetime import datetime
import uuid
import docutils.core


class RSTHandler:
    def __init__(self, source: str = "unknown") -> None:
        self.source = source

    def parse(self, file_path: str) -> TechnicalDocument:
        """Parse a reStructuredText file"""
        path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = self._extract_rst_metadata(content)

        return TechnicalDocument(
            id=f"rst-{uuid.uuid4().hex}",
            content=content,
            title=metadata.get("title", path.stem),
            file_path=str(file_path),
            document_type=DocumentType.RST,
            last_updated=datetime.fromtimestamp(path.stat().st_mtime),
            metadata=metadata,
            version=metadata.get("version"),
            dependencies=metadata.get("dependencies", []),
            api_references=metadata.get("api_references", []),
            source=self.source,
        )

    def _extract_rst_metadata(self, content: str) -> Dict[str, Any]:
        """Extrae metadatos básicos de archivos RST"""
        metadata: Dict[str, Any] = {}
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.strip() and all(c == "-" for c in line.strip()):
                if i > 0:
                    metadata["title"] = lines[i - 1].strip()
                break

        return metadata
