"""Pydantic schemas for recommendation-related models."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MediaType(str, Enum):
    """Media type enumeration."""
    MOVIE = "movie"
    TV = "tv"
    ALL = "all"


class SortBy(str, Enum):
    """Sorting options."""
    POPULARITY_DESC = "popularity.desc"
    POPULARITY_ASC = "popularity.asc"
    VOTE_AVERAGE_DESC = "vote_average.desc"
    VOTE_AVERAGE_ASC = "vote_average.asc"
    RELEASE_DATE_DESC = "release_date.desc"
    RELEASE_DATE_ASC = "release_date.asc"


class ContentBase(BaseModel):
    """Base model for movie/TV content."""
    id: int
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    media_type: MediaType
    vote_average: float = Field(ge=0, le=10)
    vote_count: int = Field(ge=0)
    popularity: float = Field(ge=0)
    
    @property
    def poster_url(self) -> Optional[str]:
        """Get full poster URL."""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self) -> Optional[str]:
        """Get full backdrop URL."""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None


class Movie(ContentBase):
    """Movie model."""
    media_type: MediaType = MediaType.MOVIE
    release_date: Optional[str] = None
    runtime: Optional[int] = None
    genres: List[Dict[str, Any]] = []
    
    
class TVShow(ContentBase):
    """TV Show model."""
    media_type: MediaType = MediaType.TV
    first_air_date: Optional[str] = None
    last_air_date: Optional[str] = None
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None
    genres: List[Dict[str, Any]] = []
    

class RecommendationQuery(BaseModel):
    """Query model for recommendations."""
    query: str = Field(..., min_length=1, description="Natural language query")
    media_type: MediaType = MediaType.ALL
    filters: Optional[Dict[str, Any]] = None
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    

class RecommendationFilters(BaseModel):
    """Filters for recommendation queries."""
    genres: Optional[List[int]] = None
    min_rating: Optional[float] = Field(None, ge=0, le=10)
    max_rating: Optional[float] = Field(None, ge=0, le=10)
    min_year: Optional[int] = Field(None, ge=1900)
    max_year: Optional[int] = Field(None, le=2100)
    min_runtime: Optional[int] = Field(None, ge=0)
    max_runtime: Optional[int] = Field(None, ge=0)
    keywords: Optional[List[str]] = None
    cast: Optional[List[str]] = None
    sort_by: SortBy = SortBy.POPULARITY_DESC
    

class MoodQuery(BaseModel):
    """Query based on mood/emotion."""
    mood: str = Field(..., description="User's current mood")
    energy_level: int = Field(5, ge=1, le=10, description="Energy level from 1-10")
    time_available: Optional[int] = Field(None, description="Time available in minutes")
    preferences: Optional[Dict[str, Any]] = None
    

class ContentRecommendation(BaseModel):
    """Recommendation response model."""
    content: ContentBase
    relevance_score: float = Field(ge=0, le=1)
    explanation: str
    mood_match: Optional[float] = Field(None, ge=0, le=1)
    reasons: List[str] = []
    

class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    query: str
    total_results: int
    page: int
    total_pages: int
    recommendations: List[ContentRecommendation]
    filters_applied: Optional[Dict[str, Any]] = None
    processing_time: float
    

class GenreResponse(BaseModel):
    """Genre information."""
    id: int
    name: str
    

class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    results: List[ContentBase]
    total_results: int
    page: int
    total_pages: int
    

class ContentDetail(ContentBase):
    """Detailed content information."""
    genres: List[GenreResponse]
    production_companies: List[Dict[str, Any]] = []
    cast: List[Dict[str, Any]] = []
    crew: List[Dict[str, Any]] = []
    keywords: List[Dict[str, Any]] = []
    videos: List[Dict[str, Any]] = []
    recommendations: List[ContentBase] = []
    similar: List[ContentBase] = []
    external_ids: Optional[Dict[str, Any]] = None
    

class UserPreference(BaseModel):
    """User preference model."""
    user_id: str
    favorite_genres: List[int] = []
    favorite_keywords: List[str] = []
    disliked_genres: List[int] = []
    preferred_runtime: Optional[Dict[str, int]] = None
    preferred_decades: List[int] = []
    mood_history: List[Dict[str, Any]] = []
    watch_history: List[int] = []
    

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
