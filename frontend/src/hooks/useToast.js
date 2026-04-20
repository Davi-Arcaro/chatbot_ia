// hooks/useToast.js
// Acesso ao ToastContext. Lanca erro se usado fora do provider para
// detectar configuracao incorreta cedo.

import { useContext } from 'react';
import { ToastContext } from '@/contexts/ToastContext.jsx';

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error('useToast deve ser usado dentro de <ToastProvider>.');
  }
  return ctx;
}
