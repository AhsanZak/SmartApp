"""
Chat service for managing conversations
"""
from sqlalchemy.orm import Session
from typing import List, Optional

from models.chat import Chat, Message
from services.model_service import ModelService
from services.document_service import DocumentService


class ChatService:
    """Service for managing chats"""
    
    def __init__(self, db: Session):
        self.db = db
        self.model_service = ModelService()
        self.document_service = DocumentService(db)
    
    def create_chat(
        self,
        title: str = "New Chat",
        model_name: str = "llama2",
        model_provider: str = "ollama",
        user_id: Optional[int] = None
    ) -> Chat:
        """Create a new chat session"""
        chat = Chat(
            title=title,
            model_name=model_name,
            model_provider=model_provider,
            user_id=user_id
        )
        
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        
        return chat
    
    def get_chat(self, chat_id: int) -> Optional[Chat]:
        """Get a chat by ID"""
        return self.db.query(Chat).filter(Chat.id == chat_id).first()
    
    def list_chats(self, skip: int = 0, limit: int = 100, user_id: Optional[int] = None) -> List[Chat]:
        """List all chats"""
        query = self.db.query(Chat)
        
        if user_id:
            query = query.filter(Chat.user_id == user_id)
        
        return query.order_by(Chat.updated_at.desc()).offset(skip).limit(limit).all()
    
    def delete_chat(self, chat_id: int) -> bool:
        """Delete a chat"""
        chat = self.get_chat(chat_id)
        if not chat:
            return False
        
        self.db.delete(chat)
        self.db.commit()
        
        return True
    
    async def send_message(
        self,
        chat_id: int,
        content: str,
        document_ids: Optional[List[int]] = None
    ) -> Message:
        """
        Send a message in a chat and get AI response
        """
        chat = self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"Chat {chat_id} not found")
        
        # Create user message
        user_message = Message(
            chat_id=chat_id,
            role="user",
            content=content,
            document_ids=document_ids or []
        )
        self.db.add(user_message)
        self.db.commit()
        
        # Get conversation history
        messages = self.db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at).all()
        
        # Build context from documents if provided
        context = ""
        if document_ids:
            for doc_id in document_ids:
                doc = self.document_service.get_document(doc_id)
                if doc and doc.extracted_text:
                    context += f"\n\nDocument: {doc.original_filename}\n{doc.extracted_text[:1000]}"
        
        # Prepare messages for the model
        conversation_history = []
        for msg in messages:
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Get AI response
        try:
            ai_response = await self.model_service.generate_response(
                messages=conversation_history,
                model_name=chat.model_name,
                model_provider=chat.model_provider,
                context=context
            )
            
            # Create assistant message
            assistant_message = Message(
                chat_id=chat_id,
                role="assistant",
                content=ai_response,
                document_ids=document_ids or []
            )
            self.db.add(assistant_message)
            self.db.commit()
            self.db.refresh(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            # Create error message
            error_message = Message(
                chat_id=chat_id,
                role="assistant",
                content=f"I apologize, but I encountered an error: {str(e)}",
                document_ids=document_ids or []
            )
            self.db.add(error_message)
            self.db.commit()
            self.db.refresh(error_message)
            
            return error_message

