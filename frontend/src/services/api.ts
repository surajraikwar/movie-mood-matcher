import axios from 'axios';
import type {
  RecommendationQuery,
  RecommendationResponse,
  MoodQuery,
  Genre,
  Content,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request/response interceptors for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const recommendationApi = {
  // Get recommendations based on natural language query
  getRecommendations: async (query: RecommendationQuery): Promise<RecommendationResponse> => {
    const response = await api.post('/api/v1/recommendations/', query);
    return response.data;
  },

  // Get mood-based recommendations
  getMoodRecommendations: async (moodQuery: MoodQuery): Promise<RecommendationResponse> => {
    const response = await api.post('/api/v1/recommendations/mood', moodQuery);
    return response.data;
  },

  // Get trending content
  getTrending: async (mediaType: 'movie' | 'tv' | 'all' = 'all', timeWindow: 'day' | 'week' = 'week'): Promise<RecommendationResponse> => {
    const response = await api.get('/api/v1/recommendations/trending', {
      params: { media_type: mediaType, time_window: timeWindow },
    });
    return response.data;
  },

  // Get popular content
  getPopular: async (mediaType: 'movie' | 'tv' | 'all' = 'all', page: number = 1): Promise<RecommendationResponse> => {
    const response = await api.get('/api/v1/recommendations/popular', {
      params: { media_type: mediaType, page },
    });
    return response.data;
  },
};

export const contentApi = {
  // Get movie details
  getMovieDetails: async (movieId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/movie/${movieId}`);
    return response.data;
  },

  // Get TV show details
  getTVDetails: async (tvId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/tv/${tvId}`);
    return response.data;
  },

  // Search content
  searchContent: async (query: string, mediaType: 'movie' | 'tv' | 'all' = 'all', page: number = 1): Promise<any> => {
    const response = await api.get('/api/v1/content/search', {
      params: { query, media_type: mediaType, page },
    });
    return response.data;
  },

  // Get similar movies
  getSimilarMovies: async (movieId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/movie/${movieId}/similar`);
    return response.data;
  },

  // Get similar TV shows
  getSimilarTV: async (tvId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/tv/${tvId}/similar`);
    return response.data;
  },

  // Get movie recommendations
  getMovieRecommendations: async (movieId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/movie/${movieId}/recommendations`);
    return response.data;
  },

  // Get TV recommendations
  getTVRecommendations: async (tvId: number): Promise<any> => {
    const response = await api.get(`/api/v1/content/tv/${tvId}/recommendations`);
    return response.data;
  },
};

export const genreApi = {
  // Get movie genres
  getMovieGenres: async (): Promise<Genre[]> => {
    const response = await api.get('/api/v1/genres/movie');
    return response.data;
  },

  // Get TV genres
  getTVGenres: async (): Promise<Genre[]> => {
    const response = await api.get('/api/v1/genres/tv');
    return response.data;
  },

  // Get all genres
  getAllGenres: async (): Promise<{ movie_genres: Genre[], tv_genres: Genre[] }> => {
    const response = await api.get('/api/v1/genres/all');
    return response.data;
  },
};
