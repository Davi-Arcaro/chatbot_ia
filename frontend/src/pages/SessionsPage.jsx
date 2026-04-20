// pages/SessionsPage.jsx
// Lista todas as sessoes existentes e permite criar/excluir.

import { useState } from 'react';
import PageContainer from '@/components/layout/PageContainer.jsx';
import Spinner from '@/components/common/Spinner.jsx';
import ConfirmDialog from '@/components/common/ConfirmDialog.jsx';
import SessionList from '@/features/sessions/SessionList.jsx';
import SessionForm from '@/features/sessions/SessionForm.jsx';
import { useSessions } from '@/hooks/useSessions';
import { useToast } from '@/hooks/useToast';
import { MESSAGES } from '@/constants';

export default function SessionsPage() {
  const { sessions, loading, error, createSession, removeSession } = useSessions();
  const toast = useToast();

  const [submitting, setSubmitting] = useState(false);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const handleCreate = async (tema) => {
    setSubmitting(true);
    try {
      await createSession(tema);
      toast.success(MESSAGES.SESSION_CREATED);
    } catch (err) {
      toast.error(err.message || MESSAGES.GENERIC_ERROR);
    } finally {
      setSubmitting(false);
    }
  };

  const confirmDelete = async () => {
    if (!pendingDelete) return;
    setDeleting(true);
    try {
      await removeSession(pendingDelete.id);
      toast.success(MESSAGES.SESSION_DELETED);
      setPendingDelete(null);
    } catch (err) {
      toast.error(err.message || MESSAGES.GENERIC_ERROR);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <PageContainer
      title="Sessoes de chat"
      subtitle="Gerencie as conversas com o professor virtual."
    >
      <div
        style={{
          display: 'grid',
          gap: 24,
          gridTemplateColumns: 'minmax(280px, 360px) 1fr',
          alignItems: 'start',
        }}
      >
        <aside className="card">
          <h3 style={{ marginTop: 0 }}>Nova sessao</h3>
          <SessionForm onSubmit={handleCreate} submitting={submitting} />
        </aside>

        <div>
          {loading && <Spinner />}
          {error && (
            <div className="card" style={{ borderColor: 'var(--danger)' }}>
              {error.message || MESSAGES.GENERIC_ERROR}
            </div>
          )}
          {!loading && !error && (
            <SessionList sessions={sessions} onDelete={setPendingDelete} />
          )}
        </div>
      </div>

      <ConfirmDialog
        open={!!pendingDelete}
        destructive
        loading={deleting}
        title="Excluir sessao"
        message={
          pendingDelete
            ? `Tem certeza que deseja excluir a sessao "${pendingDelete.tema}"? Esta acao nao pode ser desfeita.`
            : ''
        }
        confirmLabel="Excluir"
        onConfirm={confirmDelete}
        onCancel={() => (deleting ? null : setPendingDelete(null))}
      />
    </PageContainer>
  );
}
