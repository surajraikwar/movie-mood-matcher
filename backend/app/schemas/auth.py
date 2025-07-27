"""Schemas for authentication endpoints"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str]
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
