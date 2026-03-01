import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8002/api/progress';

function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
}

export function useUserStats() {
    const [stats, setStats] = useState({
        points: 0,
        streak: 0,
        level: 'Débutant',
        lessons_completed: 0,
        words_learned: 0,
        exercises_done: 0,
        quiz_score: 0,
        name: '',
        email: '',
    });
    const [loading, setLoading] = useState(true);
    const [lessonsProgress, setLessonsProgress] = useState([]);

    const fetchStats = useCallback(async () => {
        try {
            const [statsRes, lessonsRes] = await Promise.all([
                axios.get(`${API_URL}/stats/`, { headers: getAuthHeaders() }),
                axios.get(`${API_URL}/lessons/`, { headers: getAuthHeaders() }),
            ]);
            setStats(statsRes.data);
            setLessonsProgress(lessonsRes.data);
        } catch (err) {
            console.error('Failed to fetch stats', err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchStats();
    }, [fetchStats]);

    const addPoints = useCallback(async (points) => {
        try {
            const res = await axios.post(
                `${API_URL}/stats/add-points/`,
                { points },
                { headers: getAuthHeaders() }
            );
            setStats(prev => ({ ...prev, ...res.data }));
            return res.data;
        } catch (err) {
            console.error('addPoints error', err);
        }
    }, []);

    const completeLesson = useCallback(async (lessonId, lessonTitle, score = 100) => {
        try {
            const res = await axios.post(
                `${API_URL}/lessons/complete/`,
                { lesson_id: lessonId, lesson_title: lessonTitle, score },
                { headers: getAuthHeaders() }
            );
            fetchStats(); // refresh everything
            return res.data;
        } catch (err) {
            console.error('completeLesson error', err);
        }
    }, [fetchStats]);

    return { stats, loading, lessonsProgress, addPoints, completeLesson, refetch: fetchStats };
}
