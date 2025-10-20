"""
Text file processor
"""
from typing import Dict, Any
import os

from processors.base_processor import BaseProcessor


class TextProcessor(BaseProcessor):
    """Processor for text files"""
    
    def supports(self, file_extension: str) -> bool:
        """Check if text file is supported"""
        return file_extension.lower() in ["txt", "md", "json", "xml"]
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process text file and extract content
        
        Args:
            file_path: Path to text file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Read file with different encodings
            encodings = ["utf-8", "latin-1", "cp1252"]
            text = None
            
            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        text = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if text is None:
                raise Exception("Could not decode file with any supported encoding")
            
            # Get metadata
            file_ext = file_path.split(".")[-1].lower()
            metadata = {
                "file_type": file_ext,
                "file_size": os.path.getsize(file_path),
                "lines": len(text.split("\n")),
                "characters": len(text)
            }
            
            return {
                "text": text,
                "metadata": metadata
            }
            
        except Exception as e:
            raise Exception(f"Error processing text file: {str(e)}")

