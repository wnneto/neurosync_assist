import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Download, FileText, Activity,
  Calendar, User, Printer, Share2
} from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function ExameDetalhes() {
  const { id } = useParams();
  const navigate = useNavigate();
  
  // Mock data - substitua pela sua API
  const exame = {
    id,
    nome: 'Ressonância Magnética - Crânio',
    tipo: 'Imagem',
    data: '15/06/2023',
    paciente: 'João da Silva',
    medico: 'Dr. Neuro Silva',
    laboratorio: 'LabNeuro Imagem',
    resultado: 'Normal',
    observacoes: 'Exame realizado sem contraste. Não foram observadas lesões ou alterações significativas.',
    anexos: [
      { nome: 'Laudo Completo', tipo: 'PDF', tamanho: '2.4 MB' },
      { nome: 'Imagens DICOM', tipo: 'ZIP', tamanho: '124 MB' }
    ]
  };

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <Button onClick={() => navigate(-1)} variant="outline">
          <ArrowLeft className="w-5 h-5 mr-2" />
          Voltar
        </Button>
        <div className="flex space-x-3">
          <Button variant="outline">
            <Printer className="w-5 h-5 mr-2" />
            Imprimir
          </Button>
          <Button variant="outline">
            <Share2 className="w-5 h-5 mr-2" />
            Compartilhar
          </Button>
          <Button>
            <Download className="w-5 h-5 mr-2" />
            Baixar Tudo
          </Button>
        </div>
      </div>

      {/* Resumo do Exame */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-start space-x-6">
          <div className="w-20 h-20 rounded-lg bg-gradient-to-r from-indigo-100 to-blue-100 flex items-center justify-center">
            <Activity className="w-10 h-10 text-indigo-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{exame.nome}</h2>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <p className="text-sm text-gray-500">Data do Exame</p>
                <p className="font-medium flex items-center">
                  <Calendar className="w-4 h-4 mr-2 text-gray-600" />
                  {exame.data}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Paciente</p>
                <p className="font-medium flex items-center">
                  <User className="w-4 h-4 mr-2 text-gray-600" />
                  {exame.paciente}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Resultado</p>
                <p className="font-medium">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    exame.resultado === 'Normal' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {exame.resultado}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Resultados Detalhados */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Resultados</h3>
        
        <div className="prose max-w-none">
          <h4 className="text-gray-700">Observações:</h4>
          <p className="text-gray-600">{exame.observacoes}</p>
          
          <h4 className="text-gray-700 mt-6">Detalhes Técnicos:</h4>
          <ul className="text-gray-600">
            <li>Método: Ressonância Magnética 3 Tesla</li>
            <li>Área Examinada: Crânio e Encéfalo</li>
            <li>Contraste: Não utilizado</li>
            <li>Número de Cortes: 120</li>
          </ul>
        </div>
      </div>

      {/* Anexos */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Anexos</h3>
        
        <div className="space-y-3">
          {exame.anexos.map((anexo, index) => (
            <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center">
                  <FileText className="w-6 h-6 text-gray-500" />
                </div>
                <div>
                  <p className="font-medium">{anexo.nome}</p>
                  <p className="text-sm text-gray-500">{anexo.tipo} • {anexo.tamanho}</p>
                </div>
              </div>
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Baixar
              </Button>
            </div>
          ))}
        </div>
      </div>

      {/* Comentários Médicos */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Anotações Médicas</h3>
        
        <div className="space-y-4">
          <div className="border-l-4 border-indigo-500 pl-4 py-2 bg-indigo-50">
            <p className="font-medium">Dr. Neuro Silva - 16/06/2023</p>
            <p className="text-gray-700 mt-1">Paciente assintomático após tratamento. Exame dentro da normalidade.</p>
          </div>
          
          <textarea
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            rows="3"
            placeholder="Adicione uma nova anotação..."
          ></textarea>
          
          <div className="flex justify-end">
            <Button>
              Salvar Anotação
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}