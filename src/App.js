import React from 'react';
import { DeepChat } from 'deep-chat-react';
import './App.css';

function App() {
  const [introMessage, setIntroMessage] = React.useState({ text: "Loading..." });
 
  React.useEffect(() => {
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: [] })
    })
      .then(res => res.text())
      .then(res => JSON.parse(res.slice("data: ".length)))
      .then(text => setIntroMessage({ text }));
  }, []);

  return (
    <div>
      <h1>Hello World!</h1>
      <DeepChat
        connect={{url:"/api/chat", stream:true}}
        requestBodyLimits={{maxMessages:-1}}
        introMessage={introMessage.text}
      />
    </div>
  );
}

export default App;
