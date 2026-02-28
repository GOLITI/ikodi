import React from 'react';
import { Icon } from "@iconify/react";

function Skeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="glass-card p-6 border-[var(--glass-border)]">
        <div className="h-6 rounded w-1/4 mb-4" style={{ backgroundColor: 'var(--input-bg)' }} />
        <div className="space-y-2">
          <div className="h-4 rounded w-full" style={{ backgroundColor: 'var(--glass-bg)' }} />
          <div className="h-4 rounded w-5/6" style={{ backgroundColor: 'var(--glass-bg)' }} />
          <div className="h-4 rounded w-4/6" style={{ backgroundColor: 'var(--glass-bg)' }} />
        </div>
      </div>
      <div className="space-y-3">
        {[1, 2, 3].map(i => (
          <div key={i} className="glass-card p-4 border-[var(--glass-border)]">
            <div className="h-4 rounded w-1/2 mb-2" style={{ backgroundColor: 'var(--input-bg)' }} />
            <div className="h-3 rounded w-full" style={{ backgroundColor: 'var(--glass-bg)' }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function ResponseView({ data, loading }) {
  if (loading) return <Skeleton />;
  if (!data) return null;

  return (
    <div className="space-y-8 animate-fade-in pb-12">
      {/* Main Response Section */}
      <section className="glass-card relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <Icon icon="solar:chat-round-line-linear" width={80} />
        </div>

        <div className="p-6 sm:p-8">
          <div className="flex items-center gap-3 mb-4 text-[#E87A5D]">
            <Icon icon="solar:magic-stick-3-bold" width={24} />
            <h2 className="text-xl font-bold tracking-tight">Sagesse du Griot</h2>
          </div>

          <div className="text-lg leading-relaxed font-serif italic border-l-4 border-[#E87A5D]/30 pl-6 py-2" style={{ color: 'var(--text-color)' }}>
            {data.reponse}
          </div>
        </div>
      </section>

      {/* Sources Section */}
      <section>
        <div className="flex items-center justify-between mb-4 px-1">
          <h3 className="text-lg font-semibold flex items-center gap-2" style={{ color: 'var(--text-muted)' }}>
            <Icon icon="solar:library-bold" width={20} />
            Sources Culturelles ({data.nb_sources})
          </h3>
        </div>

        <div className="grid gap-4">
          {data.sources.map((s, i) => (
            <div
              key={i}
              className="glass-card group hover:translate-x-1 transition-all duration-300"
            >
              <div className="p-5 flex flex-col sm:flex-row sm:items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-[#E87A5D]/10 flex items-center justify-center shrink-0 text-[#E87A5D]">
                  <Icon
                    icon={s.type_contenu === 'conte' ? 'solar:book-2-bold' : 'solar:notes-bold'}
                    width={28}
                  />
                </div>

                <div className="flex-1">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                    <h4 className="font-bold text-lg">
                      {s.titre_parent || s.titre || 'Sans titre'}
                    </h4>
                    <span className="text-[10px] uppercase tracking-widest px-2 py-1 rounded font-bold" style={{ backgroundColor: 'var(--input-bg)', color: 'var(--text-muted)' }}>
                      Match: {(s.score * 100).toFixed(0)}%
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-x-4 gap-y-1 mb-3">
                    <div className="flex items-center gap-1.5 text-xs font-medium capitalize" style={{ color: 'var(--text-muted)' }}>
                      <Icon icon="solar:users-group-rounded-linear" width={14} />
                      {s.ethnie}
                    </div>
                    <div className="flex items-center gap-1.5 text-xs capitalize font-medium" style={{ color: 'var(--text-muted)' }}>
                      <Icon icon="solar:tag-linear" width={14} />
                      {s.type_contenu}
                    </div>
                  </div>

                  {s.morale && (
                    <div className="rounded-lg p-3 text-sm leading-relaxed border border-[var(--glass-border)]" style={{ backgroundColor: 'var(--input-bg)', color: 'var(--text-dim)' }}>
                      <span className="text-[#E87A5D] font-bold text-xs uppercase mr-2.5 tracking-tighter">Enseignement :</span>
                      {s.morale}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
