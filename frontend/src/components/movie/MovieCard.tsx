'use client';

import React from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Star, Calendar, Clock, TrendingUp } from 'lucide-react';
import { cn, getImageUrl, formatRating, formatDate, formatRuntime, getMediaTypeLabel } from '@/lib/utils';
import type { Content } from '@/types';

interface MovieCardProps {
  content: Content;
  onClick?: () => void;
  className?: string;
  showReasons?: boolean;
  reasons?: string[];
}

export function MovieCard({ content, onClick, className, showReasons = false, reasons = [] }: MovieCardProps) {
  const isMovie = content.media_type === 'movie';
  const releaseDate = isMovie ? content.release_date : content.first_air_date;
  const runtime = isMovie ? content.runtime : undefined;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={cn(
        'movie-card group relative bg-card rounded-lg overflow-hidden shadow-lg cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[2/3] overflow-hidden">
        <Image
          src={getImageUrl(content.poster_path)}
          alt={content.title}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-110"
          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
        />
        
        {/* Overlay gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Rating Badge */}
        <div className="absolute top-2 right-2 bg-black/70 backdrop-blur-sm rounded-full px-2 py-1 flex items-center gap-1">
          <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
          <span className="text-xs font-semibold text-white">
            {formatRating(content.vote_average)}
          </span>
        </div>
        
        {/* Media Type Badge */}
        <div className="absolute top-2 left-2 bg-primary/90 backdrop-blur-sm rounded-full px-2 py-1">
          <span className="text-xs font-semibold text-primary-foreground">
            {getMediaTypeLabel(content.media_type)}
          </span>
        </div>
      </div>
      
      {/* Content */}
      <div className="p-4 space-y-3">
        <h3 className="font-semibold text-base line-clamp-2 group-hover:text-primary transition-colors">
          {content.title}
        </h3>
        
        {/* Meta info */}
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          {releaseDate && (
            <div className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              <span>{formatDate(releaseDate)}</span>
            </div>
          )}
          {runtime && (
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>{formatRuntime(runtime)}</span>
            </div>
          )}
        </div>
        
        {/* Overview */}
        {content.overview && (
          <p className="text-sm text-muted-foreground line-clamp-3">
            {content.overview}
          </p>
        )}
        
        {/* Popularity indicator */}
        <div className="flex items-center gap-2">
          <TrendingUp className="w-3 h-3 text-primary" />
          <div className="flex-1 bg-secondary rounded-full h-1.5 overflow-hidden">
            <div 
              className="h-full bg-primary transition-all duration-500"
              style={{ width: `${Math.min(content.popularity / 2, 100)}%` }}
            />
          </div>
        </div>
        
        {/* Reasons (if provided) */}
        {showReasons && reasons.length > 0 && (
          <div className="pt-2 border-t border-border">
            <p className="text-xs font-medium text-muted-foreground mb-1">Why recommended:</p>
            <ul className="space-y-1">
              {reasons.slice(0, 2).map((reason, index) => (
                <li key={index} className="text-xs text-muted-foreground flex items-start gap-1">
                  <span className="text-primary mt-0.5">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </motion.div>
  );
}
