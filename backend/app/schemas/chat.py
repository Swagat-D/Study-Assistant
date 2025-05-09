from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ChatMessageBase(BaseModel):
    sender: str
    text: str
    source_chunks: Optional[Dict[str, Any]] = None


class ChatMessageCreate(ChatMessageBase):
    chat_session_id: UUID


class ChatMessage(ChatMessageBase):
    id: UUID
    chat_session_id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True


class ChatSessionBase(BaseModel):
    name: Optional[str] = None
    document_id: Optional[UUID] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ChatSessionWithMessages(ChatSession):
    messages: List[ChatMessage] = []


class ChatRequest(BaseModel):
    message: str
    document_id: Optional[UUID] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None


class ChatResponse(BaseModel):
    message: str
    source_chunks: Optional[List[Dict[str, Any]]] = None
    document_id: Optional[UUID] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatHistorySave(BaseModel):
    document_id: UUID
    messages: List[Dict[str, Any]]


class ChatHistoryExport(BaseModel):
    document_id: UUID
    format: str = "pdf"  # pdf, txt, etc.