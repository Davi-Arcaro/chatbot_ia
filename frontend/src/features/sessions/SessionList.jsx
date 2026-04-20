// features/sessions/SessionList.jsx
// Lista de sessoes existentes. Recebe dados via props (apresentacional).

import { Link } from 'react-router-dom';
import Button from '@/components/common/Button.jsx';
import EmptyState from '@/components/feedback/EmptyState.jsx';
import { formatDateTime, pluralize } from '@/utils/formatters';

export default function SessionList({ sessions, onDelete }) {
  if (!sessions || sessions.length === 0) {
    return (
      <EmptyState
        title="Nenhuma sessao ainda"
        description="Crie uma sessao de chat para conversar com o professor virtual."
      />
    );
  }

  return (
    <div className="session-list">
      {sessions.map((s) => (
        <article key={s.id} className="card session-card">
          <h4>{s.tema}</h4>
          <span className="meta">Criada em {formatDateTime(s.created_at)}</span>
          <span className="meta">{pluralize(s.message_count, 'mensagem', 'mensagens')}</span>
          <div className="actions">
            <Link to={`/sessoes/${s.id}`} className="btn btn-primary">
              Abrir
            </Link>
            <Button variant="ghost" onClick={() => onDelete(s)}>
              Excluir
            </Button>
          </div>
        </article>
      ))}
    </div>
  );
}
