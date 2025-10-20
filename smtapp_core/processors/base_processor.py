"""
Base processor class for file processing
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProcessor(ABC):
    """Base class for all file processors"""
    
    @abstractmethod
    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process a file and extract information
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing:
                - text: Extracted text content
                - metadata: Additional metadata
        """
        pass
    
    @abstractmethod
    def supports(self, file_extension: str) -> bool:
        """
        Check if this processor supports the given file extension
        
        Args:
            file_extension: File extension (without dot)
            
        Returns:
            True if supported, False otherwise
        """
        pass

