import React, { useState } from "react";
import { Icon } from "@iconify/react";

export default function ProfileScreen({ navigate }) {
  const [editMode, setEditMode] = useState(false);
  const [name, setName] = useState("Israel");
  const [about, setAbout] = useState("Passionné par les langues et la culture, Israel apprend activement le bambara et explore les instruments traditionnels.");
  const [email, setEmail] = useState("israel.user@email.com");
  const [tempName, setTempName] = useState(name);
  const [tempAbout, setTempAbout] = useState(about);
  const [tempEmail, setTempEmail] = useState(email);

  const handleEdit = () => {
    setTempName(name);
    setTempAbout(about);
    setTempEmail(email);
    setEditMode(true);
  };

  const handleSave = () => {
    setName(tempName);
    setAbout(tempAbout);
    setEmail(tempEmail);
    setEditMode(false);
  };

  return (
    <div className="min-h-screen relative pb-24 selection:bg-[#E87A5D]/30">
      <div className="bg-mesh" />

      <div className="max-w-2xl mx-auto px-6 pt-12">
        <header className="mb-10 text-center animate-fade-in">
          <h1 className="text-3xl font-bold tracking-tight mb-2">Mon Profil</h1>
          <p className="text-sm uppercase tracking-[0.2em] font-medium" style={{ color: 'var(--text-muted)' }}>Paramètres & Compte</p>
        </header>

        <main className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="glass-card relative overflow-hidden group mb-8">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <Icon icon="solar:user-bold" width={120} />
            </div>

            <div className="p-8 flex flex-col items-center">
              {/* Avatar Section */}
              <div className="relative mb-6">
                <div className="absolute -inset-1 bg-gradient-to-r from-[#E87A5D] to-[#B25944] rounded-full blur opacity-25"></div>
                <div className="relative w-32 h-32 rounded-full border-4 border-[var(--glass-border)] overflow-hidden">
                  <img
                    src="/src/assets/profile.jpg"
                    alt="Avatar"
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                </div>
                {editMode && (
                  <button className="absolute bottom-1 right-1 w-10 h-10 bg-[#E87A5D] border-4 border-[var(--bg-color)] rounded-full flex items-center justify-center text-white hover:scale-110 transition-transform shadow-lg">
                    <Icon icon="solar:camera-bold" width={18} />
                  </button>
                )}
              </div>

              {editMode ? (
                <div className="w-full space-y-6">
                  <div>
                    <label className="block text-xs font-bold uppercase tracking-widest mb-2 ml-1" style={{ color: 'var(--text-muted)' }}>Nom Complet</label>
                    <input
                      className="premium-input text-center text-xl font-bold"
                      value={tempName}
                      onChange={e => setTempName(e.target.value)}
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase tracking-widest mb-2 ml-1" style={{ color: 'var(--text-muted)' }}>À Propos</label>
                    <textarea
                      className="premium-input text-sm leading-relaxed min-h-[100px]"
                      value={tempAbout}
                      onChange={e => setTempAbout(e.target.value)}
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold uppercase tracking-widest mb-2 ml-1" style={{ color: 'var(--text-muted)' }}>Email</label>
                    <input
                      className="premium-input text-sm"
                      value={tempEmail}
                      onChange={e => setTempEmail(e.target.value)}
                    />
                  </div>

                  <div className="flex gap-3 pt-2">
                    <button onClick={handleSave} className="btn-premium flex-1">
                      <Icon icon="solar:check-read-linear" width={20} />
                      Enregistrer
                    </button>
                    <button
                      onClick={() => setEditMode(false)}
                      className="flex-1 px-4 py-2 border border-[var(--glass-border)] rounded-xl hover:bg-[var(--glass-bg)] transition-colors font-semibold"
                    >
                      Annuler
                    </button>
                  </div>
                </div>
              ) : (
                <div className="w-full text-center">
                  <h2 className="text-3xl font-bold mb-2">{name}</h2>
                  <div className="flex items-center justify-center gap-2 mb-8 py-1.5 px-4 rounded-full w-fit mx-auto border border-[var(--glass-border)]" style={{ backgroundColor: 'var(--glass-bg)' }}>
                    <Icon icon="solar:star-bold" width={16} className="text-[#FFB84D]" />
                    <span className="text-sm font-bold opacity-70">Niveau 24 Apprenant</span>
                  </div>

                  <div className="space-y-6 text-left">
                    <div className="glass-card p-5 border-[var(--glass-border)] hover:border-[var(--glass-border-hover)] transition-colors">
                      <h3 className="text-xs font-bold text-[#E87A5D] uppercase tracking-widest mb-2 flex items-center gap-2">
                        <Icon icon="solar:pen-bold" width={14} />
                        À Propos
                      </h3>
                      <p className="text-sm leading-relaxed italic" style={{ color: 'var(--text-dim)' }}>{about}</p>
                    </div>

                    <div className="glass-card p-5 border-[var(--glass-border)] hover:border-[var(--glass-border-hover)] transition-colors">
                      <h3 className="text-xs font-bold text-[#E87A5D] uppercase tracking-widest mb-2 flex items-center gap-2">
                        <Icon icon="solar:letter-bold" width={14} />
                        Contact
                      </h3>
                      <p className="text-sm font-medium" style={{ color: 'var(--text-dim)' }}>{email}</p>
                    </div>
                  </div>

                  <button
                    onClick={handleEdit}
                    className="btn-premium mt-10 w-full sm:w-auto"
                  >
                    <Icon icon="solar:pen-new-square-linear" width={20} />
                    Modifier mon profil
                  </button>
                </div>
              )}
            </div>
          </div>
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
            onClick={() => navigate('progress')}
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:chart-square-linear" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Progrès</span>
          </button>


          <button
            className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
          >
            <Icon icon="solar:user-rounded-bold" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Profil</span>
          </button>
        </div>
      </nav>
    </div>
  );
}
