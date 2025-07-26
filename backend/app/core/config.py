"""Configuration management for Movie Mood Matcher."""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Movie Mood Matcher"
    app_version: str = "0.1.0"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: Optional[str] = None
    
    # Redis
    redis_url: Optional[str] = None
    
    # External APIs
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    omdb_api_key: Optional[str] = None
    omdb_base_url: str = "http://www.omdbapi.com/"
    
    # AI/LLM Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    embedding_model: str = "text-embedding-ada-002"
    
    # Vector Database
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "movie-embeddings"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create global settings instance
settings = Settings()
