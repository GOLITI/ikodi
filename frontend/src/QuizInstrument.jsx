import React, { useState } from "react";
import { Icon } from "@iconify/react";

const instrumentQuestions = [
  {
    question: "Quel instrument ivoirien est inscrit au patrimoine immatériel de l'UNESCO ?",
    options: ["Le Djembé", "Le Balafon Sénoufo", "L'Ahoko", "Le Damlankosso"],
    correct: 1,
    explanation: "Le balafon sénoufo (ou djéguélé) est reconnu mondialement pour son ingénierie acoustique unique."
  },
  {
    question: "Quelle est la signification symbolique de la coque de noix dans l'Ahoko Baoulé ?",
    options: ["Le Père", "La Mère", "Le Fils", "La Musique"],
    correct: 1,
    explanation: "Dans la trinité familiale de l'Ahoko, la noix représente la mère, le bâton le père, et le son le fils."
  },
  {
    question: "Comment appelle-t-on le dispositif de l'Attoungblan composé de deux tambours ?",
    options: ["Un duo mono", "Une structure binaurale", "Un rythme tertiaire", "Une polyphonie"],
    correct: 1,
    explanation: "L'Attoungblan utilise une paire 'mâle' (grave) et 'femelle' (aigu) pour reproduire les tons de la parole."
  },
  {
    question: "Quel était l'usage original du Djomolo (xylophone hexatonique) ?",
    options: ["Appeler à la guerre", "Chasser les oiseaux des rizières", "Célébrer les mariages", "Communiquer entre villages"],
    correct: 1,
    explanation: "Le son percutant du Djomolo permettait d'éloigner les prédateurs dans les champs tout en trompant l'ennui."
  },
  {
    question: "Que symbolisent les graines à l'intérieur du Damlankosso chez les Abourés ?",
    options: ["Le grain de riz", "La richesse", "La fertilité et la continuité de la vie", "Le bruit de la pluie"],
    correct: 2,
    explanation: "Les boules représentent l'union homme-femme et les graines symbolisent la descendance."
  }
];

const letters = ["A", "B", "C", "D"];

