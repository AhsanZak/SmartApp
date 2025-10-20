"""
Chat endpoints for conversational interface
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from services.chat_service import ChatService

router = APIRouter()


class ChatCreate(BaseModel):
    """Schema for creating a new chat"""
    title: Optional[str] = "New Chat"
    model_name: Optional[str] = "llama2"
    model_provider: Optional[str] = "ollama"


class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    content: str
    document_ids: Optional[List[int]] = []


class MessageResponse(BaseModel):
    """Message response schema"""
    id: int
    role: str
    content: str
    created_at: Optional[str]


class ChatResponse(BaseModel):
    """Chat response schema"""
    id: int
    title: str
    model_name: str
    model_provider: str
    created_at: Optional[str]
    messages: Optional[List[MessageResponse]] = []


@router.post("/chats", response_model=ChatResponse)
async def create_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new chat session
    """
    chat_service = ChatService(db)
    chat = chat_service.create_chat(
        title=chat_data.title,
        model_name=chat_data.model_name,
        model_provider=chat_data.model_provider
    )
    
    return ChatResponse(
        id=chat.id,
        title=chat.title,
        model_name=chat.model_name,
        model_provider=chat.model_provider,
        created_at=chat.created_at.isoformat() if chat.created_at else None,
        messages=[]
    )


@router.get("/chats", response_model=List[ChatResponse])
async def list_chats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all chat sessions
    """
    chat_service = ChatService(db)
    chats = chat_service.list_chats(skip=skip, limit=limit)
    
    return [
        ChatResponse(
            id=chat.id,
            title=chat.title,
            model_name=chat.model_name,
            model_provider=chat.model_provider,
            created_at=chat.created_at.isoformat() if chat.created_at else None
        )
        for chat in chats
    ]


@router.get("/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific chat with its messages
    """
    chat_service = ChatService(db)
    chat = chat_service.get_chat(chat_id)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    messages = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at.isoformat() if msg.created_at else None
        )
        for msg in chat.messages
    ]
    
    return ChatResponse(
        id=chat.id,
        title=chat.title,
        model_name=chat.model_name,
        model_provider=chat.model_provider,
        created_at=chat.created_at.isoformat() if chat.created_at else None,
        messages=messages
    )


@router.post("/chats/{chat_id}/messages", response_model=MessageResponse)
async def send_message(
    chat_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Send a message in a chat and get AI response
    """
    chat_service = ChatService(db)
    
    # Check if chat exists
    chat = chat_service.get_chat(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Send message and get response
    try:
        response = await chat_service.send_message(
            chat_id=chat_id,
            content=message_data.content,
            document_ids=message_data.document_ids
        )
        
        return MessageResponse(
            id=response.id,
            role=response.role,
            content=response.content,
            created_at=response.created_at.isoformat() if response.created_at else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.delete("/chats/{chat_id}")
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a chat session
    """
    chat_service = ChatService(db)
    success = chat_service.delete_chat(chat_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return {"message": "Chat deleted successfully"}

