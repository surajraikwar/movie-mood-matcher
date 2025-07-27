import React from 'react';
import { motion } from 'framer-motion';
import { Star, Calendar, Clock, User, Film, Tv, TrendingUp, Info, PlayCircle, Heart, X } from 'lucide-react';
import Image from 'next/image';

// Utility function for className merging
const cn = (...classes: (string | undefined | null | false)[]) => classes.filter(Boolean).join(' ');

// Type definitions
export interface MediaItem {
  id: number;
  title?: string;
  name?: string;
  overview: string;
  poster_path?: string;
  backdrop_path?: string;
  release_date?: string;
  first_air_date?: string;
  vote_average: number;
  vote_count: number;
  media_type?: 'movie' | 'tv';
  genre_ids?: number[];
  runtime?: number;
  episode_run_time?: number[];
  popularity?: number;
}

export interface Actor {
  id: number;
  name: string;
  profile_path?: string;
  character?: string;
  known_for_department?: string;
  known_for?: MediaItem[];
  biography?: string;
  birthday?: string;
  place_of_birth?: string;
  popularity?: number;
}

export interface Genre {
  id: number;
  name: string;
}

// Genre mapping
const genreMap: Record<number, string> = {
  28: 'Action',
  12: 'Adventure',
  16: 'Animation',
  35: 'Comedy',
  80: 'Crime',
  99: 'Documentary',
  18: 'Drama',
  10751: 'Family',
  14: 'Fantasy',
  36: 'History',
  27: 'Horror',
  10402: 'Music',
  9648: 'Mystery',
  10749: 'Romance',
  878: 'Science Fiction',
  10770: 'TV Movie',
  53: 'Thriller',
  10752: 'War',
  37: 'Western',
};

// Helper function to get image URL
const getImageUrl = (path: string | undefined, size: string = 'w500') => {
  if (!path) return null;
  return `https://image.tmdb.org/t/p/${size}${path}`;
};

// Media Card Component (for movies and TV shows)
interface MediaCardProps {
  item: MediaItem;
  index?: number;
  onSelect?: (item: MediaItem) => void;
}

