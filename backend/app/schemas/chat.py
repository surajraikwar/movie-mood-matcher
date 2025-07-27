"""Schemas for chat endpoints"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatSessionCreate(BaseModel):
    title: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    role: str = "user"


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    details: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
