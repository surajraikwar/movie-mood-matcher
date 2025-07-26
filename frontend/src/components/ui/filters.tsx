'use client';

import React, { useState } from 'react';
import { tvGenres, movieGenres } from '@/mocks/genres';
import { genres as allGenres } from '@/mocks/allGenres';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface FiltersProps {
  onApplyFilters: (filters: any) => void;
}

export function Filters({ onApplyFilters }: FiltersProps) {
  const [selectedGenres, setSelectedGenres] = useState<number[]>([]);
  const [selectedMediaType, setSelectedMediaType] = useState<'movie' | 'tv' | 'all'>('all');

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
              variant={selectedGenres.includes(genre.id) ? 'primary' : 'outline'}
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
            variant={selectedMediaType === 'movie' ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setSelectedMediaType('movie')}
          >
            Movies
          </Button>
          <Button
            variant={selectedMediaType === 'tv' ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setSelectedMediaType('tv')}
          >
            TV Shows
          </Button>
          <Button
            variant={selectedMediaType === 'all' ? 'primary' : 'outline'}
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

