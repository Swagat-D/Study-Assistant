from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# Summary schemas
class SummaryBase(BaseModel):
    title: str
    content: str
    summary_type: str  # executive, detailed, etc.


class SummaryCreate(SummaryBase):
    document_id: UUID


class Summary(SummaryBase):
    id: UUID
    document_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class SummaryRequest(BaseModel):
    document_id: UUID
    summary_type: str = "general"  # general, executive, detailed
    max_length: Optional[int] = None


# Flashcard schemas
class FlashcardBase(BaseModel):
    front: str
    back: str
    difficulty: Optional[str] = None


class FlashcardCreate(FlashcardBase):
    flashcard_set_id: UUID


class Flashcard(FlashcardBase):
    id: UUID
    flashcard_set_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class FlashcardSetBase(BaseModel):
    title: str
    description: Optional[str] = None


class FlashcardSetCreate(FlashcardSetBase):
    document_id: UUID


class FlashcardSet(FlashcardSetBase):
    id: UUID
    document_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class FlashcardSetWithCards(FlashcardSet):
    flashcards: List[Flashcard] = []


class FlashcardRequest(BaseModel):
    document_id: UUID
    num_cards: int = 10
    difficulty: Optional[str] = None  # easy, medium, hard


# Quiz schemas
class QuizQuestionBase(BaseModel):
    question_text: str
    question_type: str  # multiple-choice, true-false, short-answer
    options: Optional[List[str]] = None  # For multiple choice questions
    correct_answer: str
    explanation: Optional[str] = None
    source_chunk_id: Optional[UUID] = None


class QuizQuestionCreate(QuizQuestionBase):
    quiz_id: UUID


class QuizQuestion(QuizQuestionBase):
    id: UUID
    quiz_id: UUID

    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    quiz_type: str  # multiple-choice, true-false, mixed, etc.
    difficulty: str  # easy, medium, hard
    time_limit: Optional[int] = None  # in seconds


class QuizCreate(QuizBase):
    document_id: UUID


class Quiz(QuizBase):
    id: UUID
    document_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class QuizWithQuestions(Quiz):
    questions: List[QuizQuestion] = []


class QuizRequest(BaseModel):
    document_id: UUID
    quiz_type: str = "mixed"  # multiple-choice, true-false, short-answer, mixed
    num_questions: int = 10
    difficulty: str = "medium"  # easy, medium, hard
    time_limit: Optional[int] = None  # in seconds