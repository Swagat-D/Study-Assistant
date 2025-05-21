from typing import List, Dict, Any, Optional
import logging
import re
import random

from app.utils.text_utils import extract_keywords

logger = logging.getLogger(__name__)

class QuizGenerator:
    """
    Service for generating quizzes from document content.
    
    This is a simplified implementation. In a real system, you would use
    more sophisticated NLP techniques or an LLM to generate better quiz questions.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Quiz Generator service")
    
    def generate_quiz(
        self,
        document_text: str,
        num_questions: int = 10,
        quiz_type: str = "mixed",
        difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Generate a quiz from document text.
        
        Args:
            document_text: The document text
            num_questions: Number of questions to generate
            quiz_type: Type of quiz (multiple-choice, true-false, short-answer, mixed)
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            Dict with quiz title, description, and questions
        """
        self.logger.info(
            f"Generating quiz with {num_questions} questions, "
            f"type: {quiz_type}, difficulty: {difficulty}"
        )
        
        # Extract keywords for potential question topics
        keywords = extract_keywords(document_text, max_keywords=num_questions * 3)
        
        # Determine question types based on quiz_type
        question_types = []
        if quiz_type == "multiple-choice":
            question_types = ["multiple-choice"] * num_questions
        elif quiz_type == "true-false":
            question_types = ["true-false"] * num_questions
        elif quiz_type == "short-answer":
            question_types = ["short-answer"] * num_questions
        else:  # mixed
            # Create a mix of question types
            question_types = (
                ["multiple-choice"] * (num_questions // 2) +
                ["true-false"] * (num_questions // 4) +
                ["short-answer"] * (num_questions - num_questions // 2 - num_questions // 4)
            )
            random.shuffle(question_types)
        
        # Generate questions
        questions = []
        for i in range(min(num_questions, len(question_types))):
            question_type = question_types[i]
            
            if question_type == "multiple-choice":
                question = self._generate_multiple_choice_question(document_text, keywords, difficulty)
            elif question_type == "true-false":
                question = self._generate_true_false_question(document_text, keywords, difficulty)
            else:  # short-answer
                question = self._generate_short_answer_question(document_text, keywords, difficulty)
            
            if question:
                questions.append(question)
        
        # Add sample questions if we don't have enough
        sample_questions = self._get_sample_questions()
        while len(questions) < num_questions and sample_questions:
            sample_question = sample_questions.pop(0)
            # Filter by quiz type if needed
            if quiz_type != "mixed" and sample_question["question_type"] != quiz_type:
                continue
            questions.append(sample_question)
        
        # Construct quiz
        quiz = {
            "title": "Quiz on Document Content",
            "description": f"A {difficulty} difficulty {quiz_type} quiz with {len(questions)} questions",
            "quiz_type": quiz_type,
            "difficulty": difficulty,
            "questions": questions
        }
        
        return quiz
    
    def _generate_multiple_choice_question(
        self, 
        document_text: str, 
        keywords: List[str],
        difficulty: str
    ) -> Optional[Dict[str, Any]]:
        """Generate a multiple-choice question."""
        # This is a simplified implementation
        # In a real system, you would use NLP to generate better questions
        
        # Try to find a definition sentence
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:defined\s+as\s+)?([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+refers\s+to\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+means\s+([^.!?]+)',
        ]
        
        for pattern in definition_patterns:
            matches = re.finditer(pattern, document_text)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                if 3 < len(term) < 50 and 10 < len(definition) < 200:
                    # Create a question
                    question_text = f"What is {term}?"
                    
                    # Create options (1 correct + 3 distractors)
                    correct_option = definition
                    options = [correct_option]
                    
                    # Generate distractors (in a real system, these would be better)
                    distractors = [
                        f"A type of {term} used in specialized applications",
                        f"The process of analyzing {term} in different contexts",
                        f"A framework for understanding {term} relationships"
                    ]
                    
                    options.extend(distractors)
                    random.shuffle(options)
                    
                    correct_answer = options.index(correct_option)
                    
                    return {
                        "question_text": question_text,
                        "question_type": "multiple-choice",
                        "options": options,
                        "correct_answer": correct_answer,
                        "explanation": f"The correct definition of {term} is: {definition}"
                    }
        
        return None
    
    def _generate_true_false_question(
        self, 
        document_text: str, 
        keywords: List[str],
        difficulty: str
    ) -> Optional[Dict[str, Any]]:
        """Generate a true/false question."""
        # Look for statements in the document
        sentences = re.split(r'(?<=[.!?])\s+', document_text)
        for sentence in sentences:
            # Look for statements that are likely to be facts
            if re.search(r'\bis\b|\bare\b|\bhas\b|\bhave\b', sentence) and 20 < len(sentence) < 150:
                # Randomly decide to make it true or false
                is_true = random.choice([True, False])
                
                question_text = sentence.strip()
                
                if not is_true:
                    # Modify the sentence to make it false
                    # This is a very simple approach - in a real system, use NLP
                    if " is " in question_text.lower():
                        question_text = question_text.lower().replace(" is ", " is not ")
                    elif " are " in question_text.lower():
                        question_text = question_text.lower().replace(" are ", " are not ")
                    elif " has " in question_text.lower():
                        question_text = question_text.lower().replace(" has ", " does not have ")
                    elif " have " in question_text.lower():
                        question_text = question_text.lower().replace(" have ", " do not have ")
                    else:
                        # If we can't make it false easily, skip
                        continue
                
                return {
                    "question_text": question_text,
                    "question_type": "true-false",
                    "options": None,
                    "correct_answer": "true" if is_true else "false",
                    "explanation": "Based on information from the document."
                }
        
        return None
    
    def _generate_short_answer_question(
        self, 
        document_text: str, 
        keywords: List[str],
        difficulty: str
    ) -> Optional[Dict[str, Any]]:
        """Generate a short-answer question."""
        # Try to use one of the extracted keywords
        for keyword in keywords:
            # Find sentences containing this keyword
            pattern = r'[^.!?]*\b' + re.escape(keyword) + r'\b[^.!?]*[.!?]'
            matches = re.finditer(pattern, document_text, re.IGNORECASE)
            
            sentences = []
            for match in matches:
                sentence = match.group(0).strip()
                if 20 < len(sentence) < 200:
                    sentences.append(sentence)
            
            if sentences:
                # Create a question about the keyword
                question_text = f"What is {keyword}? Provide a brief definition."
                
                # Use the sentence as the correct answer
                correct_answer = sentences[0]
                
                return {
                    "question_text": question_text,
                    "question_type": "short-answer",
                    "options": None,
                    "correct_answer": correct_answer,
                    "explanation": "This is a key term from the document."
                }
        
        return None
    
    def _get_sample_questions(self) -> List[Dict[str, Any]]:
        """Get sample questions for when extraction fails."""
        return [
            {
                "question_text": "What is a Retrieval Augmented Generation (RAG) system?",
                "question_type": "multiple-choice",
                "options": [
                    "A system that generates random text",
                    "A system that combines retrieval and generation for accurate answers",
                    "A system for editing and correcting text",
                    "A system for translating text between languages"
                ],
                "correct_answer": 1,
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
                "correct_answer": 2,
                "explanation": "The Study Assistant app supports PDF and Word document formats."
            },
            {
                "question_text": "Vector embeddings are used to represent text as numerical values.",
                "question_type": "true-false",
                "options": None,
                "correct_answer": "true",
                "explanation": "Vector embeddings convert text into numerical representations that capture semantic meaning."
            },
            {
                "question_text": "What is the purpose of chunking in document processing?",
                "question_type": "short-answer",
                "options": None,
                "correct_answer": "Chunking breaks documents into smaller pieces to improve search precision and processing efficiency.",
                "explanation": "Chunking is important for managing large documents and enabling precise retrieval."
            }
        ]


# Create a singleton instance
quiz_generator = QuizGenerator()