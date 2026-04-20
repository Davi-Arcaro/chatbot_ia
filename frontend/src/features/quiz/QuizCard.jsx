// features/quiz/QuizCard.jsx
// Apresenta uma pergunta de quiz, captura a resposta do usuario e
// exibe correcao com explicacao.

import { useState } from 'react';
import Button from '@/components/common/Button.jsx';

export default function QuizCard({ quiz, loading, onNext, onClose }) {
  const [selected, setSelected] = useState(null);

  if (!quiz) {
    return (
      <div className="card quiz-card">
        <p style={{ color: 'var(--text-muted)' }}>
          Clique em &quot;Gerar pergunta&quot; para iniciar o quiz.
        </p>
        <div style={{ display: 'flex', gap: 8 }}>
          <Button onClick={onNext} loading={loading}>
            Gerar pergunta
          </Button>
          <Button variant="ghost" onClick={onClose}>
            Voltar ao chat
          </Button>
        </div>
      </div>
    );
  }

  const answered = selected !== null;
  const correct = quiz.resposta?.toUpperCase();

  const classFor = (letter) => {
    if (!answered) return 'quiz-alt';
    if (letter === correct) return 'quiz-alt correct';
    if (letter === selected) return 'quiz-alt incorrect';
    return 'quiz-alt';
  };

  const handleNext = async () => {
    setSelected(null);
    await onNext();
  };

  return (
    <div className="card quiz-card">
      <div className="quiz-question">{quiz.pergunta}</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {Object.entries(quiz.alternativas).map(([letter, text]) => (
          <button
            key={letter}
            type="button"
            className={classFor(letter)}
            disabled={answered}
            onClick={() => setSelected(letter)}
          >
            <strong>{letter})</strong> {text}
          </button>
        ))}
      </div>

      {answered && (
        <>
          <div style={{ color: selected === correct ? 'var(--success)' : 'var(--danger-hover)' }}>
            {selected === correct
              ? 'Correto!'
              : `Incorreto. A resposta era ${correct}.`}
          </div>
          {quiz.explicacao && (
            <div className="quiz-explanation">{quiz.explicacao}</div>
          )}
        </>
      )}

      <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
        <Button variant="ghost" onClick={onClose}>
          Voltar ao chat
        </Button>
        <Button onClick={handleNext} loading={loading} disabled={!answered && loading}>
          Proxima pergunta
        </Button>
      </div>
    </div>
  );
}
