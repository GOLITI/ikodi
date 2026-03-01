import React from "react";
import { Icon } from "@iconify/react";

const instruments = [
  {
    name: "Le Balafon Sénoufo",
    img: "/src/assets/instruments/balafon.jpeg",
    tag: "Xylophone",
    region: "Nord de la Côte d'Ivoire",
    desc: "Inscrit à l'UNESCO, le djéguélé est un chef-d'œuvre d'ingénierie acoustique séculaire qui lie intimement la nature, le sacré et le quotidien.",
    history: "Architecture Acoustique au Service de la Communauté. La présence du balafon remonte au moins au XIIIe siècle. Selon la tradition, le Sosso Bala originel était un instrument sacré du roi Soumaoro Kanté. Véritable 'instrument pont', il est l'ancêtre du marimba américain.",
    organologie: "Processus méticuleux avec rituels de sollicitation des esprits. Composé de 11 à 21 lames de bois (Pterocarpus erinaceus) et de calebasses avec mirlitons (oothèques d'araignées) pour l'effet 'buzz'. \n\nSTRUCTURE :\n- Lames : Bois de Pterocarpus (Vibration primaire)\n- Châssis : Bois ou Bambou (Support)\n- Résonateurs : Calebasses (Amplification)\n- Mirlitons : Oothèques d'araignées (Timbre granuleux)\n- Percuteurs : Baguettes & Caoutchouc (Interface homme-matière)",
    symbolisme: "Inscrit au patrimoine mondial de l'UNESCO, il représente le sommet de l'ingénierie musicale mandingue et voltaïque. Le Sosso Bala originel symbolise le pouvoir mystique royal.",
    social: "Le tafal-djéguélé rythme le labour collectif. Le musicien identifie le 'champion du champ', créant une émulation qui assure la cohésion et la sécurité alimentaire."
  },
  {
    name: "L'Ahoko Baoulé",
    img: "/src/assets/instruments/Ahoko.jpeg",
    tag: "Idiophone à Friction",
    region: "Centre de la Côte d'Ivoire",
    desc: "Instrument à friction emblématique, popularisé par Antoinette Konan, symbole de l'identité Baoulé et de la fécondité.",
    offset: true,
    history: "L'identité Baoulé en mouvement. Sa popularisation mondiale est indissociable d'Antoinette Konan qui a su intégrer cet idiophone dans des créations pop-funk visionnaires.",
    organologie: "Composé d'un bâton en bois dur finement strié et d'un racleur (coque de noix ou petite calebasse évidée). Le mouvement rythmique de va-et-vient produit une texture sonore unique.",
    symbolisme: "Représente la trinité familiale : le bâton (le père), la noix évidée (la mère) et le son produit (le fils ou la vie qui en découle).",
    social: "Régulateur des tensions sociales et vecteur de mémoire, l'ahoko est passé de la brousse aux scènes internationales."
  },
  {
    name: "L'Attoungblan",
    img: "/src/assets/instruments/Attoungblan.jpeg",
    tag: "Tambour Parleur",
    region: "Sud et Est (Akans / Ébriés)",
    desc: "Dispositif binaural capable de reproduire les tons de la langue parlée pour transmettre des messages complexes.",
    history: "Linguistique Sonore et Pouvoir Politique. Utilisé par les chefs Akans pour annoncer des décès, convoquer des assemblées ou célébrer des naissances royales.",
    organologie: "Paire de tambours : le 'mâle' (fréquences graves) et la 'femelle' (fréquences aiguës). L'instrumentiste module les frappes pour imiter la parole humaine.",
    symbolisme: "L'âme et la voix de la communauté. L'Attoungblan est le médiateur entre le monde visible et les sphères invisibles.",
    social: "Régulateur de la vie politique, sa portée peut atteindre plusieurs kilomètres pour coordonner la cité."
  },
  {
    name: "Le Djidji Ayôkwé",
    img: "/src/assets/instruments/TamTam.jpeg",
    tag: "Tambour à fente",
    region: "Sud (Ébrié/Bidjan)",
    desc: "Tambour parleur géant de 4m, symbole mondial de la restitution des biens culturels africains.",
    offset: true,
    history: "Saisi en 1916 par les troupes coloniales pour briser la résistance Ébrié, sa restitution en 2026 marque un tournant historique pour le patrimoine ivoirien.",
    organologie: "Mastodonte de bois de 430 kg taillé dans un tronc d'Iroko massif évidé. Sa voix puissante servait de radar sonore pour prévenir les invasions.",
    symbolisme: "Voix des ancêtres libérée par des rituels de purification. Il incarne la souveraineté retrouvée du peuple Bidjan.",
    social: "Régulateur de la vie sociale et gardien de la paix, il fédère aujourd'hui toute la nation autour de son retour."
  },
  {
    name: "Le Djomolo Baoulé",
    img: "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&q=80&w=800",
    tag: "Xylophone Hexatonique",
    region: "Centre (Peuple Baoulé)",
    desc: "Xylophone de six à huit lames, réputé pour son exécution en canon favorisant la détente après le dur labeur.",
    history: "Xylophone du quotidien, souvent comparé au balafon mais utilisé pour des contextes plus pragmatiques de divertissement post-labour.",
    organologie: "Composé de lames de bois libres posées sur des traverses. L'exécution se fait par deux musiciens jouant avec un léger décalage temporel (canon).",
    symbolisme: "Dualité et harmonie rythmique, cherchant l'équilibre entre la répétition et l'innovation mélodique.",
    social: "Média de relaxation collective, le Djomolo renforce les liens entre travailleurs après de dures heures aux champs."
  },
  {
    name: "Le Damlankosso",
    img: "/src/assets/instruments/Damlankosso.jpeg",
    tag: "Hochet Double",
    region: "Sud-Est (Peuple Abouré)",
    desc: "Hochet sacré fabriqué à partir des fruits d'Oncoba Spinosa, utilisé pour la fertilité et la pêche.",
    offset: true,
    history: "Hochet de la Vie et de la Pêche, profondément ancré dans la mystique des eaux et de la forêt de la région Sud-Est.",
    organologie: "Composé de deux fruits d'Oncoba Spinosa vidés et séchés, contenant leurs graines dures, reliés par une cordelette.",
    symbolisme: "L'union des deux boules représente la dualité homme-femme ; les graines symbolisent la fertilité et la continuité de la vie.",
    social: "Utilisé lors des rituels de fertilité et par les pêcheurs, ses vibrations attirant les poissons dans les lagunes."
  }
];

