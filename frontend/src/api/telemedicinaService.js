import axiosInstance from "@/api/axiosInstance";

export async function iniciarTelemedicina(consultaId) {
  const response = await axiosInstance.post(`/atendimento/consulta/${consultaId}/iniciar-telemedicina/`);
  return response.data;
}