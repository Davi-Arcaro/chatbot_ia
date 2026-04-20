// components/common/Button.jsx
// Botao base reutilizavel, sem conhecimento de dominio.

export default function Button({
  variant = 'primary',
  type = 'button',
  loading = false,
  disabled = false,
  children,
  ...rest
}) {
  const className = `btn btn-${variant}`;
  return (
    <button
      type={type}
      className={className}
      disabled={disabled || loading}
      {...rest}
    >
      {loading && <span className="spinner" aria-hidden="true" />}
      {children}
    </button>
  );
}
