import React, { useState } from "react";
import { Icon } from "@iconify/react";
import videoSrc from "./assets/video/evenement.mp4";

export default function EventScreen({ navigate }) {
    const [showForm, setShowForm] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setSubmitted(true);
        setTimeout(() => {
            setShowForm(false);
            setSubmitted(false);
        }, 3000);
    };

    return (
        <div className="min-h-screen relative pb-24 font-sans bg-[var(--bg-color)] text-[var(--text-color)] transition-colors duration-400">
            <div className="bg-mesh" />

            {/* Header */}
            <header className="pt-12 pb-8 px-6 text-center animate-fade-in relative z-10">
                <div className="flex items-center justify-center gap-2 mb-3">
                    <Icon icon="solar:calendar-bold-duotone" width={24} className="text-[#E87A5D]" />
                    <span className="text-xs font-bold tracking-[0.2em] uppercase text-[#E87A5D]">
                        Évènements Culturels
                    </span>
                </div>
                <h1 className="text-4xl font-black tracking-tighter mb-2">À ne pas manquer</h1>
                <p className="text-sm font-medium" style={{ color: "var(--text-muted)" }}>
                    Célébrez et participez aux traditions vivantes de notre terre.
                </p>
            </header>

            {/* Main Content */}
            <main className="max-w-xl mx-auto px-6 relative z-10">
                <article className="glass-card rounded-[2.5rem] overflow-hidden shadow-2xl animate-fade-in group">
                    {/* Video Header container */}
                    <div className="relative aspect-[4/3] w-full bg-black">
                        <video
                            src={videoSrc}
                            className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500"
                            autoPlay
                            muted
                            loop
                            playsInline
                        />
                        {/* Gradient Overlay */}
                        <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-color)] via-transparent to-transparent opacity-90" />

                        <div className="absolute top-4 right-4">
                            <span className="bg-[#E87A5D] text-white text-[10px] uppercase font-black tracking-widest px-4 py-1.5 rounded-full shadow-lg">
                                Prochainement
                            </span>
                        </div>

                        <div className="absolute bottom-6 left-6 right-6">
                            <h2 className="text-3xl font-black text-white mb-1 shadow-sm tracking-tight drop-shadow-md">
                                Festival Poro
                            </h2>
                            <div className="flex items-center gap-2 text-white/80 text-xs font-bold uppercase tracking-widest">
                                <Icon icon="solar:map-point-bold" width={16} />
                                <span>Korhogo, Côte d'Ivoire</span>
                            </div>
                        </div>
                    </div>

                    <div className="p-8">
                        <p className="text-base leading-relaxed font-medium mb-8" style={{ color: "var(--text-dim)" }}>
                            Le Poro est un rite initiatique fondamental de la culture Sénoufo. Ce festival rassemble
                            musiciens, danseurs, et la communauté entière pour célébrer la sagesse ancestrale
                            au son des balafons sacrés, dans un moment de communion inoubliable.
                        </p>

                        {!showForm ? (
                            <button
                                onClick={() => setShowForm(true)}
                                className="w-full btn-premium py-4 text-lg font-black tracking-widest flex items-center justify-center gap-2"
                            >
                                <Icon icon="solar:ticket-sale-bold" width={24} />
                                S'INSCRIRE MAINTENANT
                            </button>
                        ) : submitted ? (
                            <div className="bg-green-500/10 border border-green-500/20 text-green-500 font-bold p-5 rounded-3xl text-center animate-fade-in flex flex-col items-center gap-2">
                                <Icon icon="solar:check-circle-bold" width={32} />
                                <span>Inscription confirmée ! À très bientôt.</span>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in bg-[var(--input-bg)] p-6 rounded-3xl border border-[var(--glass-border)]">
                                <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                                    <Icon icon="solar:pen-bold" width={20} className="text-[#E87A5D]" />
                                    Formulaire d'inscription
                                </h3>
                                <div>
                                    <input required type="text" placeholder="Nom complet" className="w-full text-base bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                                </div>
                                <div>
                                    <input required type="email" placeholder="Adresse Email" className="w-full text-base bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                                </div>
                                <div>
                                    <input required type="tel" placeholder="Numéro de téléphone" className="w-full text-base bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                                </div>
                                <div className="pt-4 flex gap-3">
                                    <button type="button" onClick={() => setShowForm(false)} className="flex-1 py-3 px-4 rounded-xl border border-[var(--glass-border)] font-bold text-sm tracking-widest hover:bg-[var(--glass-border)] transition-colors">
                                        ANNULER
                                    </button>
                                    <button type="submit" className="flex-1 btn-premium py-3 px-4 rounded-xl font-bold text-sm tracking-widest">
                                        VALIDER
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </article>
            </main>

            {/* Navigation Bar */}
            <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6">
                <div className="max-w-md mx-auto glass rounded-2xl p-2 flex justify-between items-center shadow-2xl">
                    <button
                        className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
                    >
                        <Icon icon="solar:calendar-bold" width={22} />
                        <span className="text-[10px] font-bold uppercase tracking-tighter">Évènements</span>
                    </button>
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
