import React, { useState } from "react";
import { Icon } from "@iconify/react";
import videoSrc from "./assets/video/evenement.mp4";

export default function EventWidget() {
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
                    musiciens, danseurs, et la communauté entière.
                </p>

                {!showForm ? (
                    <button
                        onClick={() => setShowForm(true)}
                        className="w-full btn-premium py-4 text-base font-black tracking-widest flex items-center justify-center gap-2"
                    >
                        <Icon icon="solar:ticket-sale-bold" width={24} />
                        S'INSCRIRE
                    </button>
                ) : submitted ? (
                    <div className="bg-green-500/10 border border-green-500/20 text-green-500 font-bold p-5 rounded-3xl text-center animate-fade-in flex flex-col items-center gap-2">
                        <Icon icon="solar:check-circle-bold" width={32} />
                        <span>Inscription confirmée ! À très bientôt.</span>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in bg-[var(--input-bg)] p-6 rounded-3xl border border-[var(--glass-border)]">
                        <h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-[#E87A5D]">
                            <Icon icon="solar:pen-bold" width={20} />
                            Formulaire
                        </h3>
                        <div>
                            <input required type="text" placeholder="Nom complet" className="w-full text-sm bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                        </div>
                        <div>
                            <input required type="email" placeholder="Adresse Email" className="w-full text-sm bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                        </div>
                        <div>
                            <input required type="tel" placeholder="Numéro de téléphone" className="w-full text-sm bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                        </div>
                        <div>
                            <input required type="date" className="w-full text-sm bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors text-[var(--text-muted)] focus:text-[var(--text-color)]" />
                        </div>
                        <div>
                            <input required type="text" placeholder="Lieu / Ville" className="w-full text-sm bg-transparent border-b-2 border-white/10 px-2 py-3 focus:outline-none focus:border-[#E87A5D] transition-colors" />
                        </div>
                        <div className="pt-4 flex gap-3">
                            <button type="button" onClick={() => setShowForm(false)} className="flex-1 py-3 px-4 rounded-xl border border-[var(--glass-border)] font-bold text-xs tracking-widest hover:bg-[var(--glass-border)] transition-colors">
                                ANNULER
                            </button>
                            <button type="submit" className="flex-1 btn-premium py-3 px-4 rounded-xl font-bold text-xs tracking-widest">
                                VALIDER
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </article>
    );
}
