export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow p-4 text-center font-bold text-xl text-indigo-700">
        NeuralSync - Dashboard
      </header>
      <main className="max-w-7xl mx-auto p-6">{children}</main>
      <footer className="text-center text-sm text-gray-500 py-4">
        NeuralSync © {new Date().getFullYear()}
      </footer>
    </div>
  );
}
