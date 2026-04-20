// services/themesService.js
// Acesso aos temas pre-definidos do backend.

import { httpClient } from '@/api/httpClient';
import { ENDPOINTS } from '@/api/endpoints';

export const themesService = {
  getAll: () => httpClient.get(ENDPOINTS.themes).then((r) => r.data),
};
