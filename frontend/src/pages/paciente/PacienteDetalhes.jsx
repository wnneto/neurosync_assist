import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  User, Calendar, Clipboard, FileText, 
  Stethoscope, Pill, Activity, AlertCircle,
  MessageSquare, Phone, ArrowLeft, Download
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function PacienteDetalhes() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('prontuario');
  const [paciente, setPaciente] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock data - substitua pela sua API
  useEffect(() => {
    const fetchPaciente = async () => {
      try {
        // Simulando chamada API
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const mockData = {
          id,
          nome: 'João da Silva',
          idade: 42,
          genero: 'Masculino',
          email: 'joao.silva@exemplo.com',
          telefone: '+55 (11) 98765-4321',
          historico: 'Hipertensão, Diabetes tipo 2',
          alergias: 'Penicilina',
          ultimaConsulta: '15/06/2023',
          proximaConsulta: '30/07/2023',
          prontuario: {
            anotacoes: 'Paciente respondeu bem ao tratamento com Metformina. Pressão arterial estável em 12x8.',
            receitas: [
              { id: 1, medicamento: 'Metformina 850mg', dosagem: '1 comprimido 2x ao dia', data: '15/06/2023' },
              { id: 2, medicamento: 'Losartana 50mg', dosagem: '1 comprimido ao dia', data: '15/06/2023' }
            ],
            exames: [
              { id: 1, nome: 'Hemograma completo', data: '10/06/2023', resultado: 'Normal' },
              { id: 2, nome: 'Glicemia em jejum', data: '10/06/2023', resultado: '98 mg/dL' },
              { id: 3, nome: 'Ressonância magnética', data: '05/05/2023', resultado: 'Sem alterações significativas' }
            ]
          }
        };
        
        setPaciente(mockData);
      } catch (error) {
        console.error('Erro ao carregar paciente:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPaciente();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!paciente) {
    return (
      <div className="text-center py-10">
        <AlertCircle className="mx-auto h-12 w-12 text-red-500" />
        <h3 className="mt-2 text-lg font-medium text-gray-900">Paciente não encontrado</h3>
        <Button onClick={() => navigate(-1)} className="mt-4">
          <ArrowLeft className="w-5 h-5 mr-2" />
          Voltar
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex justify-between items-start">
        <Button onClick={() => navigate(-1)} variant="outline">
          <ArrowLeft className="w-5 h-5 mr-2" />
          Voltar
        </Button>
        <div className="flex space-x-4">
          <Button variant="outline">
            <MessageSquare className="w-5 h-5 mr-2" />
            Enviar Mensagem
          </Button>
          <Button>
            <Phone className="w-5 h-5 mr-2" />
            Iniciar Telemedicina
          </Button>
        </div>
      </div>

      {/* Perfil do Paciente */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-start space-x-6">
          <div className="w-24 h-24 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 flex items-center justify-center">
            <User className="w-10 h-10 text-indigo-600" />
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{paciente.nome}</h2>
                <p className="text-gray-600">{paciente.idade} anos, {paciente.genero}</p>
              </div>
              <span className="inline-flex items-center px-3 py-1 rounded-full bg-green-100 text-green-800 text-sm font-medium">
                Ativo
              </span>
            </div>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">Contato</p>
                <p className="font-medium">{paciente.email}</p>
                <p className="font-medium">{paciente.telefone}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Histórico Médico</p>
                <p className="font-medium">{paciente.historico || 'Nenhum'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Alergias</p>
                <p className="font-medium">{paciente.alergias || 'Nenhuma'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Abas */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('prontuario')}
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'prontuario' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
          >
            <Clipboard className="w-5 h-5 mr-2 inline" />
            Prontuário
          </button>
          <button
            onClick={() => setActiveTab('consultas')}
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'consultas' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
          >
            <Calendar className="w-5 h-5 mr-2 inline" />
            Histórico de Consultas
          </button>
          <button
            onClick={() => setActiveTab('exames')}
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'exames' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
          >
            <Activity className="w-5 h-5 mr-2 inline" />
            Exames
          </button>
          <button
            onClick={() => setActiveTab('medicamentos')}
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'medicamentos' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
          >
            <Pill className="w-5 h-5 mr-2 inline" />
            Medicamentos
          </button>
        </nav>
      </div>

      {/* Conteúdo das Abas */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        {activeTab === 'prontuario' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Anotações Médicas</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700">{paciente.prontuario.anotacoes}</p>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">Receitas Recentes</h3>
                <Button variant="outline" size="sm">
                  <FileText className="w-4 h-4 mr-2" />
                  Nova Receita
                </Button>
              </div>
              <div className="space-y-3">
                {paciente.prontuario.receitas.map(receita => (
                  <div key={receita.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between">
                      <div>
                        <p className="font-medium">{receita.medicamento}</p>
                        <p className="text-sm text-gray-600">{receita.dosagem}</p>
                      </div>
                      <div className="text-sm text-gray-500">{receita.data}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'consultas' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Histórico de Consultas</h3>
              <Button variant="outline" size="sm">
                <Calendar className="w-4 h-4 mr-2" />
                Agendar Nova Consulta
              </Button>
            </div>
            <div className="space-y-3">
              <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                <div className="flex justify-between">
                  <div>
                    <p className="font-medium">Consulta de Rotina</p>
                    <p className="text-sm text-gray-600">Dr. Neuro Silva</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium">15/06/2023</p>
                    <p className="text-sm text-gray-600">09:00 - 09:30</p>
                  </div>
                </div>
              </div>
              {/* Mais consultas... */}
            </div>
          </div>
        )}

        {activeTab === 'exames' && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">Exames Recentes</h3>
              <Button variant="outline" size="sm">
                <Stethoscope className="w-4 h-4 mr-2" />
                Solicitar Exame
              </Button>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exame</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Resultado</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {paciente.prontuario.exames.map(exame => (
                    <tr key={exame.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium">{exame.nome}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exame.data}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          exame.resultado === 'Normal' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {exame.resultado}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-indigo-600 hover:text-indigo-900 mr-3">
                          <Download className="w-4 h-4 inline mr-1" />
                          Baixar
                        </button>
                        <button className="text-gray-600 hover:text-gray-900">
                          Visualizar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'medicamentos' && (
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Registro de Medicamentos</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {paciente.prontuario.receitas.map(receita => (
                <div key={receita.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <div className="flex items-start">
                    <div className="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                      <Pill className="w-5 h-5 text-indigo-600" />
                    </div>
                    <div className="ml-4">
                      <h4 className="font-medium">{receita.medicamento}</h4>
                      <p className="text-sm text-gray-600">{receita.dosagem}</p>
                      <p className="text-xs text-gray-500 mt-1">Prescrito em {receita.data}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}