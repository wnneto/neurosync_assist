// src/hooks/useAutoRefreshToken.js
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function useAutoRefreshToken() {
  const { user } = useAuth();

  useEffect(() => {
    if (!user) return;

    const refreshToken = async () => {
      try {
        // Implemente sua chamada API para renovar o token
        const response = await fetch('/api/refresh-token', {
          method: 'POST',
          credentials: 'include'
        });
        
        if (response.ok) {
          const { token, expiry } = await response.json();
          localStorage.setItem('token', token);
          localStorage.setItem('expiry', expiry);
        }
      } catch (error) {
        console.error('Falha ao renovar token', error);
      }
    };

    // Renova a cada 4 horas se o usuário estiver ativo
    const interval = setInterval(refreshToken, 4 * 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, [user]);
}