import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { LogOut, Menu, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

export const Header: React.FC = () => {
    const { usuario, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [showConfirmLogout, setShowConfirmLogout] = useState(false);

    // Don't render header on login/register pages, or any public guest pages
    // The header will now render on the landing page
    if (
        location.pathname === '/login' ||
        location.pathname === '/register' ||
        location.pathname.startsWith('/casamento/')
    ) {
        return null;
    }

    const handleLogout = () => {
        setShowConfirmLogout(true);
    };

    const isLandingPage = location.pathname === '/';

    return (
        <header className="bg-transparent border-b border-primary-200/50 backdrop-blur-sm fixed w-full z-40">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <Link to={usuario ? "/dashboard" : "/"} className="flex items-center">
                        <span className="text-3xl font-brand-logo text-primary-600">VouCasar</span>
                    </Link>

                    {isLandingPage ? (
                        <nav className="hidden md:flex items-center gap-8">
                            <a href="#inicio" className="text-primary-600 hover:text-primary-700 transition">
                                Início
                            </a>
                            <a href="#sobre" className="text-primary-600 hover:text-primary-700 transition">
                                Sobre
                            </a>
                            <a href="#pix-diferencial" className="text-primary-600 hover:text-primary-700 transition">
                                Diferencial
                            </a>
                            <a href="#contato" className="text-primary-600 hover:text-primary-700 transition">
                                Contato
                            </a>
                            <Link to="/login" className="btn btn-sm btn-ghost text-primary-600 hover:text-primary-700">Login</Link>
                        </nav>
                    ) : (
                        usuario && (
                            <nav className="hidden md:flex items-center gap-8">
                                <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 transition">
                                    Dashboard
                                </Link>
                                {/* Add other logged-in user navigation links here if needed */}
                                <button
                                    onClick={handleLogout}
                                    className="flex items-center text-gray-700 hover:text-red-600 transition"
                                >
                                    <LogOut className="mr-1" size={18} /> Sair
                                </button>
                            </nav>
                        )
                    )}

                    <button
                        className="md:hidden text-gray-700"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>

                {isMenuOpen && (
                    <div className="md:hidden pb-4 border-t border-primary-200/50 bg-white/90 backdrop-blur-md">
                        {isLandingPage ? (
                            <>
                                <a href="#inicio" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                    Início
                                </a>
                                <a href="#sobre" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                    Sobre
                                </a>
                                <a href="#pix-diferencial" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                    Diferencial
                                </a>
                                <a href="#contato" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                    Contato
                                </a>
                                <Link to="/login" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                    Login
                                </Link>
                            </>
                        ) : (
                            usuario && (
                                <>
                                    <Link to="/dashboard" className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                        Dashboard
                                    </Link>
                                    <Link to={`/casais/${usuario.casalId}/presentes`} className="block py-2 px-4 text-gray-700 hover:text-primary-600" onClick={() => setIsMenuOpen(false)}>
                                        Presentes
                                    </Link>
                                    <button
                                        onClick={() => {
                                            handleLogout();
                                            setIsMenuOpen(false);
                                        }}
                                        className="w-full text-left py-2 px-4 text-gray-700 hover:text-red-600"
                                    >
                                        Sair
                                    </button>
                                </>
                            )
                        )}
                    </div>
                )}
            </div>

            {/* Modal de Confirmação de Logout */}
            {showConfirmLogout && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    {/* Overlay */}
                    <div
                        className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity animate-fade-in"
                        onClick={() => setShowConfirmLogout(false)}
                    ></div>

                    {/* Modal Content */}
                    <div className="bg-white/95 backdrop-blur-md rounded-2xl p-6 max-w-sm w-full shadow-2xl border border-primary-200/50 relative z-10 transform scale-100 transition-all text-center animate-fade-in">
                        <div className="w-12 h-12 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-100">
                            <LogOut className="text-red-500" size={24} />
                        </div>
                        <h3 className="text-xl font-serif font-semibold text-gray-900 mb-2">
                            Confirmar Saída
                        </h3>
                        <p className="text-gray-600 text-sm mb-6 leading-relaxed">
                            Tem certeza de que deseja encerrar a sua sessão e sair do Painel do Casal?
                        </p>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setShowConfirmLogout(false)}
                                className="btn btn-secondary flex-1 py-2 text-sm"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={async () => {
                                    setShowConfirmLogout(false);
                                    await logout();
                                    navigate('/login');
                                }}
                                className="btn btn-danger bg-red-600 hover:bg-red-700 text-white flex-1 py-2 text-sm"
                            >
                                Sim, Sair
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </header>
    );
};
