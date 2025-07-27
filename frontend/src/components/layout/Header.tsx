'use client';

import React from 'react';
import { Film, Moon, Sun, Github, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useChatStore } from '@/lib/store';

export function Header() {
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light');
  const clearChat = useChatStore((state) => state.clearChat);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <header className="border-b bg-background">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Film className="w-8 h-8 text-primary" />
            <h1 className="text-2xl font-bold text-primary">
              Movie Mood Matcher
            </h1>
            <a 
              href="/chat" 
              className="ml-4 px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              Try StreamSage AI
            </a>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={clearChat}
            >
              Clear Chat
            </Button>
            
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
            >
              {theme === 'light' ? (
                <Moon className="w-5 h-5" />
              ) : (
                <Sun className="w-5 h-5" />
              )}
            </Button>
            
            <Button
              variant="ghost"
              size="icon"
              asChild
            >
              <a 
                href="https://github.com/yourusername/movie-mood-matcher"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="w-5 h-5" />
              </a>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
