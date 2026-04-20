// api/endpoints.js
// Constantes de URLs da API. Todos os services consomem daqui — nenhum
// path hardcoded em servicos ou componentes.

export const ENDPOINTS = {
  health: '/health',
  themes: '/themes',
  sessions: '/sessions',
  sessionById: (id) => `/sessions/${id}`,
  sessionMessages: (id) => `/sessions/${id}/messages`,
  sessionQuiz: (id) => `/sessions/${id}/quiz`,
};
