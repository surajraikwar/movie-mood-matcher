"""Chat API routes with streaming support"""
import json
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.database.config import get_db
from app.models.user import User
from app.models.chat import ChatSession, Message
from app.core.security import get_current_active_user
from app.services.ai_service import AIService
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    MessageCreate,
    MessageResponse,
    ChatRequest
)

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize AI service
ai_service = AIService()


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    session = ChatSession(
        user_id=current_user.id,
        title=session_data.title or "New Chat"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session


@router.get("/sessions", response_model=list[ChatSessionResponse])
async def get_chat_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all chat sessions for current user"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()
    
    return sessions


@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_session_messages(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a chat session"""
    # Verify session belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return session.messages


async def generate_ai_response(
    user_message: str,
    session_id: str,
    user_id: str,
    db: Session
) -> AsyncGenerator[str, None]:
    """Generate streaming AI response"""
    # Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message
    )
    db.add(user_msg)
    db.commit()
    
    # Get chat history
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.created_at).all()
    
    # Generate AI response
    ai_response = ""
    async for chunk in ai_service.generate_streaming_response(user_message, messages):
        ai_response += chunk
        # Send as Server-Sent Event format
        yield f"data: {json.dumps({'content': chunk})}\n\n"
        await asyncio.sleep(0.01)  # Small delay for smoother streaming
    
    # Save AI response
    ai_msg = Message(
        session_id=session_id,
        role="assistant",
        content=ai_response,
        details={
            "model": "gpt-4",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    db.add(ai_msg)
    
    # Update session title if it's the first message
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if len(messages) == 1:  # First user message
        session.title = user_message[:50] + "..." if len(user_message) > 50 else user_message
    
    session.updated_at = datetime.utcnow()
    db.commit()
    
    yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"


@router.post("/stream/{session_id}")
async def stream_chat_response(
    session_id: str,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Stream chat response using Server-Sent Events"""
    # Verify session belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return StreamingResponse(
        generate_ai_response(
            chat_request.message,
            session_id,
            str(current_user.id),
            db
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
