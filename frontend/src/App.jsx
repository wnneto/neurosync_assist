import { Toaster } from 'react-hot-toast';
import '@/styles/global.css';

// Importação direta (substitua pelo caminho correto)
import AppRoutes from './routes/AppRoutes';

export default function App() {
  return (
    <>
      <AppRoutes />
      <Toaster position="top-right" />
    </>
  );
}