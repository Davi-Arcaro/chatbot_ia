// hooks/useDebounce.js
// Debounce simples para inputs reativos (filtros, busca local).

import { useEffect, useState } from 'react';
import { DEBOUNCE_MS } from '@/constants';

export function useDebounce(value, delay = DEBOUNCE_MS) {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const handle = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handle);
  }, [value, delay]);

  return debounced;
}
