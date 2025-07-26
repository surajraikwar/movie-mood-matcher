# 🎬 Movie Mood Matcher

An AI-powered movie and TV series recommendation system that understands natural language queries and provides personalized suggestions based on mood, preferences, and context.

## 🌟 Features

### Core Capabilities
- **Natural Language Interface**: Chat with AI to describe what you want to watch
- **Mood-Based Recommendations**: "I want something uplifting but not too cheesy"
- **Advanced Filtering**: Genre, runtime, release year, ratings, and more
- **Multi-Source Ratings**: Aggregated scores from TMDB, IMDB (via OMDb), and Rotten Tomatoes
- **Personalized Suggestions**: Learn from user preferences over time
- **Rich Media Integration**: Trailers, posters, cast information

### Unique Features
- **Mood Ring Selector**: Visual interface to select current mood
- **Plot Twist Meter**: AI-analyzed twist intensity (spoiler-free)
- **Binge-ability Score**: Predicts how addictive a TV show is
- **Group Watch**: Find content that satisfies multiple users
- **Similar But Different**: Discover content with shared DNA but fresh perspectives

## 🏗️ Architecture

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   React Frontend    │     │   FastAPI Backend   │     │   External APIs     │
│   Chat Interface    │────▶│   Recommendation    │────▶│   TMDB / OMDb       │
│   Rich UI Components│     │   Engine            │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                      │                             
                                      ▼                             
                            ┌─────────────────────┐     ┌─────────────────────┐
                            │    LLM Service      │     │   Vector Database   │
                            │  (OpenAI/Claude)    │     │   (Pinecone)        │
                            │  NLU Processing     │     │   Content Embeddings│
                            └─────────────────────┘     └─────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- TMDB API Key
- OMDb API Key (optional)
- OpenAI API Key
- Pinecone API Key (optional for MVP)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run the backend**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. **Run the frontend**
```bash
npm run dev
```

## 📖 Usage

### Example Queries
- "I want something like Breaking Bad but lighter and funnier"
- "Show me mind-bending sci-fi movies with great plot twists"
- "I'm in the mood for a feel-good series I can binge this weekend"
- "Find me critically acclaimed foreign thrillers from the last 5 years"

### API Endpoints

```bash
# Search for recommendations
POST /api/v1/recommend
{
  "query": "Dark comedy series with strong female leads",
  "filters": {
    "min_rating": 7.5,
    "max_runtime": 60,
    "genres": ["comedy", "drama"]
  }
}

# Get detailed information
GET /api/v1/content/{content_id}

# Save user preferences
POST /api/v1/users/{user_id}/preferences
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **LLM Integration**: LangChain + OpenAI
- **Vector Store**: Pinecone / Weaviate
- **Database**: PostgreSQL
- **Caching**: Redis
- **Task Queue**: Celery

### Frontend
- **Framework**: React + Next.js
- **UI Library**: Tailwind CSS + Shadcn/ui
- **State Management**: Zustand
- **API Client**: Axios + React Query
- **Chat UI**: Custom components

### External Services
- **TMDB API**: Primary movie/TV database
- **OMDb API**: IMDB and Rotten Tomatoes ratings
- **OpenAI**: Natural language understanding
- **Pinecone**: Vector similarity search

## 📊 Data Sources

- **TMDB**: Movie/TV metadata, cast, crew, images
- **OMDb**: IMDB ratings, Rotten Tomatoes scores
- **User Generated**: Preferences, watch history, ratings

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚧 Roadmap

### Phase 1: MVP ✅
- [x] Basic project structure
- [ ] TMDB API integration
- [ ] Simple chat interface
- [ ] Keyword-based recommendations

### Phase 2: AI Enhancement
- [ ] LLM integration for NLU
- [ ] Vector embeddings for content
- [ ] Semantic search
- [ ] Mood-based filtering

### Phase 3: Advanced Features
- [ ] Multi-source ratings
- [ ] User profiles
- [ ] Collaborative filtering
- [ ] Streaming availability

### Phase 4: Production
- [ ] Performance optimization
- [ ] Mobile responsive design
- [ ] Analytics dashboard
- [ ] A/B testing

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- TMDB for their comprehensive movie database API
- OpenAI for powerful language models
- The open-source community

---

Built with ❤️ for movie lovers who can never decide what to watch
