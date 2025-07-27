"""Enhanced recommendation service with better similarity matching and genre handling."""

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


class EnhancedRecommendationService:
    """Enhanced service for generating movie and TV show recommendations."""
    
    # Genre ID mapping
    GENRE_MAP = {
        # Movies
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "science fiction": 878,
        "sci-fi": 878,
        "tv movie": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37,
        # Additional keywords
        "space": 878,
        "alien": 878,
        "aliens": 878,
        "superhero": [28, 14, 878],  # Action + Fantasy + Sci-Fi
        "zombie": [27, 28],  # Horror + Action
        "vampire": [27, 14],  # Horror + Fantasy
    }
    
    # Mood to genre mapping
    MOOD_GENRE_MAP = {
        "happy": [35, 10749, 16],  # Comedy, Romance, Animation
        "feel-good": [35, 10751, 10749],  # Comedy, Family, Romance
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
        
        # Get content based on query type
        async with self.tmdb_client:
            if parsed_query["is_similarity_query"] and parsed_query["specific_mentions"]:
                # Handle "like X" queries by finding similar content
                results = await self._get_similar_content(
                    parsed_query["specific_mentions"][0],
                    query.media_type,
                    query.page
                )
            else:
                # Handle genre/mood based queries
                filters = self._build_filters(parsed_query, query.filters)
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
            filters_applied=parsed_query.get("filters", {}),
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
            "is_similarity_query": False,
            "specific_mentions": [],
            "filters": {}
        }
        
        # Check if it's a similarity query (like, similar to, etc.)
        similarity_patterns = [
            r'(?:shows?|movies?|something)?\s*like\s+(.+?)(?:\s*$|\s*but)',
            r'similar\s+to\s+(.+?)(?:\s*$|\s*but)',
            r'(?:shows?|movies?)?\s*such\s+as\s+(.+?)(?:\s*$|\s*but)',
        ]
        
        for pattern in similarity_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                parsed["is_similarity_query"] = True
                parsed["specific_mentions"] = [match.group(1).strip()]
                break
        
        # Extract genres and keywords
        for keyword, genre_ids in self.GENRE_MAP.items():
            if keyword in query_lower:
                if isinstance(genre_ids, list):
                    parsed["genres"].extend(genre_ids)
                else:
                    parsed["genres"].append(genre_ids)
                parsed["keywords"].append(keyword)
        
        # Extract mood
        for mood, genres in self.MOOD_GENRE_MAP.items():
            if mood in query_lower:
                parsed["mood"] = mood
                parsed["genres"].extend(genres)
                break
        
        # Remove duplicates from genres
        parsed["genres"] = list(set(parsed["genres"]))
        
        # Extract other preferences
        if "highly rated" in query_lower or "best" in query_lower:
            parsed["filters"]["vote_average_gte"] = 7.5
            parsed["filters"]["vote_count_gte"] = 100
        
        if any(word in query_lower for word in ["new", "recent", "latest"]):
            current_year = datetime.now().year
            parsed["filters"]["primary_release_date_gte"] = f"{current_year - 2}-01-01"
        
        if "classic" in query_lower or "old" in query_lower:
            parsed["filters"]["primary_release_date_lte"] = "2000-01-01"
        
        return parsed
    
    async def _get_similar_content(
        self,
        title: str,
        media_type: MediaType,
        page: int
    ) -> Dict[str, Any]:
        """Get content similar to a specific movie or TV show."""
        # First, search for the mentioned content
        search_results = await self.tmdb_client.search_multi(title)
        
        if not search_results.get("results"):
            return {"results": [], "total_results": 0, "total_pages": 0}
        
        # Find the most relevant result
        target_item = None
        for item in search_results["results"]:
            if item.get("media_type") in ["movie", "tv"]:
                target_item = item
                break
        
        if not target_item:
            return {"results": [], "total_results": 0, "total_pages": 0}
        
        # Get similar content
        content_id = target_item["id"]
        content_type = target_item["media_type"]
        
        if content_type == "movie":
            similar = await self.tmdb_client.get_similar_movies(content_id)
            recommendations = await self.tmdb_client.get_movie_recommendations(content_id)
        else:
            similar = await self.tmdb_client.get_similar_tv(content_id)
            recommendations = await self.tmdb_client.get_tv_recommendations(content_id)
        
        # Combine and deduplicate results
        all_results = {}
        
        # Add similar content
        for item in similar.get("results", []):
            item["similarity_type"] = "similar"
            item["media_type"] = content_type
            all_results[item["id"]] = item
        
        # Add recommendations
        for item in recommendations.get("results", []):
            if item["id"] not in all_results:
                item["similarity_type"] = "recommended"
                item["media_type"] = content_type
                all_results[item["id"]] = item
        
        # Filter out the original item
        if content_id in all_results:
            del all_results[content_id]
        
        # Sort by vote average and popularity
        sorted_results = sorted(
            all_results.values(),
            key=lambda x: (x.get("vote_average", 0) * x.get("vote_count", 0) ** 0.5),
            reverse=True
        )
        
        return {
            "results": sorted_results[:20],  # Limit to top 20
            "total_results": len(sorted_results),
            "total_pages": 1,
            "original_title": target_item.get("title") or target_item.get("name"),
            "original_type": content_type
        }
    
    def _build_filters(
        self,
        parsed_query: Dict[str, Any],
        user_filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build TMDB API filters from parsed query and user filters."""
        filters = parsed_query.get("filters", {}).copy()
        
        # Add genre filters
        if parsed_query["genres"]:
            filters["with_genres"] = ",".join(map(str, parsed_query["genres"]))
        
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
        if media_type == MediaType.MOVIE:
            return await self.tmdb_client.discover_movies(page=page, **filters)
        elif media_type == MediaType.TV:
            return await self.tmdb_client.discover_tv(page=page, **filters)
        else:
            # For "all" media type, fetch both and combine
            movies = await self.tmdb_client.discover_movies(page=page, **filters)
            tv = await self.tmdb_client.discover_tv(page=page, **filters)
            
            # Add media_type to each result
            for movie in movies.get("results", []):
                movie["media_type"] = "movie"
            for show in tv.get("results", []):
                show["media_type"] = "tv"
                show["title"] = show.get("name", "")  # Normalize title field
            
            # Combine results
            combined_results = movies.get("results", []) + tv.get("results", [])
            
            # Sort by relevance (vote average * sqrt(vote count))
            combined_results.sort(
                key=lambda x: x.get("vote_average", 0) * (x.get("vote_count", 0) ** 0.5),
                reverse=True
            )
            
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
                    media_type="tv",
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
                    media_type="movie",
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
            explanation, reasons = self._generate_explanation(item, parsed_query, results)
            
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
        
        # For similarity queries, use different scoring
        if parsed_query["is_similarity_query"]:
            if item.get("similarity_type") == "similar":
                score = 0.9
            elif item.get("similarity_type") == "recommended":
                score = 0.8
        else:
            # Genre match
            item_genres = [g["id"] for g in item.get("genres", [])]
            if not item_genres and "genre_ids" in item:
                item_genres = item["genre_ids"]
                
            if parsed_query["genres"]:
                genre_overlap = len(set(parsed_query["genres"]) & set(item_genres))
                if genre_overlap > 0:
                    score += 0.3 * (genre_overlap / len(parsed_query["genres"]))
        
        # Rating factor
        vote_average = item.get("vote_average", 0)
        vote_count = item.get("vote_count", 0)
        
        if vote_average >= 8.0 and vote_count >= 100:
            score += 0.2
        elif vote_average >= 7.0 and vote_count >= 50:
            score += 0.1
        elif vote_average >= 6.0:
            score += 0.05
        
        return min(score, 1.0)
    
    def _generate_explanation(
        self,
        item: Dict[str, Any],
        parsed_query: Dict[str, Any],
        results: Dict[str, Any]
    ) -> Tuple[str, List[str]]:
        """Generate explanation for why this content was recommended."""
        reasons = []
        
        title = item.get("title") or item.get("name", "Unknown")
        vote_average = item.get("vote_average", 0)
        vote_count = item.get("vote_count", 0)
        
        # For similarity queries
        if parsed_query["is_similarity_query"] and results.get("original_title"):
            if item.get("similarity_type") == "similar":
                main_explanation = f"Similar to {results['original_title']}"
                reasons.append(f"Shares themes and style with {results['original_title']}")
            else:
                main_explanation = f"Fans of {results['original_title']} also enjoyed this"
                reasons.append(f"Recommended for viewers who liked {results['original_title']}")
        else:
            # For other queries
            if vote_average >= 8.0:
                main_explanation = f"{title} - Highly acclaimed ({vote_average:.1f}/10)"
                reasons.append(f"Exceptional rating of {vote_average:.1f}/10")
            elif vote_average >= 7.0:
                main_explanation = f"{title} - Well-received ({vote_average:.1f}/10)"
                reasons.append(f"Strong rating of {vote_average:.1f}/10")
            else:
                main_explanation = f"{title} matches your criteria"
            
            # Add mood/genre reasons
            if parsed_query["mood"]:
                reasons.append(f"Perfect for a {parsed_query['mood']} mood")
            
            if parsed_query["keywords"]:
                reasons.append(f"Features {', '.join(parsed_query['keywords'])} elements")
        
        # Add popularity reason
        if vote_count > 1000:
            reasons.append(f"Widely watched ({vote_count:,} ratings)")
        
        return main_explanation, reasons
