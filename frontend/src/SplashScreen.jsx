import React from "react";

export default function SplashScreen() {
  return (
    <div className="bg-gradient-to-b from-[#1B4332] to-[#0A1A12] min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden antialiased selection:bg-[#D4AF37]/30 selection:text-white">
      {/* Subtle African-inspired Geometric Pattern Overlay */}
      <div
        className="absolute inset-0 pointer-events-none mix-blend-overlay"
        style={{
          background:
            "linear-gradient(135deg, rgba(212,175,55,0.03) 25%, transparent 25%) -20px 0, " +
            "linear-gradient(225deg, rgba(212,175,55,0.03) 25%, transparent 25%) -20px 0, " +
            "linear-gradient(315deg, rgba(212,175,55,0.03) 25%, transparent 25%), " +
            "linear-gradient(45deg, rgba(212,175,55,0.03) 25%, transparent 25%)",
          backgroundSize: "40px 40px",
        }}
      ></div>

      {/* Soft Radial Light Behind Logo */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[150vw] md:w-[60vw] aspect-square rounded-full bg-[#D4AF37]/5 blur-[100px] pointer-events-none"></div>

      {/* Main Content Container */}
      <main className="relative z-10 flex flex-col items-center justify-center w-full max-w-md px-6">
        {/* Logo Section with Glowing Effect */}
        <div
          className="relative flex flex-col items-center justify-center animate-pulse"
          style={{ animationDuration: "3s" }}
        >
          {/* Subtle backdrop shadow for extra depth */}
          <div className="absolute inset-0 bg-[#D4AF37]/20 blur-2xl rounded-full scale-150"></div>

          <h1 className="relative text-6xl md:text-7xl font-semibold tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-[#FFF5D1] via-[#D4AF37] to-[#8C7323] pb-2 drop-shadow-[0_0_15px_rgba(212,175,55,0.3)]">
            Ivoiria
          </h1>
        </div>

        {/* Tagline */}
        <p className="mt-8 text-xs md:text-sm uppercase tracking-[0.25em] text-[#D4AF37]/70 font-normal text-center max-w-[280px] leading-relaxed">
          Préserver la culture<br />par la technologie
        </p>
      </main>

      {/* Subtle Loading Indicator at Bottom */}
      <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3">
        <span>
          <iconify-icon
            icon="solar:spinner-linear"
            class="text-xl text-[#D4AF37]/40 animate-spin"
            style={{ strokeWidth: 1.5 }}
          ></iconify-icon>
        </span>
        <div className="w-12 h-[1px] bg-gradient-to-r from-transparent via-[#D4AF37]/20 to-transparent"></div>
      </div>
    </div>
  );
}
