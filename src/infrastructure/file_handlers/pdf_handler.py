import io
import logging
from domain.entities import TechnicalDocument, DocumentType
from datetime import datetime
from pathlib import Path
from typing import Optional, cast, Any, Callable
from pypdf import PdfReader

try:
    from pdfminer.high_level import extract_text as pdfminer_extract_text

    extract_text: Callable[[Any], str] = cast(
        Callable[[Any], str], pdfminer_extract_text
    )
except ImportError:

    def extract_text(x: Any) -> str:
        return ""


class PDFHandler:
    def __init__(self, source: str = "unknown") -> None:
        self.source = source
        self.logger = logging.getLogger(__name__)

    def parse(self, file_path: str) -> Optional[TechnicalDocument]:
        """Improved PDF parsing with multiple extraction methods"""
        try:
            text = self._extract_with_pypdf(file_path)
            if not text.strip():
                text = self._extract_with_pdfminer(file_path)
            if not text.strip():
                text = self._extract_with_ocr(file_path)
            if not text.strip():
                raise ValueError("PDF contains no extractable text")

            return TechnicalDocument(
                id=f"pdf-{Path(file_path).stem}",
                content=text,
                title=self._extract_title(file_path),
                file_path=file_path,
                document_type=DocumentType.PDF,
                last_updated=datetime.fromtimestamp(Path(file_path).stat().st_mtime),
                metadata={},
                source=self.source,
            )
        except Exception as e:
            self.logger.error(f"Failed to parse PDF {file_path}: {str(e)}")
            return None

    def _extract_with_pypdf(self, file_path: str) -> str:
        """Extract text using PyPDF"""
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception:
            text = ""
        return text

    def _extract_with_pdfminer(self, file_path: str) -> str:
        """Extract text using pdfminer"""
        try:
            return extract_text(file_path)
        except Exception:
            return ""

    def _extract_with_ocr(self, file_path: str) -> str:
        """Extract text using OCR (optional)"""
        try:
            import pytesseract
            from PIL import Image
            import pdf2image

            images = pdf2image.convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
            return text
        except ImportError:
            self.logger.warning(
                "OCR dependencies not installed. Install with: pip install pytesseract pdf2image"
            )
            return ""
        except Exception:
            return ""

    def _extract_title(self, file_path: str) -> str:
        """Extract title from PDF metadata"""
        try:
            reader = PdfReader(file_path)
            if reader.metadata is None:
                return Path(file_path).stem
            title = reader.metadata.get("/Title", None)
            return str(title) if title is not None else Path(file_path).stem
        except Exception:
            return Path(file_path).stem
