"""
Document management endpoints
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from config.database import get_db
from config.settings import get_settings
from models.document import Document
from services.document_service import DocumentService
from pydantic import BaseModel

router = APIRouter()


class DocumentResponse(BaseModel):
    """Document response schema"""
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    created_at: Optional[str]


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a document for processing
    """
    settings = get_settings()
    document_service = DocumentService(db)
    
    # Validate file type
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if file_ext not in settings.supported_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_ext}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    file_size = len(content)
    max_size = settings.max_file_size_mb * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Create document record
    document = document_service.create_document(
        filename=unique_filename,
        original_filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        file_path=file_path,
        mime_type=file.content_type
    )
    
    # Process document asynchronously (in background)
    # For now, we'll process it synchronously
    try:
        document_service.process_document(document.id)
    except Exception as e:
        print(f"Error processing document: {e}")
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_type=document.file_type,
        file_size=document.file_size,
        status=document.status,
        created_at=document.created_at.isoformat() if document.created_at else None
    )


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all uploaded documents
    """
    document_service = DocumentService(db)
    documents = document_service.list_documents(skip=skip, limit=limit)
    
    return [
        DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            original_filename=doc.original_filename,
            file_type=doc.file_type,
            file_size=doc.file_size,
            status=doc.status,
            created_at=doc.created_at.isoformat() if doc.created_at else None
        )
        for doc in documents
    ]


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID
    """
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_filename=document.original_filename,
        file_type=document.file_type,
        file_size=document.file_size,
        status=document.status,
        created_at=document.created_at.isoformat() if document.created_at else None
    )


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a document
    """
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document deleted successfully"}

