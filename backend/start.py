#!/usr/bin/env python
"""Startup script for the backend with error handling."""

import os
import sys

# Set default environment variables if not set
defaults = {
    "APP_NAME": "Movie Mood Matcher",
    "APP_VERSION": "0.1.0",
    "DEBUG": "False",
    "API_HOST": "0.0.0.0",
    "API_PORT": "8000",
    "SECRET_KEY": "temporary-secret-key-replace-in-production",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "DATABASE_URL": "sqlite+aiosqlite:///./moviemoodmatcher.db",
    "TMDB_BASE_URL": "https://api.themoviedb.org/3",
    "OMDB_BASE_URL": "http://www.omdbapi.com/",
    "ALLOWED_ORIGINS": '["*"]',  # Allow all in development
    "LOG_LEVEL": "INFO",
}

# Apply defaults
for key, value in defaults.items():
    if key not in os.environ:
        os.environ[key] = value
        print(f"Warning: {key} not set, using default: {value}")

# Check for required API keys
if "TMDB_API_KEY" not in os.environ:
    print("ERROR: TMDB_API_KEY is required but not set!")
    print("Please set it in Railway environment variables")
    # Set a dummy value to allow startup
    os.environ["TMDB_API_KEY"] = "dummy-key-replace-me"

if "OPENAI_API_KEY" not in os.environ:
    print("Warning: OPENAI_API_KEY not set. AI features will be limited.")
    os.environ["OPENAI_API_KEY"] = "dummy-key-optional"

# Import and run uvicorn
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
