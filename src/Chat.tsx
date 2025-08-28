import React from 'react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import './Chat.css';


export default function Chat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({api: '/api/chat'}),
  });
  const [input, setInput] = React.useState<string>('');

  React.useEffect(() => {
    sendMessage({ text: "" });
  }, []);

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-content">
              {message.parts.map((part, index) =>
                part.type === 'text' ? <span key={index}>{part.text}</span> : null,
              )}
            </div>
          </div>
        ))}
      </div>
      <form
        className="chat-form"
        onSubmit={(e: React.FormEvent) => {
          e.preventDefault();
          if (input.trim()) {
            sendMessage({ text: input });
            setInput('');
          }
        }}
      >
        <input
          className="chat-input"
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
          disabled={status !== 'ready'}
          placeholder="Say something..."
        />
        <button className="chat-submit" type="submit" disabled={status !== 'ready'}>
          Submit
        </button>
      </form>
    </div>
  );
}
