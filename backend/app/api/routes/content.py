"""Content API routes for detailed movie/TV information."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ...services.tmdb_client import TMDBClient
from ...schemas.recommendation import ContentDetail, MediaType

router = APIRouter()


async def get_tmdb_client() -> TMDBClient:
    """Get TMDB client instance."""
    return TMDBClient()


@router.get("/movie/{movie_id}")
async def get_movie_details(
    movie_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific movie.
    """
    try:
        async with client:
            return await client.get_movie_details(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tv/{tv_id}")
async def get_tv_details(
    tv_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific TV show.
    """
    try:
        async with client:
            return await client.get_tv_details(tv_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_content(
    query: str,
    media_type: MediaType = MediaType.ALL,
    page: int = 1,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Search for movies and TV shows.
    """
    try:
        async with client:
            if media_type == MediaType.MOVIE:
                return await client.search_movies(query, page)
            elif media_type == MediaType.TV:
                return await client.search_tv(query, page)
            else:
                return await client.search_multi(query, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/movie/{movie_id}/similar")
async def get_similar_movies(
    movie_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get movies similar to a specific movie.
    """
    try:
        async with client:
            return await client.get_similar_movies(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tv/{tv_id}/similar")
async def get_similar_tv(
    tv_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get TV shows similar to a specific show.
    """
    try:
        async with client:
            return await client.get_similar_tv(tv_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/movie/{movie_id}/recommendations")
async def get_movie_recommendations(
    movie_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get movie recommendations based on a specific movie.
    """
    try:
        async with client:
            return await client.get_movie_recommendations(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tv/{tv_id}/recommendations")
async def get_tv_recommendations(
    tv_id: int,
    client: TMDBClient = Depends(get_tmdb_client)
) -> Dict[str, Any]:
    """
    Get TV show recommendations based on a specific show.
    """
    try:
        async with client:
            return await client.get_tv_recommendations(tv_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
