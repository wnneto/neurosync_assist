import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { gerarLinkTelemedicina } from "@/api/consultas";


const [link, setLink] = useState("");

<Button
  onClick={async () => {
    try {
      const resultado = await gerarLinkTelemedicina(consulta.id, token); // token é do usuário logado
      alert("✅ Link gerado com sucesso!");
      console.log("Resultado:", resultado);
    } catch (err) {
      alert("Erro ao gerar link. Veja o console.");
    }
  }}
>
  Gerar link de vídeo
</Button>


{link && <p className="mt-2">🔗 Link: <a href={link} target="_blank">{link}</a></p>}


export default function TelaAtendimentoMedico() {
  const [descricao, setDescricao] = useState("");
  const [pdfLink, setPdfLink] = useState(null);

  const finalizarAtendimento = async () => {
    const response = await axios.post("/api/consultas/medico/consulta/7/finalizar/", {
      descricao_complementar: descricao,
      cid10: "G44.1",
      exames_solicitados: "TC de crânio, exame oftalmológico",
      tratamento_orientado: "Repouso, evitar telas, reavaliação em 7 dias",
      visivel_para_paciente: true,
    });

    if (response.status === 201 || response.status === 200) {
      const pdfRes = await axios.get("/api/consultas/medico/consulta/7/relatorio/pdf/", {
        responseType: "blob",
      });
      const url = URL.createObjectURL(pdfRes.data);
      setPdfLink(url);
    }
  };

  return (
    <div className="grid grid-cols-12 gap-4 p-4">
      <div className="col-span-3 bg-white rounded-2xl shadow p-4 h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">Histórico do Paciente</h2>
        <div className="space-y-2">
          <p>📁 Consulta anterior: Dor lombar</p>
          <p>📄 Exames: TC de crânio</p>
          <p>💊 Alergias: Nenhuma</p>
        </div>
      </div>

      <div className="col-span-6 flex flex-col gap-4">
        <Card className="h-[50vh]">
          <CardContent className="flex items-center justify-center h-full">
            <iframe
              src="https://meet.jit.si/consulta_teste"
              allow="camera; microphone; fullscreen; display-capture"
              className="w-full h-full rounded-xl border"
              title="Video Consulta"
            ></iframe>
          </CardContent>
        </Card>

        <Card className="h-[35vh]">
          <CardContent className="h-full overflow-y-auto">
            <h2 className="text-lg font-bold mb-2">Relatório Clínico</h2>
            <textarea
              className="w-full h-40 border rounded p-2"
              placeholder="Digite o resumo da consulta aqui..."
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
            ></textarea>
            <div className="flex justify-end mt-2 gap-2">
              <Button onClick={finalizarAtendimento}>Finalizar Atendimento</Button>
              {pdfLink && (
                <a href={pdfLink} download className="btn bg-green-500 text-white rounded px-4 py-2">
                  Baixar PDF
                </a>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="col-span-3 bg-white rounded-2xl shadow p-4 h-[90vh]">
        <h2 className="text-xl font-bold mb-4">Ações Rápidas</h2>
        <div className="space-y-3">
          <Button variant="outline" className="w-full">📄 Prescrição</Button>
          <Button variant="outline" className="w-full">📂 Anexar Exames</Button>
          <Button variant="outline" className="w-full" onClick={finalizarAtendimento}>🧾 Gerar PDF</Button>
          <Button variant="destructive" className="w-full">Encerrar Sessão</Button>
        </div>
      </div>
    </div>
  );
}
