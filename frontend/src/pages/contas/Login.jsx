import { useNavigate } from "react-router-dom";
import AuthForm from "@/components/auth/AuthForm/AuthForm";

export default function Login() {
  const navigate = useNavigate();

  return (
    <AuthForm 
      mode="login" 
      onSuccess={() => navigate("/")}
      onRegisterClick={() => navigate("/auth/register")}
    />
  );
}
