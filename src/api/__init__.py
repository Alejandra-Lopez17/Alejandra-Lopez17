"""API module for technical documentation management"""

from .routers import documents, search
from .schemas import document, search as search_schemas

__all__ = ["documents", "search", "document", "search_schemas"]
