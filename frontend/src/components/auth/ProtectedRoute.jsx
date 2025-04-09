// src/components/auth/ProtectedRoute.jsx
import { useAuth } from '@/contexts/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

export default function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner fullScreen />;
  }

  // Verifica expiração mesmo que isAuthenticated seja true
  const expiry = localStorage.getItem('expiry');
  const isExpired = expiry && new Date(expiry) <= new Date();

  return isAuthenticated && !isExpired ? <Outlet /> : <Navigate to="/login" replace />;
}