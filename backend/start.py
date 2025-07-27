#!/usr/bin/env python
"""Startup script for the backend with error handling."""

import os
import sys
import traceback

print("=== Starting Movie Mood Matcher Backend ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

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
try:
    import uvicorn
    print("Successfully imported uvicorn")
except Exception as e:
    print(f"ERROR importing uvicorn: {e}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting server on port {port}")
        print("Attempting to import app.main...")
        
        # Test import first
        from app.main import app
        print("Successfully imported app")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"ERROR starting server: {e}")
        traceback.print_exc()
        sys.exit(1)
