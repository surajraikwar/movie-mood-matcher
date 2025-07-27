'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  Send,
  Sparkles,
  Film,
  MessageSquare,
  User,
  Bot,
  Loader2,
  Paperclip,
  Mic,
  CornerDownLeft,
  TrendingUp,
  Heart,
  Shuffle,
  Clock
} from 'lucide-react';
import { PromptInputBox } from '@/components/ui/ai-prompt-box-simple';
import { 
  MediaCard, 
  ActorCard, 
  ResponseContainer,
  MediaDetailModal,
  ActorDetailView,
  type MediaItem,
  type Actor
} from '@/components/ui/movie-response-cards';
import { BackgroundGradientAnimation } from '@/components/ui/background-gradient-animation';
import FloatingActionMenu from '@/components/ui/floating-action-menu';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  recommendations?: MediaItem[];
  actors?: Actor[];
}

interface MovieRecommendation {
  id: number;
  title: string;
  poster_path?: string;
  vote_average: number;
  overview: string;
  release_date: string;
}

export default function StreamSageChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `# 🎬 Welcome to StreamSage AI!

I'm your intelligent movie and TV show companion. I can help you:

- 🔍 **Find** movies and shows based on your mood
- 💡 **Recommend** content similar to your favorites
- 🎭 **Discover** new genres and hidden gems
- 💬 **Chat** about anything entertainment-related

Just tell me what you're in the mood for, or ask me anything about movies and TV shows!`,
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedMedia, setSelectedMedia] = useState<MediaItem | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Create a new chat session on mount
  useEffect(() => {
    createChatSession();
  }, []);

  const createChatSession = async () => {
    // For now, use a default session ID until auth is implemented
    setSessionId('default-session');
  };

  const handleSendMessage = async (message: string, files?: File[]) => {
    if (!message.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Create assistant message with streaming
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    };

    setMessages(prev => [...prev, assistantMessage]);

    try {
      // Use the existing recommendation endpoint
      const response = await fetch(`http://localhost:8000/api/v1/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: message,
          type: 'movie',
          limit: 10
        })
      });

      if (!response.ok) throw new Error('Failed to send message');

      const data = await response.json();
      
      // Extract media items from recommendations
      const mediaItems: MediaItem[] = [];
      if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach((rec: any) => {
          if (rec.content) {
            mediaItems.push({
              ...rec.content,
              id: rec.content.id,
              title: rec.content.title || rec.content.name,
              media_type: rec.content.media_type || (rec.content.title ? 'movie' : 'tv')
            });
          }
        });
      }
      
      // Create response text
      let responseText = '';
      if (mediaItems.length > 0) {
        responseText = `Based on your query "${message}", here are my recommendations:`;
        if (data.explanation) {
          responseText += `\n\n${data.explanation}`;
        }
      } else {
        responseText = `I couldn't find specific recommendations for "${message}". Could you try describing what you're looking for in more detail? For example:\n\n- "I want a feel-good comedy"\n- "Something like Breaking Bad"\n- "Best sci-fi movies from the 90s"\n- "Movies to watch when I'm sad"`;
      }
      
      // Simulate streaming effect
      const words = responseText.split(' ');
      let currentText = '';
      
      for (let i = 0; i < words.length; i++) {
        currentText += (i === 0 ? '' : ' ') + words[i];
        
        setMessages(prev => {
          const updated = [...prev];
          const lastMessage = updated[updated.length - 1];
          if (lastMessage.role === 'assistant') {
            lastMessage.content = currentText;
          }
          return updated;
        });
        
        // Add delay for streaming effect
        await new Promise(resolve => setTimeout(resolve, 30));
      }
      
      // Mark as done and add recommendations
      setMessages(prev => {
        const updated = [...prev];
        const lastMessage = updated[updated.length - 1];
        if (lastMessage.role === 'assistant') {
          lastMessage.isStreaming = false;
          if (mediaItems.length > 0) {
            lastMessage.recommendations = mediaItems;
          }
        }
        return updated;
      });
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Error streaming response:', error);
        setMessages(prev => {
          const updated = [...prev];
          const lastMessage = updated[updated.length - 1];
          if (lastMessage.role === 'assistant') {
            lastMessage.content = 'I apologize, but I encountered an error. Please try again.';
            lastMessage.isStreaming = false;
          }
          return updated;
        });
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const stopStreaming = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  return (
    <div className="relative flex flex-col h-screen overflow-hidden">
      {/* Animated Background */}
      <BackgroundGradientAnimation
        gradientBackgroundStart="rgb(15, 23, 42)"
        gradientBackgroundEnd="rgb(30, 41, 59)"
        firstColor="59, 130, 246"
        secondColor="139, 92, 246"
        thirdColor="236, 72, 153"
        fourthColor="34, 197, 94"
        fifthColor="251, 146, 60"
        size="60%"
        containerClassName="absolute inset-0"
        interactive={true}
      />
      
      {/* Content Container */}
      <div className="relative z-10 flex flex-col h-full">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-black/20 backdrop-blur-xl border-b border-white/10"
        >
          <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.div 
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-3 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl shadow-lg shadow-cyan-500/20"
              >
                <Film className="w-7 h-7 text-white" />
              </motion.div>
              <div>
                <h1 className="text-2xl font-bold text-white">StreamSage AI</h1>
                <p className="text-xs text-gray-400">Your intelligent entertainment companion</p>
              </div>
              <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
            </div>
            <motion.div className="flex items-center gap-2">
              <span className="flex h-2 w-2 rounded-full bg-green-400 animate-pulse"></span>
              <span className="text-sm text-gray-400">AI Ready</span>
            </motion.div>
          </div>
        </motion.div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-6xl mx-auto px-6 py-8 space-y-6">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                  className={`max-w-3xl px-6 py-4 rounded-2xl ${
                    message.role === 'user'
                      ? 'bg-gradient-to-r from-blue-600/90 to-cyan-600/90 text-white backdrop-blur-md shadow-xl shadow-cyan-500/20'
                      : 'bg-white/5 backdrop-blur-md text-gray-100 border border-white/10 shadow-xl'
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    {message.role === 'assistant' && (
                      <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
                        <Bot className="w-6 h-6 text-white" />
                      </div>
                    )}
                    <div className="flex-1">
                      {message.role === 'assistant' ? (
                        <div className="prose prose-invert max-w-none">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <p className="whitespace-pre-wrap">{message.content}</p>
                      )}
                      {message.isStreaming && (
                        <motion.div
                          animate={{ opacity: [0.5, 1, 0.5] }}
                          transition={{ duration: 1.5, repeat: Infinity }}
                          className="inline-block w-2 h-5 bg-cyan-400 ml-1 rounded-full"
                        />
                      )}
                    </div>
                  </div>
                  
                  {/* Display media recommendations */}
                  {message.recommendations && message.recommendations.length > 0 && (
                    <div className="mt-6">
                      <ResponseContainer>
                        {message.recommendations.map((item, index) => (
                          <MediaCard 
                            key={item.id} 
                            item={item} 
                            index={index}
                            onSelect={setSelectedMedia}
                          />
                        ))}
                      </ResponseContainer>
                    </div>
                  )}
                  
                  {/* Display actors */}
                  {message.actors && message.actors.length > 0 && (
                    <div className="mt-6">
                      <ResponseContainer>
                        {message.actors.map((actor, index) => (
                          <ActorCard 
                            key={actor.id} 
                            actor={actor} 
                            index={index}
                          />
                        ))}
                      </ResponseContainer>
                    </div>
                  )}
                </motion.div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>
      </div>

        {/* Input Form */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-black/20 backdrop-blur-xl border-t border-white/10 p-6"
        >
          <div className="max-w-6xl mx-auto">
            <PromptInputBox
              onSend={handleSendMessage}
              isLoading={isLoading}
              placeholder="Ask me about movies, shows, actors, or what to watch..."
              className="bg-white/10 border-white/20 hover:bg-white/15 transition-colors"
            />
          </div>
        </motion.div>
      </div>
      
      {/* Media Detail Modal */}
      <MediaDetailModal
        item={selectedMedia}
        onClose={() => setSelectedMedia(null)}
      />
      
      {/* Floating Action Menu */}
      <FloatingActionMenu
        options={[
          {
            label: "What's Trending",
            Icon: <TrendingUp className="w-4 h-4" />,
            onClick: () => handleSendMessage("What movies and shows are trending right now?")
          },
          {
            label: "My Favorites",
            Icon: <Heart className="w-4 h-4" />,
            onClick: () => handleSendMessage("Show me top-rated movies of all time")
          },
          {
            label: "Surprise Me",
            Icon: <Shuffle className="w-4 h-4" />,
            onClick: () => handleSendMessage("Surprise me with a random movie recommendation")
          },
          {
            label: "New Releases",
            Icon: <Clock className="w-4 h-4" />,
            onClick: () => handleSendMessage("What are the latest movie releases?")
          }
        ]}
      />
    </div>
  );
}
