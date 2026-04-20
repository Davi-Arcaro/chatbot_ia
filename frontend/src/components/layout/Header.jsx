// components/layout/Header.jsx
// Cabecalho com navegacao principal.

import { NavLink } from 'react-router-dom';

const APP_NAME = import.meta.env.VITE_APP_NAME || 'Chatbot Eliane';

export default function Header() {
  return (
    <header className="app-header">
      <div className="app-header-inner">
        <div className="app-header-brand">{APP_NAME}</div>
        <nav>
          <NavLink to="/" end>
            Inicio
          </NavLink>
          <NavLink to="/sessoes">Sessoes</NavLink>
        </nav>
      </div>
    </header>
  );
}
