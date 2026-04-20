// services/sessionsService.js
// CRUD de sessoes de chat. Servicos nao manipulam estado React nem
// disparam toast/navegacao — devolvem dados ou lancam erro.

import { httpClient } from '@/api/httpClient';
import { ENDPOINTS } from '@/api/endpoints';

export const sessionsService = {
  getAll: () => httpClient.get(ENDPOINTS.sessions).then((r) => r.data),

  getById: (id) =>
    httpClient.get(ENDPOINTS.sessionById(id)).then((r) => r.data),

  create: (payload) =>
    httpClient.post(ENDPOINTS.sessions, payload).then((r) => r.data),

  remove: (id) => httpClient.delete(ENDPOINTS.sessionById(id)),
};
