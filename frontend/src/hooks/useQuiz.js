// hooks/useQuiz.js
// Encapsula geracao e estado de uma pergunta de quiz.

import { useCallback, useState } from 'react';
import { quizService } from '@/services/quizService';

export function useQuiz(sessionId) {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchQuiz = useCallback(async () => {
    if (!sessionId) return null;
    setLoading(true);
    setError(null);
    try {
      const data = await quizService.generate(sessionId);
      setQuiz(data);
      return data;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const reset = useCallback(() => setQuiz(null), []);

  return { quiz, loading, error, fetchQuiz, reset };
}
