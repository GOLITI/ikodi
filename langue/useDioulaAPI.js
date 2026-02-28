// hooks/useDioulaAPI.js
// Hook React pour consommer le Microservice Dioula

import { useState, useCallback } from 'react';

const API_BASE = process.env.REACT_APP_DIOULA_API || 'http://localhost:8001';

export function useDioulaAPI() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ── NIVEAU 1 ──────────────────────────────────────────────
  const getLessons = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/niveau1/lessons`);
      return await res.json();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const getLesson = useCallback(async (lessonId) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/niveau1/lessons/${lessonId}`);
      return await res.json();
    } finally {
      setLoading(false);
    }
  }, []);

  const getQuiz = useCallback(async (lessonId) => {
    const res = await fetch(`${API_BASE}/api/niveau1/lessons/${lessonId}/quiz`);
    return await res.json();
  }, []);

  const checkAnswer = useCallback(async (lessonId, questionId, answerIndex) => {
    const res = await fetch(`${API_BASE}/api/niveau1/lessons/${lessonId}/quiz/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lesson_id: lessonId,
        question_id: questionId,
        answer_index: answerIndex,
      }),
    });
    return await res.json();
  }, []);

  // ── NIVEAU 2 ──────────────────────────────────────────────
  /**
   * Retourne l'URL audio pour une phrase Dioula.
   * Utilisez directement dans <audio src={getAudioUrl("I ni ce")} />
   */
  const getAudioUrl = useCallback((text) => {
    return `${API_BASE}/api/niveau2/audio?text=${encodeURIComponent(text)}`;
  }, []);

  const getLessonPhraseAudioUrl = useCallback((lessonId, phraseIndex) => {
    return `${API_BASE}/api/niveau2/lesson-audio/${lessonId}/${phraseIndex}`;
  }, []);

  // ── NIVEAU 3 ──────────────────────────────────────────────
  /**
   * Envoie un blob audio au backend Whisper + RAG.
   * @param {Blob} audioBlob - Enregistrement du micro
   */
  const voiceInteraction = useCallback(async (audioBlob) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');

      const res = await fetch(`${API_BASE}/api/niveau3/voice-interaction`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error(`Erreur serveur: ${res.status}`);
      return await res.json();
      // Retourne: { transcription, ai_response, similar_phrases, response_audio_base64, score }
    } catch (e) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  const textChat = useCallback(async (text, expectedPhrase = '') => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/niveau3/text-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, expected_phrase: expectedPhrase }),
      });
      return await res.json();
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Joue l'audio base64 retourné par l'IA
   * @param {string} base64Audio - La chaîne base64 de l'audio
   */
  const playBase64Audio = useCallback((base64Audio) => {
    if (!base64Audio) return;
    const audio = new Audio(`data:audio/mpeg;base64,${base64Audio}`);
    audio.play();
    return audio;
  }, []);

  return {
    loading,
    error,
    // Niveau 1
    getLessons,
    getLesson,
    getQuiz,
    checkAnswer,
    // Niveau 2
    getAudioUrl,
    getLessonPhraseAudioUrl,
    // Niveau 3
    voiceInteraction,
    textChat,
    playBase64Audio,
  };
}

// ── Utilitaire: Enregistrement micro ──────────────────────
export function useVoiceRecorder() {
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const startRecording = useCallback(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const chunks = [];

    recorder.ondataavailable = (e) => chunks.push(e.data);

    const stopPromise = new Promise((resolve) => {
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        resolve(blob);
        stream.getTracks().forEach((t) => t.stop());
      };
    });

    recorder.start();
    setMediaRecorder(recorder);
    setRecording(true);

    return stopPromise;
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
    }
  }, [mediaRecorder, recording]);

  return { recording, startRecording, stopRecording };
}
