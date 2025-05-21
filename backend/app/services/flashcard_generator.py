from typing import List, Dict, Any, Optional
import logging
import re
from uuid import UUID

from app.utils.text_utils import extract_keywords

logger = logging.getLogger(__name__)

class FlashcardGenerator:
    """
    Service for generating flashcards from document content.
    
    This is a simplified implementation. In a real system, you would use
    more sophisticated NLP techniques or an LLM to generate better flashcards.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Flashcard Generator service")
    
    def generate_flashcards(
        self,
        document_text: str,
        num_cards: int = 10,
        difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate flashcards from document text.
        
        Args:
            document_text: The document text
            num_cards: Number of flashcards to generate
            difficulty: Optional difficulty level (easy, medium, hard)
            
        Returns:
            List of flashcards with front and back
        """
        self.logger.info(f"Generating {num_cards} flashcards, difficulty: {difficulty}")
        
        # Extract keywords for potential flashcard topics
        keywords = extract_keywords(document_text, max_keywords=num_cards * 2)
        
        # Use regex to find potential definition sentences
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:defined\s+as\s+)?([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+refers\s+to\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+means\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):([^.!?]+)',
        ]
        
        flashcards = []
        definitions = []
        
        # Find definitions in text
        for pattern in definition_patterns:
            matches = re.finditer(pattern, document_text)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                if 3 < len(term) < 50 and 10 < len(definition) < 200:
                    definitions.append({
                        "term": term,
                        "definition": definition
                    })
        
        # Create flashcards from definitions
        for i, definition in enumerate(definitions):
            if i >= num_cards:
                break
                
            flashcards.append({
                "front": definition["term"],
                "back": definition["definition"],
                "difficulty": difficulty or "medium"
            })
        
        # If we don't have enough flashcards from definitions, create some from keywords
        if len(flashcards) < num_cards:
            for keyword in keywords:
                if len(flashcards) >= num_cards:
                    break
                    
                # Skip if this keyword is already covered in a flashcard
                if any(keyword.lower() in card["front"].lower() for card in flashcards):
                    continue
                
                # Find sentences containing this keyword
                keyword_pattern = r'[^.!?]*\b' + re.escape(keyword) + r'\b[^.!?]*[.!?]'
                matches = re.finditer(keyword_pattern, document_text, re.IGNORECASE)
                
                relevant_sentences = []
                for match in matches:
                    sentence = match.group(0).strip()
                    if 10 < len(sentence) < 200:
                        relevant_sentences.append(sentence)
                
                if relevant_sentences:
                    # Create a question from the keyword and use the sentence as the answer
                    front = f"What is {keyword}?" if keyword[0].islower() else f"What is a {keyword}?"
                    back = relevant_sentences[0]
                    
                    flashcards.append({
                        "front": front,
                        "back": back,
                        "difficulty": difficulty or "medium"
                    })
        
        # Create some generic flashcards if we still don't have enough
        sample_flashcards = [
            {
                "front": "What is a Retrieval-Augmented Generation (RAG) system?",
                "back": "A system that combines information retrieval with text generation to create responses grounded in specific documents or knowledge bases.",
                "difficulty": "medium"
            },
            {
                "front": "What are embeddings in the context of document search?",
                "back": "Embeddings are numerical representations of text that capture semantic meaning, allowing for similarity searches based on content rather than just keywords.",
                "difficulty": "medium"
            },
            {
                "front": "What is the purpose of chunking in document processing?",
                "back": "Chunking breaks down documents into smaller, manageable pieces that can be processed individually, improving search precision and handling large documents efficiently.",
                "difficulty": "easy"
            }
        ]
        
        # Add sample flashcards if needed
        while len(flashcards) < num_cards and sample_flashcards:
            flashcards.append(sample_flashcards.pop(0))
        
        return flashcards


# Create a singleton instance
flashcard_generator = FlashcardGenerator()