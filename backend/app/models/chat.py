"""Chat models for conversation management"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from app.database.types import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.config import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)  # Auto-generated from first message
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan", order_by="Message.created_at")
    
    def __repr__(self):
        return f"<ChatSession(id={self.id}, user_id={self.user_id})>"


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)  # Store recommendations, context, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role})>"
