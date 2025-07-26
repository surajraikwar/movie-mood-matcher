'use client';

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { MoodSelector } from '@/components/chat/MoodSelector';
import { Header } from '@/components/layout/Header';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const queryClient = new QueryClient();

export default function HomePage() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex flex-col h-screen bg-background">
        <Header />
        
        <main className="flex-1 container mx-auto p-4 overflow-hidden">
          <div className="h-full max-w-6xl mx-auto">
            <Tabs defaultValue="chat" className="h-full flex flex-col">
              <TabsList className="grid w-full max-w-md mx-auto grid-cols-2">
                <TabsTrigger value="chat">Chat Assistant</TabsTrigger>
                <TabsTrigger value="mood">Mood Selector</TabsTrigger>
              </TabsList>
              
              <TabsContent value="chat" className="flex-1 mt-4 overflow-hidden">
                <div className="h-full bg-card rounded-lg border shadow-sm">
                  <ChatInterface />
                </div>
              </TabsContent>
              
              <TabsContent value="mood" className="flex-1 mt-4 overflow-hidden">
                <div className="h-full bg-card rounded-lg border shadow-sm">
                  <MoodSelector />
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </QueryClientProvider>
  );
}
