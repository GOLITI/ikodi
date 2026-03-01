import React, { useState } from 'react';
import { Icon } from "@iconify/react";

export default function QuestionForm({ initial = '', onSubmit, loading }) {
  const [value, setValue] = useState(initial);
  const [error, setError] = useState('');

  function validate(v) {
    if (!v || v.trim().length < 3) return 'La question doit contenir au moins 3 caractères.';
    if (v.trim().length > 1000) return 'La question est trop longue.';
    return '';
  }

  const handleSubmit = () => {
    const err = validate(value);
    setError(err);
    if (!err && !loading) onSubmit(value.trim());
  };

  return (
    <div className="mb-8 animate-fade-in">
      <label className="block text-sm font-bold mb-3 ml-1 uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>
        Votre question
      </label>
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <input
            value={value}
            onChange={e => { setValue(e.target.value); if (error) setError(validate(e.target.value)); }}
            className="premium-input pr-10"
            placeholder="Ex: Raconte-moi l'histoire de Yakouba..."
            disabled={loading}
          />
          <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: 'var(--text-muted-more)' }}>
            <Icon icon="solar:pen-new-square-linear" width={20} />
          </div>
        </div>
        <button
          onClick={handleSubmit}
          disabled={loading || !!validate(value)}
          className="btn-premium whitespace-nowrap min-w-[140px]"
        >
          {loading ? (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Chargement...</span>
            </div>
          ) : (
            <>
              <Icon icon="solar:magic-stick-3-linear" width={20} />
              <span>Interroger</span>
            </>
          )}
        </button>
      </div>
      {error && <div className="text-xs text-red-400 mt-2 ml-1 flex items-center gap-1">
        <Icon icon="solar:danger-triangle-linear" width={14} />
        {error}
      </div>}
    </div>
  );
}
