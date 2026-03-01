import React from "react";
import { Icon } from "@iconify/react";

export default function ProgressScreen({ navigate }) {
  const achievements = [
    { name: "Semaine parfaite", icon: "solar:cup-star-bold", color: "#FFB84D", count: 3 },
    { name: "Polyglotte", icon: "solar:medal-ribbon-star-bold", color: "#60A5FA", unlocked: true },
    { name: "Lève-tôt", icon: "solar:leaf-bold", color: "#4ADE80", unlocked: true },
    { name: "Maîtrise", icon: "solar:magic-stick-3-bold", color: "#A78BFA", unlocked: true },
  ];

  const stats = [
    {
      label: "Langue Dioula",
      value: "68%",
      icon: "solar:chat-round-line-bold",
      color: "#4ADE80",
      trend: "+12%",
      progress: 68
    },
    {
      label: "Quiz Instruments",
      value: "94/100",
      icon: "solar:music-note-bold",
      color: "#E87A5D",
      trend: "Top 5%",
      progress: 94
    },
    {
      label: "Contes Lus",
      value: "12/30",
      icon: "solar:book-2-bold",
      color: "#A78BFA",
      trend: "2h rest.",
      progress: 40
    }
  ];

  return (
    <div className="min-h-screen relative pb-24">
      <div className="bg-mesh" />

      <div className="max-w-4xl mx-auto px-6 pt-8">
        <button className="flex items-center gap-2 text-xs font-bold tracking-widest uppercase mb-6 hover:scale-105 transition-transform" onClick={() => navigate('home')}>
          <Icon icon="solar:alt-arrow-left-bold" width={18} />
          RETOUR
        </button>
        <header className="mb-10 animate-fade-in">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Ma Progression</h1>
              <p className="text-sm uppercase tracking-[0.2em] font-medium mt-1" style={{ color: 'var(--text-muted)' }}>Évolution & Succès</p>
            </div>
            <div className="w-12 h-12 rounded-2xl glass flex items-center justify-center" style={{ color: 'var(--text-muted-more)' }}>
              <Icon icon="solar:chart-square-bold" width={24} />
            </div>
          </div>
        </header>

        <main className="space-y-10">
          {/* Stats Section */}
          <section className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <h2 className="text-xs font-bold uppercase tracking-widest mb-6 ml-1" style={{ color: 'var(--text-muted)' }}>Statistiques Clés</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {stats.map((stat, i) => (
                <div key={i} className="glass-card p-6 group">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110" style={{ backgroundColor: `${stat.color}15`, color: stat.color }}>
                      <Icon icon={stat.icon} width={20} />
                    </div>
                    <span className="text-[10px] font-bold px-2 py-1 rounded-lg border border-[var(--glass-border)]" style={{ backgroundColor: 'var(--glass-bg)', color: 'var(--text-muted)' }}>
                      {stat.trend}
                    </span>
                  </div>
                  <div className="mb-4">
                    <p className="text-xs font-medium mb-1 uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>{stat.label}</p>
                    <p className="text-2xl font-bold tracking-tight">{stat.value}</p>
                  </div>
                  <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${stat.progress}%`, backgroundColor: stat.color }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Achievements Section */}
          <section className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center justify-between mb-6 ml-1">
              <h2 className="text-xs font-bold uppercase tracking-widest" style={{ color: 'var(--text-muted)' }}>Succès & Badges</h2>
              <button className="text-[10px] font-bold text-[#E87A5D] uppercase tracking-widest flex items-center gap-1 hover:brightness-110 transition-all">
                Tout voir <Icon icon="solar:alt-arrow-right-bold" width={12} />
              </button>
            </div>

            <div className="glass-card p-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
              {achievements.map((ach, i) => (
                <div key={i} className="flex flex-col items-center p-4 rounded-2xl hover:bg-[var(--glass-bg)] transition-colors group cursor-default">
                  <div className="relative mb-3">
                    <div className="w-16 h-16 rounded-full glass border-2 border-[var(--glass-border)] flex items-center justify-center transition-all duration-500 group-hover:scale-110 shadow-xl" style={{ color: ach.color }}>
                      <Icon icon={ach.icon} width={28} />
                    </div>
                    {ach.count && (
                      <span className="absolute -top-1 -right-1 w-6 h-6 bg-[#E87A5D] border-3 border-[var(--bg-color)] rounded-full flex items-center justify-center text-[10px] font-bold text-white shadow-lg">
                        {ach.count}
                      </span>
                    )}
                  </div>
                  <p className="text-[10px] font-bold uppercase tracking-widest text-center" style={{ color: 'var(--text-dim)' }}>{ach.name}</p>
                </div>
              ))}
              {/* Locked Achievement */}
              <div className="flex flex-col items-center p-4 rounded-2xl opacity-30 grayscale cursor-not-allowed">
                <div className="w-16 h-16 rounded-full glass border-2 border-dashed border-white/20 flex items-center justify-center text-white/40">
                  <Icon icon="solar:lock-bold" width={24} />
                </div>
                <p className="text-[10px] font-bold text-white/70 uppercase tracking-widest text-center mt-3">Verrouillé</p>
              </div>
            </div>
          </section>
        </main>
      </div>

      {/* Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6 animate-fade-in">
        <div className="max-w-md mx-auto glass rounded-2xl p-2 flex justify-between items-center shadow-2xl">
          <button
            onClick={() => navigate('home')}
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:home-angle-bold" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Accueil</span>
          </button>

          <button
            className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
          >
            <Icon icon="solar:chart-square-bold" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Progrès</span>
          </button>


          <button
            onClick={() => navigate('profile')}
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:user-rounded-linear" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Profil</span>
          </button>
        </div>
      </nav>
    </div>
  );
}
