import React from "react";
import Icon from "./Icon";

export default function ObjetMystereScreen({ navigate }) {
  return (
    <div style={{ minHeight: "100vh", background: "#1B4332", color: "#fff", display: "flex", flexDirection: "column", justifyContent: "center", padding: "2rem", position: 'relative' }}>
      <button onClick={() => navigate('home')} style={{ position: 'absolute', top: '1.5rem', left: '1.5rem', background: 'rgba(255,255,255,0.1)', border: 'none', padding: '0.8rem', borderRadius: '50%', color: '#fff', cursor: 'pointer', display: 'flex' }}>
        <Icon icon="solar:alt-arrow-left-bold" width={24} />
      </button>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', flex: 1 }}>
        <h1 style={{ fontFamily: 'Playfair Display, serif', fontSize: "2.1rem", marginBottom: "1.5rem", textAlign: "center" }}>
          L’objet mystérieux
        </h1>
        <p style={{ fontSize: "1.1rem", maxWidth: 500, textAlign: "center", marginBottom: "2.5rem" }}>
          En ouvrant le tissu, tu découvres un petit gri-gri sculpté dans le bois. La vieille femme murmure : « Ce talisman te protégera lors de ton voyage. »
        </p>
        <button
          style={{
            background: "#E87A5D",
            color: "#fff",
            fontFamily: "DM Sans, sans-serif",
            fontSize: "1rem",
            fontWeight: 500,
            padding: "0.8rem 2.2rem",
            borderRadius: 999,
            border: "none",
            cursor: "pointer",
            boxShadow: "0 4px 14px rgba(232,122,93,0.3)",
            marginBottom: "1.5rem"
          }}
          onClick={() => navigate && navigate("home")}
        >
          Retour à l’accueil
        </button>
      </div>
      {/* Bottom Navigation */}
      <nav style={{ position: 'fixed', bottom: 0, left: 0, right: 0, background: 'rgba(255,255,255,0.88)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', borderTop: '1px solid rgba(27,67,50,0.07)', padding: '0.75rem 1.5rem 1.25rem', zIndex: 100 }}>
        <div className="nav-inner" style={{ maxWidth: 480, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <a href="#" className="nav-item active" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', color: '#1B4332', fontSize: '0.72rem', fontWeight: 500, cursor: 'pointer' }} onClick={e => { e.preventDefault(); navigate && navigate('home'); }}>
            <div className="nav-icon-wrap" style={{ position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon icon="solar:home-angle-bold" width="24" />
              <div className="nav-dot" style={{ position: 'absolute', top: -3, right: -4, width: 8, height: 8, background: '#E87A5D', borderRadius: '50%' }} />
            </div>
            Accueil
          </a>
          <a href="#" className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, cursor: 'pointer' }} onClick={e => { e.preventDefault(); navigate && navigate('progress'); }} onMouseEnter={e => (e.currentTarget.style.color = '#1B4332')} onMouseLeave={e => (e.currentTarget.style.color = '#1B433258')}>
            <Icon icon="solar:chart-square-linear" width="24" />
            Progression
          </a>
          <a href="#" className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, cursor: 'pointer' }} onClick={e => { e.preventDefault(); navigate && navigate('certificate'); }} onMouseEnter={e => (e.currentTarget.style.color = '#1B4332')} onMouseLeave={e => (e.currentTarget.style.color = '#1B433258')}>
            <Icon icon="solar:diploma-linear" width="24" />
            Certificat
          </a>
          <a href="#" className="nav-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4, textDecoration: 'none', color: '#1B433258', fontSize: '0.72rem', fontWeight: 500, cursor: 'pointer' }} onClick={e => { e.preventDefault(); navigate && navigate('profile'); }} onMouseEnter={e => (e.currentTarget.style.color = '#1B4332')} onMouseLeave={e => (e.currentTarget.style.color = '#1B433258')}>
            <Icon icon="solar:user-rounded-linear" width="24" />
            Profil
          </a>
        </div>
      </nav>
    </div>
  );
}
