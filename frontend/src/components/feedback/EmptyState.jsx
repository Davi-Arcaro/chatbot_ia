// components/feedback/EmptyState.jsx
// Estado vazio reutilizavel para listas e telas sem dados.

export default function EmptyState({ title, description, action }) {
  return (
    <div className="empty-state">
      {title && <p style={{ margin: '0 0 4px', color: 'var(--text)' }}>{title}</p>}
      {description && <p style={{ margin: 0 }}>{description}</p>}
      {action && <div style={{ marginTop: 12 }}>{action}</div>}
    </div>
  );
}
