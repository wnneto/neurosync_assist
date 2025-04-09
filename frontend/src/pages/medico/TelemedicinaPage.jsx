import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import JitsiMeetExternalAPI from 'jitsi-meet';

export default function TelemedicinaPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const jitsiContainerRef = useRef(null);
  const [jitsi, setJitsi] = useState(null);

  useEffect(() => {
    if (!user) return;

    const roomName = `NeuralSync-Consulta-${id}`;
    const domain = 'meet.jit.si';
    
    const options = {
      roomName,
      width: '100%',
      height: '100%',
      parentNode: jitsiContainerRef.current,
      userInfo: {
        displayName: user.name,
        email: user.email
      },
      interfaceConfigOverwrite: {
        SHOW_JITSI_WATERMARK: false,
        SHOW_WATERMARK_FOR_GUESTS: false,
        DEFAULT_BACKGROUND: '#f0f4ff',
        TOOLBAR_BUTTONS: [
          'microphone', 'camera', 'closedcaptions', 'desktop', 
          'fullscreen', 'fodeviceselection', 'hangup', 
          'profile', 'chat', 'recording', 'settings', 'tileview'
        ]
      },
      configOverwrite: {
        disableSimulcast: false,
        enableWelcomePage: false,
        enableClosePage: false,
        prejoinPageEnabled: false,
        disableDeepLinking: true,
        startWithAudioMuted: false,
        startWithVideoMuted: false
      }
    };

    const jitsiApi = new JitsiMeetExternalAPI(domain, options);
    setJitsi(jitsiApi);

    return () => {
      if (jitsi) {
        jitsi.dispose();
      }
    };
  }, [user, id]);

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {/* Header da Telemedicina */}
      <header className="bg-gray-800 p-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="font-medium text-white">Consulta em andamento</span>
          </div>
        </div>
        
        <div className="flex space-x-3">
          <button className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-white">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </button>
          <button className="px-4 py-2 bg-red-600 rounded-lg text-white hover:bg-red-700">
            Encerrar Consulta
          </button>
        </div>
      </header>

      {/* Container do Jitsi */}
      <div ref={jitsiContainerRef} className="flex-1" style={{ minHeight: '500px' }} />
      
      {/* Painel de Documentos (opcional) */}
      <div className="bg-gray-800 p-4 border-t border-gray-700">
        <div className="flex justify-center space-x-4">
          <button className="px-4 py-2 bg-indigo-600 rounded-lg text-white hover:bg-indigo-700 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Emitir Receita
          </button>
          <button className="px-4 py-2 bg-indigo-600 rounded-lg text-white hover:bg-indigo-700 flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Registrar Anotações
          </button>
        </div>
      </div>
    </div>
  );
}