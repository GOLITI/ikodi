import { useState, useEffect } from "react";
import { Icon } from "@iconify/react";
import EventWidget from "./EventWidget";
import { useUserStats } from "./hooks/useUserStats";


const ThemeSwitcher = () => {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');

  return (
    <button
      onClick={toggleTheme}
      className="w-10 h-10 rounded-xl glass flex items-center justify-center hover:scale-110 transition-transform active:scale-95"
      aria-label="Changer de thème"
    >
      <Icon
        icon={theme === 'dark' ? "solar:sun-2-bold" : "solar:moon-bold"}
        width={20}
        className={theme === 'dark' ? "text-[#FFB84D]" : "text-[#7C3AED]"}
      />
    </button>
  );
};

export default function HomeScreen({ navigate }) {
  const user = JSON.parse(localStorage.getItem('user')) || { name: 'Utilisateur', picture: null };
  const initials = user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  const { stats: userStats, loading: statsLoading } = useUserStats();

  const stats = [
    { label: 'Points', value: statsLoading ? '…' : userStats.points.toLocaleString(), icon: 'solar:star-bold', color: '#E87A5D' },
    { label: 'Série', value: statsLoading ? '…' : `${userStats.streak} Jrs`, icon: 'solar:fire-bold', color: '#FFB84D' },
    { label: 'Niveau', value: statsLoading ? '…' : userStats.level, icon: 'solar:medal-ribbon-bold', color: '#4ADE80' },
  ];

  return (
    <div className="min-h-screen relative pb-24">
      <div className="bg-mesh" />

      <div className="max-w-[1200px] mx-auto px-6">
        {/* Header Section */}
        <header className="py-10 flex justify-between items-center animate-fade-in">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">
              Bonjour, <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--text-color)] to-[var(--text-muted)]">{user.name}</span>
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <ThemeSwitcher />
            <button
              onClick={() => navigate('profile')}
              className="relative group cursor-pointer"
            >
              <div className="absolute -inset-1 bg-gradient-to-r from-[#E87A5D] to-[#B25944] rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
              {user.picture ? (
                <img
                  src={user.picture}
                  alt={user.name}
                  className="relative w-12 h-12 rounded-full border-2 border-white/10 object-cover"
                />
              ) : (
                <div className="relative w-12 h-12 rounded-full border-2 border-[#E87A5D]/50 bg-gradient-to-br from-[#E87A5D] to-[#B25944] text-white flex items-center justify-center font-black text-lg">
                  {initials}
                </div>
              )}
            </button>
          </div>
        </header>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Sidebar: Events */}
          <aside className="w-full lg:w-[400px] shrink-0 lg:-ml-20 xl:-ml-32">
            <div className="sticky top-6">
              <EventWidget />
            </div>
          </aside>

          {/* Right content: Main Dashboard */}
          <div className="flex-1">
            {/* Stats Row */}
            <div className="grid grid-cols-3 gap-4 mb-10 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              {stats.map((stat, i) => (
                <div key={i} className="glass-card p-4 flex flex-col items-center justify-center text-center">
                  <div className="mb-2" style={{ color: stat.color }}>
                    <Icon icon={stat.icon} width={20} />
                  </div>
                  <div className="text-lg font-bold">{stat.value}</div>
                  <div className="text-[10px] uppercase tracking-widest font-bold" style={{ color: 'var(--text-muted)' }}>{stat.label}</div>
                </div>
              ))}
            </div>

            {/* Categories Section */}
            <div className="space-y-6">
              <div className="flex items-center justify-between px-1">
                <h2 className="text-xl font-bold flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-[#E87A5D]/10 flex items-center justify-center text-[#E87A5D]">
                    <Icon icon="solar:compass-bold" width={18} />
                  </div>
                  Explorer l'Héritage
                </h2>
              </div>

              <div className="grid gap-4 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                {/* Instruments */}
                <div
                  onClick={() => navigate('instrument')}
                  className="glass-card group cursor-pointer overflow-hidden hover:border-[var(--glass-border-hover)]"
                >
                  <div className="flex items-center gap-5 p-5">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#E87A5D]/20 to-[#E87A5D]/5 flex items-center justify-center text-[#E87A5D] shrink-0 group-hover:scale-110 transition-transform duration-500">
                      <Icon icon="solar:music-note-bold" width={32} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h2 className="text-lg font-bold">Instruments</h2>
                        <span className="text-[10px] px-2 py-1 rounded uppercase font-bold tracking-tighter" style={{ backgroundColor: 'var(--input-bg)', color: 'var(--text-muted)' }}>Éveil Musical</span>
                      </div>
                      <p className="text-sm leading-snug pr-4" style={{ color: 'var(--text-dim)' }}>Balafon, Kora & Djembé : vibrez au rythme des anciens.</p>
                    </div>
                    <Icon icon="solar:alt-arrow-right-linear" width={20} className="group-hover:text-[#E87A5D] group-hover:translate-x-1 transition-all" style={{ color: 'var(--text-muted-more)' }} />
                  </div>
                </div>

                {/* Langue */}
                <div
                  onClick={() => navigate('learningPath')}
                  className="glass-card group cursor-pointer overflow-hidden p-1 hover:border-[var(--glass-border-hover)]"
                >
                  <div className="flex items-center gap-5 p-5">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#4ADE80]/20 to-[#4ADE80]/5 flex items-center justify-center text-[#4ADE80] shrink-0 group-hover:scale-110 transition-transform duration-500">
                      <Icon icon="solar:chat-round-line-bold" width={32} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="text-lg font-bold">Langue Dioula</h3>
                        <span className="text-[10px] bg-[var(--glass-bg)] px-2 py-1 rounded uppercase font-bold tracking-tighter" style={{ color: 'var(--text-muted)' }}>Savoir-parler</span>
                      </div>
                      <p className="text-sm opacity-50 leading-snug pr-4">Conversations, salutations et nuances de la culture.</p>
                    </div>
                    <Icon icon="solar:alt-arrow-right-linear" width={20} className="opacity-20 group-hover:text-[#4ADE80] group-hover:translate-x-1 transition-all" />
                  </div>
                </div>

                {/* Contes */}
                <div
                  onClick={() => navigate('conte')}
                  className="glass-card group cursor-pointer overflow-hidden p-1 hover:border-[var(--glass-border-hover)]"
                >
                  <div className="flex items-center gap-5 p-5">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#A78BFA]/20 to-[#A78BFA]/5 flex items-center justify-center text-[#A78BFA] shrink-0 group-hover:scale-110 transition-transform duration-500">
                      <Icon icon="solar:book-2-bold" width={32} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="text-lg font-bold">Contes & Légendes</h3>
                        <span className="text-[10px] bg-[var(--glass-bg)] px-2 py-1 rounded uppercase font-bold tracking-tighter" style={{ color: 'var(--text-muted)' }}>Immersion</span>
                      </div>
                      <p className="text-sm leading-snug pr-4" style={{ color: 'var(--text-dim)' }}>Plongez dans le folklore ancestral et ses mystères.</p>
                    </div>
                    <Icon icon="solar:alt-arrow-right-linear" width={20} className="group-hover:text-[#A78BFA] group-hover:translate-x-1 transition-all" style={{ color: 'var(--text-muted-more)' }} />
                  </div>
                </div>

                {/* Proverbes */}
                <div
                  onClick={() => navigate('proverbe')}
                  className="glass-card group cursor-pointer overflow-hidden p-1 hover:border-[var(--glass-border-hover)]"
                >
                  <div className="flex items-center gap-5 p-5">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#FFB84D]/20 to-[#FFB84D]/5 flex items-center justify-center text-[#FFB84D] shrink-0 group-hover:scale-110 transition-transform duration-500">
                      <Icon icon="solar:notes-bold" width={32} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="text-lg font-bold">Proverbes</h3>
                        <span className="text-[10px] bg-[var(--glass-bg)] px-2 py-1 rounded uppercase font-bold tracking-tighter" style={{ color: 'var(--text-muted)' }}>Sagesse</span>
                      </div>
                      <p className="text-sm leading-snug pr-4" style={{ color: 'var(--text-dim)' }}>Réflexions et adages pour guider le quotidien.</p>
                    </div>
                    <Icon icon="solar:alt-arrow-right-linear" width={20} className="group-hover:text-[#FFB84D] group-hover:translate-x-1 transition-all" style={{ color: 'var(--text-muted-more)' }} />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Bar */}
          <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6">
            <div className="max-w-md mx-auto glass rounded-2xl p-2 flex justify-between items-center shadow-2xl">
              <button
                onClick={() => navigate('home')}
                className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
              >
                <Icon icon="solar:home-angle-bold" width={22} />
                <span className="text-[10px] font-bold uppercase tracking-tighter">Accueil</span>
              </button>

              <button
                onClick={() => navigate('progress')}
                className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
                style={{ color: 'var(--text-muted)' }}
              >
                <Icon icon="solar:chart-square-linear" width={22} />
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
      </div>
    </div>
  );
}

