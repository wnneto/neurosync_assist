// src/hooks/useAuthRedirect.js
import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function useAuthRedirect(requiredRole = null) {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading) {
      if (!user) {
        navigate('/login');
      } else if (requiredRole && user.role !== requiredRole) {
        navigate('/dashboard');
      }
    }
  }, [user, isLoading, requiredRole, navigate]);

  return { user, isLoading };
}