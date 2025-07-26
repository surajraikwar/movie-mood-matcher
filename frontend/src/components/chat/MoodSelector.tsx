'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Smile, Frown, Heart, Zap, Brain, Sparkles, 
  Coffee, Moon, Sun, CloudRain, Loader2 
} from 'lucide-react';
import * as Slider from '@radix-ui/react-slider';
import { Button } from '@/components/ui/button';
import { MovieCard } from '@/components/movie/MovieCard';
import { recommendationApi } from '@/services/api';
import { cn } from '@/lib/utils';
import type { MoodQuery, ContentRecommendation } from '@/types';

const moods = [
  { id: 'happy', label: 'Happy', icon: Smile, color: 'text-yellow-500' },
  { id: 'sad', label: 'Sad', icon: Frown, color: 'text-blue-500' },
  { id: 'romantic', label: 'Romantic', icon: Heart, color: 'text-pink-500' },
  { id: 'excited', label: 'Excited', icon: Zap, color: 'text-orange-500' },
  { id: 'thoughtful', label: 'Thoughtful', icon: Brain, color: 'text-purple-500' },
  { id: 'adventurous', label: 'Adventurous', icon: Sparkles, color: 'text-green-500' },
  { id: 'relaxed', label: 'Relaxed', icon: Coffee, color: 'text-brown-500' },
  { id: 'nostalgic', label: 'Nostalgic', icon: Moon, color: 'text-indigo-500' },
];

export function MoodSelector() {
  const [selectedMood, setSelectedMood] = useState<string | null>(null);
  const [energyLevel, setEnergyLevel] = useState([5]);
  const [timeAvailable, setTimeAvailable] = useState([120]);
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<ContentRecommendation[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!selectedMood) return;

    setIsLoading(true);
    setHasSearched(true);
    
    try {
      const moodQuery: MoodQuery = {
        mood: selectedMood,
        energy_level: energyLevel[0],
        time_available: timeAvailable[0],
      };
      
      const response = await recommendationApi.getMoodRecommendations(moodQuery);
      setRecommendations(response.recommendations);
    } catch (error) {
      console.error('Error getting mood recommendations:', error);
      setRecommendations([]);
    } finally {
      setIsLoading(false);
    }
  };

  const getEnergyLabel = (value: number) => {
    if (value <= 3) return 'Low energy';
    if (value <= 7) return 'Moderate energy';
    return 'High energy';
  };

  const getTimeLabel = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours === 0) return `${mins} minutes`;
    if (mins === 0) return `${hours} hour${hours > 1 ? 's' : ''}`;
    return `${hours}h ${mins}m`;
  };

  return (
    <div className="flex flex-col h-full">
      {/* Mood Selection */}
      <div className="p-6 border-b">
        <h2 className="text-2xl font-bold mb-6">How are you feeling today?</h2>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {moods.map((mood) => {
            const Icon = mood.icon;
            return (
              <motion.button
                key={mood.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedMood(mood.id)}
                className={cn(
                  'p-4 rounded-lg border-2 transition-all',
                  selectedMood === mood.id
                    ? 'border-primary bg-primary/10'
                    : 'border-border hover:border-primary/50'
                )}
              >
                <Icon className={cn('w-8 h-8 mx-auto mb-2', mood.color)} />
                <p className="text-sm font-medium">{mood.label}</p>
              </motion.button>
            );
          })}
        </div>
        
        {/* Energy Level */}
        <div className="mb-6">
          <label className="text-sm font-medium mb-2 block">
            Energy Level: {getEnergyLabel(energyLevel[0])}
          </label>
          <Slider.Root
            className="relative flex items-center select-none touch-none w-full h-5"
            value={energyLevel}
            onValueChange={setEnergyLevel}
            max={10}
            min={1}
            step={1}
          >
            <Slider.Track className="bg-secondary relative grow rounded-full h-[3px]">
              <Slider.Range className="absolute bg-primary rounded-full h-full" />
            </Slider.Track>
            <Slider.Thumb
              className="block w-5 h-5 bg-primary rounded-full hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Energy level"
            />
          </Slider.Root>
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>Tired</span>
            <span>Energetic</span>
          </div>
        </div>
        
        {/* Time Available */}
        <div className="mb-6">
          <label className="text-sm font-medium mb-2 block">
            Time Available: {getTimeLabel(timeAvailable[0])}
          </label>
          <Slider.Root
            className="relative flex items-center select-none touch-none w-full h-5"
            value={timeAvailable}
            onValueChange={setTimeAvailable}
            max={240}
            min={30}
            step={15}
          >
            <Slider.Track className="bg-secondary relative grow rounded-full h-[3px]">
              <Slider.Range className="absolute bg-primary rounded-full h-full" />
            </Slider.Track>
            <Slider.Thumb
              className="block w-5 h-5 bg-primary rounded-full hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Time available"
            />
          </Slider.Root>
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>30 min</span>
            <span>4 hours</span>
          </div>
        </div>
        
        <Button 
          onClick={handleSearch}
          disabled={!selectedMood || isLoading}
          className="w-full"
          size="lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Finding matches...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 mr-2" />
              Get Recommendations
            </>
          )}
        </Button>
      </div>
      
      {/* Results */}
      <div className="flex-1 overflow-y-auto p-6">
        {hasSearched && !isLoading && (
          <>
            {recommendations.length > 0 ? (
              <>
                <h3 className="text-lg font-semibold mb-4">
                  Perfect matches for your mood:
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {recommendations.map((rec) => (
                    <MovieCard
                      key={rec.content.id}
                      content={rec.content}
                      showReasons={true}
                      reasons={rec.reasons}
                    />
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <CloudRain className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">
                  No recommendations found. Try adjusting your mood or preferences.
                </p>
              </div>
            )}
          </>
        )}
        
        {!hasSearched && (
          <div className="text-center py-12">
            <Sun className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">
              Select your mood and preferences above to get personalized recommendations!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
