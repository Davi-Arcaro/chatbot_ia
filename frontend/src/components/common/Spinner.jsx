// components/common/Spinner.jsx
// Indicador visual de carregamento.

export default function Spinner({ label = 'Carregando...' }) {
  return (
    <div role="status" aria-live="polite" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <span className="spinner" />
      <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>{label}</span>
    </div>
  );
}
