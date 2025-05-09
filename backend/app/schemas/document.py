from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    name: str
    file_type: str


class DocumentCreate(DocumentBase):
    pass


class DocumentChunkBase(BaseModel):
    chunk_index: int
    text_content: str
    page_number: Optional[int] = None


class DocumentChunkCreate(DocumentChunkBase):
    document_id: UUID


class DocumentChunk(DocumentChunkBase):
    id: UUID
    document_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class Document(DocumentBase):
    id: UUID
    file_path: str
    file_size: int
    num_pages: Optional[int] = None
    is_processed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: UUID
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk] = []


class DocumentSearchQuery(BaseModel):
    query: str
    document_id: Optional[UUID] = None
    max_results: int = 5


class DocumentSearchResult(BaseModel):
    document_id: UUID
    document_name: str
    chunks: List[Dict[str, Any]]
    score: float


class DocumentSummary(BaseModel):
    document_id: UUID
    summary_type: str = "general"
    max_length: Optional[int] = None


class DocumentUploadResponse(BaseModel):
    id: UUID
    name: str
    file_type: str
    file_size: int
    num_pages: Optional[int] = None
    is_processed: bool
    message: str = "Document uploaded successfully"