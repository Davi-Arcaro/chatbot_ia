// pages/HomePage.jsx
// Landing page com apresentacao e CTA para sessoes.

import { Link } from 'react-router-dom';
import PageContainer from '@/components/layout/PageContainer.jsx';

export default function HomePage() {
  return (
    <PageContainer
      title="Chatbot Educacional Eliane"
      subtitle="Tire duvidas com um professor virtual em qualquer materia."
    >
      <div className="card" style={{ maxWidth: 640 }}>
        <p style={{ marginTop: 0 }}>
          Crie uma sessao de chat escolhendo um tema (Biologia, Matematica, Historia...)
          ou digite o seu proprio. Cada sessao mantem o historico da conversa
          e permite alternar para o modo quiz a qualquer momento.
        </p>
        <Link to="/sessoes" className="btn btn-primary">
          Ver minhas sessoes
        </Link>
      </div>
    </PageContainer>
  );
}
