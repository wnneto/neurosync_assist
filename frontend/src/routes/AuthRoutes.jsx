import { Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

// Lazy loading para as páginas de auth
const Login = lazy(() => import('@/pages/contas/Login'));
const Register = lazy(() => import('@/pages/contas/Register'));

export default function AuthRoutes() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="*" element={<Navigate to="login" replace />} />
      </Routes>
    </Suspense>
  );
}