import { useState } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/solid';
import { Avatar, AvatarImage, AvatarFallback } from '@radix-ui/react-avatar';
import { ScrollArea } from '@radix-ui/react-scroll-area';
import { useSession } from 'next-auth/react';
import clsx from 'clsx';

const Chat = () => {
  const { data: session } = useSession();
  const [messages, setMessages] = useState([{
    sender: 'assistant',
    content: 'Welcome to StreamSage AI! How can I assist you today?'
  }]);
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', content: input };
    setMessages([...messages, userMessage]);

    // Send message to backend for processing
    // Simulate bot response for now
    setTimeout(() => {
      const botMessage = {
        sender: 'assistant',
        content: `You said: ${input}`
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 500);

    setInput('');
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 bg-gray-800 text-white">
        <h1 className="text-xl font-bold">StreamSage AI</h1>
        {session && (
          <Avatar>
            <AvatarImage src={session.user.image} alt={session.user.name} />
            <AvatarFallback>{session.user.name[0]}</AvatarFallback>
          </Avatar>
        )}
      </div>
      <ScrollArea className="flex-1 overflow-y-auto">
        <div className="p-4">
          {messages.map((msg, index) => (
            <div key={index} className={clsx('mb-2', {
              'text-right': msg.sender === 'user',
              'text-left': msg.sender === 'assistant'
            })}>
              <div
                className={clsx('inline-block p-2 rounded-lg', {
                  'bg-blue-600 text-white': msg.sender === 'user',
                  'bg-gray-700 text-white': msg.sender === 'assistant'
                })}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
      <form className="flex p-4" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type a message..."
          className="flex-1 p-2 border rounded-l-lg"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600">
          <PaperAirplaneIcon className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
};

export default Chat;
