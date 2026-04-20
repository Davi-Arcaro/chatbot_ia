// components/layout/PageContainer.jsx
// Wrapper de pagina com titulo e subtitulo opcionais.

export default function PageContainer({ title, subtitle, actions, children }) {
  return (
    <section>
      {(title || actions) && (
        <header
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-end',
            marginBottom: 16,
            gap: 16,
          }}
        >
          <div>
            {title && <h1 className="page-title">{title}</h1>}
            {subtitle && <p className="page-subtitle">{subtitle}</p>}
          </div>
          {actions && <div>{actions}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
