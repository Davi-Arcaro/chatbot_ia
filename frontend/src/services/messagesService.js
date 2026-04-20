// services/messagesService.js
// Envio de mensagens em uma sessao existente.

import { httpClient } from '@/api/httpClient';
import { ENDPOINTS } from '@/api/endpoints';

export const messagesService = {
  send: (sessionId, content) =>
    httpClient
      .post(ENDPOINTS.sessionMessages(sessionId), { content })
      .then((r) => r.data),
};
