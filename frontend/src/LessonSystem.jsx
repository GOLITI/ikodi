import React, { useState, useEffect, useCallback } from "react";
import { Icon } from "@iconify/react";
import { useDioulaAPI } from "./hooks/useDioulaAPI";

export default function LessonSystem({ lessonId, onBack, navigate }) {
    const { getLesson, checkAnswer, getAudioUrl, loading, error } = useDioulaAPI();
    const [lesson, setLesson] = useState(null);
    const [step, setStep] = useState(0); // 0: Content, 1: Quiz
    const [quizIndex, setQuizIndex] = useState(0);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(null);
    const [explanation, setExplanation] = useState("");
    const [score, setScore] = useState(0);
    const [completed, setCompleted] = useState(false);
    const [isPlaying, setIsPlaying] = useState(null);

    useEffect(() => {
        async function load() {
            if (lessonId) {
                const data = await getLesson(lessonId);
                if (data) setLesson(data);
            }
        }
        load();
    }, [lessonId, getLesson]);

    useEffect(() => {
        if (completed && lessonId) {
            const completedLessons = JSON.parse(localStorage.getItem('completed_dioula_lessons') || '[]');
            if (!completedLessons.includes(lessonId)) {
                completedLessons.push(lessonId);
                localStorage.setItem('completed_dioula_lessons', JSON.stringify(completedLessons));
            }
        }
    }, [completed, lessonId]);

    const handlePlayAudio = (text, index) => {
        setIsPlaying(index);
        const audio = new Audio(getAudioUrl(text));
        audio.onended = () => setIsPlaying(null);
        audio.play().catch(e => {
            console.error("Audio playback failed", e);
            setIsPlaying(null);
        });
    };

    const handleCheckAnswer = async (optionIndex) => {
        if (selectedOption !== null) return;
        setSelectedOption(optionIndex);
        const result = await checkAnswer(lessonId, lesson.quiz[quizIndex].id, optionIndex);
        setIsCorrect(result.correct);
        setExplanation(result.explanation);
        if (result.correct) {
            setScore(s => s + 10);
        }
    };

    const nextStep = () => {
        if (step === 0) {
            setStep(1);
        } else if (quizIndex < (lesson.quiz?.length || 0) - 1) {
            setQuizIndex(quizIndex + 1);
            setSelectedOption(null);
            setIsCorrect(null);
            setExplanation("");
        } else {
            setCompleted(true);
        }
    };

    if (loading && !lesson) return (
        <div className="min-h-screen flex items-center justify-center bg-[var(--bg-color)]">
            <div className="flex flex-col items-center gap-4">
                <Icon icon="solar:spinner-bold" className="animate-spin text-[#E87A5D]" width={48} />
                <p className="text-[var(--text-muted)] animate-pulse font-bold tracking-widest text-xs uppercase">Initialisation de la leçon...</p>
            </div>
        </div>
    );

    if (error || !lesson) return (
        <div className="min-h-screen flex items-center justify-center bg-[var(--bg-color)] p-6">
            <div className="glass-card p-10 text-center max-w-md">
                <Icon icon="solar:danger-bold" width={64} className="text-red-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold mb-2">Oups !</h2>
                <p className="text-[var(--text-dim)] mb-6">Impossible de charger la leçon. Vérifiez votre connexion au serveur Langue.</p>
                <button onClick={onBack} className="btn-premium w-full">Retour au parcours</button>
            </div>
        </div>
    );

    if (completed) {
        return (
            <div className="min-h-screen bg-[var(--bg-color)] flex flex-col items-center justify-center p-6 animate-fade-in">
                <div className="glass-card p-12 text-center max-w-lg w-full relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-2 bg-[#E87A5D]" />
                    <Icon icon="solar:medal-ribbon-star-bold" width={80} className="mx-auto mb-6 text-[#E87A5D]" />
                    <h2 className="text-3xl font-black mb-2 tracking-tighter uppercase">Leçon Terminée !</h2>
                    <p className="text-lg font-medium mb-8" style={{ color: 'var(--text-dim)' }}>
                        Félicitations ! Tu as maîtrisé : <br />
                        <span className="text-[var(--text-color)] font-bold">"{lesson.title}"</span>
                    </p>
                    <div className="bg-[var(--input-bg)] rounded-3xl p-8 mb-8 border border-[var(--glass-border)]">
                        <span className="text-5xl font-black text-[#E87A5D]">+{score}</span>
                        <p className="text-xs font-bold uppercase tracking-widest mt-2" style={{ color: 'var(--text-muted)' }}>Points XP Gagnés</p>
                    </div>
                    <button
                        onClick={onBack}
                        className="w-full btn-premium py-5 text-lg"
                    >
                        CONTINUER MON APPRENTISSAGE
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] flex flex-col font-sans transition-colors duration-400">
            <div className="bg-mesh" />

            {/* Header */}
            <header className="p-6 flex items-center justify-between border-b border-[var(--glass-border)] glass sticky top-0 z-50">
                <button onClick={onBack} className="p-2 hover:bg-[var(--input-bg)] rounded-xl transition-colors">
                    <Icon icon="solar:close-circle-linear" width={24} />
                </button>

                <div className="flex-1 px-8">
                    <div className="h-2 w-full bg-[var(--input-bg)] rounded-full overflow-hidden">
                        <div
                            className="h-full bg-[#E87A5D] transition-all duration-700 ease-out"
                            style={{ width: `${step === 0 ? 50 : 50 + (quizIndex + 1) / (lesson.quiz?.length || 1) * 50}%` }}
                        />
                    </div>
                </div>

                <div className="flex items-center gap-2 text-[#FFB84D]">
                    <Icon icon="solar:star-bold" width={20} />
                    <span className="font-bold text-sm tracking-widest">{score}</span>
                </div>
            </header>

            <main className="flex-1 flex flex-col items-center py-12 px-6 max-w-2xl mx-auto w-full">
                {step === 0 ? (
                    /* Content Mode */
                    <div className="w-full animate-fade-in">
                        <header className="text-center mb-12">
                            <span className="text-xs font-bold uppercase tracking-[0.3em] text-[#E87A5D] mb-2 block">Cours Interactif</span>
                            <h1 className="text-4xl font-black tracking-tighter mb-4">{lesson.title}</h1>
                            <p className="text-[var(--text-dim)] font-medium">Écoutez attentivement et répétez ces expressions essentielles.</p>
                        </header>

                        <div className="space-y-4">
                            {lesson.content.map((item, idx) => (
                                <div
                                    key={idx}
                                    className="glass-card p-6 flex items-center justify-between group hover:border-[#E87A5D]/50 transition-all cursor-pointer"
                                    onClick={() => handlePlayAudio(item.dioula, idx)}
                                >
                                    <div className="flex items-center gap-5">
                                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all ${isPlaying === idx ? 'bg-[#E87A5D] text-white animate-pulse' : 'bg-[#E87A5D]/10 text-[#E87A5D]'}`}>
                                            <Icon icon={isPlaying === idx ? "solar:pause-bold" : "solar:play-bold"} width={20} />
                                        </div>
                                        <div>
                                            <p className="text-xl font-black tracking-tight mb-1">{item.dioula}</p>
                                            <p className="text-sm font-medium" style={{ color: 'var(--text-muted)' }}>{item.french}</p>
                                        </div>
                                    </div>
                                    <Icon icon="solar:volume-loud-bold" className="text-[var(--text-muted-more)] group-hover:text-[#E87A5D] transition-colors" width={20} />
                                </div>
                            ))}
                        </div>

                        <button
                            onClick={nextStep}
                            className="w-full btn-premium mt-12 py-5 text-lg font-black tracking-widest"
                        >
                            PRÊT POUR LE QUIZ ?
                            <Icon icon="solar:alt-arrow-right-bold" width={24} />
                        </button>
                    </div>
                ) : (
                    /* Quiz Mode */
                    <div className="w-full animate-fade-in" key={quizIndex}>
                        <header className="text-center mb-12">
                            <span className="text-xs font-bold uppercase tracking-[0.3em] text-[#FFB84D] mb-2 block">Défis du Savoir</span>
                            <h2 className="text-2xl font-black tracking-tight px-4 leading-tight">
                                {lesson.quiz[quizIndex].question}
                            </h2>
                        </header>

                        <div className="grid gap-4 mb-8">
                            {lesson.quiz[quizIndex].options.map((opt, idx) => {
                                const isSelected = selectedOption === idx;
                                const showSuccess = isSelected && isCorrect;
                                const showFailure = isSelected && isCorrect === false;

                                return (
                                    <button
                                        key={idx}
                                        disabled={selectedOption !== null}
                                        onClick={() => handleCheckAnswer(idx)}
                                        className={`
                      w-full p-6 rounded-2xl border-2 text-left font-bold text-lg transition-all flex items-center justify-between group
                      ${isSelected ? '' : 'bg-[var(--input-bg)] border-[var(--glass-border)] hover:border-[var(--glass-border-hover)]'}
                      ${showSuccess ? 'bg-green-500/10 border-green-500' : ''}
                      ${showFailure ? 'bg-red-500/10 border-red-500' : ''}
                    `}
                                    >
                                        <span>{opt}</span>
                                        <div className={`
                      w-8 h-8 rounded-lg flex items-center justify-center border-2 transition-all
                      ${isSelected ? '' : 'border-[var(--glass-border)] group-hover:border-[var(--text-muted)]'}
                      ${showSuccess ? 'bg-green-500 border-green-500 text-white' : ''}
                      ${showFailure ? 'bg-red-500 border-red-500 text-white' : ''}
                    `}>
                                            {idx === 0 ? 'A' : idx === 1 ? 'B' : 'C'}
                                        </div>
                                    </button>
                                );
                            })}
                        </div>

                        {selectedOption !== null && (
                            <div className={`p-6 rounded-2xl border mb-8 animate-fadeInUp ${isCorrect ? 'bg-green-500/5 border-green-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
                                <div className="flex items-center gap-2 mb-2">
                                    <Icon icon={isCorrect ? "solar:check-circle-bold" : "solar:danger-bold"} width={20} className={isCorrect ? "text-green-500" : "text-red-500"} />
                                    <span className={`text-xs font-black uppercase tracking-widest ${isCorrect ? "text-green-500" : "text-red-500"}`}>
                                        {isCorrect ? "Excellent !" : "Oups ! La réponse était :"}
                                    </span>
                                </div>
                                <p className="text-sm font-medium leading-relaxed" style={{ color: 'var(--text-dim)' }}>
                                    {explanation}
                                </p>
                            </div>
                        )}

                        {selectedOption !== null && (
                            <button
                                onClick={nextStep}
                                className="w-full btn-premium py-5 text-lg"
                            >
                                CONTINUER
                                <Icon icon="solar:arrow-right-bold" width={24} />
                            </button>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}
