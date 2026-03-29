from fastapi import FastAPI
from api.routers import documents, search
from api.core.config import settings
from api.core.dependencies import get_db, get_embedding_service


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(documents.router)
    app.include_router(search.router)

    return app
