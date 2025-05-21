from typing import List, Dict, Any, Union, Optional
import logging
import pickle
import numpy as np
from functools import lru_cache

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating embeddings from text using various providers.
    
    This is a simplified implementation. In a real system, you would use
    a proper embedding service like OpenAI's text-embedding-ada-002 or
    a local model like SentenceTransformers.
    """

    def __init__(self, provider=None):
        self.provider = provider or settings.EMBEDDING_PROVIDER
        self.model = getattr(settings, "EMBEDDING_MODEL", "simple")
        self.embedding_dim = getattr(settings, "EMBEDDING_DIMENSION", 384)
        self._embedding_model = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing EmbeddingService with provider: {self.provider}")
    
    def generate_embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for a list of text strings.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (as lists of floats)
        """
        if not texts:
            return []
        
        # Choose embedding method based on provider
        if self.provider == "openai":
            return self._generate_openai_embeddings(texts)
        elif self.provider == "huggingface":
            return self._generate_huggingface_embeddings(texts)
        else:
            # Default to simple embeddings for development
            return self._generate_simple_embeddings(texts)
    
    def _generate_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI's API.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            import openai
            
            # Configure OpenAI API
            openai.api_key = settings.LLM_API_KEY
            
            embeddings = []
            # Process in batches to avoid API limits
            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                
                self.logger.info(f"Generating embeddings for batch of {len(batch)} texts")
                
                response = openai.Embedding.create(
                    model=self.model,
                    input=batch
                )
                
                batch_embeddings = [item["embedding"] for item in response["data"]]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except ImportError:
            self.logger.error("OpenAI package not installed. Install with 'pip install openai'")
            # Fall back to simple embeddings
            return self._generate_simple_embeddings(texts)
        except Exception as e:
            self.logger.error(f"Error generating OpenAI embeddings: {str(e)}")
            # Fall back to simple embeddings
            return self._generate_simple_embeddings(texts)
    
    def _generate_huggingface_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Hugging Face Transformers.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            from sentence_transformers import SentenceTransformer
            
            # Load model if not already loaded
            if self._embedding_model is None:
                self.logger.info(f"Loading SentenceTransformer model: {self.model}")
                self._embedding_model = SentenceTransformer(self.model)
            
            # Generate embeddings
            self.logger.info(f"Generating embeddings for {len(texts)} texts")
            embeddings = self._embedding_model.encode(texts)
            
            # Convert to list of lists
            return embeddings.tolist()
            
        except ImportError:
            self.logger.error("SentenceTransformers package not installed. Install with 'pip install sentence-transformers'")
            # Fall back to simple embeddings
            return self._generate_simple_embeddings(texts)
        except Exception as e:
            self.logger.error(f"Error generating Hugging Face embeddings: {str(e)}")
            # Fall back to simple embeddings
            return self._generate_simple_embeddings(texts)
    
    def _generate_simple_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate simple embeddings using TF-IDF like approach.
        This is a very simplified approach used as a fallback when other methods fail.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        self.logger.info(f"Generating simple embeddings for {len(texts)} texts")
        
        # Create a simple vocabulary
        vocab = set()
        for text in texts:
            words = text.lower().split()
            vocab.update(words)
        
        vocab = list(vocab)
        vocab_size = len(vocab)
        
        # Ensure embedding dimension is not larger than vocab size
        dim = min(self.embedding_dim, vocab_size)
        
        # Create word-to-index mapping
        word_to_idx = {word: i for i, word in enumerate(vocab)}
        
        # Generate embeddings
        embeddings = []
        for text in texts:
            words = text.lower().split()
            
            # Count word occurrences
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            # Create vector (simplified tf-idf like approach)
            vector = np.zeros(vocab_size, dtype=np.float32)
            for word, count in word_counts.items():
                if word in word_to_idx:
                    vector[word_to_idx[word]] = count / len(words)
            
            # Normalize vector
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            
            # Reduce dimension if needed
            if dim < vocab_size:
                # Simple dimension reduction by summing adjacent elements
                reduced_vector = np.zeros(dim, dtype=np.float32)
                for i in range(vocab_size):
                    reduced_idx = i % dim
                    reduced_vector[reduced_idx] += vector[i]
                
                # Normalize again
                norm = np.linalg.norm(reduced_vector)
                if norm > 0:
                    reduced_vector = reduced_vector / norm
                
                embeddings.append(reduced_vector.tolist())
            else:
                embeddings.append(vector.tolist())
        
        return embeddings
    
    def serialize_embedding(self, embedding: List[float]) -> bytes:
        """
        Serialize an embedding vector to binary format.
        
        Args:
            embedding: Vector to serialize
            
        Returns:
            Binary representation of the embedding
        """
        # Convert to numpy array and serialize
        embedding_array = np.array(embedding, dtype=np.float32)
        return pickle.dumps(embedding_array)
    
    def deserialize_embedding(self, binary_data: bytes) -> List[float]:
        """
        Deserialize a binary embedding back to a vector.
        
        Args:
            binary_data: Binary embedding data
            
        Returns:
            Embedding vector as a list of floats
        """
        # Load numpy array and convert to list
        embedding_array = pickle.loads(binary_data)
        return embedding_array.tolist()


# Create a singleton instance
embedding_service = EmbeddingService()