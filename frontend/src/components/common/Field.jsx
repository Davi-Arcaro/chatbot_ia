// components/common/Field.jsx
// Wrapper de campo de formulario com label e mensagem de erro.

export default function Field({ label, htmlFor, error, children }) {
  return (
    <div className="field">
      {label && <label htmlFor={htmlFor}>{label}</label>}
      {children}
      {error && <span className="error">{error}</span>}
    </div>
  );
}
