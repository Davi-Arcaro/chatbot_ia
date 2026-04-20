// hooks/useThemes.js
// Carrega a lista de temas pre-definidos do backend uma unica vez.

import { useEffect, useState } from 'react';
import { themesService } from '@/services/themesService';

export function useThemes() {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    themesService
      .getAll()
      .then((data) => {
        if (!cancelled) setThemes(data);
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

  return { themes, loading, error };
}
