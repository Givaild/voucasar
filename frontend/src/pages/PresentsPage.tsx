import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { presenteAPI, Presente, casalAPI, Casal } from '../lib/services';
import { Plus, Trash2, AlertCircle, Loader, Heart, ChevronLeft } from 'lucide-react';

export const PresentsPage: React.FC = () => {
    const { casalId } = useParams<{ casalId: string }>();
    const navigate = useNavigate();
    const [presentes, setPresentes] = useState<Presente[]>([]);
    const [casal, setCasal] = useState<Casal | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showForm, setShowForm] = useState(false);

    const [formData, setFormData] = useState({
        titulo: '',
        descricao: '',
        valor_estimado: '',
        id_categoria: '',
        status: 'disponivel',
    });

    useEffect(() => {
        if (casalId) {
            carregarDados();
        }
    }, [casalId]);

    const carregarDados = async () => {
        try {
            setLoading(true);
            const [casalData, presentesData] = await Promise.all([
                casalAPI.buscar(parseInt(casalId!)),
                presenteAPI.listarPorCasal(parseInt(casalId!)),
            ]);
            setCasal(casalData);
            setPresentes(presentesData);
        } catch (err: any) {
            setError('Erro ao carregar dados');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const novo = await presenteAPI.criar({
                id_casal: parseInt(casalId!),
                titulo: formData.titulo,
                descricao: formData.descricao,
                valor_estimado: parseFloat(formData.valor_estimado),
                id_categoria: formData.id_categoria,
                status: formData.status,
            });
            setPresentes([...presentes, novo]);
            setFormData({
                titulo: '',
                descricao: '',
                valor_estimado: '',
                id_categoria: '',
                status: 'disponivel',
            });
            setShowForm(false);
        } catch (err: any) {
            setError('Erro ao criar presente');
            console.error(err);
        }
    };

    const handleDelete = async (presenteId: number) => {
        if (window.confirm('Tem certeza que deseja deletar este presente?')) {
            try {
                await presenteAPI.deletar(presenteId);
                setPresentes(presentes.filter((p) => p.id !== presenteId));
            } catch (err: any) {
                setError('Erro ao deletar presente');
                console.error(err);
            }
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="flex flex-col items-center gap-4">
                    <Loader className="animate-spin text-primary-600" size={32} />
                    <p className="text-gray-600">Carregando presentes...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <button
                    onClick={() => navigate('/dashboard')}
                    className="flex items-center gap-2 text-primary-600 hover:text-primary-700 mb-6"
                >
                    <ChevronLeft size={20} />
                    Voltar para Dashboard
                </button>

                <div className="mb-8">
                    <div className="flex items-center gap-2 mb-2">
                        <Heart className="text-primary-600" size={28} />
                        <h1 className="text-3xl font-bold text-gray-900">Lista de Presentes</h1>
                    </div>
                    {casal && (
                        <p className="text-gray-600">
                            Casal {casal.id} - {new Date(casal.data_casamento).toLocaleDateString('pt-BR')}
                        </p>
                    )}
                </div>

                {error && (
                    <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-gap-3">
                        <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
                        <p className="text-red-700">{error}</p>
                    </div>
                )}

                <button
                    onClick={() => setShowForm(!showForm)}
                    className="btn-primary flex items-center gap-2 mb-8"
                >
                    <Plus size={20} />
                    {showForm ? 'Cancelar' : 'Adicionar Presente'}
                </button>

                {showForm && (
                    <div className="card mb-8">
                        <h2 className="text-xl font-semibold text-gray-900 mb-6">Novo Presente</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Título *
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.titulo}
                                        onChange={(e) => setFormData({ ...formData, titulo: e.target.value })}
                                        className="input-field"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Categoria
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.id_categoria}
                                        onChange={(e) => setFormData({ ...formData, id_categoria: e.target.value })}
                                        className="input-field"
                                        placeholder="Ex: Cozinha, Decoração"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Valor Estimado (R$)
                                    </label>
                                    <input
                                        type="number"
                                        step="0.01"
                                        value={formData.valor_estimado}
                                        onChange={(e) => setFormData({ ...formData, valor_estimado: e.target.value })}
                                        className="input-field"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Status
                                    </label>
                                    <select
                                        value={formData.status}
                                        onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                                        className="input-field"
                                    >
                                        <option value="disponivel">Disponível</option>
                                        <option value="comprado">Comprado</option>
                                        <option value="reservado">Reservado</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                    Descrição
                                </label>
                                <textarea
                                    value={formData.descricao}
                                    onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                                    className="input-field"
                                    rows={3}
                                    placeholder="Descrição do presente"
                                />
                            </div>

                            <button type="submit" className="btn-primary">
                                Criar Presente
                            </button>
                        </form>
                    </div>
                )}

                {presentes.length === 0 ? (
                    <div className="card text-center py-12">
                        <Heart className="mx-auto text-gray-300 mb-4" size={48} />
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Nenhum presente cadastrado</h3>
                        <p className="text-gray-600">Comece adicionando presentes à sua lista</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {presentes.map((presente) => (
                            <div key={presente.id} className="card hover:shadow-lg transition-shadow">
                                <div className="flex justify-between items-start mb-3">
                                    <h3 className="text-lg font-semibold text-gray-900 flex-1">{presente.titulo}</h3>
                                    <button
                                        onClick={() => handleDelete(presente.id)}
                                        className="text-red-600 hover:text-red-700"
                                    >
                                        <Trash2 size={20} />
                                    </button>
                                </div>

                                {presente.id_categoria && (
                                    <p className="text-sm text-primary-600 font-medium mb-2">{presente.id_categoria}</p>
                                )}

                                {presente.descricao && (
                                    <p className="text-sm text-gray-600 mb-3">{presente.descricao}</p>
                                )}

                                <div className="mb-3 pb-3 border-t border-gray-200">
                                    <p className="text-lg font-bold text-primary-600">
                                        R$ {presente.valor_estimado?.toFixed(2) || 'N/A'}
                                    </p>
                                </div>

                                <div className="flex items-center justify-between">
                                    <span
                                        className={`px-3 py-1 rounded-full text-xs font-medium ${presente.status === 'disponivel'
                                                ? 'bg-green-100 text-green-800'
                                                : presente.status === 'reservado'
                                                    ? 'bg-yellow-100 text-yellow-800'
                                                    : 'bg-blue-100 text-blue-800'
                                            }`}
                                    >
                                        {presente.status}
                                    </span>
                                    <button className="btn-secondary text-sm">Editar</button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};
