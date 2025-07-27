"""User preferences model for personalization"""
from sqlalchemy import Column, DateTime, ForeignKey, JSON
from app.database.types import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.config import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), ForeignKey("users.id"), unique=True, nullable=False)
    favorite_genres = Column(JSON, default=list)  # List of genre IDs
    watched_items = Column(JSON, default=list)  # List of {tmdb_id, type, rating, timestamp}
    preferences = Column(JSON, default=dict)  # General preferences like language, region, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id})>"
