from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


class IFileStorage(ABC):
    @abstractmethod
    def save(self, file_name: str, content: BinaryIO) -> str:
        pass

    @abstractmethod
    def get(self, file_name: str) -> Optional[BinaryIO]:
        pass

    @abstractmethod
    def delete(self, file_name: str) -> bool:
        pass
