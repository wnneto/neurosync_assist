import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { JitsiProvider } from "@/contexts/JitsiContext";
import AppRoutes from "@/routes/AppRoutes";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <JitsiProvider>
          <AppRoutes />
        </JitsiProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}