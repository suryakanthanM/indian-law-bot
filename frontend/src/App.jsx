import { useState, useRef, useEffect } from 'react';
import { Send, Scale, BookOpen, User, AlertCircle, Info, Library } from 'lucide-react';
import './App.css';

// Using a relative URL or environment variable for the API URL is best practice
// We'll default to localhost:8000 for local dev
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Welcome! I am your AI-powered Indian Legal Assistant. You can ask me any questions regarding Indian Law, from simple traffic rules to complex legal scenarios. How can I help you today?\n\n*வணக்கம்! நான் உங்கள் இந்தியச் சட்ட AI உதவியாளர். உங்களுக்கு எப்படி உதவ முடியும்?*',
      sources: null
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentSources, setCurrentSources] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call our FastAPI backend
      const response = await fetch(`${API_URL}/ask?question=${encodeURIComponent(userMessage.content)}`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.answer,
        sources: data.sources_used
      };
      
      if (data.sources_used) {
        setCurrentSources(data.sources_used);
      }

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'bot',
        content: `**Error:** Unable to connect to the legal knowledge base. Please check if the backend is running. (${error.message})`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header glass">
        <div className="header-title-container">
          <Scale className="header-icon" />
          <div>
            <h1 className="header-title">Sattam AI</h1>
            <p className="header-subtitle">Expert Indian Legal Assistant</p>
          </div>
        </div>
        <div className="status-badge">
          <div className="status-dot"></div>
          Online
        </div>
      </header>

      {/* Main Content */}
      <div className="chat-container">
        {/* Chat Area */}
        <main className="main-chat-area glass-panel">
          <div className="messages-list">
            {messages.map((message) => (
              <div 
                key={message.id} 
                className={`message-wrapper ${message.type} animate-fade-in`}
              >
                <div className={`avatar ${message.type}`}>
                  {message.type === 'user' ? <User size={20} /> : <Scale size={20} />}
                </div>
                <div className={`message-bubble ${message.type}`}>
                  <div className="message-markdown" style={{ whiteSpace: 'pre-wrap' }}>
                    {message.content}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message-wrapper bot animate-fade-in">
                <div className="avatar bot"><Scale size={20} /></div>
                <div className="message-bubble bot">
                  <div className="loading-dots">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <form onSubmit={handleSend} className="input-container">
              <input
                type="text"
                className="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about traffic laws, civil cases, IPC..."
                disabled={isLoading}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={!input.trim() || isLoading}
              >
                <Send size={20} />
              </button>
            </form>
          </div>
        </main>

        {/* Sidebar */}
        <aside className="context-sidebar glass-panel">
          <h2 className="sidebar-title">
            <Library size={20} />
            Legal References
          </h2>
          
          {currentSources ? (
            <div className="source-card animate-fade-in">
              <div className="source-header">
                <BookOpen size={16} />
                Document Metadata
              </div>
              <div className="source-content">
                <strong>Source File: </strong> {currentSources.source || 'Unknown'}
                <br /><br />
                <span className="text-sm opacity-75">
                  The AI synthesized its response primarily from this document. If you need absolute legal certainty, please review the direct source or consult a registered advocate.
                </span>
              </div>
            </div>
          ) : (
            <div className="empty-sources">
              <Info size={40} className="opacity-50" />
              <p>When you ask a question, the specific legal sources or PDFs referenced will appear here.</p>
            </div>
          )}
          
          <div style={{marginTop: 'auto'}} className="source-card">
              <div className="source-header" style={{color: 'var(--text-muted)'}}>
                <AlertCircle size={16} />
                Disclaimer
              </div>
              <div className="source-content" style={{fontSize: '0.75rem'}}>
                This chatbot provides legal information for educational purposes and should not be construed as formal legal advice. Always consult a qualified lawyer for serious matters.
              </div>
            </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
