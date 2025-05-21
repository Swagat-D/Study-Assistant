from typing import List, Dict, Any, Optional
import logging
import json
from pathlib import Path
import os
import numpy as np
import pickle

from app.core.config import settings

logger = logging.getLogger(__name__)

class SimpleVectorStore:
    """
    A simple in-memory vector store for text embeddings.
    
    In a production system, you would use a proper vector database like
    FAISS, Pinecone, or Weaviate. This is a simplified implementation
    for demonstration purposes.
    """
    
    def __init__(self, save_dir: str = "./.vectorstore"):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SimpleVectorStore")
        
        self.save_dir = save_dir
        self.embedding_dim = settings.EMBEDDING_DIMENSION  # Default dimension
        
        # Create a directory to save vector data
        os.makedirs(self.save_dir, exist_ok=True)
        
        # Storage for embeddings
        self.documents = {}  # {document_id: {document_info}}
        self.chunks = {}  # {chunk_id: {chunk_info}}
        self.embeddings = {}  # {chunk_id: embedding_vector}
        
        # Try to load existing data
        self._load_data()
    
    def _load_data(self):
        """Load vector store data from disk."""
        try:
            # Load documents
            doc_path = os.path.join(self.save_dir, "documents.json")
            if os.path.exists(doc_path):
                with open(doc_path, "r") as f:
                    self.documents = json.load(f)
            
            # Load chunks
            chunks_path = os.path.join(self.save_dir, "chunks.json")
            if os.path.exists(chunks_path):
                with open(chunks_path, "r") as f:
                    self.chunks = json.load(f)
            
            # Load embeddings
            emb_path = os.path.join(self.save_dir, "embeddings.pkl")
            if os.path.exists(emb_path):
                with open(emb_path, "rb") as f:
                    self.embeddings = pickle.load(f)
            
            self.logger.info(f"Loaded vector store with {len(self.documents)} documents and {len(self.chunks)} chunks")
        
        except Exception as e:
            self.logger.error(f"Error loading vector store data: {str(e)}")
            # Initialize empty stores
            self.documents = {}
            self.chunks = {}
            self.embeddings = {}
    
    def _save_data(self):
        """Save vector store data to disk."""
        try:
            # Save documents
            with open(os.path.join(self.save_dir, "documents.json"), "w") as f:
                json.dump(self.documents, f)
            
            # Save chunks
            with open(os.path.join(self.save_dir, "chunks.json"), "w") as f:
                json.dump(self.chunks, f)
            
            # Save embeddings
            with open(os.path.join(self.save_dir, "embeddings.pkl"), "wb") as f:
                pickle.dump(self.embeddings, f)
            
            self.logger.info(f"Saved vector store with {len(self.documents)} documents and {len(self.chunks)} chunks")
        
        except Exception as e:
            self.logger.error(f"Error saving vector store data: {str(e)}")
    
    def add_document(self, document_id: str, metadata: Dict[str, Any] = None):
        """
        Add a document to the vector store.
        
        Args:
            document_id: Unique ID for the document
            metadata: Optional metadata for the document
        """
        self.documents[document_id] = {
            "metadata": metadata or {},
        }
        self._save_data()
    
    def add_embedding(
        self,
        document_id: str,
        chunk_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict[str, Any] = None
    ):
        """
        Add an embedding to the vector store.
        
        Args:
            document_id: ID of the document this chunk belongs to
            chunk_id: Unique ID for the chunk
            text: Text content of the chunk
            embedding: Vector embedding of the chunk
            metadata: Optional metadata for the chunk
        """
        # Ensure document exists
        if document_id not in self.documents:
            self.add_document(document_id)
        
        # Add chunk
        self.chunks[chunk_id] = {
            "document_id": document_id,
            "text": text,
            "metadata": metadata or {},
        }
        
        # Add embedding
        self.embeddings[chunk_id] = np.array(embedding, dtype=np.float32)
        
        # Save data periodically (could be optimized to save less frequently)
        self._save_data()
    
    def search(
        self,
        query_embedding: List[float],
        document_ids: Optional[List[str]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.
        
        Args:
            query_embedding: Vector embedding of the query
            document_ids: Optional list of document IDs to restrict search to
            top_k: Number of results to return
            
        Returns:
            List of search results with document IDs, chunk IDs, and scores
        """
        if not self.embeddings:
            return []
        
        query_vector = np.array(query_embedding, dtype=np.float32)
        
        # Filter chunks by document ID if specified
        chunk_ids = []
        if document_ids:
            for chunk_id, chunk_info in self.chunks.items():
                if chunk_info["document_id"] in document_ids:
                    chunk_ids.append(chunk_id)
        else:
            chunk_ids = list(self.chunks.keys())
        
        if not chunk_ids:
            return []
        
        # Calculate similarity scores
        scores = {}
        for chunk_id in chunk_ids:
            if chunk_id in self.embeddings:
                chunk_vector = self.embeddings[chunk_id]
                # Use cosine similarity
                similarity = self._cosine_similarity(query_vector, chunk_vector)
                scores[chunk_id] = similarity
        
        # Sort by score and take top_k
        sorted_chunks = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        # Group results by document
        document_results = {}
        for chunk_id, score in sorted_chunks:
            chunk_info = self.chunks[chunk_id]
            document_id = chunk_info["document_id"]
            
            if document_id not in document_results:
                document_results[document_id] = {
                    "document_id": document_id,
                    "chunks": [],
                    "score": 0.0
                }
            
            document_results[document_id]["chunks"].append({
                "chunk_id": chunk_id,
                "text": chunk_info["text"],
                "score": float(score),  # Convert numpy float to regular float
                "page": chunk_info["metadata"].get("page_number")
            })
            
            # Update document score to the max chunk score
            document_results[document_id]["score"] = max(
                document_results[document_id]["score"], 
                float(score)
            )
        
        # Convert to list and sort by score
        results = list(document_results.values())
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results
    
    def delete_document(self, document_id: str):
        """
        Delete a document and all its chunks from the vector store.
        
        Args:
            document_id: ID of the document to delete
        """
        # Remove the document
        if document_id in self.documents:
            del self.documents[document_id]
        
        # Find and remove all chunks for this document
        chunks_to_remove = []
        for chunk_id, chunk_info in self.chunks.items():
            if chunk_info["document_id"] == document_id:
                chunks_to_remove.append(chunk_id)
        
        for chunk_id in chunks_to_remove:
            if chunk_id in self.chunks:
                del self.chunks[chunk_id]
            
            if chunk_id in self.embeddings:
                del self.embeddings[chunk_id]
        
        self._save_data()
    
    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        
        return dot_product / (norm_v1 * norm_v2)


# Create a singleton instance
vector_store = SimpleVectorStore()