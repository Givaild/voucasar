import React from 'react';

export const NotFoundPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
            <div className="text-center">
                <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
                <p className="text-xl text-gray-600 mb-8">Página não encontrada</p>
                <a href="/" className="btn-primary">
                    Voltar para Home
                </a>
            </div>
        </div>
    );
};
