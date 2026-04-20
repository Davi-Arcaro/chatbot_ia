// hooks/useSession.js
// Carrega o detalhe de uma sessao (tema + historico de mensagens) e
// expoe a operacao de envio de mensagem com atualizacao otimista.

import { useCallback, useEffect, useState } from 'react';
import { sessionsService } from '@/services/sessionsService';
import { messagesService } from '@/services/messagesService';

export function useSession(sessionId) {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (!sessionId) return undefined;
    let cancelled = false;
    setLoading(true);
    setError(null);
    sessionsService
      .getById(sessionId)
      .then((data) => {
        if (!cancelled) setSession(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  const sendMessage = useCallback(
    async (content) => {
      if (!sessionId) return;
      setSending(true);
      try {
        const reply = await messagesService.send(sessionId, content);
        setSession((prev) =>
          prev
            ? {
                ...prev,
                messages: [...prev.messages, reply.user_message, reply.bot_message],
                message_count: prev.message_count + 2,
              }
            : prev,
        );
      } finally {
        setSending(false);
      }
    },
    [sessionId],
  );

  return { session, loading, error, sending, sendMessage };
}
