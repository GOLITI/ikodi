import React, { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import QuestionForm from './components/QuestionForm';
import ResponseView from './components/ResponseView';

export default function ConteScreen({ onBack, navigate }) {
  const [question, setQuestion] = useState("Raconte-moi l'histoire de Yakouba et le lion");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const API_URL = (import.meta && import.meta.env && import.meta.env.VITE_API_URL) || "http://localhost:8000";

  async function submit(q) {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const payload = { question: q, nb_resultats: 3 };
      const res = await fetch(`${API_URL}/ask/conte`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json);
    } catch (e) {
      setError(e.message || String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { submit(question); }, []);

  return (
    <div className="min-h-screen relative overflow-hidden selection:bg-[#E87A5D]/30">
      <div className="bg-mesh" />

      <div className="max-w-4xl mx-auto px-4 py-8 relative z-10">
        <header className="mb-12 flex items-center justify-between animate-fade-in">
          <button
            className="w-10 h-10 rounded-full glass flex items-center justify-center hover:bg-[var(--glass-bg)] active:scale-95 transition-all"
            style={{ color: 'var(--text-muted)' }}
            onClick={onBack}
            aria-label="Retour"
          >
            <Icon icon="solar:alt-arrow-left-linear" width={24} />
          </button>

          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 bg-gradient-to-r from-[var(--text-color)] via-[var(--text-color)] to-[var(--text-muted)] bg-clip-text text-transparent">
              Contes ivoiriens
            </h1>
            <p className="text-sm uppercase tracking-[0.3em] font-medium" style={{ color: 'var(--text-muted)' }}>
              Sagesse ancestrale & légendes
            </p>
          </div>

          <div className="w-10" /> {/* Spacer */}
        </header>

        <main className="space-y-6">
          <div className="glass-card p-1 sm:p-2 border-[var(--glass-border)]">
            <QuestionForm
              initial={question}
              onSubmit={(q) => { setQuestion(q); submit(q); }}
              loading={loading}
            />
          </div>

          {error && (
            <div className="glass p-4 rounded-xl border-red-500/20 bg-red-500/5 text-red-400 text-sm flex items-center gap-3 animate-fade-in">
              <Icon icon="solar:danger-triangle-bold" width={20} />
              <span>Une erreur est survenue : {error}</span>
            </div>
          )}

          <ResponseView data={data} loading={loading} />
        </main>
      </div>
    </div>
  );
}
