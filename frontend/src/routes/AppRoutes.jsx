import { Routes, Route, Navigate } from 'react-router-dom';
import Home from '@/pages/core/Home';
import TelaAtendimentoMedico from '@/pages/medico/TelaAtendimentoMedico';
import AuthRoutes from '@/routes/AuthRoutes';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Rota principal */}
      <Route path="/" element={<Home />} />

      {/* 🔁 Redireciona as rotas antigas */}
      <Route path="/login" element={<Navigate to="/auth/login" replace />} />
      <Route path="/register" element={<Navigate to="/auth/register" replace />} />

      {/* Rotas de autenticação (novas) */}
      <Route path="/auth/*" element={<AuthRoutes />} />

      {/* Rotas protegidas */}
      <Route element={<ProtectedRoute />}>
        <Route path="/consulta/:id" element={<TelaAtendimentoMedico />} />
      </Route>

      {/* Rota 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}