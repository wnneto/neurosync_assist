import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Brain, UserCircle, ChevronDown, 
  Settings, LogOut, ArrowRight 
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const Header = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`fixed top-0 left-0 right-0 z-40 transition-all ${scrolled ? 'bg-white/90 backdrop-blur-md shadow-sm py-3' : 'bg-transparent py-6'}`}>
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Brain className="w-8 h-8 text-indigo-600" />
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            NeuralSync
          </h1>
        </div>

        {isAuthenticated ? (
          <div className="relative">
            <button 
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center space-x-2 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200 hover:shadow-md transition-all"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center">
                <UserCircle className="w-5 h-5 text-indigo-600" />
              </div>
              <span className="font-medium text-gray-700">{user?.name.split(' ')[0]}</span>
              <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-56 origin-top-right bg-white rounded-xl shadow-xl ring-1 ring-black/5 focus:outline-none z-50 animate-fade-in">
                <div className="p-1">
                  <div className="px-4 py-3 border-b border-gray-100">
                    <p className="text-sm font-medium text-gray-900">{user?.email}</p>
                    <p className="text-xs text-indigo-600">{user?.role}</p>
                  </div>
                  
                  <div className="py-1">
                    <button
                      onClick={() => navigate('/perfil')}
                      className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600"
                    >
                      <UserCircle className="w-4 h-4 mr-3" />
                      Meu Perfil
                    </button>
                    <button
                      onClick={() => navigate('/configuracoes')}
                      className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600"
                    >
                      <Settings className="w-4 h-4 mr-3" />
                      Configurações
                    </button>
                  </div>
                  
                  <div className="py-1 border-t border-gray-100">
                    <button
                      onClick={logout}
                      className="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      <LogOut className="w-4 h-4 mr-3" />
                      Sair
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <Button 
            onClick={() => navigate('/auth/login')} 
            className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-indigo-300"
          >
            Acessar Plataforma
            <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
        )}
      </div>
    </header>
  );
};

export default Header;