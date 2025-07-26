# Movie Mood Matcher - Deployment Guide

## Deploying to Railway

### Prerequisites
1. Railway account (sign up at railway.app)
2. GitHub repository with your code
3. API keys ready (but NOT in your repository)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `movie-mood-matcher` repository
5. Railway will detect the configuration and start deployment

### Step 3: Set Environment Variables

In Railway dashboard, go to your service's Variables tab and add:

```env
# Application Settings
APP_NAME=Movie Mood Matcher
APP_VERSION=0.1.0
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Security (generate a new secret key!)
SECRET_KEY=your-production-secret-key-generate-a-new-one
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (Railway provides this)
DATABASE_URL=<Railway will provide this>

# External APIs (your actual keys)
TMDB_API_KEY=<your-tmdb-api-key>
TMDB_BASE_URL=https://api.themoviedb.org/3
OPENAI_API_KEY=<your-openai-api-key>
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-ada-002

# CORS (update with your Railway domain)
ALLOWED_ORIGINS=["https://your-app.up.railway.app"]

# Optional APIs
OMDB_API_KEY=<your-omdb-api-key-if-you-have-one>
REDIS_URL=<if-you-add-redis-service>
```

### Step 4: Add PostgreSQL Database

1. In Railway dashboard, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically inject DATABASE_URL

### Step 5: Update Frontend API URL

After deployment, update your frontend to use the production API:

1. In Railway, find your app's URL
2. Set a new environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
   ```

### Security Best Practices

1. **Never commit API keys** to your repository
2. **Use environment variables** for all sensitive data
3. **Generate new SECRET_KEY** for production
4. **Enable HTTPS** (Railway does this automatically)
5. **Set DEBUG=False** in production

### Monitoring

Railway provides:
- Deployment logs
- Runtime logs
- Metrics dashboard
- Automatic HTTPS
- Auto-scaling

### Custom Domain (Optional)

1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

## Alternative: Deploy Backend and Frontend Separately

If you prefer to deploy frontend on Vercel:

1. Deploy backend to Railway (Python/FastAPI only)
2. Deploy frontend to Vercel
3. Update NEXT_PUBLIC_API_URL to point to Railway backend
4. Update CORS settings to include Vercel domain
