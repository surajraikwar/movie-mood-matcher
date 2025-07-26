import { create } from 'zustand';
import { ChatMessage, ContentRecommendation } from '@/types';
import { generateId } from '@/lib/utils';

interface ChatStore {
  messages: ChatMessage[];
  isLoading: boolean;
  currentRecommendations: ContentRecommendation[];
  
  // Actions
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  setLoading: (loading: boolean) => void;
  setRecommendations: (recommendations: ContentRecommendation[]) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isLoading: false,
  currentRecommendations: [],
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      ...message,
      id: generateId(),
      timestamp: new Date(),
    }],
  })),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setRecommendations: (recommendations) => set({ currentRecommendations: recommendations }),
  
  clearChat: () => set({ messages: [], currentRecommendations: [] }),
}));
