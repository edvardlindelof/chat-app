import React from 'react';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';

export default function Chat() {
  const { messages, sendMessage, status, setMessages } = useChat({
    transport: new DefaultChatTransport({api: '/api/chat'}),
  });
  const [input, setInput] = useState('');

  // TODO send a first message with some flag in the sendMessage "data" option,
  // to clean this mess up

  React.useEffect(() => {
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: [] })
    })
      .then(res => res.text())
      .then(streamData => {
        return streamData
          .split('\n\n')
          .filter(chunk => chunk)  // remove ""
          .map(chunk => chunk.replace('data: ', ''))
          .map(JSON.parse);
      })
      .then(events =>
        [
          {
            id: events[0].id,
            role: "assistant",
            parts: [
              {
                type: "text",
                text: events.slice(1).map(e => e.delta).join('')
              }
            ]
          }
        ]
      )
      .then(setMessages)
      .then(res => console.log(res))
  }, []);

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          {message.role === 'user' ? 'User: ' : 'AI: '}
          {message.parts.map((part, index) =>
            part.type === 'text' ? <span key={index}>{part.text}</span> : null,
          )}
        </div>
      ))}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (input.trim()) {
            sendMessage({ text: input });
            setInput('');
          }
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={status !== 'ready'}
          placeholder="Say something..."
        />
        <button type="submit" disabled={status !== 'ready'}>
          Submit
        </button>
      </form>
    </div>
  );
}
