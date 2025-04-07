import { useState } from "react";
import axios from "axios";
import { registerUser, loginUser } from "@/api/authService";
import { useNavigate } from "react-router-dom";

export default function AuthForm({
  mode = "login",
  onSuccess,
  onRegisterClick,
}) {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    nome: "",
    email: "",
    password: "",
    password2: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (mode === "register") {
      if (!form.nome || !form.email || !form.password || !form.password2) {
        alert("Preencha todos os campos obrigatórios.");
        return;
      }
      if (form.password !== form.password2) {
        alert("As senhas não coincidem.");
        return;
      }
    } else {
      if (!form.email || !form.password) {
        alert("Preencha email e senha.");
        return;
      }
    }

    try {
      if (mode === "login") {
        await loginUser(form.email, form.password);
        alert("Login realizado com sucesso!");
        onSuccess();
      } else {
        await registerUser({
          nome: form.nome,
          email: form.email,
          password1: form.password,
          password2: form.password2,
        });
        alert("Cadastro realizado com sucesso!");
        onSuccess();
      }
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || "Erro no processo.");
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
            value={form.nome}
            onChange={(e) => setForm({ ...form, nome: e.target.value })}
          />
        )}

        <input
          className="input"
          type="email"
          placeholder="Email *"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          className="input"
          type="password"
          placeholder="Senha *"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        {mode === "register" && (
          <input
            className="input"
            type="password"
            placeholder="Repita a Senha *"
            value={form.password2}
            onChange={(e) => setForm({ ...form, password2: e.target.value })}
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
            Não tem conta? Cadastre-se
          </button>
        ) : (
          <button
            className="text-blue-600 hover:underline"
            onClick={() => navigate("/login")}
          >
            Já tem conta? Faça login
          </button>
        )}
      </div>
    </div>
  );
}



