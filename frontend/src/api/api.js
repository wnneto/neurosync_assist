// src/api/index.js
import axios from 'axios';
import { useAuth } from '@/contexts/AuthContext';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  }
});

// Rotas públicas que não requerem autenticação
const publicRoutes = [
  '/dj-rest-auth/login/',
  '/dj-rest-auth/registration/',
  '/dj-rest-auth/password/reset/',
  '/dj-rest-auth/password/reset/confirm/',
  '/auth/verify', // Adicione esta linha para compatibilidade
];

// Interceptor de requisição
api.interceptors.request.use(config => {
  const isPublicRoute = publicRoutes.some(route => config.url?.includes(route));
  
  if (!isPublicRoute) {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  
  return config;
}, error => {
  return Promise.reject(error);
});

// Interceptor de resposta
api.interceptors.response.use(
  response => response,
  error => {
    // Tratamento global de erros
    if (error.response) {
      switch (error.response.status) {
        case 401: // Não autorizado
          if (!publicRoutes.some(route => error.config.url?.includes(route))) {
            const { logout } = useAuth();
            logout(); // Chama logout global
            window.location.href = '/login?sessionExpired=true';
          }
          break;
          
        case 403: // Proibido
          // Redireciona para página de acesso negado
          window.location.href = '/access-denied';
          break;
          
        case 500: // Erro interno
          // Mostra notificação de erro
          console.error('Server Error:', error.response.data);
          break;
          
        default:
          console.error('API Error:', error.response.data);
      }
    } else if (error.request) {
      console.error('Network Error:', error.message);
    } else {
      console.error('Request Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;