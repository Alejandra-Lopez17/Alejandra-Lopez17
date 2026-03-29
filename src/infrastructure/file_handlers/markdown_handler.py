import frontmatter
import yaml
from pathlib import Path
from datetime import datetime
from domain.entities import TechnicalDocument, DocumentType
from typing import Dict, Any


class MarkdownHandler:
    def __init__(self, source: str = "unknown"):
        self.source = source

    def parse(self, file_path: str) -> TechnicalDocument:
        path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            post = frontmatter.loads(content)
            metadata = post.metadata
            content = post.content

            if "dependencies" in metadata:
                if isinstance(metadata["dependencies"], str):
                    metadata["dependencies"] = [
                        d.strip() for d in metadata["dependencies"].split(",")
                    ]
                elif not isinstance(metadata["dependencies"], list):
                    metadata["dependencies"] = []
        except (yaml.YAMLError, Exception):
            metadata = {}

        try:
            last_updated = datetime.fromtimestamp(path.stat().st_mtime)
        except:
            last_updated = datetime.now()

        return TechnicalDocument(
            id=f"md-{path.stem}",
            content=content,
            title=metadata.get("title", path.stem),
            file_path=str(path),
            document_type=DocumentType.MARKDOWN,
            last_updated=last_updated,
            metadata=metadata,
            version=metadata.get("version"),
            dependencies=metadata.get("dependencies", []),
            api_references=metadata.get("api_references", []),
            source=self.source,
        )
