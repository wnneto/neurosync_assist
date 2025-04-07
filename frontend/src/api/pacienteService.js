// src/services/pacienteService.js
import axios from "axios";

export const getPacienteCompleto = async (pacienteId) => {
  const res = await axios.get(`/api/paciente/${pacienteId}/completo/`);
  return res.data;
};
