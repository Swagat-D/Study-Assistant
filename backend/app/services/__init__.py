# This file makes the 'services' directory a Python package
# Import service instances for easy access

from app.services.document_processor import document_processor
from app.services.rag import rag_service
from app.services.flashcard_generator import flashcard_generator
from app.services.quiz_generator import quiz_generator
from app.services.summarizer import summarizer