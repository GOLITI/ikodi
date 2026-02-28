import { useDioulaAPI } from "./hooks/useDioulaAPI";
import { useState, useEffect } from "react";
import { Icon } from "@iconify/react";
import React from "react";

export default function StoryScreen({ onBack, navigate }) {
  const { getAudioUrl } = useDioulaAPI();
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioInstance, setAudioInstance] = useState(null);

  const storyText = "Les murmures des ancêtres. L'air était chargé du parfum de la poussière rouge et de la myrrhe brûlée. Au-delà du cercle rassurant des feux du village, le grand baobab se dressait en sentinelle silencieuse sous une voûte étoilée. Ses branches noueuses semblaient griffer le ciel, retenant des secrets plus anciens que les anciens eux-mêmes. Tu t'éloignes de la chaleur des flammes. Le battement rythmique des djembés s'estompe, remplacé par la symphonie nocturne de la savane — le chant des grillons et l'appel lointain d'une bête solitaire. À mesure que tu approches du tronc massif, un frisson soudain et surnaturel parcourt ta peau. Les ombres à la base de l'arbre s'épaississent, tourbillonnant pour former une silhouette voûtée. Lentement, elle lève un bras ombragé, pointant vers la brousse dense et indomptée.";

  const handleListen = () => {
    if (isPlaying && audioInstance) {
      audioInstance.pause();
      setIsPlaying(false);
      return;
    }

    const url = getAudioUrl(storyText);
    const audio = new Audio(url);
    audio.onplay = () => setIsPlaying(true);
    audio.onended = () => setIsPlaying(false);
    audio.onerror = () => setIsPlaying(false);
    setAudioInstance(audio);
    audio.play();
  };

  useEffect(() => {
    return () => {
      if (audioInstance) audioInstance.pause();
    };
  }, [audioInstance]);

  return (
    <div className="app min-h-screen flex flex-col bg-[#030712] relative font-sans">
      {/* Background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <img className="w-full h-full object-cover blur-[10px] scale-110 opacity-30" src="https://images.unsplash.com/photo-1511886929837-354d827aae26?q=80&w=1000&auto=format&fit=crop" alt="" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#03071233] via-[#030712cc] to-[#030712]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(124,45,18,0.2),transparent_60%)]" />
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#030712b3] backdrop-blur border-b border-white/5">
        <div className="max-w-[1100px] mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="p-2 hover:bg-white/5 rounded-full transition-colors text-white/70">
              <Icon icon="solar:alt-arrow-left-linear" width={22} />
            </button>
            <div className="w-1 h-4 bg-[#EA580C] rounded-full" />
            <span className="text-xs font-medium uppercase tracking-widest text-[#FB923C] opacity-90">Chapitre III</span>
          </div>
          <button
            onClick={handleListen}
            className={`audio-btn w-10 h-10 rounded-full border flex items-center justify-center backdrop-blur transition ${isPlaying ? 'bg-[#EA580C] border-transparent text-white animate-pulse' : 'bg-white/5 border-white/10 text-white/70 hover:text-white hover:bg-white/10'}`}
            aria-label="Écouter"
          >
            <Icon icon={isPlaying ? "solar:stop-circle-bold" : "solar:volume-loud-linear"} width="18" />
          </button>
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 relative z-10">
        <div className="max-w-[1100px] mx-auto px-6 py-10 pb-24">
          <div className="grid md:grid-cols-[1fr_420px] gap-16 items-start">
            {/* Texte */}
            <div>
              <h1 className="font-serif text-3xl md:text-5xl font-medium text-white mb-8 leading-tight">Les murmures des ancêtres</h1>
              <div className="font-serif flex flex-col gap-6 text-[#D1D5DB] font-light leading-8 text-base md:text-lg">
                <p><span className="text-4xl text-[#FB923C] float-left leading-none mr-2 mt-1">L</span>'air était chargé du parfum de la poussière rouge et de la myrrhe brûlée. Au-delà du cercle rassurant des feux du village, le grand baobab se dressait en sentinelle silencieuse sous une voûte étoilée. Ses branches noueuses semblaient griffer le ciel, retenant des secrets plus anciens que les anciens eux-mêmes.</p>
                <p>Tu t'éloignes de la chaleur des flammes. Le battement rythmique des djembés s'estompe, remplacé par la symphonie nocturne de la savane — le chant des grillons et l'appel lointain d'une bête solitaire.</p>
                <p>À mesure que tu approches du tronc massif, un frisson soudain et surnaturel parcourt ta peau. Les ombres à la base de l'arbre s'épaississent, tourbillonnant pour former une silhouette voûtée. Lentement, elle lève un bras ombragé, pointant vers la brousse dense et indomptée.</p>
              </div>
              {/* Choix mobile */}
              <div className="flex flex-col gap-3.5 mt-10 md:hidden">
                <div className="text-xs font-medium uppercase tracking-widest text-white/30 mb-2">Que fais-tu ?</div>
                <button
                  className="choice-primary w-full bg-[#EA580C] rounded-xl py-4 px-5 text-white flex items-center justify-between gap-2 text-base font-normal hover:bg-[#F97316] transition"
                  onClick={() => navigate && navigate("suivre-silhouette")}
                >
                  <span>Suivre la silhouette</span>
                  <Icon icon="solar:arrow-right-linear" width="20" />
                </button>
                <button className="choice-secondary w-full bg-[#0A0F1A]/80 border border-[#EA580C33] rounded-xl py-4 px-5 text-[#FED7AA] flex items-center justify-between gap-2 text-base font-normal hover:bg-[#43140788] hover:border-[#EA580C66] transition">
                  <span>Retourner près du feu</span>
                  <Icon icon="solar:fire-linear" width="20" />
                </button>
              </div>
            </div>
            {/* Choix desktop */}
            <div className="choices-wrap hidden md:flex flex-col gap-3.5 sticky top-20">
              <div className="choices-label text-xs font-medium uppercase tracking-widest text-white/30 mb-2">Que fais-tu ?</div>
              <button
                className="choice-primary w-full bg-[#EA580C] rounded-xl py-4 px-5 text-white flex items-center justify-between gap-2 text-base font-normal hover:bg-[#F97316] transition"
                onClick={() => navigate && navigate("suivre-silhouette")}
              >
                <span>Suivre la silhouette</span>
                <Icon icon="solar:arrow-right-linear" width="20" />
              </button>
              <button className="choice-secondary w-full bg-[#0A0F1A]/80 border border-[#EA580C33] rounded-xl py-4 px-5 text-[#FED7AA] flex items-center justify-between gap-2 text-base font-normal hover:bg-[#43140788] hover:border-[#EA580C66] transition">
                <span>Retourner près du feu</span>
                <Icon icon="solar:fire-linear" width="20" />
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 bg-[#030712eb] backdrop-blur border-t border-white/10 py-3 px-6 z-50">
        <div className="max-w-xl mx-auto flex justify-between items-center">
          <button className="flex flex-col items-center gap-1 text-white text-xs font-medium hover:text-white/80 transition nav-item active">
            <span className="relative flex items-center justify-center">
              <Icon icon="solar:home-angle-bold" width="24" />
              <span className="absolute -top-1 -right-1 w-2 h-2 bg-[#E87A5D] rounded-full" />
            </span>
            Accueil
          </button>
          <button className="flex flex-col items-center gap-1 text-white/40 text-xs font-medium hover:text-white transition nav-item">
            <Icon icon="solar:chart-square-linear" width="24" />
            Progression
          </button>
          <button className="flex flex-col items-center gap-1 text-white/40 text-xs font-medium hover:text-white transition nav-item">
            <Icon icon="solar:diploma-linear" width="24" />
            Certificat
          </button>
          <button className="flex flex-col items-center gap-1 text-white/40 text-xs font-medium hover:text-white transition nav-item">
            <Icon icon="solar:user-rounded-linear" width="24" />
            Profil
          </button>
        </div>
      </nav>
    </div>
  );
}
