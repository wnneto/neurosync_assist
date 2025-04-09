import { useState } from 'react';
import { Calendar, Activity, Pill, FileText } from 'lucide-react';

const DashboardPaciente = () => {
  const [activeTab, setActiveTab] = useState('agenda');

  // Dados mockados - substitua pela sua API
  const appointments = [
    { id: 1, doctor: 'Dr. Neuro Silva', date: '15/06/2023', time: '09:00', type: 'Consulta' },
    { id: 2, doctor: 'Dr. Neuro Silva', date: '30/06/2023', time: '14:30', type: 'Retorno' }
  ];

  const exams = [
    { id: 1, name: 'Ressonância Magnética', date: '10/06/2023', status: 'Disponível' },
    { id: 2, name: 'Eletroencefalograma', date: '05/06/2023', status: 'Disponível' }
  ];

  const medications = [
    { id: 1, name: 'Ritalina', dosage: '10mg', frequency: '2x ao dia', prescribedBy: 'Dr. Neuro Silva' },
    { id: 2, name: 'Venlafaxina', dosage: '75mg', frequency: '1x ao dia', prescribedBy: 'Dr. Neuro Silva' }
  ];

  return (
    <div>
      {/* Abas */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('agenda')}
          className={`pb-4 px-6 ${activeTab === 'agenda' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
        >
          <div className="flex items-center">
            <Calendar className="w-5 h-5 mr-2" />
            Minha Agenda
          </div>
        </button>
        <button
          onClick={() => setActiveTab('exames')}
          className={`pb-4 px-6 ${activeTab === 'exames' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
        >
          <div className="flex items-center">
            <Activity className="w-5 h-5 mr-2" />
            Meus Exames
          </div>
        </button>
        <button
          onClick={() => setActiveTab('medicamentos')}
          className={`pb-4 px-6 ${activeTab === 'medicamentos' ? 'text-indigo-600 border-b-2 border-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
        >
          <div className="flex items-center">
            <Pill className="w-5 h-5 mr-2" />
            Medicamentos
          </div>
        </button>
      </div>

      {/* Conteúdo das abas */}
      {activeTab === 'agenda' && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Próximas Consultas</h2>
          <div className="grid gap-4">
            {appointments.map(app => (
              <div key={app.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium">Consulta com {app.doctor}</p>
                    <p className="text-sm text-gray-600">{app.date} às {app.time}</p>
                    <p className="text-xs text-indigo-600 mt-1">{app.type}</p>
                  </div>
                  <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                    Ver Detalhes
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'exames' && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Meus Exames Recentes</h2>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Exame</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {exams.map(exam => (
                  <tr key={exam.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{exam.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exam.date}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        {exam.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-indigo-600 hover:text-indigo-900 mr-3">
                        Visualizar
                      </button>
                      <button className="text-gray-600 hover:text-gray-900">
                        Download
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
          <h2 className="text-xl font-semibold mb-4">Meus Medicamentos</h2>
          <div className="grid gap-4">
            {medications.map(med => (
              <div key={med.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <div className="flex justify-between">
                  <div>
                    <p className="font-medium">{med.name} <span className="text-sm font-normal text-gray-600">{med.dosage}</span></p>
                    <p className="text-sm text-gray-600 mt-1">{med.frequency}</p>
                    <p className="text-xs text-gray-500 mt-2">Prescrito por {med.prescribedBy}</p>
                  </div>
                  <div className="flex items-center">
                    <button className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-full">
                      <FileText className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPaciente;