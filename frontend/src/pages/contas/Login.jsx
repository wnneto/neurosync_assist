// src/pages/contas/Login.jsx
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      // Substitua por sua chamada API real
      const response = await fakeApiLogin(email, password);
      login(response.user, response.token);
      navigate('/dashboard'); // Redireciona após login
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">Acesse sua conta</h2>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Senha
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              disabled={isLoading}
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </button>
          </div>
        </form>
        
        <div className="text-center text-sm text-gray-600">
          <p>Não tem uma conta? <a href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">Cadastre-se</a></p>
        </div>
      </div>
    </div>
  );
}

// Função mock - substitua pela sua API real
async function fakeApiLogin(email, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const testUsers = [
        {
          email: 'rossana@live.com',
          password: 'n88131251',
          user: { 
            id: 1, 
            name: 'Rossana', 
            role: 'Paciente', 
            email: 'rossana@live.com' 
          },
          token: 'fake-jwt-token-rossana'
        },
        // Mantenha os outros usuários de teste se necessário
        {
          email: 'medico@exemplo.com',
          password: 'senha123',
          user: { id: 2, name: 'Dr. Exemplo', role: 'Médico', email: 'medico@exemplo.com' },
          token: 'fake-jwt-token-medico'
        }
      ];
      
      const user = testUsers.find(u => u.email === email && u.password === password);
      
      if (user) {
        resolve({
          user: user.user,
          token: user.token
        });
      } else {
        reject(new Error('Email ou senha incorretos'));
      }
    }, 500);
  });
}