// services/quizService.js
// Geracao de perguntas de quiz para uma sessao existente.

import { httpClient } from '@/api/httpClient';
import { ENDPOINTS } from '@/api/endpoints';

export const quizService = {
  generate: (sessionId) =>
    httpClient.post(ENDPOINTS.sessionQuiz(sessionId)).then((r) => r.data),
};
