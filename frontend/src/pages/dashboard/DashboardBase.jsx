import { useEffect } from 'react';
import { useNavigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Calendar, FileText, Bell, User, 
  Stethoscope, Pill, Activity, 
  Settings, LogOut, MessageSquare, X
} from 'lucide-react';

const DashboardBase = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const pathSegments = location.pathname.split('/');
  const currentTab = pathSegments[pathSegments.length - 1] || 'agenda';

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  if (!user) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-center">
          <p>Carregando...</p>
        </div>
      </div>
    );
  }

  // Verificação segura das propriedades do usuário
  const userName = user?.name || 'Usuário';
  const userRole = user?.role ? user.role.toLowerCase() : 'usuário';

  const handleTabChange = (tab) => {
    navigate(`/dashboard/${tab}`);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center">
              <User className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <p className="font-medium">{userName}</p>
              <p className="text-xs text-indigo-600 capitalize">{userRole}</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 p-4 overflow-y-auto">
          <button
            onClick={() => handleTabChange('agenda')}
            className={`flex items-center w-full p-3 rounded-lg mb-2 ${
              currentTab === 'agenda' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Calendar className="w-5 h-5 mr-3" />
            Agenda
          </button>

          {userRole === 'médico' && (
            <>
              <button
                onClick={() => handleTabChange('pacientes')}
                className={`flex items-center w-full p-3 rounded-lg mb-2 ${
                  currentTab === 'pacientes' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Stethoscope className="w-5 h-5 mr-3" />
                Meus Pacientes
              </button>
              <button
                onClick={() => handleTabChange('documentos')}
                className={`flex items-center w-full p-3 rounded-lg mb-2 ${
                  currentTab === 'documentos' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <FileText className="w-5 h-5 mr-3" />
                Documentos Rápidos
              </button>
            </>
          )}

          {userRole === 'paciente' && (
            <>
              <button
                onClick={() => handleTabChange('exames')}
                className={`flex items-center w-full p-3 rounded-lg mb-2 ${
                  currentTab === 'exames' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Activity className="w-5 h-5 mr-3" />
                Meus Exames
              </button>
              <button
                onClick={() => handleTabChange('medicamentos')}
                className={`flex items-center w-full p-3 rounded-lg mb-2 ${
                  currentTab === 'medicamentos' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Pill className="w-5 h-5 mr-3" />
                Medicamentos
              </button>
            </>
          )}

          <button
            onClick={() => handleTabChange('configuracoes')}
            className={`flex items-center w-full p-3 rounded-lg mb-2 ${
              currentTab === 'configuracoes' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Settings className="w-5 h-5 mr-3" />
            Configurações
          </button>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <button
            onClick={logout}
            className="flex items-center w-full p-3 rounded-lg text-red-600 hover:bg-red-50"
          >
            <LogOut className="w-5 h-5 mr-3" />
            Sair
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white shadow-sm p-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-800 capitalize">
            {currentTab === 'agenda' && 'Minha Agenda'}
            {currentTab === 'pacientes' && 'Meus Pacientes'}
            {currentTab === 'documentos' && 'Documentos Rápidos'}
            {currentTab === 'exames' && 'Meus Exames'}
            {currentTab === 'medicamentos' && 'Meus Medicamentos'}
            {currentTab === 'configuracoes' && 'Configurações'}
          </h1>
          <div className="flex items-center space-x-4">
            <button className="p-2 rounded-full hover:bg-gray-100 relative">
              <Bell className="w-5 h-5 text-gray-600" />
              <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardBase;