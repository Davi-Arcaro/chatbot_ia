// features/sessions/SessionForm.jsx
// Formulario controlado para criar uma nova sessao de chat. Usa
// React Hook Form + Zod conforme Secao 9 da arquitetura.

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import Button from '@/components/common/Button.jsx';
import Field from '@/components/common/Field.jsx';
import { useThemes } from '@/hooks/useThemes';
import { THEME_MAX_LENGTH, THEME_MIN_LENGTH } from '@/constants';

const schema = z.object({
  preset: z.string().optional(),
  custom: z
    .string()
    .trim()
    .max(THEME_MAX_LENGTH, `Maximo de ${THEME_MAX_LENGTH} caracteres.`)
    .optional()
    .or(z.literal('')),
});

export default function SessionForm({ onSubmit, submitting }) {
  const { themes, loading: loadingThemes } = useThemes();

  const {
    register,
    handleSubmit,
    watch,
    setError,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: { preset: '', custom: '' },
  });

  const preset = watch('preset');

  const submit = (data) => {
    const tema = data.custom?.trim() || data.preset?.trim() || '';
    if (!tema) {
      setError('custom', { message: 'Escolha um tema ou digite um personalizado.' });
      return;
    }
    if (tema.length < THEME_MIN_LENGTH) {
      setError('custom', {
        message: `Informe ao menos ${THEME_MIN_LENGTH} caracteres.`,
      });
      return;
    }
    onSubmit(tema);
  };

  return (
    <form onSubmit={handleSubmit(submit)} noValidate>
      <Field label="Tema pre-definido" htmlFor="preset" error={errors.preset?.message}>
        <select id="preset" {...register('preset')} disabled={loadingThemes}>
          <option value="">Selecione um tema...</option>
          {themes.map((t) => (
            <option key={t.id} value={t.name}>
              {t.name}
            </option>
          ))}
        </select>
      </Field>

      <Field
        label="Ou digite um tema personalizado"
        htmlFor="custom"
        error={errors.custom?.message}
      >
        <input
          id="custom"
          type="text"
          placeholder="Ex: Astronomia"
          autoComplete="off"
          {...register('custom')}
        />
      </Field>

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 8 }}>
        <Button type="submit" loading={submitting} disabled={submitting && !preset}>
          Criar sessao
        </Button>
      </div>
    </form>
  );
}
