// constants/index.js
// Enums, limites e mensagens reutilizaveis pela aplicacao.

export const MESSAGE_MAX_LENGTH = 4000;
export const THEME_MIN_LENGTH = 3;
export const THEME_MAX_LENGTH = 60;
export const DEBOUNCE_MS = 300;

export const ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
};

export const MESSAGES = {
  LOADING: 'Carregando...',
  GENERIC_ERROR: 'Algo deu errado. Tente novamente.',
  NETWORK_ERROR: 'Falha de conexao com o servidor.',
  SESSION_CREATED: 'Sessao criada com sucesso.',
  SESSION_DELETED: 'Sessao excluida.',
  MESSAGE_SENT: '',
  QUIZ_GENERATED: 'Nova pergunta gerada.',
};
