from typing import List, Dict, Any
import re
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing line breaks.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Replace multiple line breaks with a single one
    text = re.sub(r'\n+', '\n', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text


def chunk_text(
    text: str, 
    chunk_size: int = None, 
    chunk_overlap: int = None
) -> List[str]:
    """
    Split text into chunks of a specified size.
    
    Args:
        text (str): Text to split
        chunk_size (int, optional): Maximum size of each chunk
        chunk_overlap (int, optional): Overlap between chunks
        
    Returns:
        List[str]: List of text chunks
    """
    if not text:
        return []
    
    # Use settings or defaults
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    # Clean the text
    text = clean_text(text)
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_size = len(sentence)
        
        # If adding this sentence would exceed chunk size, finalize the current chunk
        if current_size + sentence_size > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            
            # Keep overlap sentences for the next chunk
            if chunk_overlap > 0:
                # Calculate how many sentences to keep based on overlap
                overlap_size = 0
                overlap_sentences = []
                
                for s in reversed(current_chunk):
                    if overlap_size + len(s) <= chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_size += len(s) + 1  # +1 for space
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_size = overlap_size
            else:
                current_chunk = []
                current_size = 0
        
        # Add the sentence to the current chunk
        current_chunk.append(sentence)
        current_size += sentence_size + 1  # +1 for space
    
    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract important keywords from text.
    This is a simple implementation that can be replaced with more sophisticated NLP.
    
    Args:
        text (str): Text to extract keywords from
        max_keywords (int): Maximum number of keywords to extract
        
    Returns:
        List[str]: List of keywords
    """
    # Clean the text
    text = clean_text(text.lower())
    
    # Remove common stop words (simplified list)
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
        'at', 'from', 'by', 'for', 'with', 'about', 'against', 'between',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'to', 'of', 'in', 'on', 'off', 'over', 'under', 'again', 'further',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        's', 't', 'can', 'will', 'just', 'don', "don't", 'should', 'now',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
        'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'could',
        'should', 'shall', 'might', 'may', 'must', 'i', 'me', 'my', 'myself',
        'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
        'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
        'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
        'those', 'am', 'as', 'also'
    }
    
    # Split into words and remove stop words
    words = [word for word in re.findall(r'\b\w+\b', text) if word not in stop_words and len(word) > 3]
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and take top keywords
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [keyword for keyword, _ in keywords[:max_keywords]]


def generate_simple_summary(text: str, max_length: int = 500) -> str:
    """
    Generate a simple summary of the text.
    This is a basic extractive summary that can be replaced with more sophisticated NLP.
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum length of the summary
        
    Returns:
        str: Summary text
    """
    # Clean the text
    text = clean_text(text)
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Special case for short texts
    if len(text) <= max_length:
        return text
    
    # If we have very few sentences, just return the first few
    if len(sentences) <= 3:
        return ' '.join(sentences[:2])
    
    # Simple extractive summarization: take the first sentence and some important ones
    summary = [sentences[0]]  # Always include the first sentence
    
    # Calculate sentence importance based on keyword occurrence
    keywords = extract_keywords(text, max_keywords=20)
    sentence_scores = []
    
    for i, sentence in enumerate(sentences):
        # Skip the first sentence (already included)
        if i == 0:
            continue
            
        # Score based on position (earlier sentences are more important)
        position_score = 1.0 / (i + 1)
        
        # Score based on keyword occurrence
        keyword_score = sum(1 for keyword in keywords if keyword in sentence.lower())
        
        # Score based on sentence length (prefer medium-length sentences)
        length = len(sentence)
        length_score = 1.0 if 10 <= length <= 30 else 0.5
        
        # Combine scores
        total_score = (position_score * 0.3) + (keyword_score * 0.6) + (length_score * 0.1)
        
        sentence_scores.append((i, total_score, sentence))
    
    # Sort sentences by score and select top ones
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    
    # Add top sentences to summary (up to max_length)
    current_length = len(summary[0])
    
    for _, _, sentence in top_sentences:
        if current_length + len(sentence) + 1 <= max_length:  # +1 for space
            summary.append(sentence)
            current_length += len(sentence) + 1
        else:
            break
    
    # Sort summary sentences by their original order to maintain coherence
    sorted_summary = [sentences[0]]  # First sentence
    for sentence in sentences[1:]:
        if sentence in summary[1:]:
            sorted_summary.append(sentence)
            
    return ' '.join(sorted_summary)