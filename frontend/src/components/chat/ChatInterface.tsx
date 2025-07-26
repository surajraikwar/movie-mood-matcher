'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Loader2, Film } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { MovieCard } from '@/components/movie/MovieCard';
import { useChatStore } from '@/lib/store';
import { recommendationApi } from '@/services/api';
import { cn } from '@/lib/utils';
import type { RecommendationQuery } from '@/types';

export function ChatInterface() {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  
  const { messages, isLoading, addMessage, setLoading, setRecommendations } = useChatStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    addMessage({ type: 'user', content: userMessage });
    
    // Set loading state
    setLoading(true);
    
    try {
      // Make API call
      const query: RecommendationQuery = {
        query: userMessage,
        media_type: 'all',
        limit: 10,
      };
      
      const response = await recommendationApi.getRecommendations(query);
      
      // Add assistant message with recommendations
      const assistantMessage = response.recommendations.length > 0
        ? `I found ${response.total_results} options based on "${userMessage}". Here are my top recommendations:`
        : `I couldn't find any specific recommendations for "${userMessage}". Try describing what you're in the mood for, like "funny movies from the 90s" or "thriller series with plot twists".`;
      
      addMessage({ 
        type: 'assistant', 
        content: assistantMessage,
        recommendations: response.recommendations 
      });
      
      setRecommendations(response.recommendations);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      addMessage({ 
        type: 'assistant', 
        content: 'Sorry, I encountered an error while fetching recommendations. Please try again.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const suggestedQueries = [
    "I want something funny and light-hearted",
    "Show me mind-bending sci-fi movies",
    "I'm in the mood for a thriller series",
    "Find me feel-good movies from the 90s",
  ];

  return (
    <div className="flex flex-col h-full">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <Film className="w-16 h-16 text-primary mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">Welcome to Movie Mood Matcher</h2>
            <p className="text-muted-foreground mb-8">
              Tell me what you're in the mood for, and I'll find the perfect movie or TV show for you!
            </p>
            
            {/* Suggested queries */}
            <div className="max-w-2xl mx-auto">
              <p className="text-sm text-muted-foreground mb-3">Try one of these:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {suggestedQueries.map((query, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    className="text-sm text-left justify-start"
                    onClick={() => setInput(query)}
                  >
                    <Sparkles className="w-4 h-4 mr-2 text-primary" />
                    {query}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        )}
        
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className={cn(
                'chat-message',
                message.type === 'user' ? 'flex justify-end' : 'flex justify-start'
              )}
            >
              <div
                className={cn(
                  'max-w-[80%] rounded-lg p-4',
                  message.type === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                )}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                
                {/* Show recommendations if available */}
                {message.recommendations && message.recommendations.length > 0 && (
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {message.recommendations.map((rec) => (
                      <MovieCard
                        key={rec.content.id}
                        content={rec.content}
                        showReasons={true}
                        reasons={rec.reasons}
                        className="w-full"
                      />
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-muted rounded-lg p-4 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Finding perfect matches for you...</span>
            </div>
          </motion.div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-4 border-t bg-background">
        <div className="flex gap-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            placeholder="Describe what you want to watch..."
            className="flex-1 resize-none rounded-lg border bg-background px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary min-h-[44px] max-h-[120px]"
            rows={1}
          />
          <Button type="submit" disabled={!input.trim() || isLoading}>
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </form>
    </div>
  );
}
