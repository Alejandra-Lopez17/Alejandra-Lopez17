import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Technical Documentation Manager"
    VERSION: str = "1.0.0"

    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "data/tech_docs_db")
    DOCUMENTS_DIR: str = os.getenv("DOCUMENTS_DIR", "data/documents")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    @classmethod
    def create_directories(cls) -> None:
        Path(cls.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.create_directories()
