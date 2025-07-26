'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { apiClient } from '@/lib/api-client';

interface FiltersProps {
  onApplyFilters: (filters: any) => void;
}

interface Genre {
  id: number;
  name: string;
}

export function Filters({ onApplyFilters }: FiltersProps) {
  const [selectedGenres, setSelectedGenres] = useState<number[]>([]);
  const [selectedMediaType, setSelectedMediaType] = useState<'movie' | 'tv' | 'all'>('all');
  const [allGenres, setAllGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch genres from API
    const fetchGenres = async () => {
      try {
        const response = await apiClient.get('/genres/all');
        if (response.data) {
          // Combine movie and TV genres, removing duplicates
          const movieGenres = response.data.movie || [];
          const tvGenres = response.data.tv || [];
          const genreMap = new Map();
          
          [...movieGenres, ...tvGenres].forEach(genre => {
            genreMap.set(genre.id, genre);
          });
          
          setAllGenres(Array.from(genreMap.values()));
        }
      } catch (error) {
        console.error('Failed to fetch genres:', error);
        // Fallback genres if API fails
        setAllGenres([
          { id: 28, name: 'Action' },
          { id: 12, name: 'Adventure' },
          { id: 16, name: 'Animation' },
          { id: 35, name: 'Comedy' },
          { id: 18, name: 'Drama' },
          { id: 27, name: 'Horror' },
          { id: 10749, name: 'Romance' },
          { id: 878, name: 'Sci-Fi' },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchGenres();
  }, []);

  const toggleGenre = (id: number) => {
    setSelectedGenres((current) =>
      current.includes(id) ? current.filter((g) => g !== id) : [...current, id]
    );
  };

  return (
    <div className="p-4 space-y-4 bg-secondary rounded-lg">
      <h3 className="text-lg font-semibold">Filter Options</h3>
      <div className="space-y-2">
        <h4 className="text-sm font-medium">Genres</h4>
        <div className="flex flex-wrap gap-2">
          {allGenres.map((genre) => (
            <Button
              key={genre.id}
              variant={selectedGenres.includes(genre.id) ? 'default' : 'outline'}
              size="sm"
              onClick={() => toggleGenre(genre.id)}
              className={cn(selectedGenres.includes(genre.id) && 'opacity-100', 'opacity-80')}
            >
              {genre.name}
            </Button>
          ))}
        </div>
      </div>
      <div className="space-y-2">
        <h4 className="text-sm font-medium">Media Type</h4>
        <div className="flex gap-2">
          <Button
            variant={selectedMediaType === 'movie' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedMediaType('movie')}
          >
            Movies
          </Button>
          <Button
            variant={selectedMediaType === 'tv' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedMediaType('tv')}
          >
            TV Shows
          </Button>
          <Button
            variant={selectedMediaType === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setSelectedMediaType('all')}
          >
            All
          </Button>
        </div>
      </div>
      <Button variant="secondary" onClick={() => onApplyFilters({ genres: selectedGenres, mediaType: selectedMediaType })}>
        Apply Filters
      </Button>
    </div>
  );
}

