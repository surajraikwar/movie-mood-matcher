"""Authentication API routes"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError

from app.database.config import get_db
from app.models.user import User, AuthProvider
from app.models.preferences import UserPreferences
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    get_current_user
)
from app.core.config import settings
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    Token,
    LoginRequest,
    RefreshTokenRequest
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Validate email
    try:
        valid_email = validate_email(user_data.email)
        email = valid_email.email
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == email) | 
        (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    user = User(
        email=email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        is_verified=False  # Will implement email verification later
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create auth provider entry
    auth_provider = AuthProvider(
        user_id=user.id,
        provider="email"
    )
    db.add(auth_provider)
    
    # Create user preferences
    preferences = UserPreferences(
        user_id=user.id
    )
    db.add(preferences)
    
    db.commit()
    
    # TODO: Send verification email
    # background_tasks.add_task(send_verification_email, user.email, user.id)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with email/username and password"""
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == form_data.username) | 
        (User.username == form_data.username)
    ).first()
    
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    from app.core.security import verify_token
    
    try:
        payload = verify_token(token_data.refresh_token, "refresh")
        user_id = payload.get("sub")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout current user (client should discard tokens)"""
    # In a production app, you might want to:
    # 1. Blacklist the token
    # 2. Clear server-side session
    # 3. Log the logout event
    return {"message": "Successfully logged out"}