export const MediaCard: React.FC<MediaCardProps> = ({ item, index = 0, onSelect }) => {
  const title = item.title || item.name || 'Unknown';
  const releaseDate = item.release_date || item.first_air_date;
  const year = releaseDate ? new Date(releaseDate).getFullYear() : null;
  const rating = item.vote_average ? item.vote_average.toFixed(1) : 'N/A';
  const posterUrl = getImageUrl(item.poster_path);
  const isTV = item.media_type === 'tv' || !!item.first_air_date;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="group cursor-pointer"
      onClick={() => onSelect?.(item)}
      whileHover={{ y: -8, transition: { duration: 0.3 } }}
    >
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-b from-white/10 to-white/5 backdrop-blur-md border border-white/20 hover:border-white/40 transition-all duration-300 hover:shadow-2xl hover:shadow-cyan-500/20">
        <div className="aspect-[2/3] relative overflow-hidden bg-gray-900">
          {posterUrl ? (
            <Image
              src={posterUrl}
              alt={title}
              fill
              className="object-cover transition-transform duration-300 group-hover:scale-110"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              {isTV ? <Tv className="w-16 h-16 text-gray-600" /> : <Film className="w-16 h-16 text-gray-600" />}
            </div>
          )}
          
          {/* Rating Badge */}
          <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-sm rounded-full px-2 py-1 flex items-center gap-1">
            <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
            <span className="text-xs font-medium text-white">{rating}</span>
          </div>
          
          {/* Media Type Badge */}
          <div className="absolute top-2 left-2 bg-black/70 backdrop-blur-sm rounded-full px-2 py-1">
            {isTV ? (
              <Tv className="w-3 h-3 text-blue-400" />
            ) : (
              <Film className="w-3 h-3 text-purple-400" />
            )}
          </div>
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold text-white mb-1 line-clamp-1 group-hover:text-blue-400 transition-colors">
            {title}
          </h3>
          {year && (
            <div className="flex items-center gap-1 text-sm text-gray-400 mb-2">
              <Calendar className="w-3 h-3" />
              <span>{year}</span>
            </div>
          )}
          <p className="text-sm text-gray-300 line-clamp-2">{item.overview}</p>
          
          {/* Genres */}
          {item.genre_ids && item.genre_ids.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-3">
              {item.genre_ids.slice(0, 3).map((genreId) => (
                <span
                  key={genreId}
                  className="text-xs px-2 py-1 bg-gray-700/50 rounded-full text-gray-300"
                >
                  {genreMap[genreId] || 'Unknown'}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

// Actor Card Component
interface ActorCardProps {
  actor: Actor;
  index?: number;
  onSelect?: (actor: Actor) => void;
  showCharacter?: boolean;
}

export const ActorCard: React.FC<ActorCardProps> = ({ actor, index = 0, onSelect, showCharacter = true }) => {
  const profileUrl = getImageUrl(actor.profile_path, 'w185');
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      className="group cursor-pointer"
      onClick={() => onSelect?.(actor)}
    >
      <div className="relative overflow-hidden rounded-xl bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 hover:border-gray-600 transition-all duration-300 hover:shadow-xl">
        <div className="aspect-[3/4] relative overflow-hidden bg-gray-900">
          {profileUrl ? (
            <Image
              src={profileUrl}
              alt={actor.name}
              fill
              className="object-cover transition-transform duration-300 group-hover:scale-110"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <User className="w-16 h-16 text-gray-600" />
            </div>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold text-white mb-1 line-clamp-1 group-hover:text-blue-400 transition-colors">
            {actor.name}
          </h3>
          {showCharacter && actor.character && (
            <p className="text-sm text-gray-400 line-clamp-1">as {actor.character}</p>
          )}
          {actor.known_for_department && (
            <span className="text-xs text-gray-500">{actor.known_for_department}</span>
          )}
        </div>
      </div>
    </motion.div>
  );
};

// Media Detail Modal Component
interface MediaDetailModalProps {
  item: MediaItem | null;
  onClose: () => void;
}

export const MediaDetailModal: React.FC<MediaDetailModalProps> = ({ item, onClose }) => {
  if (!item) return null;
  
  const title = item.title || item.name || 'Unknown';
  const releaseDate = item.release_date || item.first_air_date;
  const year = releaseDate ? new Date(releaseDate).getFullYear() : null;
  const rating = item.vote_average ? item.vote_average.toFixed(1) : 'N/A';
  const posterUrl = getImageUrl(item.poster_path);
  const backdropUrl = getImageUrl(item.backdrop_path, 'original');
  const isTV = item.media_type === 'tv' || !!item.first_air_date;
  const runtime = item.runtime || (item.episode_run_time?.[0]);
  
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="relative max-w-4xl w-full bg-gray-900 rounded-2xl overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Backdrop */}
        {backdropUrl && (
          <div className="relative h-64 md:h-96">
            <Image
              src={backdropUrl}
              alt={title}
              fill
              className="object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/50 to-transparent" />
          </div>
        )}
        
        {/* Content */}
        <div className="relative p-6 md:p-8">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Poster */}
            {posterUrl && (
              <div className="flex-shrink-0">
                <div className="relative w-32 md:w-48 aspect-[2/3] rounded-lg overflow-hidden">
                  <Image
                    src={posterUrl}
                    alt={title}
                    fill
                    className="object-cover"
                  />
                </div>
              </div>
            )}
            
            {/* Details */}
            <div className="flex-1">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">{title}</h2>
                  <div className="flex items-center gap-4 text-sm text-gray-400">
                    {year && (
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>{year}</span>
                      </div>
                    )}
                    {runtime && (
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        <span>{runtime} min</span>
                      </div>
                    )}
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                      <span className="text-white font-medium">{rating}</span>
                      <span className="text-gray-500">({item.vote_count} votes)</span>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={onClose}
                  className="p-2 rounded-full bg-gray-800 hover:bg-gray-700 transition-colors"
                >
                  <X className="w-5 h-5 text-gray-400" />
                </button>
              </div>
              
              {/* Overview */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-2">Overview</h3>
                <p className="text-gray-300 leading-relaxed">{item.overview}</p>
              </div>
              
              {/* Genres */}
              {item.genre_ids && item.genre_ids.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-white mb-2">Genres</h3>
                  <div className="flex flex-wrap gap-2">
                    {item.genre_ids.map((genreId) => (
                      <span
                        key={genreId}
                        className="px-3 py-1 bg-gray-800 rounded-full text-sm text-gray-300"
                      >
                        {genreMap[genreId] || 'Unknown'}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Action Buttons */}
              <div className="flex gap-3">
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition-colors">
                  <PlayCircle className="w-5 h-5" />
                  <span>Watch Trailer</span>
                </button>
                <button className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white transition-colors">
                  <Heart className="w-5 h-5" />
                  <span>Add to Favorites</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

// Response Container Component
interface ResponseContainerProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
}

export const ResponseContainer: React.FC<ResponseContainerProps> = ({ 
  children, 
  title, 
  subtitle,
  className 
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn("w-full", className)}
    >
      {(title || subtitle) && (
        <div className="mb-6">
          {title && <h2 className="text-2xl font-bold text-white mb-1">{title}</h2>}
          {subtitle && <p className="text-gray-400">{subtitle}</p>}
        </div>
      )}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {children}
      </div>
    </motion.div>
  );
};

// Actor Detail View Component
interface ActorDetailViewProps {
  actor: Actor;
  onClose?: () => void;
}

export const ActorDetailView: React.FC<ActorDetailViewProps> = ({ actor, onClose }) => {
  const profileUrl = getImageUrl(actor.profile_path, 'h632');
  const age = actor.birthday ? 
    Math.floor((new Date().getTime() - new Date(actor.birthday).getTime()) / (1000 * 60 * 60 * 24 * 365.25)) : 
    null;
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 p-6"
    >
      <div className="flex flex-col md:flex-row gap-6">
        {/* Profile Image */}
        <div className="flex-shrink-0">
          <div className="relative w-48 h-64 rounded-lg overflow-hidden bg-gray-900">
            {profileUrl ? (
              <Image
                src={profileUrl}
                alt={actor.name}
                fill
                className="object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <User className="w-24 h-24 text-gray-600" />
              </div>
            )}
          </div>
        </div>
        
        {/* Actor Info */}
        <div className="flex-1">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2">{actor.name}</h2>
              {actor.known_for_department && (
                <span className="text-gray-400">{actor.known_for_department}</span>
              )}
            </div>
            {onClose && (
              <button
                onClick={onClose}
                className="p-2 rounded-full bg-gray-700 hover:bg-gray-600 transition-colors"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            )}
          </div>
          
          {/* Personal Info */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            {actor.birthday && (
              <div>
                <p className="text-sm text-gray-500">Born</p>
                <p className="text-white">
                  {new Date(actor.birthday).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                  })}
                  {age && ` (${age} years old)`}
                </p>
              </div>
            )}
            {actor.place_of_birth && (
              <div>
                <p className="text-sm text-gray-500">Place of Birth</p>
                <p className="text-white">{actor.place_of_birth}</p>
              </div>
            )}
            {actor.popularity && (
              <div>
                <p className="text-sm text-gray-500">Popularity</p>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-400" />
                  <p className="text-white">{actor.popularity.toFixed(1)}</p>
                </div>
              </div>
            )}
          </div>
          
          {/* Biography */}
          {actor.biography && (
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Biography</h3>
              <p className="text-gray-300 leading-relaxed line-clamp-6">{actor.biography}</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Known For */}
      {actor.known_for && actor.known_for.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold text-white mb-4">Known For</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {actor.known_for.map((item, index) => (
              <MediaCard key={item.id} item={item} index={index} />
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};

