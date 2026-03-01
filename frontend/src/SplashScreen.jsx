import React from "react";

export default function SplashScreen() {
  return (
    <div className="min-h-screen relative flex flex-col items-center justify-center bg-[var(--bg-color)] text-[var(--text-color)] overflow-hidden font-sans">
      <div className="bg-mesh" />

      {/* Main Content Container */}
      <main className="relative z-10 flex flex-col items-center justify-center w-full max-w-md px-6 animate-fade-in">
        {/* Logo Section */}
        <div className="relative flex flex-col items-center justify-center mb-6">
          <div className="w-24 h-24 rounded-[2rem] bg-gradient-to-br from-[#E87A5D] to-[#B25944] flex items-center justify-center shadow-2xl shadow-[#E87A5D]/30 mb-8 animate-bounce" style={{ animationDuration: '2.5s' }}>
            <span className="text-white font-black text-5xl tracking-tighter">I</span>
          </div>

          <h1 className="text-6xl md:text-7xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-[var(--text-color)] via-[var(--text-color)] to-[var(--text-muted)] drop-shadow-sm">
            IKODI
          </h1>
        </div>

        {/* Tagline */}
        <div className="flex items-center gap-2 mt-4 bg-[#E87A5D]/10 px-4 py-2 rounded-full border border-[#E87A5D]/20">
          <span className="w-2 h-2 rounded-full bg-[#E87A5D] animate-pulse" />
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#E87A5D]">
            Héritage & Technologie
          </p>
        </div>
      </main>

      {/* Subtle Loading Indicator at Bottom */}
      <div className="absolute bottom-16 left-1/2 -translate-x-1/2 flex flex-col items-center gap-4 animate-fade-in" style={{ animationDelay: '0.5s' }}>
        <div className="w-12 h-12 rounded-full glass flex items-center justify-center">
          <div className="w-6 h-6 border-4 border-[#E87A5D]/20 border-t-[#E87A5D] rounded-full animate-spin" />
        </div>
        <div className="text-[10px] font-bold tracking-widest uppercase" style={{ color: 'var(--text-muted)' }}>
          Chargement
        </div>
      </div>
    </div>

  );
}
