// features/chat/MessageInput.jsx
// Input controlado para envio de mensagens. Submit no Enter, quebra de
// linha no Shift+Enter.

import { useState } from 'react';
import Button from '@/components/common/Button.jsx';
import { MESSAGE_MAX_LENGTH } from '@/constants';

export default function MessageInput({ onSend, sending }) {
  const [value, setValue] = useState('');

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || sending) return;
    onSend(trimmed);
    setValue('');
  };

  const onKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  return (
    <div className="chat-input-bar">
      <textarea
        rows={2}
        placeholder="Digite sua pergunta..."
        value={value}
        maxLength={MESSAGE_MAX_LENGTH}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        disabled={sending}
        aria-label="Mensagem"
      />
      <Button onClick={submit} loading={sending} disabled={!value.trim()}>
        Enviar
      </Button>
    </div>
  );
}
