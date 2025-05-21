from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.sql.expression import select, delete

from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base class for all repositories providing common CRUD operations.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: str) -> Optional[ModelType]:
        """
        Get an entity by id.
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all entities with pagination.
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new entity.
        """
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """
        Update an entity.
        """
        obj = self.get(id)
        if obj:
            for field, value in obj_in.items():
                setattr(obj, field, value)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
        return obj
    
    def delete(self, id: str) -> bool:
        """
        Delete an entity.
        """
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
    
    def filter(self, **kwargs) -> List[ModelType]:
        """
        Filter entities by attributes.
        """
        return self.db.query(self.model).filter_by(**kwargs).all()
    
    def get_by(self, **kwargs) -> Optional[ModelType]:
        """
        Get a single entity by attributes.
        """
        return self.db.query(self.model).filter_by(**kwargs).first()


class UserRepository(BaseRepository):
    """Repository for User model operations."""
    
    def get_by_email(self, email: str):
        """Get a user by email."""
        return self.db.query(self.model).filter(self.model.email == email).first()
    
    def get_by_username(self, username: str):
        """Get a user by username."""
        return self.db.query(self.model).filter(self.model.username == username).first()


class DocumentRepository(BaseRepository):
    """Repository for Document model operations."""
    
    def get_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100):
        """Get documents by owner id."""
        return self.db.query(self.model)\
            .filter(self.model.owner_id == owner_id)\
            .offset(skip)\
            .limit(limit)\
            .all()


class ChatSessionRepository(BaseRepository):
    """Repository for ChatSession model operations."""
    
    def get_by_user_and_document(self, user_id: str, document_id: str):
        """Get chat sessions by user id and document id."""
        return self.db.query(self.model)\
            .filter(self.model.user_id == user_id, self.model.document_id == document_id)\
            .order_by(self.model.created_at.desc())\
            .first()
    
    def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100):
        """Get chat sessions by user id."""
        return self.db.query(self.model)\
            .filter(self.model.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()


class ChatMessageRepository(BaseRepository):
    """Repository for ChatMessage model operations."""
    
    def get_by_session(self, session_id: str, skip: int = 0, limit: int = 100):
        """Get messages by chat session id."""
        return self.db.query(self.model)\
            .filter(self.model.chat_session_id == session_id)\
            .order_by(self.model.timestamp.asc())\
            .offset(skip)\
            .limit(limit)\
            .all()


class FlashcardSetRepository(BaseRepository):
    """Repository for FlashcardSet model operations."""
    
    def get_by_document(self, document_id: str):
        """Get flashcard sets by document id."""
        return self.db.query(self.model)\
            .filter(self.model.document_id == document_id)\
            .first()


class FlashcardRepository(BaseRepository):
    """Repository for Flashcard model operations."""
    
    def get_by_set(self, set_id: str, skip: int = 0, limit: int = 100):
        """Get flashcards by flashcard set id."""
        return self.db.query(self.model)\
            .filter(self.model.flashcard_set_id == set_id)\
            .offset(skip)\
            .limit(limit)\
            .all()


class QuizRepository(BaseRepository):
    """Repository for Quiz model operations."""
    
    def get_by_document(self, document_id: str):
        """Get quizzes by document id."""
        return self.db.query(self.model)\
            .filter(self.model.document_id == document_id)\
            .all()


class QuizQuestionRepository(BaseRepository):
    """Repository for QuizQuestion model operations."""
    
    def get_by_quiz(self, quiz_id: str, skip: int = 0, limit: int = 100):
        """Get questions by quiz id."""
        return self.db.query(self.model)\
            .filter(self.model.quiz_id == quiz_id)\
            .offset(skip)\
            .limit(limit)\
            .all()


class SummaryRepository(BaseRepository):
    """Repository for Summary model operations."""
    
    def get_by_document_and_type(self, document_id: str, summary_type: str):
        """Get summaries by document id and type."""
        return self.db.query(self.model)\
            .filter(self.model.document_id == document_id, self.model.summary_type == summary_type)\
            .first()