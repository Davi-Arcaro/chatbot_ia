// components/feedback/ToastViewport.jsx
// Renderiza a fila de toasts mantida pelo ToastContext.

import { useToast } from '@/hooks/useToast';

export default function ToastViewport() {
  const { toasts, remove } = useToast();
  if (toasts.length === 0) return null;
  return (
    <div className="toast-viewport" role="region" aria-label="Notificacoes">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`toast toast-${t.type}`}
          role="status"
          onClick={() => remove(t.id)}
        >
          {t.message}
        </div>
      ))}
    </div>
  );
}
