"""
Embedding service for creating vector embeddings
"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from config.settings import get_settings


class EmbeddingService:
    """Service for creating embeddings"""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
    
    def _load_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            self.model = SentenceTransformer(self.settings.default_embeddings_model)
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        if not text:
            return [0.0] * self.settings.vector_dimensions
        
        self._load_model()
        
        # Create embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        
        # Convert to list
        return embedding.tolist()
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        if not texts:
            return []
        
        self._load_model()
        
        # Create embeddings
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Convert to list
        return embeddings.tolist()
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score between -1 and 1
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Compute cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        return float(similarity)

