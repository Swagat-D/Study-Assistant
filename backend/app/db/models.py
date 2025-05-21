import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, LargeBinary, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

# SQLite doesn't support UUID type natively, so we use String instead
# This is fine for development, but in production with PostgreSQL you would use UUID type


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="owner")
    chat_sessions = relationship("ChatSession", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx, etc.
    file_size = Column(Integer, nullable=False)  # in bytes
    num_pages = Column(Integer, nullable=True)
    text_content = Column(Text, nullable=True)  # Full text content
    document_metadata = Column(JSON, nullable=True)  # Document metadata
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    owner_id = Column(String, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="document")
    summaries = relationship("Summary", back_populates="document", cascade="all, delete-orphan")
    flashcard_sets = relationship("FlashcardSet", back_populates="document", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document {self.name}>"


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_index = Column(Integer, nullable=False)
    text_content = Column(Text, nullable=False)
    embedding = Column(LargeBinary, nullable=True)  # Vector embedding as binary
    page_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    document_id = Column(String, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    def __repr__(self):
        return f"<DocumentChunk {self.chunk_index} of {self.document_id}>"


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = Column(String, ForeignKey("users.id"))
    document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    document = relationship("Document", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="chat_session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ChatSession {self.id}>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender = Column(String, nullable=False)  # user or bot
    text = Column(Text, nullable=False)
    source_chunks = Column(JSON, nullable=True)  # References to document chunks
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    chat_session_id = Column(String, ForeignKey("chat_sessions.id"))
    
    # Relationships
    chat_session = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self):
        return f"<ChatMessage {self.id}>"


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary_type = Column(String, nullable=False)  # executive, detailed, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    document_id = Column(String, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="summaries")
    
    def __repr__(self):
        return f"<Summary {self.id}>"


class FlashcardSet(Base):
    __tablename__ = "flashcard_sets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    document_id = Column(String, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="flashcard_sets")
    flashcards = relationship("Flashcard", back_populates="flashcard_set", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FlashcardSet {self.id}>"


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    difficulty = Column(String, nullable=True)  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    flashcard_set_id = Column(String, ForeignKey("flashcard_sets.id"))
    
    # Relationships
    flashcard_set = relationship("FlashcardSet", back_populates="flashcards")
    
    def __repr__(self):
        return f"<Flashcard {self.id}>"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    quiz_type = Column(String, nullable=False)  # multiple-choice, true-false, mixed, etc.
    difficulty = Column(String, nullable=False)  # easy, medium, hard
    time_limit = Column(Integer, nullable=True)  # in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign keys
    document_id = Column(String, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quiz {self.id}>"


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # multiple-choice, true-false, short-answer
    options = Column(JSON, nullable=True)  # For multiple choice questions
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    source_chunk_id = Column(String, nullable=True)  # Reference to source chunk
    
    # Foreign keys
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    
    def __repr__(self):
        return f"<QuizQuestion {self.id}>"