// components/feedback/ErrorBoundary.jsx
// Captura erros de renderizacao para evitar tela branca.

import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    // Log para diagnostico em dev. Em producao seria enviado a um servico externo.
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.error('ErrorBoundary capturou:', error, info);
    }
  }

  handleReset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 32, maxWidth: 600, margin: '40px auto' }}>
          <h2>Algo deu errado</h2>
          <p style={{ color: 'var(--text-muted)' }}>
            Ocorreu um erro inesperado na interface. Recarregue a pagina ou tente novamente.
          </p>
          <button className="btn btn-primary" onClick={this.handleReset}>
            Tentar novamente
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
