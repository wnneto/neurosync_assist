// src/hooks/useSessionCheck.js
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function useSessionCheck() {
  const { logout } = useAuth();

  useEffect(() => {
    const checkSession = () => {
      const expiry = localStorage.getItem('expiry');
      if (expiry && new Date(expiry) <= new Date()) {
        logout();
      }
    };

    // Verifica a cada minuto
    const interval = setInterval(checkSession, 60000);
    return () => clearInterval(interval);
  }, [logout]);
}