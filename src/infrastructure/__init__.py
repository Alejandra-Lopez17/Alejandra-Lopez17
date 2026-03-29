"""Módulo de infraestructura para persistencia y manejo de archivos"""

from .persistence.chroma_repository import ChromaDocumentRepository
from .persistence.file_storage import LocalFileStorage
from .file_handlers.markdown_handler import MarkdownHandler
from .file_handlers.rst_handler import RSTHandler
from .file_handlers.pdf_handler import PDFHandler
from .file_handlers.text_handler import TextHandler

__all__ = [
    "ChromaDocumentRepository",
    "LocalFileStorage",
    "MarkdownHandler",
    "RSTHandler",
    "PDFHandler",
    "TextHandler",
]

ChromaDocumentRepository = ChromaDocumentRepository
LocalFileStorage = LocalFileStorage
MarkdownHandler = MarkdownHandler
RSTHandler = RSTHandler
PDFHandler = PDFHandler
TextHandler = TextHandler
