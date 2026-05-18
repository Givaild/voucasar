import axios, { AxiosInstance } from 'axios';

// 1. Detecta se o navegador está rodando localmente
const isLocalhost = Boolean(
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname.getOwnPropertyNames?.length === 0
);

// 2. Define a URL base dinamicamente com base no ambiente
const API_BASE_URL = isLocalhost
    ? 'http://localhost:8000'
    : 'https://voucasar.cauamarvila.com.br/api'; // Altere '/api' se o seu backend responder na raiz de outro subdomínio

const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
    xsrfCookieName: 'csrf_token',
    xsrfHeaderName: 'X-CSRF-Token',
});

export default api;
