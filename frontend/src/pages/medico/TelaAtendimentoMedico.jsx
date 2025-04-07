// frontend/src/pages/TelaAtendimentoMedico.jsx

import React, { useEffect, useState } from "react";
import { Button } from "@mui/material";
import { finalizarAtendimento, gerarPDF } from "@/api/consultas";
import { getPacienteCompleto } from "@/api/pacienteService";
import { Card, CardContent } from "@/components/ui/card";
import { iniciarTelemedicina } from "@/api/telemedicinaService";

export default function TelaAtendimentoMedico({ consultaId = 7, pacienteId = 1 }) {
  const [descricao, setDescricao] = useState("");
  const [receita, setReceita] = useState("");
  const [pdfLink, setPdfLink] = useState(null);
  const [pacienteData, setPacienteData] = useState(null);
  const [link, setLink] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getPacienteCompleto(pacienteId);
      setPacienteData(data);
    };
    fetchData();
  }, [pacienteId]);

  const handleIniciarVideo = async () => {
    try {
      const response = await iniciarTelemedicina(consultaId);
      if (response && response.link_telemedicina) {
        setLink(response.link_telemedicina);
      } else {
        console.warn("Nenhum link retornado da API.");
      }
    } catch (error) {
      console.error("Erro ao iniciar telemedicina", error);
    }
  };

  const handleFinalizar = async () => {
    try {
      await finalizarAtendimento(consultaId, {
        descricao_complementar: descricao,
        cid10: "G44.1",
        exames_solicitados: "TC de crânio, exame oftalmológico",
        tratamento_orientado: receita,
        visivel_para_paciente: true,
      });

      const blob = await gerarPDF(consultaId);
      const url = URL.createObjectURL(blob);
      setPdfLink(url);
    } catch (err) {
      alert("Erro ao finalizar atendimento.");
      console.error(err);
    }
  };

  if (!pacienteData) return <p className="p-4">Carregando dados do paciente...</p>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="container mx-auto grid grid-cols-12 gap-6">
        {/* Histórico e Dados do Paciente */}
        <div className="col-span-3 bg-white rounded-2xl shadow p-4 h-[90vh] overflow-y-auto">
          <h2 className="text-xl font-bold mb-4">📋 Dados do Paciente</h2>
          <p><strong>Nome:</strong> {pacienteData.nome}</p>
          <p><strong>Sexo:</strong> {pacienteData.sexo}</p>
          <p><strong>Email:</strong> {pacienteData.email}</p>
          <p><strong>CPF:</strong> {pacienteData.cpf}</p>
          <p><strong>Data de Nascimento:</strong> {pacienteData.data_nascimento}</p>
          <p><strong>Alergias:</strong> {pacienteData.dados_medicos?.alergias?.join(", ") || "Nenhuma"}</p>

          <h2 className="text-xl font-bold mt-6 mb-2">📁 Histórico</h2>
          {pacienteData.historico?.map((h, i) => (
            <div key={i} className="border-b pb-2 mb-2">
              <p>📅 {new Date(h.data).toLocaleDateString()}</p>
              <p>🩺 CID: {h.cid10}</p>
              <p>🧾 Resumo: {h.descricao_complementar}</p>
            </div>
          ))}
        </div>

        {/* Central - Vídeo */}
        <div className="col-span-6 flex flex-col gap-4 h-[90vh] overflow-y-auto">
          <Card className="flex-1">
            <CardContent className="h-full flex justify-center items-center">
              {!link ? (
                <Button
                  onClick={handleIniciarVideo}
                  className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
                >
                  🎥 Iniciar Telemedicina
                </Button>
              ) : (
                <iframe
                  src={link}
                  allow="camera; microphone; fullscreen; display-capture"
                  className="w-full h-full rounded-xl border"
                  title="Video Consulta"
                ></iframe>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Ações Rápidas */}
        <div className="col-span-3 bg-white rounded-2xl shadow p-4 h-[90vh] overflow-y-auto">
          <h2 className="text-xl font-bold mb-4">⚡ Ações Rápidas</h2>
          <Button variant="outline" className="w-full mb-2">📄 Prescrição</Button>
          <Button variant="outline" className="w-full mb-2">📂 Anexar Exames</Button>
          <Button variant="outline" className="w-full mb-2" onClick={handleFinalizar}>🧾 Gerar PDF</Button>
          <Button variant="destructive" className="w-full">⛔ Encerrar Sessão</Button>

          <CardContent>
            <h2 className="text-lg font-bold mb-2">📝 Relatório Clínico</h2>
            <textarea
              className="w-full h-24 border rounded p-2 text-sm"
              placeholder="Digite o resumo da consulta..."
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
            ></textarea>
          </CardContent>

          <CardContent>
            <h2 className="text-lg font-bold mb-2">💊 Receita Médica</h2>
            <textarea
              className="w-full h-24 border rounded p-2 text-sm"
              placeholder="Digite ou edite a receita..."
              value={receita}
              onChange={(e) => setReceita(e.target.value)}
            ></textarea>

            <div className="flex justify-end mt-2 gap-2">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white" onClick={handleFinalizar}>
                Finalizar Atendimento
              </Button>
              {pdfLink && (
                <a
                  href={pdfLink}
                  download
                  className="btn bg-green-500 hover:bg-green-600 text-white rounded px-4 py-2"
                >
                  Baixar PDF
                </a>
              )}
            </div>
          </CardContent>
        </div>
      </div>
    </div>
  );
}
