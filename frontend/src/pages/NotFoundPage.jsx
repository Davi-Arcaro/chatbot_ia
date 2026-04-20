// pages/NotFoundPage.jsx

import { Link } from 'react-router-dom';
import PageContainer from '@/components/layout/PageContainer.jsx';

export default function NotFoundPage() {
  return (
    <PageContainer title="404" subtitle="Pagina nao encontrada">
      <div className="card">
        <p>O endereco acessado nao existe.</p>
        <Link to="/" className="btn btn-primary">
          Voltar ao inicio
        </Link>
      </div>
    </PageContainer>
  );
}
