"""
Document service for managing documents
"""
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from models.document import Document, DocumentChunk
from processors.file_processor_factory import FileProcessorFactory
from services.embedding_service import EmbeddingService


class DocumentService:
    """Service for managing documents"""
    
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
    
    def create_document(
        self,
        filename: str,
        original_filename: str,
        file_type: str,
        file_size: int,
        file_path: str,
        mime_type: Optional[str] = None
    ) -> Document:
        """
        Create a new document record
        """
        document = Document(
            filename=filename,
            original_filename=original_filename,
            file_type=file_type,
            file_size=file_size,
            file_path=file_path,
            mime_type=mime_type,
            status="uploaded"
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return document
    
    def get_document(self, document_id: int) -> Optional[Document]:
        """Get a document by ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def list_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """List all documents"""
        return self.db.query(Document).offset(skip).limit(limit).all()
    
    def delete_document(self, document_id: int) -> bool:
        """Delete a document"""
        document = self.get_document(document_id)
        if not document:
            return False
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete chunks
        self.db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).delete()
        
        # Delete document
        self.db.delete(document)
        self.db.commit()
        
        return True
    
    def process_document(self, document_id: int) -> Document:
        """
        Process a document: extract text, create embeddings, etc.
        """
        document = self.get_document(document_id)
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        try:
            # Update status
            document.status = "processing"
            self.db.commit()
            
            # Get appropriate processor
            processor = FileProcessorFactory.get_processor(document.file_type)
            
            # Extract text and metadata
            extracted_data = processor.process(document.file_path)
            
            document.extracted_text = extracted_data.get("text", "")
            document.metadata = extracted_data.get("metadata", {})
            
            # Create embedding for the document
            if document.extracted_text:
                embedding = self.embedding_service.create_embedding(document.extracted_text)
                document.embedding = embedding
                
                # Create chunks and their embeddings
                chunks = self._create_chunks(document.extracted_text)
                for idx, chunk_text in enumerate(chunks):
                    chunk_embedding = self.embedding_service.create_embedding(chunk_text)
                    
                    chunk = DocumentChunk(
                        document_id=document.id,
                        chunk_index=idx,
                        content=chunk_text,
                        embedding=chunk_embedding
                    )
                    self.db.add(chunk)
            
            # Update status
            document.status = "completed"
            self.db.commit()
            self.db.refresh(document)
            
        except Exception as e:
            document.status = "failed"
            document.error_message = str(e)
            self.db.commit()
            raise
        
        return document
    
    def _create_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
    
    def search_similar_documents(self, query: str, limit: int = 5) -> List[Document]:
        """
        Search for similar documents using vector similarity
        """
        # Create embedding for query
        query_embedding = self.embedding_service.create_embedding(query)
        
        # Search using pgvector
        # This is a simplified version - you'd use proper vector search
        documents = self.db.query(Document).filter(
            Document.embedding.isnot(None)
        ).limit(limit).all()
        
        return documents

