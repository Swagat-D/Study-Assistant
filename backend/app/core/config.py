import os
import secrets
from typing import List, Optional, Dict, Any, Union

from pydantic import BaseSettings, PostgresDsn, validator, AnyHttpUrl


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = "postgresql://postgres:postgres@localhost/study_assistant"
    
    # Vector database
    VECTOR_DB_TYPE: str = "faiss"  # Options: faiss, qdrant, weaviate, pgvector
    VECTOR_DB_URL: Optional[str] = None
    
    # File storage
    UPLOAD_DIRECTORY: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    
    # LLM settings
    LLM_PROVIDER: str = "openai"  # Options: openai, huggingface, local
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_API_KEY: Optional[str] = None
    
    # Embedding settings
    EMBEDDING_PROVIDER: str = "openai"  # Options: openai, huggingface, local
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    EMBEDDING_DIMENSION: int = 1536
    
    # Document processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Feature flags
    ENABLE_AUTH: bool = False
    ENABLE_MULTILINGUAL: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Load settings
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)