import os
from pathlib import Path
from typing import BinaryIO, Optional
from domain.repositories import IFileStorage


class LocalFileStorage(IFileStorage):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, file_name: str, content: BinaryIO) -> str:
        file_path = self.base_path / file_name
        with open(file_path, "wb") as f:
            f.write(content.read())
        return str(file_path)

    def get(self, file_name: str) -> Optional[BinaryIO]:
        file_path = self.base_path / file_name
        if not file_path.exists():
            return None
        return open(file_path, "rb")

    def delete(self, file_name: str) -> bool:
        file_path = self.base_path / file_name
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
