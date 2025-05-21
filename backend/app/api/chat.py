from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
import io
import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas import chat as schemas
from app.core.security import get_current_active_user
from app.services.rag import rag_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("/message", response_model=schemas.ChatResponse)
async def send_message(
    chat_request: schemas.ChatRequest,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chat system and get a response.
    """
    try:
        # Get or create chat session
        chat_session = None
        if chat_request.document_id:
            # Check if document exists and belongs to user
            document = db.query(models.Document).filter(
                models.Document.id == str(chat_request.document_id),
                models.Document.owner_id == user.id
            ).first()
            
            if not document:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Document not found"
                )
            
            # Find existing chat session for this document
            chat_session = db.query(models.ChatSession).filter(
                models.ChatSession.user_id == user.id,
                models.ChatSession.document_id == str(chat_request.document_id)
            ).order_by(models.ChatSession.created_at.desc()).first()
            
            if not chat_session:
                # Create new chat session
                chat_session = models.ChatSession(
                    user_id=user.id,
                    document_id=str(chat_request.document_id),
                    name=f"Chat with {document.name}"
                )
                db.add(chat_session)
                db.commit()
                db.refresh(chat_session)
        else:
            # Find or create a general chat session
            chat_session = db.query(models.ChatSession).filter(
                models.ChatSession.user_id == user.id,
                models.ChatSession.document_id == None
            ).order_by(models.ChatSession.created_at.desc()).first()
            
            if not chat_session:
                # Create new general chat session
                chat_session = models.ChatSession(
                    user_id=user.id,
                    name="General Chat"
                )
                db.add(chat_session)
                db.commit()
                db.refresh(chat_session)
        
        # Save user message to database
        user_message = models.ChatMessage(
            chat_session_id=chat_session.id,
            sender="user",
            text=chat_request.message
        )
        db.add(user_message)
        db.commit()
        
        # Process the message using RAG
        conversation_history = []
        if chat_request.conversation_history:
            conversation_history = chat_request.conversation_history
        else:
            # Get last few messages from chat session
            chat_history = db.query(models.ChatMessage).filter(
                models.ChatMessage.chat_session_id == chat_session.id
            ).order_by(models.ChatMessage.timestamp.desc()).limit(10).all()
            
            conversation_history = [
                {"sender": msg.sender, "text": msg.text}
                for msg in reversed(chat_history)
            ]
        
        # Generate response
        response_data = rag_service.generate_response(
            query=chat_request.message,
            document_id=chat_request.document_id,
            conversation_history=conversation_history
        )
        
        # Save bot response to database
        bot_message = models.ChatMessage(
            chat_session_id=chat_session.id,
            sender="bot",
            text=response_data["message"],
            source_chunks=response_data.get("source_chunks")
        )
        db.add(bot_message)
        db.commit()
        
        return schemas.ChatResponse(
            message=response_data["message"],
            source_chunks=response_data.get("source_chunks"),
            document_id=chat_request.document_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@router.get("/history/{document_id}", response_model=schemas.ChatSessionWithMessages)
async def get_chat_history(
    document_id: str,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for a specific document.
    """
    # Check if document exists and belongs to user
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Find chat session for this document
    chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user.id,
        models.ChatSession.document_id == document_id
    ).order_by(models.ChatSession.created_at.desc()).first()
    
    if not chat_session:
        # No chat history exists
        return schemas.ChatSessionWithMessages(
            id="00000000-0000-0000-0000-000000000000",
            user_id=user.id,
            document_id=document_id,
            name=f"Chat with {document.name}",
            created_at=document.created_at,
            messages=[]
        )
    
    # Get messages for the chat session
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.chat_session_id == chat_session.id
    ).order_by(models.ChatMessage.timestamp.asc()).all()
    
    return schemas.ChatSessionWithMessages(
        id=chat_session.id,
        user_id=chat_session.user_id,
        document_id=chat_session.document_id,
        name=chat_session.name,
        created_at=chat_session.created_at,
        updated_at=chat_session.updated_at,
        messages=messages
    )

@router.post("/history/save")
async def save_chat_history(
    chat_history: schemas.ChatHistorySave,
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Save chat history for a document.
    """
    # Check if document exists and belongs to user
    document = db.query(models.Document).filter(
        models.Document.id == str(chat_history.document_id),
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Get or create chat session
    chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user.id,
        models.ChatSession.document_id == str(chat_history.document_id)
    ).order_by(models.ChatSession.created_at.desc()).first()
    
    if not chat_session:
        chat_session = models.ChatSession(
            user_id=user.id,
            document_id=str(chat_history.document_id),
            name=f"Chat with {document.name}"
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
    
    # Clear existing messages
    db.query(models.ChatMessage).filter(
        models.ChatMessage.chat_session_id == chat_session.id
    ).delete()
    
    # Add new messages
    for message_data in chat_history.messages:
        message = models.ChatMessage(
            chat_session_id=chat_session.id,
            sender=message_data["sender"],
            text=message_data["text"],
            source_chunks=message_data.get("source_chunks"),
            timestamp=datetime.fromisoformat(message_data.get("timestamp")) if "timestamp" in message_data else datetime.utcnow()
        )
        db.add(message)
    
    db.commit()
    
    return {"message": "Chat history saved successfully"}

@router.get("/export/{document_id}")
async def export_chat_transcript(
    document_id: str,
    format: str = "txt",
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Export chat transcript as a file.
    """
    # Check if document exists and belongs to user
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Find chat session for this document
    chat_session = db.query(models.ChatSession).filter(
        models.ChatSession.user_id == user.id,
        models.ChatSession.document_id == document_id
    ).order_by(models.ChatSession.created_at.desc()).first()
    
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No chat history found for this document"
        )
    
    # Get messages for the chat session
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.chat_session_id == chat_session.id
    ).order_by(models.ChatMessage.timestamp.asc()).all()
    
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages found in chat history"
        )
    
    # Generate transcript
    if format.lower() == "txt":
        # Plain text format
        transcript = f"Chat Transcript: {chat_session.name}\n"
        transcript += f"Document: {document.name}\n"
        transcript += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for message in messages:
            sender = "AI" if message.sender == "bot" else "You"
            timestamp = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            transcript += f"[{timestamp}] {sender}: {message.text}\n\n"
        
        # Create response
        output = io.StringIO()
        output.write(transcript)
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=transcript_{document_id}.txt"}
        )
    else:
        # Unsupported format
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported export format: {format}"
        )