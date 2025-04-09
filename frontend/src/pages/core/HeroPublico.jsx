// pages/core/HeroPublico.jsx
import { Link } from "react-router-dom";

export default function HeroPublico() {
  return (
    <div className="text-center py-5">
      <h2 className="mb-3">Bem-vindo ao NeuralSync</h2>
      <p className="mb-4">Plataforma de saúde moderna e acessível para todos.</p>
      <Link to="/login" className="btn btn-primary me-2">Entrar</Link>
      <Link to="/cadastro" className="btn btn-outline-primary">Cadastre-se</Link>
    </div>
  );
}
