import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Mail, Lock, AlertCircle } from 'lucide-react';

export const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await login(email, senha);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                <div className="bg-white rounded-lg shadow-xl p-8">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-bold text-primary-600 mb-2">💍 VouCasar</h1>
                        <p className="text-gray-600">Organize sua lista de casamento</p>
                    </div>

                    {error && (
                        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-gap-3">
                            <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
                            <p className="text-red-700 text-sm">{error}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                                Email
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                                <input
                                    id="email"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input-field pl-10"
                                    placeholder="seu@email.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="senha" className="block text-sm font-medium text-gray-700 mb-2">
                                Senha
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                                <input
                                    id="senha"
                                    type="password"
                                    value={senha}
                                    onChange={(e) => setSenha(e.target.value)}
                                    className="input-field pl-10"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? 'Autenticando...' : 'Entrar'}
                        </button>
                    </form>

                    <div className="text-center text-sm text-gray-600 mt-6 flex flex-col gap-2">
                        <p>Não tem conta?</p>
                        <button
                            onClick={() => navigate('/register')}
                            className="text-primary-600 font-semibold hover:text-primary-500 hover:underline"
                        >
                            Cadastre-se agora
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
