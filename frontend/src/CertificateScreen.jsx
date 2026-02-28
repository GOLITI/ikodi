import React from "react";
import Icon from "./Icon";

export default function CertificateScreen({ navigate }) {
  return (
    <div className="bg-[#F8F6F0] min-h-screen flex flex-col justify-center items-center p-4 sm:p-8 md:p-12 font-sans text-stone-800 antialiased" style={{ minHeight: '100vh' }}>
      {/* Certificate Wrapper */}
      <div className="relative w-full max-w-5xl bg-white overflow-hidden flex flex-col items-center justify-center" style={{ boxShadow: '0 40px 80px -20px rgba(0, 0, 0, 0.08)', minHeight: 'clamp(600px, 80vh, 900px)' }}>
        {/* Decorative Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
          <div className="absolute -top-[30%] -left-[10%] w-[60%] h-[60%] bg-gradient-to-br from-stone-50 to-transparent rounded-full blur-3xl opacity-60"></div>
          <div className="absolute -bottom-[30%] -right-[10%] w-[60%] h-[60%] bg-gradient-to-tl from-[#C2A362]/5 to-transparent rounded-full blur-3xl opacity-60"></div>
        </div>
        {/* Outer Border */}
        <div className="absolute inset-0 border-[3px] m-4 sm:m-6 pointer-events-none z-20" style={{ borderColor: '#C2A362', opacity: 0.85 }}></div>
        {/* Inner Border */}
        <div className="absolute inset-0 border m-6 sm:m-8 pointer-events-none z-20" style={{ borderColor: '#C2A362', opacity: 0.3 }}></div>
        {/* Content Container */}
        <div className="relative z-10 w-full p-10 sm:p-16 md:p-24 flex flex-col h-full items-center text-center justify-between">
          {/* Header / App Logo */}
          <div className="flex flex-col items-center mb-10 sm:mb-16">
            <div className="flex items-center justify-center w-12 h-12 rounded-full border border-stone-200 mb-3 bg-white shadow-sm">
              <span className="text-xl font-medium tracking-tighter text-stone-900 uppercase">C</span>
            </div>
            <div className="h-8 w-px bg-stone-200"></div>
          </div>
          {/* Main Certificate Body */}
          <div className="flex-1 flex flex-col items-center justify-center w-full max-w-4xl">
            <p className="text-xs sm:text-sm uppercase tracking-widest text-stone-400 font-medium mb-8 sm:mb-12">This certifies that</p>
            {/* Recipient Name */}
            <h1 className="text-5xl sm:text-7xl md:text-8xl font-medium text-stone-900 tracking-tight leading-none mb-10 pb-6 border-b border-stone-100 w-full" style={{ fontFamily: 'Georgia, Times New Roman, serif' }}>
              Eleanor Vance
            </h1>
            <p className="text-sm sm:text-base text-stone-500 leading-relaxed mb-10 max-w-2xl">
              has successfully completed the comprehensive assessment program, demonstrating exceptional proficiency, and is hereby officially awarded the
            </p>
            {/* Certificate Title */}
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-medium tracking-tight mt-2" style={{ color: '#C2A362', fontFamily: 'Georgia, Times New Roman, serif' }}>
              Certificate of Cultural Achievement
            </h2>
          </div>
          {/* Footer Details */}
          <div className="w-full grid grid-cols-1 sm:grid-cols-3 gap-10 items-end mt-16 sm:mt-24 text-left relative pt-10">
            {/* Top Separator Line for Footer */}
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-stone-200 to-transparent opacity-60"></div>
            {/* Left: Date & Score */}
            <div className="flex flex-col gap-6 order-2 sm:order-1">
              <div>
                <p className="text-xs uppercase tracking-widest text-stone-400 mb-1 border-b border-stone-100 pb-1.5 w-max">Date of Issue</p>
                <p className="text-base font-medium text-stone-800 pt-1.5">October 24, 2023</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-widest text-stone-400 mb-1 border-b border-stone-100 pb-1.5 w-max">Final Score</p>
                <p className="text-base font-medium text-stone-800 pt-1.5">98% — Distinction</p>
              </div>
            </div>
            {/* Center: Seal Placeholder */}
            <div className="flex justify-center items-center opacity-90 order-1 sm:order-2 mb-8 sm:mb-0">
              <div className="relative flex items-center justify-center w-24 h-24 rounded-full border border-[#C2A362]/20 bg-white">
                <div className="absolute inset-1 rounded-full border border-[#C2A362]/30 border-dashed"></div>
                <Icon icon="solar:star-circle-linear" className="text-5xl" style={{ color: '#C2A362', strokeWidth: 1.5 }} />
              </div>
            </div>
            {/* Right: QR Verification */}
            <div className="flex flex-col items-end text-right order-3">
              <div className="p-3 border border-stone-200 rounded-xl bg-stone-50 mb-3 hover:border-stone-300 transition-colors duration-300 shadow-sm">
                <Icon icon="solar:qr-code-linear" className="text-6xl text-stone-800 block" style={{ strokeWidth: 1.5 }} />
              </div>
              <p className="text-xs uppercase tracking-widest text-stone-400">Verify Record</p>
              <p className="text-xs text-stone-400 mt-1 font-mono tracking-wider">ID: CA-902-881</p>
            </div>
          </div>
        </div>
      </div>
      {/* Barre de navigation en bas */}
      <nav className="fixed bottom-0 left-0 w-full bg-white border-t border-stone-200 flex justify-around items-center py-2 z-50">
        <button onClick={() => navigate('home')} className="flex flex-col items-center text-xs text-stone-700 focus:outline-none">
          <Icon icon="solar:home-2-linear" className="text-xl mb-1" />
          Accueil
        </button>
        <button onClick={() => navigate('progress')} className="flex flex-col items-center text-xs text-stone-700 focus:outline-none">
          <Icon icon="solar:chart-2-linear" className="text-xl mb-1" />
          Progression
        </button>
        <button onClick={() => navigate('certificate')} className="flex flex-col items-center text-xs text-[#C2A362] font-semibold focus:outline-none">
          <Icon icon="solar:award-star-linear" className="text-xl mb-1" />
          Certificat
        </button>
        <button onClick={() => navigate('profile')} className="flex flex-col items-center text-xs text-stone-700 focus:outline-none">
          <Icon icon="solar:user-linear" className="text-xl mb-1" />
          Profil
        </button>
      </nav>
    </div>
  );
}
