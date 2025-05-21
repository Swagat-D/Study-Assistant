from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas import study_tools as schemas
from app.core.security import get_current_active_user
from app.services.flashcard_generator import flashcard_generator

router = APIRouter(
    prefix="/study-tools",
    tags=["Study Tools"],
)

@router.post("/flashcards", response_model=schemas.FlashcardSetWithCards)
async def generate_flashcards(
    flashcard_request: schemas.FlashcardRequest,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate flashcards for a document.
    """
    # Get document
    document = db.query(models.Document).filter(
        models.Document.id == str(flashcard_request.document_id),
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check if flashcard set already exists
    existing_set = db.query(models.FlashcardSet).filter(
        models.FlashcardSet.document_id == str(flashcard_request.document_id)
    ).first()
    
    if existing_set:
        # Get flashcards
        flashcards = db.query(models.Flashcard).filter(
            models.Flashcard.flashcard_set_id == existing_set.id
        ).all()
        
        return schemas.FlashcardSetWithCards(
            id=existing_set.id,
            document_id=existing_set.document_id,
            title=existing_set.title,
            description=existing_set.description,
            created_at=existing_set.created_at,
            flashcards=flashcards
        )
    
    # Generate flashcards
    generated_flashcards = flashcard_generator.generate_flashcards(
        document_text=document.text_content,
        num_cards=flashcard_request.num_cards,
        difficulty=flashcard_request.difficulty
    )
    
    # Create flashcard set
    flashcard_set = models.FlashcardSet(
        document_id=str(flashcard_request.document_id),
        title=f"Flashcards for {document.name}",
        description=f"Generated flashcards for {document.name}"
    )
    
    db.add(flashcard_set)
    db.flush()
    
    # Create flashcards
    db_flashcards = []
    for card_data in generated_flashcards:
        flashcard = models.Flashcard(
            flashcard_set_id=flashcard_set.id,
            front=card_data["front"],
            back=card_data["back"],
            difficulty=card_data["difficulty"]
        )
        db.add(flashcard)
        db_flashcards.append(flashcard)
    
    db.commit()
    db.refresh(flashcard_set)
    
    # Get all flashcards
    flashcards = db.query(models.Flashcard).filter(
        models.Flashcard.flashcard_set_id == flashcard_set.id
    ).all()
    
    return schemas.FlashcardSetWithCards(
        id=flashcard_set.id,
        document_id=flashcard_set.document_id,
        title=flashcard_set.title,
        description=flashcard_set.description,
        created_at=flashcard_set.created_at,
        flashcards=flashcards
    )

@router.post("/quiz", response_model=schemas.QuizWithQuestions)
async def generate_quiz(
    quiz_request: schemas.QuizRequest,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate a quiz for a document.
    
    This is a simplified implementation. In a real system, you would use
    NLP techniques or an LLM to generate quiz questions.
    """
    # Get document
    document = db.query(models.Document).filter(
        models.Document.id == str(quiz_request.document_id),
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Create a new quiz
    quiz = models.Quiz(
        document_id=str(quiz_request.document_id),
        title=f"Quiz for {document.name}",
        description=f"A {quiz_request.difficulty} difficulty quiz with {quiz_request.num_questions} questions",
        quiz_type=quiz_request.quiz_type,
        difficulty=quiz_request.difficulty,
        time_limit=quiz_request.time_limit
    )
    
    db.add(quiz)
    db.flush()
    
    # Create some sample questions
    sample_questions = [
        {
            "question_text": "What is a Retrieval Augmented Generation (RAG) system?",
            "question_type": "multiple-choice",
            "options": [
                "A system that generates random text",
                "A system that combines retrieval and generation for accurate answers",
                "A system for editing and correcting text",
                "A system for translating text between languages"
            ],
            "correct_answer": "A system that combines retrieval and generation for accurate answers",
            "explanation": "RAG systems combine information retrieval with text generation to create responses that are grounded in specific documents."
        },
        {
            "question_text": "Which file formats are supported by the Study Assistant app?",
            "question_type": "multiple-choice",
            "options": [
                "PDF only",
                "Word (DOCX) only",
                "PDF and Word (DOCX)",
                "PDF, Word, and Excel"
            ],
            "correct_answer": "PDF and Word (DOCX)",
            "explanation": "The Study Assistant app supports PDF and Word document formats."
        },
        {
            "question_text": "What is the purpose of chunking in document processing?",
            "question_type": "multiple-choice",
            "options": [
                "To make the document smaller in file size",
                "To improve the visual appearance of the document",
                "To break the document into smaller pieces for better search and retrieval",
                "To remove irrelevant content from the document"
            ],
            "correct_answer": "To break the document into smaller pieces for better search and retrieval",
            "explanation": "Chunking breaks documents into smaller pieces to improve search precision and processing efficiency."
        },
        {
            "question_text": "Vector embeddings are used to represent text as numerical values.",
            "question_type": "true-false",
            "options": None,
            "correct_answer": "True",
            "explanation": "Vector embeddings convert text into numerical representations that capture semantic meaning."
        },
        {
            "question_text": "The Study Assistant app can only generate flashcards, not quizzes.",
            "question_type": "true-false",
            "options": None,
            "correct_answer": "False",
            "explanation": "The Study Assistant app can generate both flashcards and quizzes."
        }
    ]
    
    # Add questions to the quiz
    for i, q_data in enumerate(sample_questions):
        if i >= quiz_request.num_questions:
            break
            
        # Format correct answer based on question type
        correct_answer = q_data["correct_answer"]
        if q_data["question_type"] == "multiple-choice":
            correct_answer = str(q_data["options"].index(q_data["correct_answer"]))
        elif q_data["question_type"] == "true-false":
            correct_answer = "true" if q_data["correct_answer"] == "True" else "false"
        
        question = models.QuizQuestion(
            quiz_id=quiz.id,
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            options=q_data["options"],
            correct_answer=correct_answer,
            explanation=q_data["explanation"],
        )
        
        db.add(question)
    
    db.commit()
    db.refresh(quiz)
    
    # Get all questions
    questions = db.query(models.QuizQuestion).filter(
        models.QuizQuestion.quiz_id == quiz.id
    ).all()
    
    return schemas.QuizWithQuestions(
        id=quiz.id,
        document_id=quiz.document_id,
        title=quiz.title,
        description=quiz.description,
        quiz_type=quiz.quiz_type,
        difficulty=quiz.difficulty,
        time_limit=quiz.time_limit,
        created_at=quiz.created_at,
        questions=questions
    )