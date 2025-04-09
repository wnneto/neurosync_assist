import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { AuthProvider } from '@/contexts/AuthContext';
import { useAuth } from '@/contexts/AuthContext';

// Importações básicas
const Home = lazy(() => import('@/pages/core/Home'));
const Login = lazy(() => import('@/pages/contas/Login'));
const Register = lazy(() => import('@/pages/contas/Register'));
const Sobre = lazy(() => import('@/pages/core/Sobre'));
const ForgotPassword = lazy(() => import('@/pages/contas/ForgotPassword'));
const ResetPassword = lazy(() => import('@/pages/contas/ResetPassword'));
const NotFoundPage = lazy(() => import('@/pages/erros/NotFoundPage'));

// Importações Dashboard
const DashboardBase = lazy(() => import('@/pages/dashboard/DashboardBase'));
const DashboardMedico = lazy(() => import('@/pages/dashboard/DashboardMedico'));
const DashboardPaciente = lazy(() => import('@/pages/dashboard/DashboardPaciente'));
// Importações Médico
const TelemedicinaPage = lazy(() => import('@/pages/medico/TelemedicinaPage'));
// Importações Paciente
const PacienteDetalhes = lazy(() => import('@/pages/paciente/PacienteDetalhes'));
const ExameDetalhes = lazy(() => import('@/pages/paciente/ExameDetalhes'));


function DashboardRedirect() {
  const { user } = useAuth();
  
  if (user?.role === 'Médico') {
    return <Navigate to="/dashboard/medico" replace />;
  } else if (user?.role === 'Paciente') {
    return <Navigate to="/dashboard/paciente" replace />;
  }
  
  return <Navigate to="/dashboard" replace />;
}

export default function AppRoutes() {
  return (
    <AuthProvider>
      <Suspense fallback={<LoadingSpinner fullScreen />}>
        <Routes>
          {/* Rotas públicas */}
          <Route path="/" element={<Home />} />
          <Route path="/sobre" element={<Sobre />} />
          <Route path="/auth/login" element={<Login />} />
          <Route path="/auth/register" element={<Register />} />
          <Route path="/login" element={<Navigate to="/auth/login" replace />} />
          <Route path="/register" element={<Navigate to="/auth/register" replace />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password/:token" element={<ResetPassword />} />

          {/* Rotas protegidas - Dashboard */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<DashboardBase />}>
              <Route index element={<DashboardRedirect />} />
              <Route path="medico" element={<DashboardMedico />} />
              <Route path="paciente" element={<DashboardPaciente />} />
              
              {/* Sub-rotas do médico */}
              <Route path="medico/paciente/:id" element={<PacienteDetalhes />} />
              <Route path="medico/telemedicina/:id" element={<TelemedicinaPage />} />
              
              {/* Sub-rotas do paciente */}
              <Route path="paciente/exames/:id" element={<ExameDetalhes />} />
            </Route>
          </Route>

          {/* Rota 404 */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </AuthProvider>
  );
}