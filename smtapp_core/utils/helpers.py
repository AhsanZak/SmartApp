"""
Helper utility functions
"""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict


def generate_unique_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())


def generate_file_hash(file_content: bytes) -> str:
    """
    Generate SHA256 hash of file content
    
    Args:
        file_content: File content as bytes
        
    Returns:
        Hex string of hash
    """
    return hashlib.sha256(file_content).hexdigest()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = filename.split("/")[-1].split("\\")[-1]
    
    # Remove potentially dangerous characters
    dangerous_chars = ['..', '~', '$', '&', '|', ';', '`']
    for char in dangerous_chars:
        filename = filename.replace(char, '')
    
    return filename


def chunk_text(text: str, max_length: int = 500, overlap: int = 50) -> list:
    """
    Split text into chunks with overlap
    
    Args:
        text: Text to chunk
        max_length: Maximum length of each chunk
        overlap: Number of characters to overlap
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + max_length
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_length - overlap
    
    return chunks

