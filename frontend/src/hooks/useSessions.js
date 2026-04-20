// hooks/useSessions.js
// Estado de servidor para a lista de sessoes. Expoe operacoes de
// criacao e exclusao com refetch automatico para manter a UI consistente.

import { useCallback, useEffect, useState } from 'react';
import { sessionsService } from '@/services/sessionsService';

export function useSessions() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refetch = useCallback(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    sessionsService
      .getAll()
      .then((data) => {
        if (!cancelled) setSessions(data);
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
  }, []);

  useEffect(() => {
    const cleanup = refetch();
    return cleanup;
  }, [refetch]);

  const createSession = useCallback(
    async (tema) => {
      const created = await sessionsService.create({ tema });
      refetch();
      return created;
    },
    [refetch],
  );

  const removeSession = useCallback(
    async (id) => {
      await sessionsService.remove(id);
      refetch();
    },
    [refetch],
  );

  return { sessions, loading, error, refetch, createSession, removeSession };
}
