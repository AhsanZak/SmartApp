"""
PDF file processor
"""
from typing import Dict, Any
from pypdf import PdfReader
import os

from processors.base_processor import BaseProcessor


class PDFProcessor(BaseProcessor):
    """Processor for PDF files"""
    
    def supports(self, file_extension: str) -> bool:
        """Check if PDF is supported"""
        return file_extension.lower() == "pdf"
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process PDF file and extract text
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            reader = PdfReader(file_path)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            
            # Get metadata
            metadata = {
                "pages": len(reader.pages),
                "file_size": os.path.getsize(file_path)
            }
            
            # Add PDF metadata if available
            if reader.metadata:
                metadata.update({
                    "title": reader.metadata.get("/Title", ""),
                    "author": reader.metadata.get("/Author", ""),
                    "subject": reader.metadata.get("/Subject", ""),
                    "creator": reader.metadata.get("/Creator", ""),
                })
            
            return {
                "text": text.strip(),
                "metadata": metadata
            }
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

