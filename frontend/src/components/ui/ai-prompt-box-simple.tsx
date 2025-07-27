'use client';

import React from 'react';
import { ArrowUp, Mic, Paperclip, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface PromptInputBoxProps {
  onSend?: (message: string, files?: File[]) => void;
  isLoading?: boolean;
  placeholder?: string;
  className?: string;
}

export const PromptInputBox = React.forwardRef<HTMLDivElement, PromptInputBoxProps>(
  ({ onSend = () => {}, isLoading = false, placeholder = "Ask me about movies, shows, or actors...", className = "" }, ref) => {
    const [input, setInput] = React.useState('');
    const textareaRef = React.useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e?: React.FormEvent) => {
      e?.preventDefault();
      if (input.trim() && !isLoading) {
        onSend(input);
        setInput('');
      }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    };

    // Auto-resize textarea
    React.useEffect(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 240) + 'px';
      }
    }, [input]);

    return (
      <div
        ref={ref}
        className={`rounded-3xl border border-white/20 bg-white/10 backdrop-blur-xl p-4 shadow-lg transition-all duration-300 ${className}`}
      >
        <div className="flex items-end gap-3">
          <div className="flex-1">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              className="w-full resize-none bg-transparent text-white placeholder:text-white/50 focus:outline-none min-h-[24px] max-h-[240px]"
              rows={1}
              disabled={isLoading}
            />
          </div>
          
          <div className="flex items-center gap-2 pb-1">
            <button
              type="button"
              className="p-2 text-white/60 hover:text-white/80 transition-colors rounded-full hover:bg-white/10"
              title="Attach file"
            >
              <Paperclip className="h-5 w-5" />
            </button>
            
            <button
              type="button"
              className="p-2 text-white/60 hover:text-white/80 transition-colors rounded-full hover:bg-white/10"
              title="Voice message"
            >
              <Mic className="h-5 w-5" />
            </button>
            
            <button
              onClick={handleSubmit}
              disabled={!input.trim() || isLoading}
              className={`p-2 rounded-full transition-all ${
                input.trim() && !isLoading
                  ? 'bg-white text-purple-900 hover:bg-white/90'
                  : 'bg-white/20 text-white/40 cursor-not-allowed'
              }`}
              title="Send message"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <ArrowUp className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
        
        {/* Quick suggestions */}
        <div className="mt-3 flex flex-wrap gap-2">
          {['What should I watch tonight?', 'Shows like Breaking Bad', 'Best sci-fi movies'].map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => setInput(suggestion)}
              className="px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-sm text-white/70 hover:text-white transition-all"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    );
  }
);

PromptInputBox.displayName = 'PromptInputBox';
