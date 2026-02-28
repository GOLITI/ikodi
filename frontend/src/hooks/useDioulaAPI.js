// hooks/useDioulaAPI.js
import { useState, useCallback } from 'react';

const API_BASE = 'http://localhost:8001';

export function useDioulaAPI() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const getLessons = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${API_BASE}/api/niveau1/lessons`);
            if (!res.ok) throw new Error('Erreur de chargement des leçons');
            return await res.json();
        } catch (e) {
            setError(e.message);
            return { lessons: [] };
        } finally {
            setLoading(false);
        }
    }, []);

    const getLesson = useCallback(async (lessonId) => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE}/api/niveau1/lessons/${lessonId}`);
            if (!res.ok) throw new Error('Erreur de chargement de la leçon');
            return await res.json();
        } catch (e) {
            setError(e.message);
            return null;
        } finally {
            setLoading(false);
        }
    }, []);

    const getQuiz = useCallback(async (lessonId) => {
        try {
            const res = await fetch(`${API_BASE}/api/niveau1/lessons/${lessonId}/quiz`);
            return await res.json();
        } catch (e) {
            setError(e.message);
            return null;
        }
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

    const getAudioUrl = useCallback((text) => {
        return `${API_BASE}/api/niveau2/audio?text=${encodeURIComponent(text)}&language=fr`;
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
        } catch (e) {
            setError(e.message);
            return null;
        } finally {
            setLoading(false);
        }
    }, []);

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
        } catch (e) {
            setError(e.message);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    const playBase64Audio = useCallback((base64Audio) => {
        if (!base64Audio) return;
        const audio = new Audio(`data:audio/mpeg;base64,${base64Audio}`);
        audio.play();
        return audio;
    }, []);

    return {
        loading,
        error,
        getLessons,
        getLesson,
        getQuiz,
        checkAnswer,
        getAudioUrl,
        textChat,
        voiceInteraction,
        playBase64Audio,
    };
}

export function useVoiceRecorder() {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);

    const startRecording = useCallback(async () => {
        try {
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
        } catch (err) {
            console.error("Erreur micro:", err);
            throw err;
        }
    }, []);

    const stopRecording = useCallback(() => {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            setRecording(false);
        }
    }, [mediaRecorder]);

    return { recording, startRecording, stopRecording };
}
