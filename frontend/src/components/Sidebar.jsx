// src/components/Sidebar.jsx
import { Link, useLocation } from 'react-router-dom';
import { 
  Calendar, Clipboard, Stethoscope, Activity, 
  Pill, Settings, LogOut, User, FileText 
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const isActive = (path) => location.pathname.includes(path);

  if (!user) return null;

  const patientLinks = [
    { path: '/dashboard/paciente/agenda', icon: Calendar, label: 'Agenda' },
    { path: '/dashboard/paciente/exames', icon: Activity, label: 'Exames' },
    { path: '/dashboard/paciente/medicamentos', icon: Pill, label: 'Medicamentos' }
  ];

  const doctorLinks = [
    { path: '/dashboard/medico/agenda', icon: Calendar, label: 'Agenda' },
    { path: '/dashboard/medico/pacientes', icon: Stethoscope, label: 'Pacientes' },
    { path: '/dashboard/medico/documentos', icon: Clipboard, label: 'Documentos' }
  ];

  const commonLinks = [
    { path: '/dashboard/configuracoes', icon: Settings, label: 'Configurações' }
  ];

  const links = user.role === 'Médico' 
    ? [...doctorLinks, ...commonLinks] 
    : [...patientLinks, ...commonLinks];

  return (
    <div className="w-64 bg-white shadow-md flex flex-col h-full">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center">
            <User className="w-5 h-5 text-indigo-600" />
          </div>
          <div>
            <p className="font-medium">{user.name}</p>
            <p className="text-xs text-indigo-600">{user.role}</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 overflow-y-auto">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={`flex items-center w-full p-3 rounded-lg mb-2 ${
              isActive(link.path) 
                ? 'bg-indigo-50 text-indigo-600' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <link.icon className="w-5 h-5 mr-3" />
            {link.label}
          </Link>
        ))}
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
  );
};

export default Sidebar;