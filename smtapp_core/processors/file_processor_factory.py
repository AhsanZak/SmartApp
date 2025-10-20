"""
Factory for creating file processors
"""
from typing import Optional

from processors.base_processor import BaseProcessor
from processors.pdf_processor import PDFProcessor
from processors.docx_processor import DOCXProcessor
from processors.excel_processor import ExcelProcessor
from processors.text_processor import TextProcessor
from processors.audio_processor import AudioProcessor
from processors.video_processor import VideoProcessor
from processors.image_processor import ImageProcessor


class FileProcessorFactory:
    """Factory for creating appropriate file processors"""
    
    # Register all processors
    _processors = [
        PDFProcessor(),
        DOCXProcessor(),
        ExcelProcessor(),
        TextProcessor(),
        AudioProcessor(),
        VideoProcessor(),
        ImageProcessor(),
    ]
    
    @classmethod
    def get_processor(cls, file_extension: str) -> BaseProcessor:
        """
        Get the appropriate processor for a file extension
        
        Args:
            file_extension: File extension (without dot)
            
        Returns:
            Appropriate processor instance
            
        Raises:
            ValueError: If no processor supports the file extension
        """
        file_extension = file_extension.lower()
        
        for processor in cls._processors:
            if processor.supports(file_extension):
                return processor
        
        raise ValueError(f"No processor found for file type: {file_extension}")
    
    @classmethod
    def register_processor(cls, processor: BaseProcessor):
        """
        Register a custom processor
        
        Args:
            processor: Processor instance to register
        """
        cls._processors.append(processor)

