from typing import Dict, Any, List, Optional
import logging
import re

from app.utils.text_utils import extract_keywords, generate_simple_summary

logger = logging.getLogger(__name__)

class Summarizer:
    """
    Service for generating summaries from document content.
    
    This is a simplified implementation. In a real system, you would use
    more sophisticated NLP techniques or an LLM to generate better summaries.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Summarizer service")
    
    def generate_summary(
        self,
        document_text: str,
        summary_type: str = "general",
        max_length: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a summary of the document text.
        
        Args:
            document_text: The document text
            summary_type: Type of summary (brief, general, detailed)
            max_length: Maximum length of the summary
            
        Returns:
            Dict with summary title, content, and type
        """
        self.logger.info(f"Generating {summary_type} summary, max length: {max_length}")
        
        # Determine max length based on summary type if not provided
        if not max_length:
            if summary_type == "brief":
                max_length = 500
            elif summary_type == "detailed":
                max_length = 2000
            else:  # general
                max_length = 1000
        
        # Generate summary using our utility function
        summary_text = generate_simple_summary(document_text, max_length=max_length)
        
        # Extract key concepts and main points
        key_concepts = self._extract_key_concepts(document_text)
        main_points = self._extract_main_points(document_text, max_points=5)
        
        # Build structured summary
        summary = {
            "title": "Document Summary",
            "content": summary_text,
            "summary_type": summary_type,
            "sections": [
                {
                    "heading": "Key Concepts",
                    "content": ", ".join(key_concepts)
                },
                {
                    "heading": "Main Points",
                    "content": "\n".join([f"- {point}" for point in main_points])
                }
            ]
        }
        
        return summary
    
    def _extract_key_concepts(self, text: str, max_concepts: int = 8) -> List[str]:
        """Extract key concepts from text."""
        # Use the keyword extraction function
        keywords = extract_keywords(text, max_keywords=max_concepts)
        return keywords
    
    def _extract_main_points(self, text: str, max_points: int = 5) -> List[str]:
        """Extract main points from text."""
        # This is a simplified approach
        # In a real system, you would use more sophisticated techniques
        
        # Look for sentences that seem important
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out short sentences
        sentences = [s for s in sentences if len(s) > 30]
        
        # Look for sentences with indicator phrases
        indicators = [
            r'important', r'significant', r'key', r'main', r'critical',
            r'essential', r'fundamental', r'primary', r'crucial', r'notable'
        ]
        
        important_sentences = []
        for sentence in sentences:
            if any(re.search(r'\b' + indicator + r'\b', sentence, re.IGNORECASE) for indicator in indicators):
                important_sentences.append(sentence.strip())
        
        # If we don't have enough, add sentences from the beginning
        # (first sentences often contain important information)
        if len(important_sentences) < max_points:
            for sentence in sentences[:10]:  # Look at first 10 sentences
                if sentence not in important_sentences:
                    important_sentences.append(sentence.strip())
                if len(important_sentences) >= max_points:
                    break
        
        # Return at most max_points sentences
        return important_sentences[:max_points]


# Create a singleton instance
summarizer = Summarizer()