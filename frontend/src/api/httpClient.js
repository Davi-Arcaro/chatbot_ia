// api/httpClient.js
// Instancia unica do Axios, com interceptors de erro centralizados.
// Componentes nunca devem importar este arquivo diretamente: o caminho
// canonico e component -> hook -> service -> httpClient.

import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Timeout alto: a inferencia em LLM local (CPU) pode demorar mais que uma
// API remota. 120s acompanha o OLLAMA_TIMEOUT padrao do backend.
export const httpClient = axios.create({
  baseURL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export class ApiError extends Error {
  constructor(message, { status, detail } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

export class NetworkError extends Error {
  constructor(message = 'Falha de conexao com o servidor.') {
    super(message);
    this.name = 'NetworkError';
  }
}

httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      const detail = data?.detail || data?.error || error.message;
      const message =
        typeof detail === 'string' ? detail : 'Erro inesperado da API.';
      return Promise.reject(new ApiError(message, { status, detail }));
    }
    if (error.request) {
      return Promise.reject(new NetworkError());
    }
    return Promise.reject(new ApiError(error.message || 'Erro desconhecido.'));
  },
);
