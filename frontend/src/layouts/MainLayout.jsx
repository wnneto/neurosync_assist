import useSessionCheck from '@/hooks/useSessionCheck';

export default function MainLayout({ children }) {
  useSessionCheck();
  
  return (
    <div className="min-h-screen bg-gray-50">
      {children}
    </div>
  );
}