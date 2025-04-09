// src/hooks/useCheckAuth.js
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function useCheckAuth() {
  const { logout } = useAuth();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Implemente uma verificação de token com sua API
        // await api.verifyToken();
      } catch (error) {
        logout();
      }
    };

    const interval = setInterval(checkAuth, 5 * 60 * 1000); // Verifica a cada 5 minutos
    return () => clearInterval(interval);
  }, [logout]);
}