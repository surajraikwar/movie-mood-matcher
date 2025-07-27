"""User models for authentication and authorization"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from app.database.types import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.config import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    auth_providers = relationship("AuthProvider", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class AuthProvider(Base):
    __tablename__ = "auth_providers"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)  # 'email', 'google', 'apple'
    provider_user_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="auth_providers")
    
    def __repr__(self):
        return f"<AuthProvider(provider={self.provider}, user_id={self.user_id})>"
