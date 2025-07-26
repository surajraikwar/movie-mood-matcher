export interface Movie {
  id: number;
  title: string;
  overview?: string;
  poster_path?: string;
  backdrop_path?: string;
  media_type: 'movie';
  vote_average: number;
  vote_count: number;
  popularity: number;
  release_date?: string;
  runtime?: number;
  genres?: Genre[];
}

export interface TVShow {
  id: number;
  title: string;
  overview?: string;
  poster_path?: string;
  backdrop_path?: string;
  media_type: 'tv';
  vote_average: number;
  vote_count: number;
  popularity: number;
  first_air_date?: string;
  last_air_date?: string;
  number_of_seasons?: number;
  number_of_episodes?: number;
  genres?: Genre[];
}

export type Content = Movie | TVShow;

export interface Genre {
  id: number;
  name: string;
}

export interface ContentRecommendation {
  content: Content;
  relevance_score: number;
  explanation: string;
  mood_match?: number;
  reasons: string[];
}

export interface RecommendationResponse {
  query: string;
  total_results: number;
  page: number;
  total_pages: number;
  recommendations: ContentRecommendation[];
  filters_applied?: Record<string, any>;
  processing_time: number;
}

export interface RecommendationQuery {
  query: string;
  media_type?: 'movie' | 'tv' | 'all';
  filters?: Record<string, any>;
  page?: number;
  limit?: number;
}

export interface MoodQuery {
  mood: string;
  energy_level: number;
  time_available?: number;
  preferences?: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  recommendations?: ContentRecommendation[];
}

export interface UserPreferences {
  favoriteGenres: number[];
  dislikedGenres: number[];
  preferredDecades: number[];
  watchHistory: number[];
}
