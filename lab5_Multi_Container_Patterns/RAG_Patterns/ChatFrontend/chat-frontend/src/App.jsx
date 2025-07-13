import { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      console.log('Backend URL:', import.meta.env.VITE_BACKEND_URL);
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const botMessage = { role: 'bot', content: data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'system', content: 'Error: Unable to fetch response.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-app">
      <header className="chat-header">Azure OpenAI Chat</header>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${msg.role === 'user' ? 'user' : 'bot'}`}
          >
            {msg.content}
          </div>
        ))}
        {loading && <div className="chat-message bot">Typing...</div>}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;