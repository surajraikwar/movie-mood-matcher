"""Recommendation API routes."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any

from ...services.enhanced_recommendation_service import EnhancedRecommendationService as RecommendationService
from ...schemas.recommendation import (
    RecommendationQuery,
    RecommendationResponse,
    MoodQuery,
    MediaType
)

router = APIRouter()

# Dependency to get recommendation service
async def get_recommendation_service() -> RecommendationService:
    """Get recommendation service instance."""
    return RecommendationService()


@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    query: RecommendationQuery,
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    Get movie/TV recommendations based on natural language query.
    
    Examples:
    - "I want something funny and light-hearted"
    - "Show me action movies from the 90s"
    - "I'm looking for a thriller series like Breaking Bad"
    """
    try:
        return await service.get_recommendations(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mood", response_model=RecommendationResponse)
async def get_mood_recommendations(
    mood_query: MoodQuery,
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    Get recommendations based on current mood and energy level.
    """
    # Convert mood query to recommendation query
    query_text = f"I'm feeling {mood_query.mood}"
    
    if mood_query.energy_level < 3:
        query_text += " and tired"
    elif mood_query.energy_level > 7:
        query_text += " and energetic"
    
    if mood_query.time_available:
        if mood_query.time_available < 60:
            query_text += ", something short"
        elif mood_query.time_available < 120:
            query_text += ", standard length"
        else:
            query_text += ", I have plenty of time"
    
    recommendation_query = RecommendationQuery(
        query=query_text,
        media_type=MediaType.ALL,
        filters=mood_query.preferences
    )
    
    try:
        return await service.get_recommendations(recommendation_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending", response_model=RecommendationResponse)
async def get_trending_recommendations(
    media_type: MediaType = MediaType.ALL,
    time_window: str = "week",
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    Get trending movies and TV shows.
    
    Parameters:
    - media_type: Filter by movie, tv, or all
    - time_window: "day" or "week"
    """
    # Create a query for trending content
    recommendation_query = RecommendationQuery(
        query=f"trending {media_type.value} this {time_window}",
        media_type=media_type
    )
    
    try:
        return await service.get_recommendations(recommendation_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/popular", response_model=RecommendationResponse)
async def get_popular_recommendations(
    media_type: MediaType = MediaType.ALL,
    page: int = 1,
    service: RecommendationService = Depends(get_recommendation_service)
) -> RecommendationResponse:
    """
    Get popular movies and TV shows.
    """
    recommendation_query = RecommendationQuery(
        query=f"popular {media_type.value}",
        media_type=media_type,
        page=page
    )
    
    try:
        return await service.get_recommendations(recommendation_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
