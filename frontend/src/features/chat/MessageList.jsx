// features/chat/MessageList.jsx
// Renderiza o historico de mensagens de uma sessao.

import { useEffect, useRef } from 'react';

export default function MessageList({ messages, sending }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length, sending]);

  return (
    <div className="chat-messages">
      {messages.length === 0 && (
        <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: 24 }}>
          Comece a conversa enviando uma pergunta abaixo.
        </div>
      )}
      {messages.map((m, idx) => (
        <div key={idx} className={`chat-message ${m.role}`}>
          {m.content}
        </div>
      ))}
      {sending && (
        <div className="chat-message assistant" style={{ opacity: 0.7 }}>
          <span className="spinner" style={{ marginRight: 8 }} />
          Pensando...
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}
