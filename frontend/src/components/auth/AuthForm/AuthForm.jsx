import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser, registerUser } from "@/api/authService";
import { useAuth } from "@/contexts/AuthContext";
import toast from "react-hot-toast";

export default function AuthForm({ mode = "login", onRegisterClick }) {
  const navigate = useNavigate();
  const { login } = useAuth(); // 🔑 Usa o contexto de autenticação

  const [form, setForm] = useState({
    nome: "",
    email: "",
    password: "",
    password2: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (mode === "login") {
        const { token, user } = await loginUser(form.email, form.password);
        login(user, token);
        toast.success("Login realizado com sucesso!");
        navigate("/");
      } else {
        if (!form.nome || !form.email || !form.password || !form.password2) {
          toast.error("Preencha todos os campos obrigatórios.");
          return;
        }

        if (form.password !== form.password2) {
          toast.error("As senhas não coincidem.");
          return;
        }

        await registerUser({
          nome: form.nome,
          email: form.email,
          password1: form.password,
          password2: form.password2,
        });

        toast.success("Cadastro realizado com sucesso!");
        navigate("/auth/login");
      }
    } catch (err) {
      toast.error(err.message || "Erro no processo de autenticação.");
      console.error(err);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white shadow-xl rounded-xl p-8">
      <h2 className="text-2xl font-bold text-center mb-6">
        {mode === "login" ? "Login" : "Cadastro"}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {mode === "register" && (
          <input
            className="input"
            placeholder="Nome completo *"
            name="nome"
            value={form.nome}
            onChange={handleChange}
          />
        )}

        <input
          className="input"
          type="email"
          placeholder="Email *"
          name="email"
          value={form.email}
          onChange={handleChange}
        />
        <input
          className="input"
          type="password"
          placeholder="Senha *"
          name="password"
          value={form.password}
          onChange={handleChange}
        />
        {mode === "register" && (
          <input
            className="input"
            type="password"
            placeholder="Repita a Senha *"
            name="password2"
            value={form.password2}
            onChange={handleChange}
          />
        )}

        <button type="submit" className="btn-blue w-full">
          {mode === "login" ? "Entrar" : "Cadastrar"}
        </button>
      </form>

      <div className="text-center mt-4">
        {mode === "login" ? (
          <button
            className="text-blue-600 hover:underline"
            onClick={onRegisterClick}
          >

          </button>
        ) : (
          <button
            className="text-blue-600 hover:underline"
            onClick={() => navigate("/auth/login")}
          >
            Já tem conta? Faça login
          </button>
        )}
      </div>
    </div>
  );
}
