import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Wallet, ShieldCheck, Zap } from 'lucide-react';

export const LandingPage: React.FC = () => {
    const [isDevSectionOpen, setIsDevSectionOpen] = useState(false);
    return (
        <div className="min-h-screen bg-gradient-to-br from-amber-50 to-rose-50 text-gray-800">
            {/* Hero Section */}
            <section id="inicio" className="relative h-screen flex items-center justify-center text-center overflow-hidden">
                {/* Background Image/Overlay */}
                <div
                    className="absolute inset-0 bg-cover bg-center filter brightness-75 transition-all duration-500 ease-in-out"
                    style={{ backgroundImage: "url('/noivos.jpg')", transform: 'scale(1.05)' }}
                ></div>
                <div className="absolute inset-0 bg-black bg-opacity-40"></div>

                <div className="relative z-10 p-6 max-w-4xl mx-auto">
                    <h1 className="text-6xl md:text-8xl font-bold font-serif text-white leading-tight animate-fade-in-down">
                        Seu Grande Dia, Sem Complicações
                    </h1>
                    <p className="mt-6 text-xl md:text-2xl text-white opacity-90 animate-fade-in delay-200">
                        Crie sua lista de presentes dos sonhos e receba os valores via PIX, diretamente na sua conta.
                    </p>
                    <div className="mt-10 flex justify-center space-x-4 animate-fade-in delay-400">
                        <Link to="/login" className="btn btn-primary btn-lg transform transition-transform duration-300 hover:scale-105 shadow-lg">
                            Começar Agora
                        </Link>
                        <a href="#sobre" className="btn btn-secondary btn-lg transform transition-transform duration-300 hover:scale-105 shadow-lg">
                            Saiba Mais
                        </a>
                    </div>
                </div>
            </section>

            {/* Sobre Section */}
            <section id="sobre" className="py-20 px-6 md:py-24 bg-white shadow-inner">
                <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-12">
                    <div className="md:w-1/2">
                        <img
                            src="/public/casal.jpeg"
                            className="rounded-xl shadow-2xl object-cover w-full h-96 transform hover:scale-105 transition-transform duration-300 brightness-75"
                        />
                    </div>
                    <div className="md:w-1/2 text-center md:text-left">
                        <h2 className="text-4xl font-serif text-primary-800 mb-6">Simplificando o Seu Casamento</h2>
                        <p className="text-lg leading-relaxed text-gray-700 mb-4">
                            Todo presente de casamento carrega um carinho enorme, e cada casal sabe exatamente o que mais precisa para o início da vida a dois.
                            O VouCasar nasceu para dar total flexibilidade à sua lista. Você estipula os valores dos produtos e seus convidados contribuem de forma prática. No final, a escolha é sua: receba o saldo direto via PIX ou acesse os links das lojas virtuais para comprar os produtos reais. É a praticidade que você precisa com o carinho que você merece.
                        </p>
                    </div>
                </div>
            </section>


            {/* PIX Highlight Section */}
            <section id="pix-diferencial" className="py-20 px-6 md:py-24 bg-gradient-to-r from-rose-100 to-amber-100">
                <div className="max-w-6xl mx-auto text-center">
                    <h2 className="text-4xl font-serif text-primary-800 mb-6">Focamos na sua felicidade e na liberdade de usar cada contribuição.</h2>
                    <p className="text-xl text-gray-700 mb-10 max-w-3xl mx-auto">
                        Com o VouCasar, seus convidados contribuem com os valores dos presentes de forma direta e segura. Você recebe o saldo direto no seu PIX ou compra através dos links das lojas virtuais. Sem intermediários, sem taxas abusivas e com total transparência.
                    </p>
                    <div className="grid md:grid-cols-3 gap-8 mt-12">
                        <div className="bg-white p-8 rounded-lg shadow-xl transform hover:scale-105 transition-transform duration-300">
                            <Wallet className="w-16 h-16 text-primary-600 mx-auto mb-4" />
                            <h3 className="text-2xl font-semibold text-gray-900 mb-3">Liberdade Financeira</h3>
                            <p className="text-gray-600">Receba o valor dos presentes em dinheiro e use como preferir, sem amarras.</p>
                        </div>
                        <div className="bg-white p-8 rounded-lg shadow-xl transform hover:scale-105 transition-transform duration-300">
                            <ShieldCheck className="w-16 h-16 text-green-500 mx-auto mb-4" />
                            <h3 className="text-2xl font-semibold text-gray-900 mb-3">Transparência Total</h3>
                            <p className="text-gray-600">Acompanhe cada contribuição em tempo real no seu painel.</p>
                        </div>
                        <div className="bg-white p-8 rounded-lg shadow-xl transform hover:scale-105 transition-transform duration-300">
                            <Zap className="w-16 h-16 text-purple-600 mx-auto mb-4" />
                            <h3 className="text-2xl font-semibold text-gray-900 mb-3">Praticidade para Todos</h3>
                            <p className="text-gray-600">Convidados contribuem com poucos cliques, sem burocracia.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Sobre o Desenvolvedor - Collapsible */}
            <section className="py-10 px-6 bg-white text-center">
                <button
                    onClick={() => setIsDevSectionOpen(!isDevSectionOpen)}
                    className="text-primary-600 font-semibold hover:text-primary-800 transition underline"
                >
                    {isDevSectionOpen ? 'Ocultar informações do desenvolvedor' : 'Conheça mais o desenvolvedor'}
                </button>

                {isDevSectionOpen && (
                    <div className="max-w-4xl mx-auto pt-10 animate-fade-in">
                        <div className="flex flex-col md:flex-row items-center gap-10 bg-gray-50 p-8 rounded-2xl shadow-lg border border-gray-100">
                            <div className="flex-shrink-0">
                                <img
                                    src="/public/dev.jpeg" // Placeholder
                                    alt="Desenvolvedor"
                                    className="w-40 h-40 rounded-full object-cover shadow-md border-4 border-white"
                                />
                            </div>
                            <div className="text-center md:text-left">
                                <h3 className="text-2xl font-semibold text-gray-900 mb-3">Opa! Você me encontrou!!</h3>
                                <p className="text-lg text-gray-700 leading-relaxed mb-4">
                                    Sou Cauã Gomes Marvila e desenvolvi o VouCasar com muito carinho para ajudar casais a terem um momento especial sem preocupações financeiras. 
                                    A ideia foi criar algo simples, moderno e funcional. Espero que aproveitem!
                                </p>
                                <div className="flex gap-4 justify-center md:justify-start">
                                    <a href="https://www.linkedin.com/in/cauagmarvila" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:text-primary-800 font-semibold underline">
                                        LinkedIn
                                    </a>
                                    <a href="https://github.com/CauaGoms" target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:text-primary-800 font-semibold underline">
                                        GitHub
                                    </a>
                                </div>
                            </div>

                        </div>

                        <div className="mt-16 bg-amber-50 p-8 rounded-2xl shadow-inner border border-amber-100">
                            <h3 className="text-3xl font-serif text-amber-900 mb-6">Aceita um cafezinho? ☕</h3>
                            <p className="text-lg text-amber-800 mb-8 max-w-2xl mx-auto">
                                Se o VouCasar te ajudou de alguma forma, considere colaborar com o desenvolvimento do projeto. 
                                Qualquer valor é muito bem-vindo e me ajuda a manter tudo funcionando e trazer novas melhorias!
                            </p>
                            <div className="bg-white p-6 rounded-xl shadow-md inline-block">
                                <div className="w-40 h-40 bg-gray-200 flex items-center justify-center text-gray-500 mb-4 rounded-lg">
                                    <img
                                    src="/public/qrcode.png" // Placeholder
                                    alt="Desenvolvedor"
                                    />
                                </div>
                                <p className="text-sm font-mono text-gray-600"></p>
                            </div>
                        </div>
                    </div>
                )}
            </section>

            {/* Call to Action */}
            <section className="py-20 px-6 md:py-24 bg-primary-700 text-white text-center">
                <div className="max-w-3xl mx-auto">
                    <h2 className="text-4xl font-serif mb-6">Pronto para Planejar Seu Casamento?</h2>
                    <p className="text-xl opacity-90 mb-10">
                        Junte-se a vários casais que já estão transformando a forma como planejam seus casamentos.
                    </p>
                    <Link to="/register" className="btn btn-secondary btn-lg transform transition-transform duration-300 hover:scale-105 shadow-lg">
                        Crie Sua Conta Grátis
                    </Link>
                </div>
            </section>

            {/* Contato Section */}
            <section id="contato" className="py-20 px-6 md:py-24 bg-gradient-to-br from-rose-50 to-amber-50">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-4xl font-serif text-primary-800 mb-8">Fale Conosco</h2>
                    <p className="text-lg text-gray-700 mb-8">
                        Tem alguma dúvida, sugestão ou precisa de suporte? Estamos prontos para ajudar.
                        Entre em contato diretamente através do email abaixo.
                    </p>
                    {/* Placeholder for a contact form or direct email link */}
                    <div className="bg-white p-8 rounded-lg shadow-xl max-w-lg mx-auto">
                        <p className="text-xl font-semibold text-gray-900 mb-4">Email de Contato:</p>
                        <a href="mailto:cauagmarvila@gmail.com" className="text-primary-600 text-2xl font-bold hover:underline">
                            cauagmarvila@gmail.com
                        </a>
                        <p className="text-sm text-gray-500 mt-6">Responderemos o mais breve possível.</p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-800 text-white py-10 px-6 text-center">
                <div className="max-w-6xl mx-auto">
                    <div className="flex flex-col md:flex-row justify-between items-center mb-8">
                        <Link to="/" className="text-4xl font-brand-logo text-white mb-4 md:mb-0">VouCasar</Link>
                        <nav className="flex space-x-6">
                            <a href="#inicio" className="hover:text-primary-400 transition-colors">Início</a>
                            <a href="#sobre" className="hover:text-primary-400 transition-colors">Sobre</a>
                            <a href="#pix-diferencial" className="hover:text-primary-400 transition-colors">Diferencial</a>
                            <a href="#contato" className="hover:text-primary-400 transition-colors">Contato</a>
                            <Link to="/login" className="hover:text-primary-400 transition-colors">Login</Link>
                        </nav>
                    </div>
                    <div className="border-t border-gray-700 pt-8 text-sm text-gray-400">
                        <p>&copy; {new Date().getFullYear()} VouCasar. Todos os direitos reservados.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};
