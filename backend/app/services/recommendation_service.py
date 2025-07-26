"""Recommendation service for processing natural language queries and providing movie/TV recommendations."""

import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import time
from loguru import logger

from ..schemas.recommendation import (
    RecommendationQuery,
    RecommendationResponse,
    ContentRecommendation,
    ContentBase,
    MediaType,
    Movie,
    TVShow
)
from .tmdb_client import TMDBClient


class RecommendationService:
    """Service for generating movie and TV show recommendations."""
    
    # Mood to genre mapping
    MOOD_GENRE_MAP = {
        "happy": [35, 10749, 16],  # Comedy, Romance, Animation
        "sad": [18, 10749],  # Drama, Romance
        "excited": [28, 12, 878],  # Action, Adventure, Sci-Fi
        "scared": [27, 53],  # Horror, Thriller
        "relaxed": [35, 10751, 99],  # Comedy, Family, Documentary
        "romantic": [10749, 18],  # Romance, Drama
        "adventurous": [12, 28, 14],  # Adventure, Action, Fantasy
        "thoughtful": [18, 9648, 878],  # Drama, Mystery, Sci-Fi
        "nostalgic": [10751, 16, 35],  # Family, Animation, Comedy
        "angry": [28, 80, 53],  # Action, Crime, Thriller
    }
    
    # Keywords that indicate specific preferences
    PREFERENCE_KEYWORDS = {
        "funny": [35],  # Comedy
        "scary": [27],  # Horror
        "action": [28],  # Action
        "romantic": [10749],  # Romance
        "mystery": [9648],  # Mystery
        "thriller": [53],  # Thriller
        "drama": [18],  # Drama
        "family": [10751],  # Family
        "animated": [16],  # Animation
        "documentary": [99],  # Documentary
        "crime": [80],  # Crime
        "fantasy": [14],  # Fantasy
        "sci-fi": [878],  # Science Fiction
        "historical": [36],  # History
        "war": [10752],  # War
        "western": [37],  # Western
        "music": [10402],  # Music
    }
    
    # Time-based recommendations
    RUNTIME_PREFERENCES = {
        "quick": (0, 30),  # Short content
        "short": (30, 90),  # Short movies/episodes
        "standard": (90, 150),  # Standard length
        "long": (150, 300),  # Long movies
        "binge": (30, 60),  # TV episodes for binging
    }
    
    def __init__(self):
        self.tmdb_client = TMDBClient()
        
    async def get_recommendations(
        self,
        query: RecommendationQuery
    ) -> RecommendationResponse:
        """Get recommendations based on natural language query."""
        start_time = time.time()
        
        # Parse the query to extract intent and filters
        parsed_query = self._parse_query(query.query)
        filters = self._build_filters(parsed_query, query.filters)
        
        # Get content from TMDB
        async with self.tmdb_client:
            results = await self._fetch_content(
                parsed_query,
                filters,
                query.media_type,
                query.page
            )
        
        # Process and rank results
        recommendations = self._process_results(
            results,
            parsed_query,
            query.limit
        )
        
        # Build response
        processing_time = time.time() - start_time
        
        return RecommendationResponse(
            query=query.query,
            total_results=results.get("total_results", 0),
            page=query.page,
            total_pages=results.get("total_pages", 1),
            recommendations=recommendations,
            filters_applied=filters,
            processing_time=processing_time
        )
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query to extract intent and preferences."""
        query_lower = query.lower()
        
        parsed = {
            "original": query,
            "genres": [],
            "keywords": [],
            "mood": None,
            "time_preference": None,
            "year_preference": None,
            "rating_preference": None,
            "specific_mentions": [],
        }
        
        # Extract mood
        for mood, genres in self.MOOD_GENRE_MAP.items():
            if mood in query_lower:
                parsed["mood"] = mood
                parsed["genres"].extend(genres)
                break
        
        # Extract genre preferences
        for keyword, genres in self.PREFERENCE_KEYWORDS.items():
            if keyword in query_lower:
                parsed["genres"].extend(genres)
                parsed["keywords"].append(keyword)
        
        # Extract time preferences
        for time_key, _ in self.RUNTIME_PREFERENCES.items():
            if time_key in query_lower:
                parsed["time_preference"] = time_key
                break
        
        # Extract year preferences
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', query)
        if year_match:
            parsed["year_preference"] = int(year_match.group())
        
        # Extract rating preferences
        if "highly rated" in query_lower or "best" in query_lower:
            parsed["rating_preference"] = "high"
        elif "underrated" in query_lower:
            parsed["rating_preference"] = "underrated"
        
        # Extract specific movie/show mentions (e.g., "like Breaking Bad")
        like_pattern = r'like\s+([A-Z][A-Za-z\s]+?)(?:\s+but|$)'
        like_matches = re.findall(like_pattern, query, re.IGNORECASE)
        if like_matches:
            parsed["specific_mentions"] = [match.strip() for match in like_matches]
        
        # Remove duplicates from genres
        parsed["genres"] = list(set(parsed["genres"]))
        
        return parsed
    
    def _build_filters(
        self,
        parsed_query: Dict[str, Any],
        user_filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build TMDB API filters from parsed query and user filters."""
        filters = {}
        
        # Add genre filters
        if parsed_query["genres"]:
            filters["with_genres"] = ",".join(map(str, parsed_query["genres"]))
        
        # Add time-based filters
        if parsed_query["time_preference"]:
            min_runtime, max_runtime = self.RUNTIME_PREFERENCES[parsed_query["time_preference"]]
            filters["with_runtime_gte"] = min_runtime
            filters["with_runtime_lte"] = max_runtime
        
        # Add year filters
        if parsed_query["year_preference"]:
            year = parsed_query["year_preference"]
            filters["primary_release_date_gte"] = f"{year}-01-01"
            filters["primary_release_date_lte"] = f"{year}-12-31"
        
        # Add rating filters
        if parsed_query["rating_preference"] == "high":
            filters["vote_average_gte"] = 7.5
            filters["vote_count_gte"] = 100
        elif parsed_query["rating_preference"] == "underrated":
            filters["vote_average_gte"] = 6.5
            filters["vote_count_gte"] = 50
            filters["vote_count_lte"] = 1000
        
        # Merge with user-provided filters
        if user_filters:
            filters.update(user_filters)
        
        return filters
    
    async def _fetch_content(
        self,
        parsed_query: Dict[str, Any],
        filters: Dict[str, Any],
        media_type: MediaType,
        page: int
    ) -> Dict[str, Any]:
        """Fetch content from TMDB based on parsed query and filters."""
        # If specific content is mentioned, search for it first
        if parsed_query["specific_mentions"]:
            search_query = " ".join(parsed_query["specific_mentions"])
            if media_type == MediaType.MOVIE:
                return await self.tmdb_client.search_movies(search_query, page)
            elif media_type == MediaType.TV:
                return await self.tmdb_client.search_tv(search_query, page)
            else:
                return await self.tmdb_client.search_multi(search_query, page)
        
        # Otherwise, use discover endpoints
        if media_type == MediaType.MOVIE:
            return await self.tmdb_client.discover_movies(page=page, **filters)
        elif media_type == MediaType.TV:
            return await self.tmdb_client.discover_tv(page=page, **filters)
        else:
            # For "all" media type, fetch both and combine
            movies = await self.tmdb_client.discover_movies(page=page, **filters)
            tv = await self.tmdb_client.discover_tv(page=page, **filters)
            
            # Combine results
            combined_results = movies.get("results", []) + tv.get("results", [])
            
            # Add media_type to each result
            for movie in movies.get("results", []):
                movie["media_type"] = "movie"
            for show in tv.get("results", []):
                show["media_type"] = "tv"
                show["title"] = show.get("name", "")  # Normalize title field
            
            return {
                "results": combined_results,
                "total_results": movies.get("total_results", 0) + tv.get("total_results", 0),
                "total_pages": max(movies.get("total_pages", 1), tv.get("total_pages", 1)),
                "page": page
            }
    
    def _process_results(
        self,
        results: Dict[str, Any],
        parsed_query: Dict[str, Any],
        limit: int
    ) -> List[ContentRecommendation]:
        """Process and rank TMDB results into recommendations."""
        recommendations = []
        
        for item in results.get("results", [])[:limit]:
            # Create content object
            if item.get("media_type") == "tv" or "first_air_date" in item:
                content = TVShow(
                    id=item["id"],
                    title=item.get("name", item.get("title", "")),
                    overview=item.get("overview"),
                    poster_path=item.get("poster_path"),
                    backdrop_path=item.get("backdrop_path"),
                    vote_average=item.get("vote_average", 0),
                    vote_count=item.get("vote_count", 0),
                    popularity=item.get("popularity", 0),
                    first_air_date=item.get("first_air_date"),
                    genres=item.get("genres", [])
                )
            else:
                content = Movie(
                    id=item["id"],
                    title=item.get("title", ""),
                    overview=item.get("overview"),
                    poster_path=item.get("poster_path"),
                    backdrop_path=item.get("backdrop_path"),
                    vote_average=item.get("vote_average", 0),
                    vote_count=item.get("vote_count", 0),
                    popularity=item.get("popularity", 0),
                    release_date=item.get("release_date"),
                    runtime=item.get("runtime"),
                    genres=item.get("genres", [])
                )
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance(item, parsed_query)
            
            # Generate explanation
            explanation, reasons = self._generate_explanation(item, parsed_query)
            
            recommendation = ContentRecommendation(
                content=content,
                relevance_score=relevance_score,
                explanation=explanation,
                reasons=reasons
            )
            
            recommendations.append(recommendation)
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return recommendations
    
    def _calculate_relevance(self, item: Dict[str, Any], parsed_query: Dict[str, Any]) -> float:
        """Calculate relevance score for a content item."""
        score = 0.5  # Base score
        
        # Genre match
        item_genres = [g["id"] for g in item.get("genres", [])]
        if not item_genres and "genre_ids" in item:
            item_genres = item["genre_ids"]
            
        genre_overlap = len(set(parsed_query["genres"]) & set(item_genres))
        if genre_overlap > 0:
            score += 0.2 * (genre_overlap / len(parsed_query["genres"]))
        
        # Rating factor
        vote_average = item.get("vote_average", 0)
        if vote_average > 7.5:
            score += 0.1
        elif vote_average > 6.5:
            score += 0.05
        
        # Popularity factor
        popularity = item.get("popularity", 0)
        if popularity > 100:
            score += 0.1
        elif popularity > 50:
            score += 0.05
        
        # Mood alignment (if mood was specified)
        if parsed_query["mood"] and genre_overlap > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_explanation(
        self,
        item: Dict[str, Any],
        parsed_query: Dict[str, Any]
    ) -> Tuple[str, List[str]]:
        """Generate explanation for why this content was recommended."""
        reasons = []
        
        # Genre matches
        item_genres = [g["id"] for g in item.get("genres", [])]
        if not item_genres and "genre_ids" in item:
            item_genres = item["genre_ids"]
            
        genre_overlap = set(parsed_query["genres"]) & set(item_genres)
        if genre_overlap:
            genre_names = [k for k, v in self.PREFERENCE_KEYWORDS.items() 
                          if any(g in v for g in genre_overlap)]
            if genre_names:
                reasons.append(f"Matches your preference for {', '.join(genre_names)}")
        
        # Rating
        vote_average = item.get("vote_average", 0)
        if vote_average > 8:
            reasons.append(f"Highly rated ({vote_average}/10)")
        elif vote_average > 7:
            reasons.append(f"Well-rated ({vote_average}/10)")
        
        # Mood
        if parsed_query["mood"]:
            reasons.append(f"Good for when you're feeling {parsed_query['mood']}")
        
        # Time preference
        if parsed_query["time_preference"] and "runtime" in item:
            runtime = item["runtime"]
            min_time, max_time = self.RUNTIME_PREFERENCES[parsed_query["time_preference"]]
            if min_time <= runtime <= max_time:
                reasons.append(f"Fits your time preference ({runtime} minutes)")
        
        # Create explanation
        title = item.get("title", item.get("name", "This content"))
        if reasons:
            explanation = f"{title} - {reasons[0]}"
        else:
            explanation = f"{title} might interest you"
        
        return explanation, reasons
