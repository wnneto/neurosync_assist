import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, Clipboard, Stethoscope, FileText } from 'lucide-react';

const DashboardMedico = () => {
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showTelemedicine, setShowTelemedicine] = useState(false);
  const navigate = useNavigate();

  // Dados mockados - substitua pela sua API
  const appointments = [
    { id: 1, patient: 'João Silva', time: '09:00', type: 'Consulta', status: 'confirmado' },
    { id: 2, patient: 'Maria Souza', time: '10:30', type: 'Retorno', status: 'confirmado' },
    { id: 3, patient: 'Carlos Oliveira', time: '14:00', type: 'Telemedicina', status: 'pendente' }
  ];

  const patients = [
    { id: 1, name: 'João Silva', lastAppointment: '15/06/2023', exams: 5 },
    { id: 2, name: 'Maria Souza', lastAppointment: '10/06/2023', exams: 2 },
    { id: 3, name: 'Carlos Oliveira', lastAppointment: '05/06/2023', exams: 3 }
  ];

  const quickDocuments = [
    { type: 'Atestado', template: 'Modelo padrão' },
    { type: 'Receita', template: 'Modelo padrão' },
    { type: 'Solicitação de Exame', template: 'Modelo padrão' },
    { type: 'Declaração', template: 'Modelo padrão' }
  ];

  const startTelemedicine = (appointment) => {
    if (appointment.type === 'Telemedicina') {
      // Enviar notificação para o paciente
      console.log(`Notificação enviada para ${appointment.patient}`);
      setShowTelemedicine(true);
      setSelectedPatient(appointment.patient);
    }
  };

  return (
    <div>
      {/* Agenda */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Agenda do Dia</h2>
        <div className="grid gap-4">
          {appointments.map(app => (
            <div key={app.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">{app.patient}</p>
                  <p className="text-sm text-gray-600">{app.time} - {app.type}</p>
                </div>
                {app.type === 'Telemedicina' ? (
                  <Button 
                    onClick={() => startTelemedicine(app)}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white"
                  >
                    Iniciar Telemedicina
                  </Button>
                ) : (
                  <Button 
                    onClick={() => navigate(`/paciente/${app.id}`)}
                    className="bg-gray-100 hover:bg-gray-200 text-gray-800"
                  >
                    Ver Prontuário
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Seção de Telemedicina */}
      {showTelemedicine && (
        <div className="mb-8 bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium">Sessão de Telemedicina com {selectedPatient}</h3>
            <button 
              onClick={() => setShowTelemedicine(false)}
              className="text-red-600 hover:text-red-800"
            >
              Encerrar Sessão
            </button>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-inner border border-gray-300 h-64 flex items-center justify-center mb-4">
            <div className="text-center text-gray-500">
              <p>Videochamada ativa com {selectedPatient}</p>
              <p className="text-sm mt-2">Tempo decorrido: 05:32</p>
            </div>
          </div>
          <div className="flex space-x-4">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Compartilhar Tela
            </Button>
            <Button className="bg-green-600 hover:bg-green-700 text-white">
              Enviar Arquivo
            </Button>
          </div>
        </div>
      )}

      {/* Documentos Rápidos */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Documentos Rápidos</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickDocuments.map((doc, index) => (
            <div key={index} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center mb-2">
                <Clipboard className="w-5 h-5 text-indigo-600 mr-2" />
                <h3 className="font-medium">{doc.type}</h3>
              </div>
              <p className="text-sm text-gray-600">{doc.template}</p>
              <Button className="mt-3 w-full bg-indigo-50 hover:bg-indigo-100 text-indigo-600">
                Preencher
              </Button>
            </div>
          ))}
        </div>
      </div>

      {/* Lista de Pacientes */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Meus Pacientes</h2>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paciente</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Última Consulta</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exames</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {patients.map(patient => (
                <tr key={patient.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                        <User className="w-5 h-5 text-indigo-600" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{patient.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{patient.lastAppointment}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{patient.exams} exames</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => navigate(`/paciente/${patient.id}`)}
                      className="text-indigo-600 hover:text-indigo-900 mr-3"
                    >
                      Ver Prontuário
                    </button>
                    <button className="text-gray-600 hover:text-gray-900">
                      Mensagem
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardMedico;