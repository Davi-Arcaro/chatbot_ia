// features/chat/ChatWindow.jsx
// Container que compoe header da sessao, lista de mensagens e input.

import Button from '@/components/common/Button.jsx';
import MessageList from './MessageList.jsx';
import MessageInput from './MessageInput.jsx';

export default function ChatWindow({ session, sending, onSend, onOpenQuiz }) {
  return (
    <div className="chat-window">
      <header className="chat-header">
        <div>
          <strong>{session.tema}</strong>
          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
            Modo conversa
          </div>
        </div>
        <Button variant="ghost" onClick={onOpenQuiz}>
          Modo quiz
        </Button>
      </header>
      <MessageList messages={session.messages} sending={sending} />
      <MessageInput onSend={onSend} sending={sending} />
    </div>
  );
}
