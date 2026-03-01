import React, { useState, useEffect, useRef } from "react";
import { Icon } from "@iconify/react";
import { useDioulaAPI, useVoiceRecorder } from "./hooks/useDioulaAPI";

export default function ConversationAIScreen({ onBack, navigate }) {
  const { voiceInteraction, textChat, playBase64Audio, loading, error } = useDioulaAPI();
  const { recording, startRecording, stopRecording } = useVoiceRecorder();

  const [messages, setMessages] = useState([
    { role: 'ai', text: "I ni ce ! Je suis ton assistant Dioula. Pose-moi une question ou parle pour pratiquer.", audio: null }
  ]);
  const [inputText, setInputText] = useState("");
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendText = async () => {
    if (!inputText.trim()) return;

    const userMsg = { role: 'user', text: inputText };
    setMessages(prev => [...prev, userMsg]);
    setInputText("");

    const response = await textChat(inputText);
    if (response) {
      const aiMsg = {
        role: 'ai',
        text: response.ai_response,
        audio: response.response_audio_base64
      };
      setMessages(prev => [...prev, aiMsg]);
      if (response.response_audio_base64) {
        playBase64Audio(response.response_audio_base64);
      }
    }
  };

  const handleToggleRecord = async () => {
    if (recording) {
      const audioBlob = await stopRecording();
      setMessages(prev => [...prev, { role: 'user', text: "🎤 Envoi de l'audio..." }]);

      try {
        const response = await voiceInteraction(audioBlob);
        if (response) {
          // Replace last "envoi" message with actual transcription
          setMessages(prev => {
            const last = [...prev];
            last[last.length - 1] = { role: 'user', text: response.transcription };
            return [...last, {
              role: 'ai',
              text: response.ai_response,
              audio: response.response_audio_base64
            }];
          });
          if (response.response_audio_base64) {
            playBase64Audio(response.response_audio_base64);
          }
        }
      } catch (e) {
        setMessages(prev => [...prev, { role: 'ai', text: "Désolé, j'ai eu un problème avec l'audio. Réessaie ?" }]);
      }
    } else {
      await startRecording();
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[var(--bg-color)] text-[var(--text-color)] font-sans relative overflow-hidden">
      <div className="bg-mesh" />

      {/* Header */}
      <header className="p-6 glass border-b border-[var(--glass-border)] flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-[var(--input-bg)] rounded-xl transition-colors">
            <Icon icon="solar:alt-arrow-left-bold" width={24} />
          </button>
          <div>
            <h1 className="text-xl font-black uppercase tracking-tight">Assistant IA</h1>
          </div>
        </div>
        <div className="w-10 h-10 rounded-full glass flex items-center justify-center text-[#E87A5D]">
          <Icon icon="solar:stars-bold" width={20} />
        </div>
      </header>

      {/* Chat Area */}
      {recording ? (
        <main className="flex-1 flex flex-col items-center justify-center relative p-6 pb-40 animate-fade-in bg-gradient-to-b from-transparent to-[#0A1A12]/50">
          {/* Concentric circles */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full border border-[#E87A5D] opacity-10 animate-ping" style={{ animationDuration: '2s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full border border-[#E87A5D] opacity-5 animate-ping" style={{ animationDuration: '2.5s', animationDelay: '0.5s' }} />

          {/* Big Mic Button */}
          <div className="relative z-10 w-28 h-28 bg-[#E87A5D] rounded-full flex items-center justify-center shadow-[0_0_80px_rgba(232,122,93,0.5)] mb-12">
            <Icon icon="solar:microphone-3-bold" width={56} className="text-white" />
          </div>

          {/* Sound waves imitation */}
          <div className="flex items-center gap-1.5 mb-16">
            <div className="w-1.5 h-3 bg-[#E87A5D]/40 rounded-full animate-pulse" />
            <div className="w-1.5 h-6 bg-[#E87A5D]/60 rounded-full animate-pulse" style={{ animationDelay: '0.1s' }} />
            <div className="w-1.5 h-10 bg-[#E87A5D]/80 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }} />
            <div className="w-1.5 h-14 bg-white rounded-full animate-pulse" style={{ animationDelay: '0.3s' }} />
            <div className="w-1.5 h-10 bg-[#E87A5D]/80 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }} />
            <div className="w-1.5 h-6 bg-[#E87A5D]/60 rounded-full animate-pulse" style={{ animationDelay: '0.5s' }} />
            <div className="w-1.5 h-3 bg-[#E87A5D]/40 rounded-full animate-pulse" style={{ animationDelay: '0.6s' }} />
          </div>

          {/* Card with text */}
          <div className="glass w-full max-w-md rounded-[1.5rem] p-6 border border-[#E87A5D]/20 shadow-xl flex flex-col">
            <div className="text-[10px] font-bold uppercase tracking-widest text-[#4ADE80] mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#4ADE80] animate-pulse" />
              TRADUCTION EN DIRECT
            </div>
            <p className="text-xl font-medium text-white mb-1">Je vous écoute...</p>
            <p className="text-sm font-medium" style={{ color: 'var(--text-muted)' }}>Parlez pour continuer la conversation</p>
          </div>
        </main>
      ) : (
        <main
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-6 space-y-6 pb-40 scroll-smooth"
        >
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
              <div className={`max-w-[85%] flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                {msg.role === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-[#E87A5D]/10 text-[#E87A5D] flex items-center justify-center shrink-0 border border-[#E87A5D]/20">
                    <Icon icon="solar:magic-stick-3-bold" width={16} />
                  </div>
                )}
                <div className={`
                p-4 rounded-2xl shadow-xl border
                ${msg.role === 'user'
                    ? 'bg-gradient-to-br from-[#E87A5D] to-[#B25944] text-white border-orange-400/30 rounded-tr-sm'
                    : 'glass text-[var(--text-color)] border-[var(--glass-border)] rounded-tl-sm'}
              `}>
                  <p className="text-sm font-medium leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  {msg.audio && (
                    <button
                      onClick={() => playBase64Audio(msg.audio)}
                      className="mt-3 flex items-center gap-2 text-[10px] font-black uppercase tracking-widest bg-white/10 hover:bg-white/20 px-2 py-1 rounded-md transition-colors"
                    >
                      <Icon icon="solar:volume-loud-bold" width={12} />
                      Écouter
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start animate-fade-in">
              <div className="glass p-4 rounded-2xl flex gap-2">
                <div className="w-1.5 h-1.5 bg-[var(--text-muted)] rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                <div className="w-1.5 h-1.5 bg-[var(--text-muted)] rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="w-1.5 h-1.5 bg-[var(--text-muted)] rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          )}
        </main>
      )}

      {/* Input Area */}
      <footer className="fixed bottom-0 left-0 right-0 p-6 z-50">
        <div className="max-w-2xl mx-auto flex items-center gap-3">
          <div className="flex-1 relative">
            <textarea
              rows={1}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Écrivez ici..."
              className="premium-input pr-14 h-[56px] min-h-[56px] py-[16px] resize-none overflow-hidden block"
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSendText())}
            />
            <button
              onClick={handleSendText}
              disabled={loading || !inputText.trim()}
              className="absolute right-2 top-2 w-10 h-10 bg-[#E87A5D] text-white rounded-xl flex items-center justify-center shadow-lg hover:scale-110 transition-transform disabled:opacity-50 disabled:scale-100"
            >
              <Icon icon="solar:plain-linear" width={22} />
            </button>
          </div>

          <button
            onClick={handleToggleRecord}
            className={`
              w-14 h-14 rounded-2xl flex items-center justify-center shadow-2xl transition-all duration-300 shrink-0
              ${recording ? 'bg-red-500 animate-pulse scale-110' : 'bg-gradient-to-br from-[#E87A5D] to-[#B25944] text-white'}
            `}
          >
            <Icon icon={recording ? "solar:stop-circle-bold" : "solar:microphone-3-bold"} width={28} />
          </button>
        </div>
      </footer>
    </div>
  );
}
