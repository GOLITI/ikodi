import React from "react";
import Icon from "./Icon";

// Props: mot, traduction, options, bonneReponseIndex, onContinuer, onFermer, coeurs, progression, onAudio, onSelectOption, selectedOptionIndex
// Renommé pour cohérence
export default function LessonVocalScreen({
  mot = "I ni cɛ",
  traduction = "Bonjour / Merci",
  options = [
    "Comment allez-vous ?",
    "Bonjour / Merci",
    "À plus tard"
  ],
  bonneReponseIndex = 1,
  selectedOptionIndex = 1,
  onSelectOption = () => {},
  onContinuer = () => {},
  onFermer = () => {},
  coeurs = 4,
  progression = 65,
  onAudio = () => {}
}) {
  return (
    <div className="app" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', background: '#FAF6F0', color: '#111827', fontFamily: 'DM Sans, sans-serif' }}>
      {/* Barre du haut */}
      <header className="top-bar" style={{ position: 'sticky', top: 0, zIndex: 50, background: 'rgba(250,246,240,0.92)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)', borderBottom: '1px solid rgba(0,0,0,0.05)' }}>
        <div className="top-bar-inner" style={{ maxWidth: 1100, margin: '0 auto', padding: '1.1rem 1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button className="close-btn" aria-label="Fermer" onClick={onFermer} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#9CA3AF', display: 'flex', alignItems: 'center', padding: 4, borderRadius: '50%', transition: 'color 0.2s, background 0.2s', flexShrink: 0 }}>
            <Icon icon="solar:close-circle-linear" width="26" />
          </button>
          <div className="progress-track" style={{ flex: 1, height: 10, background: '#EAE4D9', borderRadius: 999, overflow: 'hidden' }}>
            <div className="progress-fill" style={{ height: '100%', width: progression + '%', background: '#234B3D', borderRadius: 999, transition: 'width 0.7s ease' }}></div>
          </div>
          <div className="hearts" style={{ display: 'flex', alignItems: 'center', gap: 5, color: '#F06543', fontSize: '0.875rem', fontWeight: 500, flexShrink: 0 }}>
            <Icon icon="solar:heart-linear" width="22" />
            <span>{coeurs}</span>
          </div>
        </div>
      </header>

      {/* Contenu principal */}
      <main style={{ flex: 1, paddingBottom: '7rem' }}>
        <div className="content-inner" style={{ maxWidth: 1100, margin: '0 auto', padding: '2rem 1.5rem' }}>
          <h2 className="lesson-title" style={{ fontSize: '1.1rem', fontWeight: 600, color: '#234B3D', marginBottom: '2.5rem', letterSpacing: '-0.01em' }}>Nouveau mot à apprendre</h2>
          {/* Mot */}
          <div className="word-showcase" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', marginBottom: '2.5rem', gap: '0.75rem' }}>
            <h1 className="word-main" style={{ fontFamily: 'Lora, serif', fontSize: 'clamp(3rem, 8vw, 5rem)', fontWeight: 600, color: '#111827', letterSpacing: '-0.02em', lineHeight: 1 }}>{mot}</h1>
            <p className="word-translation" style={{ fontSize: '1.05rem', fontWeight: 500, color: 'rgba(35,75,61,0.7)', letterSpacing: '0.02em' }}>{traduction}</p>
          </div>
          {/* Audio */}
          <div className="audio-wrap" style={{ display: 'flex', justifyContent: 'center', marginBottom: '2.5rem' }}>
            <button className="audio-btn" aria-label="Écouter la prononciation" onClick={onAudio} style={{ width: 80, height: 80, borderRadius: '50%', background: '#F06543', border: 'none', cursor: 'pointer', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 20px -6px rgba(240,101,67,0.6)', animation: 'soft-pulse 2.5s infinite', transition: 'transform 0.2s, background 0.2s' }}>
              <Icon icon="solar:play-linear" width="32" style={{ marginLeft: 4 }} />
            </button>
          </div>
          {/* Options */}
          <div className="options" style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
            {options.map((opt, idx) => (
              <button
                key={idx}
                className={`option-btn${selectedOptionIndex === idx ? ' selected' : ''}`}
                style={{
                  width: '100%',
                  background: selectedOptionIndex === idx ? '#FFF5F2' : '#fff',
                  border: `2px solid ${selectedOptionIndex === idx ? '#F06543' : '#EAE4D9'}`,
                  borderRadius: 16,
                  padding: '1rem 1.25rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  textAlign: 'left',
                  boxShadow: selectedOptionIndex === idx ? '0 4px 12px -4px rgba(240,101,67,0.15)' : '0 1px 4px rgba(0,0,0,0.04)',
                  transition: 'border-color 0.2s, background 0.2s, transform 0.2s',
                  color: selectedOptionIndex === idx ? '#D84C2A' : '#4B5563',
                  fontWeight: selectedOptionIndex === idx ? 600 : 500
                }}
                onClick={() => onSelectOption(idx)}
                disabled={selectedOptionIndex !== null && selectedOptionIndex !== idx}
              >
                <span>{opt}</span>
                {selectedOptionIndex === idx ? (
                  <Icon icon="solar:check-circle-linear" width="26" style={{ color: '#F06543', flexShrink: 0 }} />
                ) : (
                  <div className="option-radio" style={{ width: 24, height: 24, borderRadius: '50%', border: '2px solid #EAE4D9', flexShrink: 0 }}></div>
                )}
              </button>
            ))}
          </div>
        </div>
      </main>

      {/* CTA continuer */}
      <div className="cta-bar" style={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 90, padding: '1rem 1.5rem 0', background: 'linear-gradient(to top, #FAF6F0 70%, transparent)' }}>
        <div className="cta-inner" style={{ maxWidth: 1100, margin: '0 auto', paddingBottom: '5.5rem' }}>
          <button className="cta-btn" style={{ width: '100%', background: '#F06543', color: 'white', border: 'none', borderRadius: 18, padding: '1rem 1.5rem', fontFamily: 'DM Sans, sans-serif', fontSize: '1.05rem', fontWeight: 600, boxShadow: '0 4px 14px rgba(240,101,67,0.39)', cursor: 'pointer', letterSpacing: '0.02em', transition: 'background 0.2s, box-shadow 0.2s, transform 0.15s' }} onClick={onContinuer}>
            Continuer
          </button>
        </div>
      </div>

      {/* Bottom Nav */}
      <nav style={{ position: 'fixed', bottom: 0, left: 0, right: 0, background: 'rgba(255,255,255,0.88)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', borderTop: '1px solid rgba(27,67,50,0.07)', padding: '0.75rem 1.5rem 1.25rem', zIndex: 100 }}>
        <div className="nav-inner" style={{ maxWidth: 480, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <button className="nav-item active" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', background: 'none', border: 'none', cursor: 'pointer', color: '#1B4332', fontSize: '0.72rem', fontWeight: 500, transition: 'color 0.2s ease', padding: '0.25rem 0.5rem' }}>
            <div className="nav-icon-wrap" style={{ position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon icon="solar:home-angle-bold" width="24" />
              <div className="nav-dot" style={{ position: 'absolute', top: -3, right: -4, width: 8, height: 8, background: '#E87A5D', borderRadius: '50%' }}></div>
            </div>
            Accueil
          </button>
          <button className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', background: 'none', border: 'none', cursor: 'pointer', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, transition: 'color 0.2s ease', padding: '0.25rem 0.5rem' }}>
            <Icon icon="solar:chart-square-linear" width="24" />
            Progression
          </button>
          <button className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', background: 'none', border: 'none', cursor: 'pointer', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, transition: 'color 0.2s ease', padding: '0.25rem 0.5rem' }}>
            <Icon icon="solar:diploma-linear" width="24" />
            Certificat
          </button>
          <button className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', background: 'none', border: 'none', cursor: 'pointer', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, transition: 'color 0.2s ease', padding: '0.25rem 0.5rem' }}>
            <Icon icon="solar:user-rounded-linear" width="24" />
            Profil
          </button>
        </div>
      </nav>
    </div>
  );
}
