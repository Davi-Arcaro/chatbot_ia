// pages/ChatPage.jsx
// Tela de conversa com o bot. Alterna entre modo chat e modo quiz.

import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import PageContainer from '@/components/layout/PageContainer.jsx';
import Spinner from '@/components/common/Spinner.jsx';
import ChatWindow from '@/features/chat/ChatWindow.jsx';
import QuizCard from '@/features/quiz/QuizCard.jsx';
import { useSession } from '@/hooks/useSession';
import { useQuiz } from '@/hooks/useQuiz';
import { useToast } from '@/hooks/useToast';
import { MESSAGES } from '@/constants';

export default function ChatPage() {
  const { id } = useParams();
  const { session, loading, error, sending, sendMessage } = useSession(id);
  const { quiz, loading: quizLoading, fetchQuiz, reset } = useQuiz(id);
  const toast = useToast();

  const [mode, setMode] = useState('chat');

  const handleSend = async (content) => {
    try {
      await sendMessage(content);
    } catch (err) {
      toast.error(err.message || MESSAGES.GENERIC_ERROR);
    }
  };

  const handleNextQuiz = async () => {
    try {
      await fetchQuiz();
    } catch (err) {
      toast.error(err.message || MESSAGES.GENERIC_ERROR);
    }
  };

  const closeQuiz = () => {
    reset();
    setMode('chat');
  };

  if (loading) {
    return (
      <PageContainer title="Carregando sessao...">
        <Spinner />
      </PageContainer>
    );
  }

  if (error || !session) {
    return (
      <PageContainer title="Sessao indisponivel">
        <div className="card">
          <p>{error?.message || 'Sessao nao encontrada.'}</p>
          <Link to="/sessoes" className="btn btn-primary">
            Voltar para sessoes
          </Link>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer
      title={session.tema}
      subtitle={mode === 'chat' ? 'Modo conversa' : 'Modo quiz'}
      actions={
        <Link to="/sessoes" className="btn btn-ghost">
          Voltar
        </Link>
      }
    >
      {mode === 'chat' ? (
        <ChatWindow
          session={session}
          sending={sending}
          onSend={handleSend}
          onOpenQuiz={() => setMode('quiz')}
        />
      ) : (
        <QuizCard
          quiz={quiz}
          loading={quizLoading}
          onNext={handleNextQuiz}
          onClose={closeQuiz}
        />
      )}
    </PageContainer>
  );
}
