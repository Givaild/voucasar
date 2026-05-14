import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { casalAPI, Casal } from '../lib/services';
import { Calendar, MapPin, Heart, Plus, AlertCircle, Loader } from 'lucide-react';

export const DashboardPage: React.FC = () => {
    const { usuario } = useAuth();
    const navigate = useNavigate();
    const [casais, setCasais] = useState<Casal[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        carregarCasais();
    }, []);

    const carregarCasais = async () => {
        try {
            setLoading(true);
            const dados = await casalAPI.listar();
            setCasais(dados);
        } catch (err: any) {
            setError('Erro ao carregar casais');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const formatarData = (data: string) => {
        return new Date(data).toLocaleDateString('pt-BR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="flex flex-col items-center gap-4">
                    <Loader className="animate-spin text-primary-600" size={32} />
                    <p className="text-gray-600">Carregando dados...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">Bem-vindo, {usuario?.nome}!</h1>
                    <p className="text-gray-600">Gerencie sua lista de casamento</p>
                </div>

                {error && (
                    <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-gap-3">
                        <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
                        <p className="text-red-700">{error}</p>
                    </div>
                )}

                <div className="mb-8">
                    <button
                        onClick={() => navigate('/casais/novo')}
                        className="btn-primary flex items-center gap-2"
                    >
                        <Plus size={20} />
                        Criar Novo Casal
                    </button>
                </div>

                {casais.length === 0 ? (
                    <div className="card text-center py-12">
                        <Heart className="mx-auto text-gray-300 mb-4" size={48} />
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Nenhum casal cadastrado</h3>
                        <p className="text-gray-600 mb-4">Comece criando um novo casal para organizar sua lista de presentes</p>
                        <button
                            onClick={() => navigate('/casais/novo')}
                            className="btn-primary inline-flex items-center gap-2"
                        >
                            <Plus size={20} />
                            Criar Casal
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {casais.map((casal) => (
                            <div
                                key={casal.id}
                                className="card hover:shadow-lg transition-shadow cursor-pointer"
                                onClick={() => navigate(`/casais/${casal.id}/presentes`)}
                            >
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <h3 className="text-lg font-semibold text-gray-900 mb-1">Casal #{casal.id}</h3>
                                        <p className="text-sm text-gray-600">IDs: {casal.id_usuario_1} e {casal.id_usuario_2}</p>
                                    </div>
                                    <Heart className="text-primary-600" size={24} />
                                </div>

                                <div className="space-y-3">
                                    <div className="flex items-center gap-2 text-gray-700">
                                        <Calendar size={18} className="text-primary-600" />
                                        <span className="text-sm">{formatarData(casal.data_casamento)}</span>
                                    </div>

                                    {casal.chave_pix && (
                                        <div className="flex items-center gap-2 text-gray-700">
                                            <MapPin size={18} className="text-primary-600" />
                                            <span className="text-sm font-mono text-gray-600">{casal.chave_pix}</span>
                                        </div>
                                    )}
                                </div>

                                <div className="mt-4 pt-4 border-t border-gray-200">
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            navigate(`/casais/${casal.id}/presentes`);
                                        }}
                                        className="btn-secondary w-full text-sm"
                                    >
                                        Ver Presentes
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};
