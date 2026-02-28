import React, { useState, useEffect } from "react";
import { Icon } from "@iconify/react";
import QuizInstrument from "./QuizInstrument";
import { useDioulaAPI } from "./hooks/useDioulaAPI";

const InstrumentDetail = ({ onBack, onQuiz, instrument }) => {
  const [showQuiz, setShowQuiz] = useState(false);
  const { getAudioUrl } = useDioulaAPI();
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioInstance, setAudioInstance] = useState(null);

  useEffect(() => {
    if (instrument?.quiz) {
      setShowQuiz(true);
    }
  }, [instrument]);

  const handleListen = () => {
    if (isPlaying && audioInstance) {
      audioInstance.pause();
      setIsPlaying(false);
      return;
    }

    const textToRead = `${inst.name}. ${inst.desc}. Histoire : ${inst.history}. Organologie : ${inst.organologie}. Symbolisme : ${inst.symbolisme}. Fonctions sociales : ${inst.social}`;
    const url = getAudioUrl(textToRead);
    const audio = new Audio(url);

    audio.onplay = () => setIsPlaying(true);
    audio.onended = () => setIsPlaying(false);
    audio.onerror = () => {
      console.error("Audio playback error");
      setIsPlaying(false);
    };

    setAudioInstance(audio);
    audio.play();
  };

  // Stop audio on unmount
  useEffect(() => {
    return () => {
      if (audioInstance) {
        audioInstance.pause();
      }
    };
  }, [audioInstance]);

  const inst = instrument || {
    name: "Le Balafon Sénoufo",
    img: "/src/assets/instruments/balafon.jpeg",
    tag: "Xylophone",
    region: "Nord de la Côte d'Ivoire",
    desc: "Inscrit à l'UNESCO, le djéguélé est un chef-d'œuvre d'ingénierie acoustique séculaire qui lie intimement la nature, le sacré et le quotidien.",
    history: "Architecture Acoustique au Service de la Communauté. La présence du balafon remonte au moins au XIIIe siècle. Selon la tradition, le Sosso Bala originel était un instrument sacré du roi Soumaoro Kanté. Véritable 'instrument pont', il est l'ancêtre du marimba américain.",
    organologie: "Processus méticuleux avec rituels de sollicitation des esprits. Composé de 11 à 21 lames de bois (Pterocarpus erinaceus) et de calebasses avec mirlitons (oothèques d'araignées) pour l'effet 'buzz'. \n\nSTRUCTURE :\n- Lames : Bois de Pterocarpus (Vibration primaire)\n- Châssis : Bois ou Bambou (Support)\n- Résonateurs : Calebasses (Amplification)\n- Mirlitons : Oothèques d'araignées (Timbre granuleux)\n- Percuteurs : Baguettes & Caoutchouc (Interface homme-matière)",
    symbolisme: "Inscrit au patrimoine mondial de l'UNESCO, il représente le sommet de l'ingénierie musicale mandingue et voltaïque.",
    social: "Le tafal-djéguélé rythme le labour collectif, moteur de productivité et de cohésion sociale."
  };

  if (showQuiz) {
    return (
      <QuizInstrument
        onExit={() => setShowQuiz(false)}
      />
    );
  }

  return (
    <div className="bg-[var(--bg-color)] min-h-screen text-[var(--text-color)] transition-colors duration-400 relative pb-28">
      {/* Hero image */}
      <div className="relative w-full h-[45vh] overflow-hidden">
        <img
          src={inst.img}
          alt={inst.name}
          className="w-full h-full object-cover grayscale-[0.2] hover:grayscale-0 transition-all duration-700"
          onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&q=80&w=800'; }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-color)] via-transparent to-transparent opacity-90" />

        {/* Floating nav */}
        <div className="absolute top-0 left-0 right-0 z-20 flex justify-between items-center px-6 py-8">
          <button
            className="w-10 h-10 rounded-full bg-black/20 backdrop-blur-xl flex items-center justify-center hover:bg-[#E87A5D] transition-colors text-white"
            aria-label="Retour"
            onClick={onBack}
          >
            <Icon icon="solar:arrow-left-linear" width="22" />
          </button>
          <div className="bg-black/20 backdrop-blur-xl px-4 py-1.5 rounded-full border border-white/10">
            <span className="font-bold uppercase tracking-widest text-[10px] text-white">{inst.tag}</span>
          </div>
          <button
            className="w-10 h-10 rounded-full bg-black/20 backdrop-blur-xl flex items-center justify-center hover:bg-[#E87A5D] transition-colors text-white"
            aria-label="Partager"
          >
            <Icon icon="solar:share-bold" width="20" />
          </button>
        </div>
      </div>

      {/* Content wrapper */}
      <main className="max-w-3xl mx-auto px-6 -mt-24 relative z-10 animate-fade-in">
        <div className="glass-card p-8 md:p-12 mb-10 overflow-hidden relative">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[#E87A5D]/5 rounded-bl-full -z-10" />

          <header className="mb-12">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Icon icon="solar:map-point-bold" width={16} className="text-[#E87A5D]" />
                <span className="text-xs font-bold uppercase tracking-widest text-[#E87A5D]">{inst.region}</span>
              </div>
              <button
                onClick={handleListen}
                className={`flex items-center gap-2 px-4 py-2 rounded-2xl border transition-all ${isPlaying ? 'bg-red-500 text-white border-transparent animate-pulse' : 'bg-[#E87A5D]/10 text-[#E87A5D] border-[#E87A5D]/20 hover:bg-[#E87A5D]/20'}`}
              >
                <Icon icon={isPlaying ? "solar:stop-circle-bold" : "solar:play-circle-bold"} width={18} />
                <span className="text-[10px] font-black uppercase tracking-widest">{isPlaying ? 'Arrêter' : 'Écouter l\'histoire'}</span>
              </button>
            </div>
            <h1 className="text-4xl md:text-6xl font-black mb-8 leading-tight tracking-tighter">{inst.name}</h1>
            <p className="text-xl leading-relaxed font-serif italic mb-10 border-l-4 border-[#E87A5D]/30 pl-6 py-2" style={{ color: 'var(--text-dim)' }}>
              "{inst.desc}"
            </p>

            <button
              onClick={() => setShowQuiz(true)}
              className="w-full bg-[#E87A5D] text-white px-8 py-5 rounded-3xl font-bold shadow-2xl shadow-[#E87A5D]/30 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-4 group"
            >
              <Icon icon="solar:medal-star-bold" width={28} className="group-hover:rotate-12 transition-transform" />
              COMMENCER LE QUIZ CULTUREL
            </button>
          </header>

          <div className="space-y-16">
            {/* History Section */}
            <section className="relative">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-2xl bg-[#E87A5D]/10 flex items-center justify-center text-[#E87A5D] shadow-inner">
                  <Icon icon="solar:history-bold" width={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-black tracking-tight">Histoire & Origines</h2>
                  <div className="h-1 w-12 bg-[#E87A5D] rounded-full mt-1" />
                </div>
              </div>
              <p className="text-base leading-9 font-medium text-justify" style={{ color: 'var(--text-color)' }}>
                {inst.history}
              </p>
            </section>

            {/* Organology Section */}
            <section className="relative">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-2xl bg-[#E87A5D]/10 flex items-center justify-center text-[#E87A5D] shadow-inner">
                  <Icon icon="solar:settings-bold" width={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-black tracking-tight">Organologie & Structure</h2>
                  <div className="h-1 w-12 bg-[#E87A5D] rounded-full mt-1" />
                </div>
              </div>
              <div className="text-base leading-9 font-medium whitespace-pre-wrap p-6 rounded-3xl border border-[var(--glass-border)] bg-[var(--input-bg)]" style={{ color: 'var(--text-dim)' }}>
                {inst.organologie}
              </div>
            </section>

            {/* Symbolism Section */}
            <section className="bg-[var(--input-bg)] rounded-[2.5rem] p-10 border border-[var(--glass-border)] relative overflow-hidden">
              <div className="absolute top-0 right-0 p-6 opacity-5">
                <Icon icon="solar:star-fall-2-bold" width={120} />
              </div>
              <h2 className="text-2xl font-black mb-6 flex items-center gap-4">
                <Icon icon="solar:stars-bold" width={32} className="text-[#FFB84D]" />
                Symbolisme Sacré
              </h2>
              <p className="text-base leading-9 font-medium" style={{ color: 'var(--text-color)' }}>
                {inst.symbolisme}
              </p>
            </section>

            {/* Social Function Section */}
            <section>
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 rounded-2xl bg-blue-500/10 flex items-center justify-center text-blue-500 shadow-inner">
                  <Icon icon="solar:users-group-rounded-bold" width={24} />
                </div>
                <h3 className="text-2xl font-black tracking-tight">Impact & Société</h3>
              </div>
              <p className="text-base leading-9 font-medium" style={{ color: 'var(--text-dim)' }}>
                {inst.social}
              </p>
            </section>
          </div>
        </div>
      </main>

      {/* Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6">
        <div className="max-w-md mx-auto glass rounded-[2rem] p-3 flex justify-between items-center shadow-2xl border border-white/20">
          <button
            onClick={onBack}
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:home-angle-bold-duotone" width={24} />
            <span className="text-[10px] font-black uppercase tracking-widest">Accueil</span>
          </button>

          <button
            className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
          >
            <Icon icon="solar:vinyl-bold-duotone" width={24} />
            <span className="text-[10px] font-black uppercase tracking-widest">Musée</span>
          </button>

          <button
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:graph-bold-duotone" width={24} />
            <span className="text-[10px] font-black uppercase tracking-widest">Progrès</span>
          </button>

          <button
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:user-bold-duotone" width={24} />
            <span className="text-[10px] font-black uppercase tracking-widest">Profil</span>
          </button>
        </div>
      </nav>
    </div>
  );
};

export default InstrumentDetail;