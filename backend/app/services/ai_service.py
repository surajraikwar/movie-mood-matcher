"""AI Service for natural language chat and movie recommendations"""
import asyncio
from typing import AsyncGenerator, List, Optional
import openai
from openai import AsyncOpenAI
import json

from app.core.config import settings
from app.services.tmdb_client import TMDBClient
from app.models.chat import Message


class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.tmdb_client = TMDBClient()
        
    async def generate_streaming_response(
        self,
        user_message: str,
        chat_history: List[Message]
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response for user message"""
        
        # Build conversation history
        messages = [
            {
                "role": "system",
                "content": """You are StreamSage AI, an intelligent movie and TV show recommendation assistant. 
                You help users discover content based on their preferences, moods, and interests.
                You can:
                1. Recommend movies and TV shows based on mood, genre, or similarity to other content
                2. Provide detailed information about movies and shows
                3. Explain why certain recommendations match user preferences
                4. Engage in natural conversation about entertainment
                
                Always be helpful, conversational, and provide specific recommendations with reasons.
                When recommending content, include ratings, genres, and brief descriptions.
                Use the TMDB database to fetch real movie and show information when needed."""
            }
        ]
        
        # Add chat history
        for msg in chat_history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Check if the message is asking for recommendations
            if self._is_recommendation_query(user_message):
                # Extract search parameters
                search_params = await self._extract_search_params(user_message)
                
                # Fetch recommendations from TMDB
                recommendations = await self._get_recommendations(search_params)
                
                # Create enhanced prompt with real data
                enhanced_message = f"{user_message}\n\nAvailable recommendations from database: {json.dumps(recommendations[:5])}"
                messages[-1]["content"] = enhanced_message
            
            # Generate streaming response
            stream = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=1000
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _is_recommendation_query(self, message: str) -> bool:
        """Check if the message is asking for recommendations"""
        recommendation_keywords = [
            "recommend", "suggest", "show me", "find", "looking for",
            "what should i watch", "something like", "similar to",
            "mood", "feel like", "want to watch", "any good"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in recommendation_keywords)
    
    async def _extract_search_params(self, message: str) -> dict:
        """Extract search parameters from natural language query"""
        # This is a simplified version - in production, you'd use NLP
        params = {}
        
        # Check for genres
        genres = ["action", "comedy", "drama", "horror", "romance", "thriller", "sci-fi", "fantasy"]
        for genre in genres:
            if genre in message.lower():
                params["genre"] = genre
                break
        
        # Check for mood-based keywords
        if any(word in message.lower() for word in ["happy", "uplifting", "feel good"]):
            params["mood"] = "happy"
        elif any(word in message.lower() for word in ["sad", "emotional", "cry"]):
            params["mood"] = "emotional"
        elif any(word in message.lower() for word in ["excited", "action", "thrilling"]):
            params["mood"] = "exciting"
        
        # Check for specific movie/show mentions
        if "like" in message.lower() or "similar to" in message.lower():
            # Extract movie name (simplified)
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["like", "similar"] and i + 1 < len(words):
                    params["similar_to"] = " ".join(words[i+1:]).strip(".,!?")
                    break
        
        return params
    
    async def _get_recommendations(self, params: dict) -> List[dict]:
        """Get movie/show recommendations based on parameters"""
        recommendations = []
        
        try:
            if "similar_to" in params:
                # Search for the movie/show first
                search_response = await self.tmdb_client.search_multi(params["similar_to"])
                search_results = search_response.get("results", [])
                if search_results:
                    # Get similar content
                    similar = await self.tmdb_client.get_similar(
                        search_results[0]["id"],
                        search_results[0].get("media_type", "movie")
                    )
                    recommendations.extend(similar[:5])
            
            elif "genre" in params:
                # Get movies by genre
                genre_map = {
                    "action": 28,
                    "comedy": 35,
                    "drama": 18,
                    "horror": 27,
                    "romance": 10749,
                    "thriller": 53,
                    "sci-fi": 878,
                    "fantasy": 14
                }
                genre_id = genre_map.get(params["genre"])
                if genre_id:
                    movies_response = await self.tmdb_client.discover_movies(with_genres=str(genre_id))
                    movies = movies_response.get("results", [])
                    recommendations.extend(movies[:5])
            
            else:
                # Get popular/trending content
                trending_response = await self.tmdb_client.get_trending()
                trending = trending_response.get("results", [])
                recommendations.extend(trending[:5])
                
        except Exception as e:
            print(f"Error fetching recommendations: {e}")
        
        return recommendations
