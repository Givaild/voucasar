import axios, { AxiosInstance } from 'axios';

const isLocalhost = Boolean(
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname === ''
);

const API_BASE_URL = isLocalhost
    ? 'http://localhost:8000/api'
    : 'https://voucasar.cauamarvila.com.br/api';

const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Token CSRF em memória — lido do header X-CSRF-Token das respostas GET
let csrfToken: string | null = null;

// Captura o token de qualquer resposta do backend
api.interceptors.response.use((response) => {
    const token = response.headers['x-csrf-token'];
    if (token) csrfToken = token;
    return response;
});

// Injeta o token nos métodos mutantes
api.interceptors.request.use((config) => {
    const mutante = ['post', 'put', 'delete', 'patch'];
    if (csrfToken && config.method && mutante.includes(config.method)) {
        config.headers['X-CSRF-Token'] = csrfToken;
    }
    return config;
});

export default api;
