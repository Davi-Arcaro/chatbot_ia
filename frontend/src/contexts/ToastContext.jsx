// contexts/ToastContext.jsx
// Contexto global de toasts. Mantem fila de mensagens e expoe API
// imperativa via useToast() para qualquer componente disparar feedback.

import { createContext, useCallback, useMemo, useState } from 'react';

export const ToastContext = createContext(null);

let nextId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const remove = useCallback((id) => {
    setToasts((current) => current.filter((t) => t.id !== id));
  }, []);

  const push = useCallback(
    (message, type = 'info', duration = 3500) => {
      const id = ++nextId;
      setToasts((current) => [...current, { id, message, type }]);
      if (duration > 0) {
        setTimeout(() => remove(id), duration);
      }
      return id;
    },
    [remove],
  );

  const value = useMemo(
    () => ({
      toasts,
      remove,
      success: (msg) => push(msg, 'success'),
      error: (msg) => push(msg, 'error', 5000),
      info: (msg) => push(msg, 'info'),
    }),
    [toasts, remove, push],
  );

  return (
    <ToastContext.Provider value={value}>{children}</ToastContext.Provider>
  );
}
