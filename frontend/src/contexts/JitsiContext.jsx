import { createContext, useContext, useState, useCallback } from 'react';
import { JitsiMeeting } from '@jitsi/react-sdk';

const JitsiContext = createContext();

export function JitsiProvider({ children }) {
  const [roomName, setRoomName] = useState('');
  const [isInMeeting, setIsInMeeting] = useState(false);

  const startMeeting = useCallback((customRoomName = '') => {
    const room = customRoomName || `NeuroSyncRoom-${Date.now()}`;
    setRoomName(room);
    setIsInMeeting(true);
    return room;
  }, []);

  const endMeeting = useCallback(() => {
    setIsInMeeting(false);
    setRoomName('');
  }, []);

  return (
    <JitsiContext.Provider
      value={{
        roomName,
        isInMeeting,
        startMeeting,
        endMeeting
      }}
    >
      {children}
    </JitsiContext.Provider>
  );
}

export function useJitsi() {
  const context = useContext(JitsiContext);
  if (!context) {
    throw new Error('useJitsi must be used within a JitsiProvider');
  }
  return context;
}