// routes/AppRoutes.jsx
// Definicao centralizada de rotas. Lazy loading nas paginas mais pesadas.

import { lazy, Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';
import Spinner from '@/components/common/Spinner.jsx';

import HomePage from '@/pages/HomePage.jsx';
import SessionsPage from '@/pages/SessionsPage.jsx';
import NotFoundPage from '@/pages/NotFoundPage.jsx';

const ChatPage = lazy(() => import('@/pages/ChatPage.jsx'));

export default function AppRoutes() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sessoes" element={<SessionsPage />} />
        <Route path="/sessoes/:id" element={<ChatPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}
