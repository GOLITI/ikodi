import React, { useState, useEffect } from "react";
import { Icon } from "@iconify/react";
import { useDioulaAPI } from "./hooks/useDioulaAPI";

export default function LearningPath({ navigate, setSelectedLessonId }) {
  const { getLessons, loading } = useDioulaAPI();
  const [lessons, setLessons] = useState([]);
  const [completedLessonIds, setCompletedLessonIds] = useState([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    async function fetchLessons() {
      const data = await getLessons();
      if (data && data.lessons) {
        setLessons(data.lessons);
      }
    }
    fetchLessons();

    // Load progress from localStorage
    const saved = JSON.parse(localStorage.getItem('completed_dioula_lessons') || '[]');
    setCompletedLessonIds(saved);
  }, [getLessons]);

  // Calculate overall completion percentage for the hero card
  useEffect(() => {
    if (lessons.length > 0) {
      const percentage = Math.round((completedLessonIds.length / lessons.length) * 100);
      setProgress(percentage);
    }
  }, [lessons, completedLessonIds]);

  const handleStartLesson = (id) => {
    setSelectedLessonId(id);
    navigate('lessonSystem');
  };

  if (loading && lessons.length === 0) {
    return (
      <div className="min-h-screen bg-[var(--bg-color)] flex items-center justify-center">
        <Icon icon="solar:spinner-bold" width={48} className="animate-spin text-[#E87A5D]" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] pb-24 font-sans relative overflow-hidden">
      <div className="bg-mesh" />

      {/* Floating Header */}
      <header className="sticky top-0 z-50 p-6 glass border-b border-[var(--glass-border)] flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('home')} className="p-2 hover:bg-[var(--input-bg)] rounded-xl transition-colors">
            <Icon icon="solar:alt-arrow-left-bold" width={24} />
          </button>
          <div>
            <h1 className="text-xl font-black tracking-tight uppercase">Parcours Dioula</h1>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#E87A5D]">Maîtrise la culture Ivoirienne</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 bg-[#E87A5D]/10 px-3 py-1.5 rounded-full text-[#E87A5D]">
            <Icon icon="solar:fire-bold" width={14} />
            <span className="text-xs font-black">12</span>
          </div>
          <div className="flex items-center gap-1.5 bg-[#FFB84D]/10 px-3 py-1.5 rounded-full text-[#FFB84D]">
            <Icon icon="solar:star-bold" width={14} />
            <span className="text-xs font-black">450</span>
          </div>
        </div>
      </header>

      {/* Hero Stats */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="glass-card p-8 flex items-center justify-between overflow-hidden relative">
          <div className="absolute -right-10 top-0 opacity-10">
            <Icon icon="solar:book-bookmark-bold" width={240} />
          </div>

          <div className="relative z-10 w-2/3">
            <h2 className="text-xs font-bold uppercase tracking-widest text-[#E87A5D] mb-1">Section 1</h2>
            <h3 className="text-2xl font-black mb-4 tracking-tighter uppercase">Les Fondations</h3>
            <div className="w-full h-3 bg-[var(--bg-color)] rounded-full overflow-hidden border border-[var(--glass-border)]">
              <div className="h-full bg-gradient-to-r from-[#E87A5D] to-[#FFB84D] transition-all duration-1000" style={{ width: `${progress}%` }} />
            </div>
            <p className="text-[10px] font-bold uppercase tracking-widest mt-3 text-[var(--text-muted)]">{progress}% de complétion du niveau</p>
          </div>

          <div className="text-right flex flex-col items-end">
            <div className="w-14 h-14 bg-[#E87A5D]/20 rounded-2xl flex items-center justify-center text-[#E87A5D] mb-2 animate-pulse">
              <Icon icon="solar:crown-bold" width={28} />
            </div>
            <span className="text-[10px] font-black uppercase tracking-widest">Niveau 1</span>
          </div>
        </div>
      </div>

      {/* Vertical Path */}
      <main className="max-w-md mx-auto px-6 relative py-12">
        {/* Track Line */}
        <div className="absolute left-1/2 -translate-x-1/2 top-0 bottom-0 w-2.5 bg-[var(--input-bg)] rounded-full border border-[var(--glass-border)]" />

        <div className="relative space-y-24 flex flex-col items-center">
          {lessons.map((lesson, idx) => {
            const isDone = completedLessonIds.includes(lesson.id);
            // Lock if previous lesson is NOT done. First lesson (idx 0) is never locked by previous.
            const isLocked = idx > 0 && !completedLessonIds.includes(lessons[idx - 1].id);
            const isActive = !isDone && !isLocked;

            // Zigzag alignment
            const xShift = idx % 2 === 0 ? '-30%' : '30%';

            return (
              <div
                key={lesson.id}
                className="relative group w-full flex flex-col items-center animate-fade-in"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                {/* Connector Glow */}
                {isActive && (
                  <div className="absolute -inset-4 bg-[#E87A5D]/10 blur-xl rounded-full animate-pulse z-0" />
                )}

                <button
                  onClick={() => handleStartLesson(lesson.id)}
                  disabled={isLocked}
                  className={`
                    w-20 h-20 rounded-[2rem] relative z-10 border-4 transition-all duration-500 hover:scale-110 active:scale-95 flex items-center justify-center shadow-2xl
                    ${isDone ? 'bg-gradient-to-br from-green-400 to-green-600 border-green-200' : ''}
                    ${isActive ? 'bg-gradient-to-br from-[#E87A5D] to-[#B25944] border-orange-200 rotate-12 scale-110' : ''}
                    ${isLocked ? 'bg-[var(--input-bg)] border-[var(--glass-border)] opacity-60 grayscale' : ''}
                  `}
                  style={{ transform: `translateX(${xShift}) ${isActive ? 'scale(1.15) rotate(12deg)' : ''}` }}
                >
                  <Icon
                    icon={isLocked ? "solar:lock-bold" : (lesson.emoji || "solar:book-2-bold")}
                    width={52}
                    className={isLocked ? "text-[var(--text-muted-more)]" : "text-white"}
                  />

                  {isDone && (
                    <div className="absolute -bottom-1 -right-1 w-7 h-7 bg-white rounded-full flex items-center justify-center text-green-600 border-2 border-green-500 shadow-lg">
                      <Icon icon="solar:check-circle-bold" width={18} />
                    </div>
                  )}

                  {isActive && (
                    <div className="absolute -top-10 bg-[#E87A5D] text-white text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-lg border-2 border-orange-200 shadow-xl animate-bounce">
                      En cours
                    </div>
                  )}
                </button>

                <div className={`mt-4 text-center absolute -bottom-16 w-48`} style={{ transform: `translateX(${xShift})` }}>
                  <h4 className={`text-sm font-black tracking-tight transition-colors ${isActive ? 'text-[var(--text-color)]' : 'text-[var(--text-muted)]'}`}>
                    {lesson.title}
                  </h4>
                  <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#E87A5D]/70">{lesson.phrase_count} Expressions</p>
                </div>
              </div>
            );
          })}
        </div>
      </main>

      {/* Floating Chat Button */}
      <button
        onClick={() => navigate('aiConversationLesson')}
        className="fixed bottom-32 right-6 w-16 h-16 btn-premium rounded-3xl shadow-2xl flex items-center justify-center group overflow-hidden"
      >
        <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" />
        <Icon icon="solar:magic-stick-3-bold" width={44} />
      </button>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 px-6 pb-6">
        <div className="max-w-md mx-auto glass rounded-2xl p-2 flex justify-between items-center shadow-2xl border border-[var(--glass-border)]">
          <button onClick={() => navigate('home')} className="flex-1 flex flex-col items-center gap-1 transition-colors py-2" style={{ color: 'var(--text-muted)' }}>
            <Icon icon="solar:home-angle-linear" width={22} />
            <span className="text-[10px] font-black uppercase tracking-tighter">Accueil</span>
          </button>
          <button className="flex-1 flex flex-col items-center gap-1 text-[#E87A5D] py-2">
            <Icon icon="solar:book-2-bold" width={22} />
            <span className="text-[10px] font-black uppercase tracking-tighter">Langue</span>
          </button>
          <button onClick={() => navigate('progress')} className="flex-1 flex flex-col items-center gap-1 transition-colors py-2" style={{ color: 'var(--text-muted)' }}>
            <Icon icon="solar:chart-square-linear" width={22} />
            <span className="text-[10px] font-black uppercase tracking-tighter">Progrès</span>
          </button>
          <button onClick={() => navigate('profile')} className="flex-1 flex flex-col items-center gap-1 transition-colors py-2" style={{ color: 'var(--text-muted)' }}>
            <Icon icon="solar:user-rounded-linear" width={22} />
            <span className="text-[10px] font-black uppercase tracking-tighter">Profil</span>
          </button>
        </div>
      </nav>
    </div>
  );
}