export default function QuizInstrument({ onExit, onFinish }) {
  const [step, setStep] = useState(0);
  const [selected, setSelected] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);

  const q = instrumentQuestions[step];

  function handleSelect(idx) {
    if (selected !== null) return;
    setSelected(idx);
    setShowResult(true);
    if (idx === q.correct) {
      setScore(s => s + 1);
    }
  }

  function handleContinue() {
    if (step < instrumentQuestions.length - 1) {
      setStep(step + 1);
      setSelected(null);
      setShowResult(false);
    } else {
      setCompleted(true);
    }
  }

  if (completed) {
    return (
      <div className="min-h-screen bg-[var(--bg-color)] flex flex-col items-center justify-center p-6 animate-fade-in">
        <div className="glass-card p-12 text-center max-w-lg w-full relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-[#E87A5D]" />
          <Icon icon="solar:medal-star-bold" width={80} className="mx-auto mb-6 text-[#E87A5D]" />
          <h2 className="text-3xl font-black mb-2">Félicitations !</h2>
          <p className="text-lg font-medium mb-8" style={{ color: 'var(--text-dim)' }}>
            Vous avez terminé le quiz sur les instruments ivoiriens.
          </p>
          <div className="bg-[var(--input-bg)] rounded-3xl p-8 mb-8 border border-[var(--glass-border)]">
            <span className="text-5xl font-black text-[#E87A5D]">{Math.round((score / instrumentQuestions.length) * 100)}%</span>
            <p className="text-xs font-bold uppercase tracking-widest mt-2" style={{ color: 'var(--text-muted)' }}>Score Final</p>
          </div>
          <button
            onClick={onExit}
            className="w-full bg-[#E87A5D] text-white py-4 rounded-2xl font-bold shadow-xl shadow-[#E87A5D]/20 hover:scale-[1.02] active:scale-95 transition-all"
          >
            RETOURNER AU MUSÉE
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] flex flex-col font-sans transition-colors duration-400">
      <div className="flex-1 flex flex-col items-center py-12 px-6">
        {/* Header */}
        <header className="w-full max-w-xl flex items-center justify-between mb-12">
          <button
            className="w-10 h-10 rounded-full bg-[var(--input-bg)] border border-[var(--glass-border)] flex items-center justify-center text-[var(--text-muted)] hover:text-[#E87A5D] transition-colors"
            onClick={onExit}
          >
            <Icon icon="solar:arrow-left-linear" width="20" />
          </button>

          <div className="flex flex-col items-center gap-2">
            <span className="text-[10px] font-black uppercase tracking-widest text-[#E87A5D]">
              Instrument Quiz
            </span>
            <div className="flex gap-1.5">
              {instrumentQuestions.map((_, i) => (
                <div
                  key={i}
                  className={`h-1.5 rounded-full transition-all duration-500 ${i === step ? 'w-8 bg-[#E87A5D]' : i < step ? 'w-4 bg-[#E87A5D]/40' : 'w-4 bg-[var(--glass-border)]'}`}
                />
              ))}
            </div>
          </div>

          <div className="w-10 h-10 rounded-xl bg-[#E87A5D]/10 flex items-center justify-center font-black text-[#E87A5D] text-xs">
            {step + 1}
          </div>
        </header>

        {/* Question */}
        <div className="w-full max-w-xl animate-fade-in" key={step}>
          <h1 className="text-2xl md:text-3xl font-black mb-10 leading-tight text-center">
            {q.question}
          </h1>

          {/* Options */}
          <div className="grid gap-4 mb-10">
            {q.options.map((opt, idx) => {
              const matches = selected === idx;
              const isCorrect = idx === q.correct;
              const showWrong = matches && !isCorrect;
              const showRight = (showResult && isCorrect);

              return (
                <button
                  key={idx}
                  disabled={selected !== null}
                  onClick={() => handleSelect(idx)}
                  className={`
                    group flex items-center gap-4 rounded-2xl border-2 p-5 text-left transition-all duration-300
                    ${matches ? 'border-[#E87A5D] bg-[#E87A5D]/5' : 'border-[var(--glass-border)] bg-[var(--input-bg)] hover:border-[var(--glass-border-hover)]'}
                    ${showRight ? 'border-green-500 bg-green-500/10' : ''}
                    ${showWrong ? 'border-red-500 bg-red-500/10' : ''}
                  `}
                >
                  <span className={`
                    w-10 h-10 rounded-xl flex items-center justify-center font-black text-sm border-2 transition-colors
                    ${matches ? 'bg-[#E87A5D] border-[#E87A5D] text-white' : 'bg-[var(--bg-color)] border-[var(--glass-border)] text-[var(--text-muted)] group-hover:border-[var(--text-muted)]'}
                    ${showRight ? 'bg-green-500 border-green-500 text-white' : ''}
                    ${showWrong ? 'bg-red-500 border-red-500 text-white' : ''}
                  `}>
                    {letters[idx]}
                  </span>
                  <span className="flex-1 font-bold text-lg">{opt}</span>

                  {showResult && isCorrect && <Icon icon="solar:check-circle-bold" className="text-green-500" width={24} />}
                  {showWrong && <Icon icon="solar:close-circle-bold" className="text-red-500" width={24} />}
                </button>
              );
            })}
          </div>

          {/* Explanation */}
          {showResult && (
            <div className="animate-fadeInUp bg-[#E87A5D]/10 rounded-2xl p-6 border border-[#E87A5D]/20 mb-8">
              <div className="flex items-center gap-2 mb-2 text-[#E87A5D]">
                <Icon icon="solar:info-circle-bold" width={18} />
                <span className="text-xs font-black uppercase tracking-widest">Le saviez-vous ?</span>
              </div>
              <p className="text-sm font-medium leading-relaxed" style={{ color: 'var(--text-dim)' }}>
                {q.explanation}
              </p>
            </div>
          )}

          {/* Continue */}
          {showResult && (
            <button
              className="w-full bg-[var(--text-color)] text-[var(--bg-color)] py-5 rounded-3xl font-black shadow-2xl hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-3"
              onClick={handleContinue}
            >
              {step < instrumentQuestions.length - 1 ? 'QUESTION SUIVANTE' : 'VOIR LE RÉSULTAT'}
              <Icon icon="solar:arrow-right-bold" width={20} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
