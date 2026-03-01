import React, { useState } from 'react';
import { Icon } from '@iconify/react';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

export default function AuthScreen({ onLoginSuccess }) {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const API_URL = 'http://127.0.0.1:8002/api/auth';

    const handleAuth = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const endpoint = isLogin ? '/login/' : '/register/';
            const payload = isLogin ? { email, password } : { email, password, name };
            const response = await axios.post(`${API_URL}${endpoint}`, payload);

            localStorage.setItem('access_token', response.data.tokens.access);
            localStorage.setItem('refresh_token', response.data.tokens.refresh);
            onLoginSuccess(response.data.user);
        } catch (err) {
            setError(err.response?.data?.error || 'Une erreur est survenue');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleSuccess = async (credentialResponse) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/google/`, {
                token: credentialResponse.credential,
            });
            localStorage.setItem('access_token', response.data.tokens.access);
            localStorage.setItem('refresh_token', response.data.tokens.refresh);
            onLoginSuccess(response.data.user);
        } catch (err) {
            setError(err.response?.data?.error || 'Erreur connexion Google');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-[var(--bg-color)] text-[var(--text-color)] overflow-hidden p-6 font-sans relative">
            <div className="bg-mesh" />

            <div className="glass w-full max-w-md p-8 rounded-[2rem] shadow-2xl relative z-10 border border-[#E87A5D]/20 animate-fade-in">
                <div className="flex flex-col items-center mb-8">
                    <div className="w-16 h-16 rounded-[1.5rem] bg-gradient-to-br from-[#E87A5D] to-[#B25944] flex items-center justify-center shadow-lg shadow-[#E87A5D]/30 mb-4">
                        <span className="text-white font-black text-3xl tracking-tighter">I</span>
                    </div>
                    <h1 className="text-3xl font-black tracking-tighter">{isLogin ? 'Connexion' : 'Créer un compte'}</h1>
                    <p className="text-sm mt-2 text-[var(--text-muted)] font-medium text-center">
                        {isLogin ? 'Bon retour sur IKODI' : 'Rejoignez la plateforme IKODI'}
                    </p>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-500 text-sm p-4 rounded-xl mb-6 flex items-center gap-2">
                        <Icon icon="solar:danger-triangle-bold" width={20} />
                        <span>{error}</span>
                    </div>
                )}

                <form onSubmit={handleAuth} className="flex flex-col gap-4">
                    {!isLogin && (
                        <div>
                            <label className="text-xs font-bold uppercase tracking-widest text-[#E87A5D] ml-1 mb-1 block">Nom complet</label>
                            <input
                                type="text"
                                required
                                className="premium-input w-full"
                                placeholder="Votre nom"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                disabled={loading}
                            />
                        </div>
                    )}
                    <div>
                        <label className="text-xs font-bold uppercase tracking-widest text-[#E87A5D] ml-1 mb-1 block">Adresse Email</label>
                        <input
                            type="email"
                            required
                            className="premium-input w-full"
                            placeholder="votre@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            disabled={loading}
                        />
                    </div>
                    <div>
                        <label className="text-xs font-bold uppercase tracking-widest text-[#E87A5D] ml-1 mb-1 block">Mot de passe</label>
                        <input
                            type="password"
                            required
                            className="premium-input w-full"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-premium w-full mt-4 flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                <Icon icon={isLogin ? "solar:login-3-bold" : "solar:user-plus-bold"} width={20} />
                                <span>{isLogin ? 'Se connecter' : "S'inscrire"}</span>
                            </>
                        )}
                    </button>
                </form>

                <div className="relative my-8 flex items-center justify-center">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-[var(--glass-border)]"></div>
                    </div>
                    <span className="relative px-4 text-xs font-bold uppercase tracking-widest text-[var(--text-muted)] bg-[var(--bg-color)] rounded-full">
                        Ou continuer avec
                    </span>
                </div>

                <div className="flex justify-center flex-col items-center">
                    <GoogleLogin
                        onSuccess={handleGoogleSuccess}
                        onError={() => setError('Google Login Failed')}
                        theme="filled_black"
                        shape="pill"
                    />
                </div>

                <div className="mt-8 text-center text-sm">
                    <span className="text-[var(--text-muted)]">
                        {isLogin ? "Vous n'avez pas de compte ? " : "Vous avez déjà un compte ? "}
                    </span>
                    <button
                        onClick={() => setIsLogin(!isLogin)}
                        className="text-[#E87A5D] font-bold hover:underline transition-all"
                        disabled={loading}
                    >
                        {isLogin ? "S'inscrire" : "Se connecter"}
                    </button>
                </div>
            </div>
        </div>
    );
}