export default function InstrumentScreen({ onBack, onHome, onInstrumentDetail }) {
  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-color)] text-[var(--text-color)] transition-colors duration-400">
      {/* Top nav */}
      <div className="w-full border-b border-[var(--glass-border)]">
        <div className="max-w-[1200px] mx-auto px-6 py-6 flex items-center">
          <button className="flex items-center gap-2 text-xs font-bold tracking-widest uppercase hover:scale-105 transition-transform" style={{ color: "var(--text-muted)" }} onClick={onBack}>
            <Icon icon="solar:alt-arrow-left-bold" width={18} />
            RETOUR
          </button>
        </div>
      </div>

      {/* Header */}
      <header className="text-center pt-16 pb-12 flex flex-col items-center animate-fade-in">
        <div className="flex items-center gap-2 mb-4 bg-[#E87A5D]/10 px-4 py-1.5 rounded-full border border-[#E87A5D]/20">
          <span className="w-2 h-2 rounded-full bg-[#E87A5D] animate-pulse" />
          <span className="text-[10px] font-bold text-[#E87A5D] tracking-widest uppercase">Bibliothèque Sonore Vivante</span>
        </div>
        <h1 className="text-4xl md:text-5xl font-bold mb-5 max-w-2xl leading-tight px-4">Patrimoine Instrumental de Côte d’Ivoire</h1>
        <p className="text-base max-w-lg font-medium leading-relaxed px-4" style={{ color: 'var(--text-muted)' }}>
          Une étude ethnomusicologique approfondie sur l'âme battante de nos cultures ancestrales.
        </p>

        <button
          onClick={() => onInstrumentDetail && onInstrumentDetail({ quiz: true })}
          className="mt-8 flex items-center gap-2 bg-[#E87A5D] text-white px-8 py-3 rounded-full font-bold shadow-lg shadow-[#E87A5D]/20 hover:scale-105 transition-transform group"
        >
          <Icon icon="solar:question-square-bold" width={20} className="group-hover:rotate-12 transition-transform" />
          TESTEZ VOS CONNAISSANCES (QUIZ)
        </button>
      </header>

      {/* Grid */}
      <main className="flex-1 pb-32">
        <div className="max-w-[1200px] mx-auto px-6 pb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-start">
            {instruments.map((inst, i) => (
              <article
                key={inst.name}
                className={`glass-card group cursor-pointer overflow-hidden hover:border-[var(--glass-border-hover)] animate-fade-in ${inst.offset ? 'lg:translate-y-12' : ''}`}
                style={{ animationDelay: `${i * 0.1}s` }}
                onClick={() => onInstrumentDetail && onInstrumentDetail(inst)}
              >
                <div className="relative aspect-[16/10] overflow-hidden bg-[var(--input-bg)]">
                  <div className="absolute top-4 right-4 z-10">
                    <span className="bg-[#E87A5D] text-white text-[10px] font-bold px-3 py-1 rounded-full shadow-lg">
                      {inst.tag}
                    </span>
                  </div>
                  <img
                    src={inst.img}
                    alt={inst.name}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&q=80&w=800'; }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-[var(--bg-color)]/80 via-transparent to-transparent opacity-60" />
                </div>

                <div className="p-6">
                  <div className="flex justify-between items-center mb-3">
                    <h2 className="text-xl font-bold">{inst.name}</h2>
                    <Icon icon="solar:arrow-right-up-linear" width={18} className="text-[#E87A5D] group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                  </div>
                  <div className="flex items-center gap-1.5 mb-4" style={{ color: 'var(--text-muted)' }}>
                    <Icon icon="solar:map-point-bold" width={14} className="text-[#E87A5D]" />
                    <span className="text-xs font-bold uppercase tracking-wider">{inst.region}</span>
                  </div>
                  <p className="text-sm font-medium leading-relaxed line-clamp-2" style={{ color: 'var(--text-dim)' }}>
                    {inst.desc}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </main>

      {/* Navigation Bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6">
        <div className="max-w-md mx-auto glass rounded-2xl p-2 flex justify-between items-center shadow-2xl">
          <button
            onClick={onHome}
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:home-angle-bold" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Accueil</span>
          </button>

          <button
            className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2"
          >
            <Icon icon="solar:vinyl-bold" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Musée</span>
          </button>

          <button
            onClick={() => onHome && onHome()} // Fallback to home for now
            className="flex-1 flex flex-col items-center gap-1 transition-colors py-2"
            style={{ color: 'var(--text-muted)' }}
          >
            <Icon icon="solar:chart-square-linear" width={22} />
            <span className="text-[10px] font-bold uppercase tracking-tighter">Progrès</span>
          </button>

          <button
            onClick={() => onHome && onHome()} // Fallback to home for now
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
