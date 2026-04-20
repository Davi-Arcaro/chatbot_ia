import AppRoutes from '@/routes/AppRoutes.jsx';
import Header from '@/components/layout/Header.jsx';
import ToastViewport from '@/components/feedback/ToastViewport.jsx';

export default function App() {
  return (
    <div className="app-shell">
      <Header />
      <main className="app-main">
        <AppRoutes />
      </main>
      <ToastViewport />
    </div>
  );
}
