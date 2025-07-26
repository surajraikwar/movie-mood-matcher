"""Genre API routes."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ...services.tmdb_client import TMDBClient
from ...schemas.recommendation import GenreResponse, MediaType

router = APIRouter()


async def get_tmdb_client() -> TMDBClient:
    """Get TMDB client instance."""
    return TMDBClient()


@router.get("/movie", response_model=List[GenreResponse])
async def get_movie_genres(
    client: TMDBClient = Depends(get_tmdb_client)
) -> List[GenreResponse]:
    """
    Get list of movie genres.
    """
    try:
        async with client:
            genres = await client.get_genres("movie")
            return [GenreResponse(**genre) for genre in genres]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tv", response_model=List[GenreResponse])
async def get_tv_genres(
    client: TMDBClient = Depends(get_tmdb_client)
) -> List[GenreResponse]:
    """
    Get list of TV show genres.
    """
    try:
        async with client:
            genres = await client.get_genres("tv")
            return [GenreResponse(**genre) for genre in genres]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_genres(
    client: TMDBClient = Depends(get_tmdb_client)
) -> dict:
    """
    Get all genres for both movies and TV shows.
    """
    try:
        async with client:
            movie_genres = await client.get_genres("movie")
            tv_genres = await client.get_genres("tv")
            
            return {
                "movie_genres": [GenreResponse(**genre) for genre in movie_genres],
                "tv_genres": [GenreResponse(**genre) for genre in tv_genres]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
