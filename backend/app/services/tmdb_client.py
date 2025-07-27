"""TMDB API client for fetching movie and TV show data."""

import httpx
from typing import Dict, List, Optional, Any
from loguru import logger
from ..core.config import settings


class TMDBClient:
    """Client for interacting with The Movie Database (TMDB) API."""
    
    def __init__(self):
        self.api_key = settings.tmdb_api_key
        self.base_url = settings.tmdb_base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the TMDB API."""
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"TMDB API error: {e}")
            raise
    
    async def search_multi(self, query: str, page: int = 1) -> Dict:
        """Search for movies, TV shows, and people."""
        return await self._make_request(
            "/search/multi",
            params={"query": query, "page": page}
        )
    
    async def search_movies(self, query: str, page: int = 1, **filters) -> Dict:
        """Search for movies with optional filters."""
        params = {
            "query": query,
            "page": page,
            "include_adult": filters.get("include_adult", False),
        }
        
        # Add optional filters
        if "year" in filters:
            params["year"] = filters["year"]
        if "language" in filters:
            params["language"] = filters["language"]
        if "region" in filters:
            params["region"] = filters["region"]
            
        return await self._make_request("/search/movie", params=params)
    
    async def search_tv(self, query: str, page: int = 1, **filters) -> Dict:
        """Search for TV shows."""
        params = {
            "query": query,
            "page": page,
            "include_adult": filters.get("include_adult", False),
        }
        
        if "first_air_date_year" in filters:
            params["first_air_date_year"] = filters["first_air_date_year"]
            
        return await self._make_request("/search/tv", params=params)
    
    async def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a movie."""
        return await self._make_request(
            f"/movie/{movie_id}",
            params={"append_to_response": "credits,videos,keywords,recommendations"}
        )
    
    async def get_tv_details(self, tv_id: int) -> Dict:
        """Get detailed information about a TV show."""
        return await self._make_request(
            f"/tv/{tv_id}",
            params={"append_to_response": "credits,videos,keywords,recommendations"}
        )
    
    async def discover_movies(self, **filters) -> Dict:
        """Discover movies based on various filters."""
        params = {
            "sort_by": filters.get("sort_by", "popularity.desc"),
            "page": filters.get("page", 1),
            "include_adult": filters.get("include_adult", False),
        }
        
        # Genre filters
        if "with_genres" in filters:
            params["with_genres"] = filters["with_genres"]
        if "without_genres" in filters:
            params["without_genres"] = filters["without_genres"]
            
        # Date filters
        if "primary_release_date_gte" in filters:
            params["primary_release_date.gte"] = filters["primary_release_date_gte"]
        if "primary_release_date_lte" in filters:
            params["primary_release_date.lte"] = filters["primary_release_date_lte"]
            
        # Rating filters
        if "vote_average_gte" in filters:
            params["vote_average.gte"] = filters["vote_average_gte"]
        if "vote_average_lte" in filters:
            params["vote_average.lte"] = filters["vote_average_lte"]
        if "vote_count_gte" in filters:
            params["vote_count.gte"] = filters["vote_count_gte"]
            
        # Runtime filters
        if "with_runtime_gte" in filters:
            params["with_runtime.gte"] = filters["with_runtime_gte"]
        if "with_runtime_lte" in filters:
            params["with_runtime.lte"] = filters["with_runtime_lte"]
            
        # Other filters
        if "with_keywords" in filters:
            params["with_keywords"] = filters["with_keywords"]
        if "with_cast" in filters:
            params["with_cast"] = filters["with_cast"]
        if "with_crew" in filters:
            params["with_crew"] = filters["with_crew"]
        if "with_companies" in filters:
            params["with_companies"] = filters["with_companies"]
            
        return await self._make_request("/discover/movie", params=params)
    
    async def discover_tv(self, **filters) -> Dict:
        """Discover TV shows based on various filters."""
        params = {
            "sort_by": filters.get("sort_by", "popularity.desc"),
            "page": filters.get("page", 1),
        }
        
        # Similar filters as movies but for TV
        if "with_genres" in filters:
            params["with_genres"] = filters["with_genres"]
        if "air_date_gte" in filters:
            params["air_date.gte"] = filters["air_date_gte"]
        if "air_date_lte" in filters:
            params["air_date.lte"] = filters["air_date_lte"]
        if "vote_average_gte" in filters:
            params["vote_average.gte"] = filters["vote_average_gte"]
            
        return await self._make_request("/discover/tv", params=params)
    
    async def get_genres(self, media_type: str = "movie") -> List[Dict]:
        """Get list of genres."""
        endpoint = f"/genre/{media_type}/list"
        response = await self._make_request(endpoint)
        return response.get("genres", [])
    
    async def get_trending(self, media_type: str = "all", time_window: str = "week") -> Dict:
        """Get trending movies, TV shows, or people."""
        endpoint = f"/trending/{media_type}/{time_window}"
        return await self._make_request(endpoint)
    
    async def get_popular_movies(self, page: int = 1) -> Dict:
        """Get popular movies."""
        return await self._make_request("/movie/popular", params={"page": page})
    
    async def get_popular_tv(self, page: int = 1) -> Dict:
        """Get popular TV shows."""
        return await self._make_request("/tv/popular", params={"page": page})
    
    async def get_movie_recommendations(self, movie_id: int) -> Dict:
        """Get movie recommendations based on a specific movie."""
        return await self._make_request(f"/movie/{movie_id}/recommendations")
    
    async def get_tv_recommendations(self, tv_id: int) -> Dict:
        """Get TV show recommendations based on a specific show."""
        return await self._make_request(f"/tv/{tv_id}/recommendations")
    
    async def get_similar_movies(self, movie_id: int) -> Dict:
        """Get similar movies."""
        return await self._make_request(f"/movie/{movie_id}/similar")
    
    async def get_similar_tv(self, tv_id: int) -> Dict:
        """Get similar TV shows."""
        return await self._make_request(f"/tv/{tv_id}/similar")
    
    async def search_keywords(self, query: str) -> List[Dict]:
        """Search for keywords."""
        response = await self._make_request(
            "/search/keyword",
            params={"query": query}
        )
        return response.get("results", [])
    
    async def get_similar(self, content_id: int, media_type: str) -> List[Dict]:
        """Get similar content based on media type."""
        if media_type == "movie":
            response = await self.get_similar_movies(content_id)
        else:
            response = await self.get_similar_tv(content_id)
        return response.get("results", [])
