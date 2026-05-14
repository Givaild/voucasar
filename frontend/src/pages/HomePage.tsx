import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart } from 'lucide-react';

export const HomePage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-screen flex flex-col items-center justify-center">
                <div className="text-center">
                    <Heart className="inline-block text-primary-600 mb-4 animate-bounce" size={64} />
                    <h1 className="text-5xl font-bold text-gray-900 mb-4">💍 CaseBem</h1>
                    <p className="text-xl text-gray-700 mb-2">Organize sua lista de casamento com facilidade</p>
                    <p className="text-lg text-gray-600 mb-8">Gerencie presentes, preços e convidados em um único lugar</p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button
                            onClick={() => navigate('/login')}
                            className="btn-primary px-8 py-3 text-lg"
                        >
                            Entrar
                        </button>
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="btn-secondary px-8 py-3 text-lg"
                        >
                            Explorar
                        </button>
                    </div>
                </div>

                <div className="absolute bottom-8 text-center text-gray-600">
                    <p>Tornando casamentos mais fáceis ♡</p>
                </div>
            </div>
        </div>
    );
};
