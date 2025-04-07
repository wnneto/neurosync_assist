// services/consultas.js
import { axiosInstance } from "@/lib/axios";

export async function gerarLinkTelemedicina(consultaId) {
  const response = await axiosInstance.post(`/api/consultas/gerar-link/${consultaId}/`);
  return response.data;
}

export async function finalizarAtendimento(consultaId, payload) {
  const response = await axiosInstance.post(`/api/consultas/medico/consulta/${consultaId}/finalizar/`, payload);
  return response;
}

export async function gerarPDF(consultaId) {
  const response = await axiosInstance.get(`/api/consultas/medico/consulta/${consultaId}/relatorio/pdf/`, {
    responseType: "blob",
  });
  return response.data;
}
