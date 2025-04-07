import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

export default function Home() {
  const { user } = useAuth(); // Use o contexto de autenticação

  return (
    <div className="max-w-md mx-auto mt-10 text-center">
      <h1 className="text-3xl font-bold">Bem-vindo ao NeuralSync</h1>
      {user ? (
        <p className="mt-4 text-lg">Olá, <strong>{user.nome.split(" ")[0]}</strong> 👋</p>
      ) : (
        <p className="mt-4 text-lg">Por favor faça login ou cadastre-se</p>
      )}
    </div>
  );
}